import json
import datetime as dt
from pathlib import Path

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
BASE_DIR = Path(__file__).parent.parent


def file_output(results, cli_args):
    now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{cli_args.branch1}_{cli_args.branch2}_{cli_args.arch}_{now_formatted}.json'
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(results, file)
