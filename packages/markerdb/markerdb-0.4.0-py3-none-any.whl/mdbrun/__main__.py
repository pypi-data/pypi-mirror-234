"""
This module exists only to make module level execution also viable.

python -m dbrun

"""

from mdbrun.main import run

def main():
    """
    A simple wrapper over the task_selector
    """
    run()


if __name__ == '__main__':
    main()
