from __future__ import annotations

import argparse
import sys

from compile import Compile
from help_output import __version__

DESCRIPTION = (
    "BrainDuck — a high-level language that compiles to Brainfuck. "
    "Source files use the .bd extension."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="brainduck",
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input", "-i",
        default="input.bd",
        help="input .bd source file (default: input.bd)",
    )
    parser.add_argument(
        "--output", "-o",
        default="output.bf",
        help="output .bf file (default: output.bf)",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="also execute the compiled Brainfuck and print its output",
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="enable debug output (memory tracing between steps)",
    )
    parser.add_argument(
        "--result", "-r",
        action="store_true",
        help="print only the final memory state, not step-by-step traces",
    )
    parser.add_argument(
        "--show", "-s",
        type=int,
        default=100,
        help="number of memory cells to display (default: 100)",
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s v{__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        with open(args.input, "r", encoding="utf-8") as file:
            source = file.read()
    except OSError as exc:
        print(f"brainduck: cannot read input file {args.input!r}: {exc}",
              file=sys.stderr)
        return 1

    compiler = Compile(
        DEBUG=args.debug,
        ONLY_RESULT=args.result,
        SHOW_MEMORY=args.show,
    )

    try:
        result_code = compiler.compile(code=source)
    except (ValueError, IndexError) as exc:
        print(f"brainduck: compilation failed: {exc}", file=sys.stderr)
        return 1

    try:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(result_code)
    except OSError as exc:
        print(f"brainduck: cannot write output file {args.output!r}: {exc}",
              file=sys.stderr)
        return 1

    print(f"brainduck: compiled {args.input} -> {args.output} "
          f"({len(result_code)} cells)")

    if args.run:
        compiler.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())