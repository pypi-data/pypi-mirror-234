# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import importlib
import sys
import es7s

if __name__ == '__main__':
    default = ['cli', 'd', 'gtk', 'tmux', 'web']
    for arg in (sys.argv[1:] or default):
        print(arg, end='...')
        try:
            importlib.import_module(arg, es7s)
        except ImportError as e:
            print(e)
        print("", flush=True)
