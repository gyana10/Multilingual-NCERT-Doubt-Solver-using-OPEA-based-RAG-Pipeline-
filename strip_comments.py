import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
EXCLUDE_DIRS = {"venv", "__pycache__", ".git"}


def strip_comments_from_python(source: str) -> str:
    """Remove full-line Python comments starting with '#' while preserving code.

    This intentionally does NOT try to remove inline comments to avoid
    accidentally modifying code where '#' might appear in strings.
    """
    lines = source.splitlines()
    new_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        new_lines.append(line)
    if source.endswith("\n") and not new_lines:
        return ""
    return "\n".join(new_lines) + ("\n" if source.endswith("\n") and new_lines else "")


def main() -> None:
    for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            if filename.startswith("test_"):
                continue

            full_path = os.path.join(dirpath, filename)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    original = f.read()
            except (OSError, UnicodeDecodeError):
                continue

            new_source = strip_comments_from_python(original)
            if new_source != original:
                try:
                    with open(full_path, "w", encoding="utf-8", newline="") as f:
                        f.write(new_source)
                except OSError:
                    continue


if __name__ == "__main__":
    main()
