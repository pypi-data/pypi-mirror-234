import sys
from takenote.core import notes


def main():
    print("Welcome to take-note-cli.")

    notes.main(sys.argv[1:])


if __name__ == "__main__":
    main()
