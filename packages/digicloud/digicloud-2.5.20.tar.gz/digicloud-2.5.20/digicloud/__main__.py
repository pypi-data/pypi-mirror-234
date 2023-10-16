"""
    Allow to run digicloud as python module.

    Example:
        ``python3 -m digicloud account logout``
"""
import sys

from digicloud.main import main


if __name__ == '__main__':
    sys.exit(main())
