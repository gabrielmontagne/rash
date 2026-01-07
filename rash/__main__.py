import os
import subprocess
from argparse import ArgumentParser, FileType
from curses import wrapper
from datetime import datetime
import logging

args = None

script_dir = os.path.dirname(os.path.realpath(__file__))
click_sound_path = os.path.join(script_dir, "click.wav")
end_sound_path = os.path.join(script_dir, "end.wav")


def play(path):
    subprocess.Popen(["paplay", path])


def ts():
    now = datetime.now()
    return now.strftime("\n\n[[Щ %Y-%m-%d (%A)/%H:%M]]::\n\n")


def get_positions(stdscr, center):
    if center:
        height, width = stdscr.getmaxyx()
        char_y, char_x = height // 2, width // 2
        prompt_y, prompt_x = char_y + 2, char_x
    else:
        char_y, char_x = 1, 1
        prompt_y, prompt_x = 3, 1
    return char_y, char_x, prompt_y, prompt_x


def run(stdscr):
    stdscr.clear()

    start_time = datetime.now()
    time_limit = args.minutes * 60 if args.minutes else None
    char_limit = args.length

    char_y, char_x, prompt_y, prompt_x = get_positions(stdscr, args.center)
    prompt_index = 0

    if args.prompt:
        stdscr.addstr(prompt_y, prompt_x, args.prompt[0])

    args.outfile.write(ts())

    if not args.quiet:
        play(click_sound_path)

    char_count = 0
    while True:
        a = stdscr.get_wch()

        if not isinstance(a, str):
            logging.debug(f"Got non string {a}; skipping")
            continue

        if a == "\x04":  # Check for Ctrl+D (ASCII character '\x04')
            logging.debug("EOD Ctrl+D")
            break

        args.outfile.write(a)
        args.outfile.flush()

        if args.center:
            char_y, char_x, _, _ = get_positions(stdscr, True)

        stdscr.addstr(char_y, char_x, a)
        char_count += 1

        if char_count % args.timestamp_interval == 0:
            args.outfile.write(ts())
            if args.prompt:
                prompt_index = (prompt_index + 1) % len(args.prompt)
                _, _, prompt_y, prompt_x = get_positions(stdscr, args.center)
                stdscr.move(prompt_y, prompt_x)
                stdscr.clrtoeol()
                stdscr.addstr(prompt_y, prompt_x, args.prompt[prompt_index])

        if char_count % args.click_interval == 0 and not args.quiet:
            play(click_sound_path)

        if char_limit and char_count >= char_limit:
            break

        if time_limit and (datetime.now() - start_time).total_seconds() >= time_limit:
            break


def main():
    global args

    print("running module rash")
    parser = ArgumentParser()
    parser.add_argument("outfile", type=FileType("a"))
    parser.add_argument("-l", "--length", type=int, default=None)
    parser.add_argument("-m", "--minutes", type=int, default=None)
    parser.add_argument("-c", "--click-interval", type=int, default=50)
    parser.add_argument("-t", "--timestamp-interval", type=int, default=1000)
    parser.add_argument("-p", "--prompt", type=str, action="append", default=[])
    parser.add_argument("-C", "--center", action="store_true", default=False)
    parser.add_argument("-q", "--quiet", action="store_true", default=False)

    args = parser.parse_args()
    try:
        wrapper(run)
    except KeyboardInterrupt:
        pass

    if not args.quiet:
        play(end_sound_path)


if __name__ == "__main__":
    main()
