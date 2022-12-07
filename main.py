import argparse
from pdfmon import monitor_directory

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("directory", help="the directory to monitor")
    parser.add_argument("words",
                        help="the list of words to check comma separated")

    args = parser.parse_args()

    monitor_directory(args.directory, args.words.split(','))
