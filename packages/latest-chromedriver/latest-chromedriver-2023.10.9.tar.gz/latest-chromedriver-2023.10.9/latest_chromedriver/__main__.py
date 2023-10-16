"""The main script is just a demo."""

import os

import latest_chromedriver


def demo():
    """Setting the correct path test"""
    latest_chromedriver.safely_set_chromedriver_path()
    print("\nThe Path would be transformed to:")
    print(os.environ['PATH'])


if __name__ == '__main__':
    demo()
