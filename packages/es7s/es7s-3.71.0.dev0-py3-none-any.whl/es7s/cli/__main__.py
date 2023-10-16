# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import sys

from es7s import APP_NAME
from ._entrypoint import invoker as entrypoint_fn


def main():
    entrypoint_fn()


def edit_image():  # @why
    sys.argv = [APP_NAME, 'exec', 'edit-image'] + sys.argv[1:]
    entrypoint_fn()


if __name__ == "__main__":
    main()
