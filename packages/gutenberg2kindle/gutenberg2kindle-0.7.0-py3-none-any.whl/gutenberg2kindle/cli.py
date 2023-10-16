"""
Functions and other helpers for `gutenberg2kindle`'s command-line interface.
"""

import argparse
import getpass
import socket
import sys
from typing import Final, Optional, Union

from gutenberg2kindle import __version__
from gutenberg2kindle.config import (
    AVAILABLE_SETTINGS,
    get_config,
    interactive_config,
    set_config,
    setup_settings,
)
from gutenberg2kindle.email import send_book
from gutenberg2kindle.gutenberg import download_book

COMMAND_SEND: Final[str] = "send"
COMMAND_GET_CONFIG: Final[str] = "get-config"
COMMAND_SET_CONFIG: Final[str] = "set-config"
COMMAND_INTERACTIVE_CONFIG: Final[str] = "interactive-config"
COMMAND_VERSION: Final[str] = "version"
AVAILABLE_COMMANDS: Final[list[str]] = [
    COMMAND_SEND,
    COMMAND_GET_CONFIG,
    COMMAND_SET_CONFIG,
    COMMAND_INTERACTIVE_CONFIG,
    COMMAND_VERSION,
]


def get_parser() -> argparse.ArgumentParser:
    """
    Generate and return a parser for the CLI tool
    """
    parser = argparse.ArgumentParser(
        prog="gutenberg2kindle",
        description=(
            "A CLI tool to download and send ebooks from Project Gutenberg to "
            " a Kindle email address via SMTP"
        ),
        epilog="Happy reading! :-)",
    )
    parser.add_argument(
        "command",
        metavar="COMMAND",
        type=str,
        choices=AVAILABLE_COMMANDS,
        help=(
            "Command to use. Supported options allow the user to "
            "either set the tool's config options, read the current "
            "config, or send some books using the current config. "
            f"Supported values are {', '.join(AVAILABLE_COMMANDS)}."
        ),
    )
    parser.add_argument(
        "--book-id",
        "-b",
        metavar="BOOK_ID",
        type=int,
        nargs="+",
        default=[],
        help=(
            "ID of the Project Gutenberg book you want to download. "
            "Can be specified multiple times to download more than one "
            "book at the same time."
        ),
    )
    parser.add_argument(
        "--name",
        "-n",
        metavar="NAME",
        type=str,
        choices=AVAILABLE_SETTINGS,
        help="Setting to get / set, whenever these commands are used.",
    )
    parser.add_argument(
        "--value",
        "-a",
        metavar="VALUE",
        type=str,
        help="Value to set for the specified setting name, if required.",
    )
    parser.add_argument(
        "--ignore-errors",
        "-i",
        action="store_true",
        help=(
            "If set, the tool will ignore any errors that occur while "
            "downloading books, useful when attempting to download and send "
            "multiple books at once. Default is false."
        ),
    )
    parser.set_defaults(ignore_errors=False)

    return parser


def format_setting(name: str, value: Union[str, int]) -> str:
    """Formats a setting with its value for printing"""
    return f"{name}:\t\t{value}"


def print_settings(
    setting_or_dict: Union[str, int, dict[str, Union[str, int]]]
) -> None:
    """
    Auxiliary function that prints the current settings, passed as a
    dictionary, or defaults to printing the received value if it's
    a string or an int
    """

    if isinstance(setting_or_dict, dict):
        for setting_name, setting_value in setting_or_dict.items():
            print(format_setting(setting_name, setting_value))
    else:
        print(setting_or_dict)


def handle_book_download(book_ids: list[int], ignore_errors: bool) -> None:
    """
    Given a list of book IDs, downloads and sends the books
    using the current tool config
    """

    books_amount = len(book_ids)

    # request password
    password = getpass.getpass("Please enter your SMTP password: ")

    for book_id in book_ids:
        book = download_book(book_id)

        if book is None:
            print(f"Book `{book_id}` could not be downloaded!")
            books_amount -= 1

            if ignore_errors:
                print(f"Skipping book `{book_id}`...")
                continue
            sys.exit(1)

        print(f"Sending book `{book_id}`...")
        try:
            sent: bool = send_book(book_id, book, password)
        except socket.error as err:  # pylint: disable=no-member
            print(
                "SMTP credentials are invalid! "
                "Please validate your current config.\n"
                f"Server error message: {err}"
            )
            sys.exit(1)
        else:
            book.close()

        if sent:
            print(f"Book `{book_id}` sent!")
        else:
            print(f"Book `{book_id}` could not be sent, please check its file size.")
            books_amount -= 1

    if books_amount > 1:
        print(f"{books_amount} books sent successfully!")


def main() -> None:
    """
    Run the tool's CLI
    """

    # setup tool
    setup_settings()

    # parse arguments
    parser = get_parser()
    args = parser.parse_args()

    # cast certain arguments to expected types
    command: str = args.command
    name: Optional[str] = args.name
    value: Optional[str] = args.value
    ignore_errors: bool = args.ignore_errors

    if command == COMMAND_SEND:
        book_id_list: list[int] = args.book_id
        handle_book_download(book_id_list, ignore_errors)

    elif command == COMMAND_GET_CONFIG:
        print_settings(get_config(name))

    elif command == COMMAND_SET_CONFIG:
        if name is None:
            print("Please specify a setting name with the `--name` flag")
            sys.exit(1)

        if value is None:
            print("Please specify a setting value with the `--value` flag")
            sys.exit(1)

        set_config(name, value)
        print(format_setting(name, value))

    elif command == COMMAND_INTERACTIVE_CONFIG:
        interactive_config()

    elif command == COMMAND_VERSION:
        print(f"gutenberg2kindle version {__version__}")


if __name__ == "__main__":
    main()
