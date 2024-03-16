import os
from argparse import ArgumentParser, FileType
from curses import wrapper
from playsound import playsound
from datetime import datetime

args = None

script_dir = os.path.dirname(os.path.realpath(__file__))
click_sound_path = os.path.join(script_dir, 'click.wav')
end_sound_path = os.path.join(script_dir, 'end.wav')

def ts():
    now = datetime.now()
    return now.strftime("\n\n[[Щ %Y-%m-%d (%A)/%H:%M]]::\n\n")

def run(stdscr):
    stdscr.clear()
    char_count = 0

    args.outfile.write(ts())
    playsound(click_sound_path, block=False)

    for i in range(args.length):
        a = stdscr.get_wch()
        args.outfile.write(a)
        args.outfile.flush()
        stdscr.addstr(1, 1, a)
        char_count += 1

        if char_count % args.timestamp_interval == 0:
            args.outfile.write(ts())

        if char_count % args.click_interval == 0:
            playsound(click_sound_path, block=False)


def main():
    global args

    print('running module rash')
    parser = ArgumentParser()
    parser.add_argument(
        'outfile',
        type=FileType('a')
    )
    parser.add_argument('-l', '--length', type=int, default=10000)
    parser.add_argument('-c', '--click-interval', type=int, default=50)
    parser.add_argument('-t', '--timestamp-interval', type=int, default=1000)

    args = parser.parse_args()
    try:
        wrapper(run)
    except KeyboardInterrupt:
        pass

    playsound(end_sound_path, block=False)

if __name__ == '__main__':
    main()
