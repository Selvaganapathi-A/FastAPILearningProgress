from api_models import Login
from collections.abc import Callable
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from template_loader import html_generator
from typing import Annotated


template_generator: Callable[[str], str] = html_generator()


app: FastAPI = FastAPI()


@app.post('/api/v1/login', tags=['login', 'old-login'])
async def login_v1(
    email: Annotated[str, Form()], token: Annotated[str, Form()]
):
    return {
        'version': 'v1',
        'Form': {
            'email': email,
            'token': token,
        },
    }


@app.post('/api/v2/login')
async def login_v2(form: Annotated[Login, Form()]):
    return {
        'version': 'v2',
        'Form': form.model_dump(
            # * this should exclude password being sent automatically to the client
            exclude={'password'},
        ),
    }


# ...
"""
python-multipart package required to read files
    The files will be uploaded as "form data".

    - If you declare the type of your path operation function parameter as bytes,
      FastAPI will read the file for you and you will receive the contents as bytes.

    - Keep in mind that this means that the whole contents will be stored in memory.
      This will work well for small files.
"""


@app.get('/api/v1/file/one/get')
async def v1_file_get():
    return HTMLResponse(template_generator('File Single'))


@app.post('/api/v1/file/one')
async def v1_file(
    file: Annotated[
        bytes,
        File(
            title='Single File Upload',
            description='Upload File and it stored in Memory',
        ),
    ],
):
    print('Length of File :', len(file))
    return HTMLResponse(template_generator('File Single'))


# ...


@app.get('/api/v1/file/many/get')
async def v1_files_get():
    return HTMLResponse(template_generator('File Multiple'))


@app.post('/api/v1/file/many')
async def v1_files(file: Annotated[list[bytes], File()]):
    for i, _file_sent in enumerate(file, start=1):
        print(i, 'Length of File :', len(_file_sent))
    return HTMLResponse(template_generator('File Multiple'))


# ...
"""
# Using UploadFile has several advantages over bytes:

    - You don't have to use File() in the default value of the parameter.
    - It uses a "spooled" file:
        A file stored in memory up to a maximum size limit, and after passing
        this limit it will be stored in disk.
    - This means that it will work well for large files like images, videos,
      large binaries, etc. without consuming all the memory.
    - You can get metadata from the uploaded file.
    - It has a file-like async interface.
    - It exposes an actual Python SpooledTemporaryFile object that
      you can pass directly to other libraries that expect a file-like object.
"""

"""
## UploadFile has the following attributes:

    - filename: A str with the original file name that was uploaded (e.g.
    myimage.jpg).

    - content_type: A str with the content type (MIME type / media type) (e.g. image/jpeg).

    - file: A SpooledTemporaryFile (a file-like object). This is the
    actual Python file object that you can pass directly to other
    functions or libraries that expect a "file-like" object.


## UploadFile has the following async methods. They all call the
## corresponding file methods underneath (using the internal
## SpooledTemporaryFile).

    - write(data): Writes data (str or bytes) to the file.

    - read(size): Reads size (int) bytes/characters of the file.

    - seek(offset): Goes to the byte position offset (int) in the file.
        E.g., await myfile.seek(0) would go to the start of the file.
        This is especially useful if you run await myfile.read() once
        and then need to read the contents again.
    - close(): Closes the file.

As all these methods are async methods, you need to "await" them."""


@app.get('/api/v2/file/one/get')
async def v2_file_get():
    return HTMLResponse(template_generator('UploadFile Single'))


@app.post('/api/v2/file/one')
async def v2_file(file: Annotated[UploadFile, File()]):
    print(file.filename)
    print(file.content_type)
    print(file.size)
    print(file.headers)
    return HTMLResponse(template_generator('UploadFile Single'))


@app.post('/api/v2/image/one')
async def v2_image(file: UploadFile):
    """
    Note:
        We Can Directly specify file object as UploadFile too...
        That Works well for simpler codebase
    """
    print(file.filename)
    print(file.content_type)
    print(file.size)
    print(file.headers)
    return {}


# ...


@app.get('/api/v2/file/many/get')
async def v2_files_get():
    return HTMLResponse(template_generator('UploadFile Multiple'))


@app.post('/api/v2/file/many')
async def v2_files(file: Annotated[list[UploadFile], File()]):
    for i, fd in enumerate(file, 1):
        print(i, fd.filename)
        print(i, fd.content_type)
        print(i, fd.size)
        print(i, fd.headers)
        print()
    return HTMLResponse(template_generator('UploadFile Multiple'))


"""
Technical Details

    - Data from forms is normally encoded using the "media type"
      `application/x-www-form-urlencoded` when it doesn't include files.


    But when the form includes files, it is encoded as
    `multipart/form-data`. If you use `File`, FastAPI will know it has
    to get the files from the correct part of the body.


Warning
    - You can declare multiple `File` and `Form` parameters in a path
    operation, but you can't also declare `Body` fields that you expect
    to receive as JSON, as the request will have the body encoded using
    `multipart/form-data` instead of `application/json`.

    - This is not a limitation of FastAPI, it's part of the HTTP protocol.
"""
