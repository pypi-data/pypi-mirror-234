from torxtools.ctxtools import suppress_traceback

from scaffold.cli import main

if __name__ == "__main__":
    with suppress_traceback():
        main()
