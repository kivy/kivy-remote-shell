import os
# Hack to allow import from main app dir:
_parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, _parentdir)

# get the argument passed
arg = os.getenv('PYTHON_SERVICE_ARGUMENT')

import twistedshell
twistedshell.install_shell(context=globals(), service=True)
