from fastapi import FastAPI, Request, Response, responses
from typing import Awaitable, Callable

import time


app: FastAPI = FastAPI()


@app.middleware('http')
async def broker(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time.perf_counter_ns()
    response: Response = await call_next(request)
    end = time.perf_counter_ns()
    response.headers['Time-To-Process'] = (
        f'{(end - start) / 1000:.2f} microseconds'
    )
    response.headers['access-method'] = request.method
    return response


@app.delete('/')
@app.patch('/')
@app.put('/')
@app.post('/')
@app.get('/')
async def root() -> dict[str, str]:
    return {'message': 'Simple FASTAPI Response'}


@app.options('/')
def get_item_options(response: Response):
    response.headers['Access-Control-Allow-Methods'] = (
        'GET, POST, PUT, PATCH, OPTIONS, HEAD, DELETE'
    )
    return {'additions': ['Aji', 'Guacamole']}


@app.head('/')
def get_items_headers(response: Response):
    response.headers['X-Cat-Dog'] = 'Alone in the world'


""" HTTP Method Purposes """


@app.get('/api/v3/')
async def api_v3_get():
    return {
        """purpose': 'The GET requests a representation of the
        specified resource. Requests using GET should only be
        used to request data"""
    }


@app.post('/api/v3/')
async def api_v3_post():
    """
        The POST sends data to the server. The type of the body of the
         request is indicated by the Content-Type header.

    The difference between PUT and POST is that PUT is idempotent:
    calling it once or several times successively has the same effect
    (that is no side effect), where successive identical POST may have
    additional effects, like passing an order several times.

    A POST request is typically sent via an HTML form and results in a
    change on the server. In this case, the content type is selected by
    putting the adequate string in the enctype attribute of the <form>
    element or the formenctype attribute of the <input> or <button> elements:

        application/x-www-form-urlencoded: the keys and values are
        encoded in key-value tuples separated by '&', with a '='
        between the key and the value. Non-alphanumeric characters in
        both keys and values are percent encoded: this is the reason
        why this type is not suitable to use with binary data (use
        multipart/form-data instead)

        multipart/form-data: each value is sent as a block of data
        ("body part"), with a user agent-defined delimiter ("boundary")
        separating each part. The keys are given in the Content-Disposition header of each part.
        text/plain

    When the POST request is sent via a method other than an HTML form
    — like via an XMLHttpRequest — the body can take any type. As
    described in the HTTP 1.1 specification, POST is designed to allow
    a uniform method to cover the following functions:

        Annotation of existing resources
        Posting a message to a bulletin board, newsgroup, mailing list, or similar group of articles;
        Adding a new user through a signup modal;
        Providing a block of data, such as the result of submitting a form, to a data-handling process;
        Extending a database through an append operation.

    """
    return {'purpose': 'The POST sends data to the server.'}


@app.put('/api/v3/')
async def api_v3_put():
    return {
        'purpose': """The PUT creates a new resource or replaces a
        representation of the target resource with the request payload."""
    }


@app.patch('/api/v3/')
async def api_v3_patch():
    return {'purpose': 'The PATCH applies partial modifications to a resource.'}


@app.options('/api/v3/')
async def api_v3_options():
    """
    The OPTIONS requests permitted communication options for a given URL or server.
        A client can specify a URL with this method, or an asterisk (*) to refer
        to the entire server.

    Syntax
        OPTIONS /index.html HTTP/1.1
        OPTIONS * HTTP/1.1

    The response then contains an Allow header that holds the allowed methods:

        Response HTTP/1.1 204 No Content
        Allow: OPTIONS, GET, HEAD, POST
        Cache-Control: max-age=604800
        Date: Thu, 13 Oct 2016 11:45:00 GMT
        Server: EOS (lax004/2813)

    Preflighted requests in CORS

    In CORS, a preflight request is sent with the OPTIONS method so that the
    server can respond if it is acceptable to send the request. In this example,
     we will request permission for these parameters:

        The Access-Control-Request-Method header sent in the preflight request
        tells the server that when the actual request is sent, it will have a
        POST request method.
        The Access-Control-Request-Headers header tells the server that when
        the actual request is sent, it will have the X-PINGOTHER and
        Content-Type headers.

    Client Request
    ```
    OPTIONS /resources/post-here/ HTTP/1.1
    Host: bar.example
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-us,en;q=0.5
    Accept-Encoding: gzip,deflate
    Connection: keep-alive
    Origin: https://foo.example
    Access-Control-Request-Method: POST
    Access-Control-Request-Headers: X-PINGOTHER, Content-Type
    ```

    HTTP/1.1 204 No Content
    ``` Server Response
    Date: Mon, 01 Dec 2008 01:15:39 GMT
    Server: Apache/2.0.61 (Unix)
    Access-Control-Allow-Origin: https://foo.example
    Access-Control-Allow-Methods: POST, GET, OPTIONS
    Access-Control-Allow-Headers: X-PINGOTHER, Content-Type
    Access-Control-Max-Age: 86400
    Vary: Accept-Encoding, Origin
    Keep-Alive: timeout=2, max=100
    Connection: Keep-Alive
    ```

    """
    return responses.Response(
        status_code=204,
        headers={
            'Access-Control-Allow-Origin': 'http://127.0.0.1:3000',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS, PATCH',
            'Access-Control-Allow-Headers': 'X-TOKEN, Content-Type',
            'Access-Control-Max-Age': '86400',
        },
    )


@app.delete('/api/v3/')
async def api_v3_delete():
    """Responses

    If a DELETE method is successfully applied, there are several response status codes possible:

        A 202 (Accepted) status code if the action will likely succeed but has not yet been enacted.

        A 204 (No Content) status code if the action has been enacted
        and no further information is to be supplied.

        A 200 (OK) status code if the action has been enacted and the
        response message includes a representation describing the status.
    """
    return {'purpose': 'The DELETE deletes the specified resource. '}


@app.head('/api/v3/', status_code=204)
async def api_v3_head():
    """The HEAD requests the headers that would be returned if the HEAD
    request's URL was instead requested with the HTTP GET method. For
    example, if a URL might produce a large download, a HEAD request
    could read its Content-Length header to check the filesize without
    actually downloading the file."""
    return {'purpose': ''}
