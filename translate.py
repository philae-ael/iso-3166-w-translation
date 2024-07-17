import json 
import argparse 
import logging
from pathlib import Path
from typing import Any, Dict

BASE_FILE = "./base.json"
logger = logging.getLogger(__name__)

def main(base: Path, lang: str):
    logger.debug(f"base file: {base}, lang: {lang}")

    with open(base) as f:
        logger.debug(f"reading base file {base}")
        base_data = json.load(f)
    output = base.parent /  f"base-{lang}.json"

    output_data :Dict[str, Dict[str, Any]] = {}
    try:
        with open(output) as f:
            logger.debug(f"reading trad file {output}")
            for entry in json.load(f):
                output_data[entry["code"]] = {
                    "en": entry["en"], 
                    lang: entry[lang]
                }
    except FileNotFoundError: 
        pass

    try: 
        for entry in base_data:
            if entry['alpha-2'] in output_data:
                logger.info(f"skiping {entry['name']}")
                continue
            logger.info(f"go entry {entry}")
            print(f"name={entry['name']}, code={entry['alpha-2']}")
            trad = input(f"trad {lang} >>> ")
            output_data[
                entry['alpha-2']
            ] =  {
                "en": entry["name"], 
                lang: trad, 
            } 

    except KeyboardInterrupt:
        pass

    arr = []
    for k, v in output_data.items():
        arr.append({
            "code": k,
            **v
        })

    with open(output, "w") as f: 
        json.dump(arr, f)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser  = argparse.ArgumentParser()
    parser.add_argument("lang")
    parser.add_argument("--base-file", default=BASE_FILE, type=Path)

    args = parser.parse_args()
    main(args.base_file, args.lang)
