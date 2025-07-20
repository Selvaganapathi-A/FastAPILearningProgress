from collections.abc import Callable
from pathlib import Path
from string import Template

import orjson


def html_generator():
    data: dict[str, str] = {}

    src = Path(__file__).parent / 'forms.json'
    with src.open('rb') as reader:
        data = orjson.loads(reader.read())
        reader.close()

    def inner(key: str):
        if key not in data or key == 'base':
            raise KeyError('Enter Correct Keyword.', data.keys())
        form = Template(data[key]).substitute()
        return Template(data['base']).substitute(form=form)

    return inner


def main():
    _html: Callable[[str], str] = html_generator()
    _html('File Single')
    _html('File Multiple')
    _html('UploadFile Multiple')
    _html('UploadFile Single')


if __name__ == '__main__':
    main()
