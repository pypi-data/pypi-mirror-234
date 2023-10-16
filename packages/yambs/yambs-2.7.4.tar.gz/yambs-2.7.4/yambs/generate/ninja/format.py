"""
A module for writing formatting-related ninja build rules.
"""

# built-in
from os import linesep
from pathlib import Path
from typing import Iterable, TextIO

# third-party
from vcorelib import DEFAULT_ENCODING
from vcorelib.paths import rel

# internal
from yambs.config.common import CommonConfig
from yambs.generate.ninja import write_continuation


def render_format(
    config: CommonConfig,
    paths: Iterable[Path],
    root: Path = None,
    suffix: str = "",
) -> None:
    """Render the ninja source for formatting files."""

    with config.ninja_root.joinpath("format.ninja").open(
        "w", encoding=DEFAULT_ENCODING
    ) as path_fd:
        write_format_target(path_fd, paths, suffix, root)


def write_format_target(
    stream: TextIO, paths: Iterable[Path], suffix: str, root: Path = None
) -> None:
    """
    Write rules and targets for running clang-format on first-party sources
    and headers.
    """

    cmd = f"clang-format{suffix}"

    # Actually formats sources.
    stream.write("rule clang-format" + linesep)
    stream.write(f"  command = {cmd} -i $in" + linesep + linesep)

    # Just checks formatting.
    stream.write("rule clang-format-check" + linesep)
    stream.write(f"  command = {cmd} -n --Werror $in" + linesep)

    paths = list(paths)
    if paths:
        for sfx in ["", "-check"]:
            stream.write(linesep)
            line = f"build format{sfx}: clang-format{sfx} "
            offset = " " * len(line)

            stream.write(line)
            stream.write(
                str(paths[0] if root is None else rel(paths[0], base=root))
            )

            for source in paths[1:]:
                write_continuation(stream, offset)
                stream.write(
                    str(source if root is None else rel(source, base=root))
                )

            stream.write(linesep)
