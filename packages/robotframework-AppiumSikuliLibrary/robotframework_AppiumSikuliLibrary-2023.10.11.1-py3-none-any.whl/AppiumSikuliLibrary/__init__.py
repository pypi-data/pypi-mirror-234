"""
Created on 2015-08-20

@author: wang_yang1980@hotmail.com
"""

from .sikuli import AppiumSikuliLibrary


def main():
    lib = AppiumSikuliLibrary(mode='CREATE')


if __name__ == '__main__':
    main()

