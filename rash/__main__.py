from argparse import ArgumentParser, FileType
from curses import wrapper, beep
from sys import stdout
from time import sleep

args = None


def run(stdscr):

    stdscr.clear()

    for i in range(1000):
        stdscr.addstr(0, 1, str(i) * 10)
        a = stdscr.get_wch()
        args.outfile.write(a)
        stdscr.addstr(1, 1, a * 10)
        beep()


def main():
    global args

    print('running module rash')
    parser = ArgumentParser()
    parser.add_argument(
        'outfile',
        type=FileType('w')
    )
    args = parser.parse_args()
    try:
        wrapper(run)
    except KeyboardInterrupt:
        print('ciao.')

if __name__ == '__main__':
    main()
