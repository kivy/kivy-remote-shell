"""TODO: ctrl + left/right (move past word), ctrl + backspace/del (del word), shift + del (del line)
    ...: Smart movement through leading indentation.
    ...: Except for first line, up/down to work normally on multi-line console input.
"""
from code import InteractiveConsole
from collections import deque
from dataclasses import dataclass
from io import StringIO
from itertools import chain, takewhile
from more_itertools import ilen
import sys
from kivy.uix.codeinput import CodeInput
from pygments.lexers import PythonConsoleLexer


@dataclass(frozen=True)
class Key:
    # ANY equals everything! -- if you don't care about matching modifiers, set them equal to Key.ANY
    ANY = type('ANY', (), {  '__eq__': lambda *args: True,
                           '__repr__': lambda  self: 'ANY',
                           '__hash__': lambda  self: -1})()

    code:  int
    shift: bool = False
    ctrl:  bool = False

    def __eq__(self, other):
        if isinstance(other, int): return other == self.code
        return self.__dict__ == other.__dict__

    def iter_similar(self):
        """Return an iterator that yields keys equal to self."""
        yield self
        yield Key(self.code, self.shift, Key.ANY)
        yield Key(self.code,    Key.ANY, self.ctrl)
        yield Key(self.code,    Key.ANY, Key.ANY)


SHIFT, CTRL = (303, 304), (305, 306)

EXACT = map(Key, (13,  9, 275, 276, 278, 279))
ANY_MODS = (Key(code, Key.ANY, Key.ANY) for code in (273, 274, 8, 127))

KEYS \
 = ENTER, TAB, RIGHT, LEFT, HOME, END, UP, DOWN, BACKSPACE, DELETE \
 = tuple(chain(EXACT, ANY_MODS))

del EXACT; del ANY_MODS  # Generators exhausted and we don't need them anymore

CUT  = Key(120, False, True)  # <ctrl + c>
COPY = Key(99 , False, True)  # <ctrl + x>
REDO = Key(122,  True, True)  # <ctrl + shift + z>

SELECT_LEFT  = Key(276, True, False)  # <shift + left>
SELECT_RIGHT = Key(275, True, False)  # <shift + right>
SELECT_HOME  = Key(278, True, False)  # <shift + home>
SELECT_END   = Key(279, True, False)  # <shift + end>


class RedirectConsoleOut:
    """Redirect sys.excepthook and sys.stdout in a single context manager.
       InteractiveConsole (IC) `write` method won't be used if sys.excepthook isn't sys.__excepthook__,
       so we redirect sys.excepthook when pushing to the IC.  This redirect probably isn't necessary:
       testing was done in IPython which sets sys.excepthook to a crashhandler, but running this file
       normally would probably avoid the need for a redirect; still, better safe than sorry.
    """
    def __init__(self):
        self.stack = deque()

    def __enter__(self):
        self.old_hook = sys.excepthook
        self.old_out  = sys.stdout

        sys.excepthook = sys.__excepthook__
        sys.stdout     = StringIO()

        sys.stdout.write('\n')

    def __exit__(self, type, value, tb):
        self.stack.append(sys.stdout.getvalue())

        sys.stdout     = self.old_out
        sys.excepthook = self.old_hook


class Console(InteractiveConsole):
    def __init__(self, text_input, locals=None, filename="<console>"):
        super().__init__(locals, filename)
        self.text_input  = text_input
        self.out_context = RedirectConsoleOut()

    def push(self, line):
        out = self.out_context
        with out: needs_more = super().push(line)

        if not needs_more:
            out.stack.reverse()
            self.text_input.text += ''.join(out.stack)
        out.stack.clear()

        return needs_more

    def write(self, data):
        self.out_context.stack.append(data)


class InputHandler:
    def __init__(self, text_input):
        self.text_input = text_input

        self.pre        = {        COPY: self._copy,
                                    CUT: self._cut,
                                   REDO: self._redo}

        self.post       = {        LEFT: self._left,
                                  RIGHT: self._right,
                                    END: self._end,
                                   HOME: self._home,
                            SELECT_LEFT: self._select_left,
                           SELECT_RIGHT: self._select_right,
                             SELECT_END: self._select_end,
                            SELECT_HOME: self._select_home,
                                    TAB: self._tab,
                                  ENTER: self._enter,
                                     UP: self._up,
                                   DOWN: self._down,
                              BACKSPACE: self._backspace}

    def __call__(self, key, read_only):
        if handle := self.pre.get(key): return handle

        if read_only: return self._read_only

        for key in key.iter_similar():
            if handle := self.post.get(key): return handle

    def _copy(self, **kwargs): self.text_input.copy()

    def _cut(self, read_only, **kwargs):
        self.text_input.copy() if read_only else self.text_input.cut()

    def _redo(self, **kwargs): self.text_input.do_redo()

    def _left(self, at_home, **kwargs):
        self.text_input.cancel_selection()
        if not at_home: self.text_input.move_cursor('left')

    def _right(self, at_end, **kwargs):
        self.text_input.cancel_selection()
        if not at_end: self.text_input.move_cursor('right')

    def _end(self, **kwargs):
        self.text_input.cancel_selection()
        self.text_input.move_cursor('end')

    def _home(self, **kwargs):
        self.text_input.cancel_selection()
        self.text_input.move_cursor('home')

    def _select_left(self, at_home, has_selection, _from, _to, **kwargs):
        if at_home: return
        i = self.text_input.move_cursor('left')
        if not has_selection: self.text_input.select_text(i, i + 1)
        elif   i <   _from  : self.text_input.select_text(i, _to)
        elif   i >=  _from  : self.text_input.select_text(_from, i)

    def _select_right(self, at_end, has_selection, _from, _to, **kwargs):
        if at_end: return
        i = self.text_input.move_cursor('right')
        if not has_selection: self.text_input.select_text(i - 1, i)
        elif   i >  _to     : self.text_input.select_text(_from, i)
        elif   i <= _to     : self.text_input.select_text(i, _to)

    def _select_end(self, has_selection, _to, _from, i, end, **kwargs):
        if not has_selection: start = i
        elif    _to == i    : start = _from
        else                : start = _to
        self.text_input.select_text(start, end)
        self.text_input.move_cursor('end')

    def _select_home(self, has_selection, _to, _from, i, home, **kwargs):
        if not has_selection: fin = i
        elif   _from == i   : fin = _to
        else                : fin = _from
        self.text_input.select_text(home, fin)
        self.text_input.move_cursor('home')

    def _tab(self, has_selection, at_home, **kwargs):
        ti = self.text_input
        if not has_selection and at_home: ti.insert_text(' ' * ti.tab_width)

    def _enter(self, home, **kwargs):
        ti = self.text_input
        text = ti.text[home:].rstrip()

        if text and (len(ti.history) == 1 or ti.history[1] != text):
            ti.history.popleft()
            ti.history.appendleft(text)
            ti.history.appendleft('')
        ti._history_index = 0

        needs_more = ti.console.push(text)
        ti.prompt(needs_more)

    def _up(self, **kwargs): self.text_input.input_from_history()

    def _down(self, **kwargs): self.text_input.input_from_history(reverse=True)

    def _backspace(self, at_home, has_selection, window, keycode, text, modifiers, **kwargs):
        ti = self.text_input
        if not at_home or has_selection:
            super(KivyConsole, ti).keyboard_on_key_down(window, keycode, text, modifiers)

    def _read_only(self, key, window, keycode, text, modifiers, **kwargs):
        ti = self.text_input
        ti.cancel_selection()
        ti.move_cursor('end')
        if key.code not in KEYS:
            super(KivyConsole, ti).keyboard_on_key_down(window, keycode, text, modifiers)


class KivyConsole(CodeInput):
    prompt_1 = '\n>>> '
    prompt_2 = '\n... '

    _home_pos      = 0
    _indent_level  = 0
    _history_index = 0

    def __init__(self, *args, locals=None, banner=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer         = PythonConsoleLexer()
        self.history       = deque([''])
        self.console       = Console(self, locals)
        self.input_handler = InputHandler(self)

        if banner is None:
            self.text = (f'Python {sys.version.splitlines()[0]}\n'
                         'Welcome to the KivyConsole -- A Python interpreter widget for Kivy!\n')
        else: self.text = banner
        self.prompt()

    def prompt(self, needs_more=False):
        if needs_more:
            prompt = self.prompt_2
            self._indent_level  = self.count_indents()
            if self.text.rstrip().endswith(':'): self._indent_level += 1
        else:
            prompt = self.prompt_1
            self._indent_level = 0

        indent = self.tab_width * self._indent_level
        self.text += prompt + ' ' * indent
        self._home_pos = self.cursor_index() - indent
        self.reset_undo()

    def count_indents(self):
        return ilen(takewhile(str.isspace, self.history[1])) // self.tab_width

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """Emulate a python console: disallow editing of previous console output."""
        if keycode[0] in CTRL or keycode[0] in SHIFT and 'ctrl' in modifiers: return

        key = Key(keycode[0], 'shift' in modifiers, 'ctrl' in modifiers)

        # force `selection_from` <= `selection_to` (mouse selections can reverse the order):
        _from, _to    = sorted((self.selection_from, self.selection_to))
        has_selection = bool(self.selection_text)
        i, home, end  = self.cursor_index(), self._home_pos, len(self.text)

        read_only = i < home or has_selection and _from < home
        at_home   = i == home
        at_end    = i == end

        kwargs = locals(); del kwargs['self']
        if handle := self.input_handler(key, read_only): return handle(**kwargs)

        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def move_cursor(self, pos):
        """Similar to `do_cursor_movement` but we account for `_home_pos` and we return the new cursor index."""
        if   pos == 'end'  : index = len(self.text)
        elif pos == 'home' : index = self._home_pos
        elif pos == 'left' : index = self.cursor_index() - 1
        elif pos == 'right': index = self.cursor_index() + 1
        self.cursor = self.get_cursor_from_index(index)
        return index

    def input_from_history(self, reverse=False):
        self._history_index += -1 if reverse else 1
        self._history_index = min(max(0, self._history_index), len(self.history) - 1)
        self.text = self.text[: self._home_pos] + self.history[self._history_index]


if __name__ == "__main__":
    from textwrap import dedent
    from kivy.app import App
    from kivy.lang import Builder

    KV = """
    KivyConsole:
        font_name : './UbuntuMono-R.ttf'
        style_name: 'monokai'
    """


    class KivyInterpreter(App):
        def build(self): return Builder.load_string(dedent(KV))


    KivyInterpreter().run()