import argparse
import json
import re
from classes.youtube import youtube
from pathlib import Path


def build_index(directory: Path, filetype: str) -> list[dict[str, str, str]]:
	"""Return an index containing each recipe's title and relative path."""
	recipes = []
	errors = []

	for path in sorted(directory.rglob("*")):
		
		if (filetype == "txt" and re.search('.txt', str(path)) != None) :
			print(str(path))
			yt = youtube()
			for line in path.read_text(encoding="utf-8").splitlines():
				if re.search( yt.YOUTUBE_URL, line ) :
					UrlEredmeny = yt.get_url( line )
					print(UrlEredmeny)
					fName = yt.getHtml( UrlEredmeny )
					fJson = yt.loadAndSaveJson( fName )
					title = yt.getTitle(fJson)

					recipes.append({"title": title, "url": yt.YOUTUBE_URL + UrlEredmeny})
					break
		if (filetype == "json") :
			yt = youtube()
			print(path)
			pos = re.search('youtube_', str(path))
			url = str(path)[pos.start():]
			url = re.sub('youtube_', 'https://youtu.be/', url)
			url = re.sub('.json', url)
			title = yt.getTitle(path)
			recipes.append({"title": title, "url": url})
		if (filetype == "jsonx" and re.search('index\d.json', str(path)) != None) :
			with open(str(path), "r", encoding="utf-8") as f:
				data = json.load(f)
				for d in data:
					if (d["title"] == "hibás" and d not in errors) :
						errors.append(d)
					elif d not in recipes:
						recipes.append(d)
	output_path = Path("./errors.json")
	with output_path.open("w", encoding="utf-8") as f:
		json.dump(errors, f, ensure_ascii=False, indent=2)

	return recipes


def main() -> None:
	parser = argparse.ArgumentParser(description="Index Markdown recipe files.")
	parser.add_argument("directory", type=Path, help="Directory containing recipes")
	parser.add_argument("filetype", type=str, help="input file type")
	parser.add_argument("-o", "--output", type=Path, default=Path("index.json"))
	args = parser.parse_args()

	print(args.filetype)
	data = build_index(args.directory, args.filetype)
	args.output.write_text(
		json.dumps(data, ensure_ascii=False, indent=2) + "\n",
		encoding="utf-8",
	)
	print(f"Wrote {args.output}")
	print(f"Wrote {args.output}")


if __name__ == "__main__":
	main()
