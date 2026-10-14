import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
SOURCE_DIR = ROOT / "raw-sources" / "md"
LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")


def markdown_files(directory):
    return sorted(path for path in directory.rglob("*.md") if path.is_file())


def page_files():
    return [
        path
        for path in markdown_files(WIKI_DIR)
        if "archive" not in path.relative_to(WIKI_DIR).parts
    ]


def link_target(value):
    target = value.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    return target[:-3] if target.lower().endswith(".md") else target


def main():
    wiki_pages = page_files()
    source_pages = markdown_files(SOURCE_DIR)
    targets = {}
    for path in wiki_pages + source_pages:
        relative = path.relative_to(ROOT).with_suffix("").as_posix()
        targets.setdefault(relative, []).append(path)
        targets.setdefault(path.stem, []).append(path)

    errors = []
    for path in wiki_pages:
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in LINK_PATTERN.finditer(line):
                target = link_target(match.group(1))
                matches = targets.get(target, [])
                if not matches:
                    errors.append(f"{path.relative_to(ROOT)}:{line_number}: missing link target: {target}")
                elif len(set(matches)) > 1:
                    errors.append(f"{path.relative_to(ROOT)}:{line_number}: ambiguous link target: {target}")

    index_path = WIKI_DIR / "index.md"
    index_text = index_path.read_text(encoding="utf-8")
    indexed = {
        link_target(match.group(1))
        for match in LINK_PATTERN.finditer(index_text)
    }
    for path in wiki_pages:
        if path.name in {"index.md", "log.md"}:
            continue
        relative = path.relative_to(ROOT).with_suffix("").as_posix()
        if relative not in indexed and path.stem not in indexed:
            errors.append(f"wiki/index.md: missing page from index: {relative}")

    if errors:
        print("Wiki validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    page_count = sum(path.name not in {"index.md", "log.md"} for path in wiki_pages)
    print(f"Wiki validation passed: {page_count} pages indexed; all links resolve uniquely.")
    return 0


if __name__ == "__main__":
    sys.exit(main())