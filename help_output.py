from __future__ import annotations

__version__ = "0.2.0"


def help_output() -> None:
    text = (
        "BrainDuck v0.2.0\n"
        "A high-level language that compiles to Brainfuck.\n\n"
        "Usage: brainduck [options]\n\n"
        "Options:\n"
        "  -i, --input FILE    input .bd source file (default: input.bd)\n"
        "  -o, --output FILE   output .bf file (default: output.bf)\n"
        "      --run           also run the compiled Brainfuck\n"
        "  -d, --debug         enable debug output\n"
        "  -r, --result        print only the final memory state\n"
        "  -s, --show N        number of memory cells to display\n"
        "  -h, --help          show this help message and exit\n"
        "  -v, --version       show version and exit\n"
    )
    print(text)


def version_output() -> None:
    print(f"BrainDuck v{__version__}")