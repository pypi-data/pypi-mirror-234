import click
import sys


@click.command()
@click.argument("file", nargs=1, type=click.Path(exists=True, resolve_path=True))
def main(file):
    """Parse a changelog or version file."""
    if file.endswith("CHANGELOG.md"):
        print(parse_changelog(file))
    elif file.endswith("VERSION"):
        print(parse_version(file))
    else:
        print("Unknown file type")

    sys.exit()


def escape_control_chars(content):
    """Escape control characters for the Slack section of the circleCI payload."""
    replacements = {"\n": "\\n", "\t": "\\t"}

    for old_string, new_string in replacements.items():
        content = content.replace(old_string, new_string).strip()

    return content


def parse_changelog(file_path):
    """Return the most recent changes from a changelog file.

    We escape newlines for the Slack section of the circleCI payload.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        current_block = []
        for line in file:
            if "Version:" in line or "Unreleased:" in line:
                if current_block:
                    return escape_control_chars("\n".join(current_block))
            current_block.append(line.strip())

    return escape_control_chars("\n".join(current_block))


def parse_version(file_path):
    """Replace the -rc, -beta, and -alpha parts of a version string with r, b, and a, respectively."""
    replacements = {"-rc.": "r", "-beta.": "b", "-alpha.": "a"}

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    for old_string, new_string in replacements.items():
        content = content.replace(old_string, new_string).strip()

    return content
