# Gutenberg2Kindle

A small Python tool to download and send ebooks from Project Gutenberg to a Kindle email address via SMTP

## What's this?

`gutenberg2kindle` is a small command-line interface tool that aims to automatically download an `.epub` book from [Project Gutenberg](https://www.gutenberg.org/)'s library of free books in the public domain, and then send the ebook's file to a Kindle email address (although, generally, it can be sent to any email address), with just one command.

The book is sent through a SMTP server with TLS, requiring the user to configure the server settings beforehand via tool commands.

## Installation

You can use your Python package manager (e.g. [pip](https://pip.pypa.io/en/stable/)) to install `gutenberg2kindle`.

```bash
pip install gutenberg2kindle
```

## Usage

`gutenberg2kindle` comes with a command-line interface; its help text can be accessed via:

```bash
gutenberg2kindle --help
```

You can check the tool's current configuration via:

```bash
# will print all config variables with their current values
gutenberg2kindle get-config

# will print only the value for the key you're specifying
gutenberg2kindle get-config --name <key name>
```

You can set a value for any of the settings via:

```bash
gutenberg2kindle set-config --name <key name> --value <key value>
```

Or you can do it all at once interactively, being able to check (and modify, if needed) the current config, just by running:

```bash
gutenberg2kindle interactive-config
```

Finally, once you're done configuring your project, you can send any ebook via its Project Gutenberg book ID (with flags `-b` or `--book-id`):

```bash
gutenberg2kindle send -b <book id as an integer, e.g. 1>
```

You can send multiple books at the same time in the same run, the `-b` / `--book-id` flag accepts multiple arguments. Book will be downloaded and sent one by one, and if the download fails at some point execution will stop. In case you want to skip books that couldn't be downloaded, consider adding the `-i` / `--ignore-errors` flag.

```bash
gutenberg2kindle send -b <first book id> [<second book id> <third book id>...]
gutenberg2kindle send -i -b <first book id> [<second book id> <third book id>...]
```

Note that, if using Gmail as your SMTP server, you might need to set up an [App Password](https://support.google.com/accounts/answer/185833) to use instead of your regular password.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Contributions for issues that are already open by maintainers are welcome and encouraged.

Please make sure to update tests as appropriate; a minimum coverage of 75% is expected (and enforced by Github Actions!).

## License

This project is licensed under the [GNU Affero General Public License v3.0](https://github.com/aitorres/gutenberg2kindle/blob/main/LICENSE).
