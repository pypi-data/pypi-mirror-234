""" Load and execute main method """
from sys import exit as sys_exit
from .main import main  # pylint: disable=relative-beyond-top-level

if __name__ == "__main__":
    sys_exit(main())
