from argparse import ArgumentParser, FileType
from curses import wrapper, beep
from sys import stdout
from time import sleep

def run(stdscr):
    
    stdscr.clear()

    print('running module rash')
    parser = ArgumentParser()
    parser.add_argument(
        'outfile',
        type=FileType('w')
    )
    args = parser.parse_args()

    for i in range(1000):
        stdscr.addstr(0, 1, str(i) * 10)
        a = stdscr.getkey()
        args.outfile.write(a)
        stdscr.addstr(1, 1, a * 10)
        beep()




def main():

    wrapper(run)





if __name__ == '__main__':
    main()
