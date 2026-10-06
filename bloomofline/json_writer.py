import json
from datetime import date, datetime
from pathlib import Path


def json_writer(data: list, model_name: str) -> None:
    full_path = 'logs/' + str(date.today())
    Path(full_path).mkdir(parents=True, exist_ok=True)
    is_exist = Path(full_path + '/' + model_name + '.json').exists()
    with open(full_path + '/' + model_name + '.json', 'a', encoding='utf-8') as write_file:
        data = {'sync_time': str(datetime.now()), 'data': data}
        if is_exist:
            write_file.write(',\n')
        else:
            write_file.write('[\n')
        json.dump(data, write_file, indent=4, default=str)
