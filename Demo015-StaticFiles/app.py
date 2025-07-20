from fastapi import FastAPI, staticfiles


app: FastAPI = FastAPI()

app.mount(
    '/static',
    staticfiles.StaticFiles(
        directory=r'D:/dodo-WD-BE/Truss/Demo015-StaticFiles/static/',
    ),
    name='static-09e3drf6',
)


@app.get('/')
async def get_root():
    return {
        'route': '/',
        'message': 'rootpath',
    }
