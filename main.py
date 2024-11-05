import sys
import os
from guiCalc import render_window


def cli_calc() -> int:
    while True:
        print('Choose the type of operation to perform: ')
        print('1. sum')
        print('2. sub')
        print('3. mul')
        print('4. div')
        print('0. exit')
        mode = input('mode: ')
        if mode == '0':
            return os.EX_OK
        a = int(input('first number: '))
        b = int(input('second number: '))

        if mode == '1':
            print(a + b)
        if mode == '2':
            print(a - b)
        if mode == '3':
            print(a * b)
        if mode == '4':
            print(a / b)


if __name__ == '__main__':
    raise SystemExit(render_window(sys.argv))
