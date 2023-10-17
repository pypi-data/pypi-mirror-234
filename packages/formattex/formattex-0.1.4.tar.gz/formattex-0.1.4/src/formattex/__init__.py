import argparse
import shutil

from pathlib import Path
from importlib import metadata

from .intermediate_repr import create_internal_repr_texfile


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("files", nargs="*", help="src files to be formatted.")

    # parser.add_argument(
    #     "--fast",
    #     type=bool,
    #     default=True,
    #     help="If --fast given, skip temporary sanity checks.",
    # )

    parser.add_argument(
        "-l",
        "--line-length",
        type=int,
        default=87,
        help="How many characters per line to allow. [default: 87]",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbose mode",
    )

    parser.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        help="Inplace mode (warning!)",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Show program's version number and exit",
    )

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.verbose:
        print(args)

    for path_input in args.files:
        path_input = Path(path_input).absolute()
        if path_input.name.startswith("tmp_"):
            continue
        repr = create_internal_repr_texfile(path_input, verbose=args.verbose)

        if args.inplace:
            path_save_input = path_input.with_stem(f"tmp_saved_input_{path_input.stem}")
            shutil.copyfile(path_input, path_save_input)
            if args.verbose:
                print(f"Processing {path_input} (input saved in {path_save_input})")
            path_output = path_input
        else:
            path_output = path_input.with_stem(f"tmp_{path_input.stem}_formatted")

        formatted = repr.save_formatted(path_output, line_length=args.line_length)

        if args.verbose >= 3:
            print(formatted)


__version__ = metadata.version("formattex")
