import argparse
import json
from pathlib import Path


def build_index(directory: Path) -> list[dict[str, str]]:
	"""Return an index containing each recipe's title and relative path."""
	recipes = []
	for path in sorted(directory.rglob("*.md")):
		title = path.stem
		for line in path.read_text(encoding="utf-8").splitlines():
			if line.startswith("# "):
				title = line[2:].strip()
				break
		recipes.append({"title": title, "path": str(path.relative_to(directory))})
	return recipes


def main() -> None:
	parser = argparse.ArgumentParser(description="Index Markdown recipe files.")
	parser.add_argument("directory", type=Path, help="Directory containing recipes")
	parser.add_argument("-o", "--output", type=Path, default=Path("index.json"))
	args = parser.parse_args()

	args.output.write_text(
		json.dumps(build_index(args.directory), ensure_ascii=False, indent=2) + "\n",
		encoding="utf-8",
	)
	print(f"Wrote {args.output}")


if __name__ == "__main__":
	main()
