from itertools import product
from pathlib import Path
from string import Template

import json
import orjson


def main():
    base = """<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta
			name="viewport"
			content="width=device-width, initial-scale=1.0" />
		<meta
			name="color-scheme"
			content="dark light" />
		<style>
			*,
			*::before,
			*::after {
				margin: 0;
				padding: 0;
				box-sizing: border-box;
			}

			html {
				font-size: 32px;
			}

			body {
				padding: 1em 1em 2em 1em;
				display: grid;
				grid-template-columns: repeat(auto-fit, minmax(15em, 1fr));
			}

			hr {
				display: flow-root;
				border: none;
				background-color: light-dark(black, white);
				min-width: 1px;
				min-height: 1px;
			}

			.form-container {
				background-image: linear-gradient(
					to bottom right in hsl,
					hsl(0 100% 50% / 0.2),
					hsl(240 100% 50% / 0.2)
				);
				min-height: 10em;
				box-shadow: 0 0 8px light-dark(black, white);
				border-radius: 0.25em;
				margin: 1em;
				padding: 0.5em;
				-webkit-margin-collapse: separate;
			}

			form {
				display: flex;
				justify-content: flex-end;
				align-items: center;
				flex-flow: column;
				width: 100%;
				max-height: 100%;
			}

			form > div {
				width: 100%;
				display: flex;
				flex-flow: column;
				padding: 0.5em;
				gap: 0.3em;
			}

			form > div > label {
				text-align: right;
				font-size: 0.75em;
				text-decoration: underline;
				text-decoration-thickness: 2px;
			}

			input,
			button {
				font-size: 0.75em;
				border-radius: 0.2em;
				padding: 0.3em 0.6em;
			}

			input[type='file'],
			button {
				border: 1px solid light-dark(black, white);
				outline: 1px solid light-dark(black, white);
				outline-offset: -1px;
				transition: outline-offset 100ms linear;
			}

			button:focus-within,
			input:focus-within {
				outline: 1px solid light-dark(black, white);
				outline-offset: 2px;
			}

			div + button {
				margin-top: 1em;
			}
		</style>
		<title>Document</title>
	</head>

	<body>
        $form
	</body>
</html>
"""
    template = Template(r"""<div class="form-container">
      <h3>$title</h3>
      <hr />
      <form action="$actionURL" method="post" enctype="multipart/form-data">
        <div>
          <label for="input-file">Upload File</label>
          <input type="file" name="file" id="input-file" accept="image/jpeg" $multiple/>
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>""")
    titles = ['Single', 'Multiple']
    features = {
        'File': '/api/v1/file',
        'UploadFile': '/api/v2/file',
    }

    json_content = dict[str, str]()
    json_content['base'] = base

    for feat, title in product(features, titles):
        # print(features, feat, title)
        # print(features[feat])
        txt = template.substitute(
            title=f'{feat} {title}',
            actionURL=features[feat]
            + '/'
            + ('one' if title == 'Single' else 'many'),
            multiple='' if title == 'Single' else 'multiple',
        )
        json_content[f'{feat} {title}'] = txt
        print()
    #
    json_file = Path(__file__).parent / 'forms.json'
    writer = json_file.open('wb')
    writer.write(orjson.dumps(json_content))
    writer.flush()
    writer.close()
    pass


if __name__ == '__main__':
    main()
    pass
