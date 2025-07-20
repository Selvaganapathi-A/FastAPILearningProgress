from fastapi import FastAPI


tags_metadata = [
    {
        'name': 'users',
        'description': 'Operations with users. The **login** logic is also here.',
    },
    {
        'name': 'items',
        'description': 'Manage items. So _fancy_ they have their own docs.',
        'externalDocs': {
            'description': 'Items external docs',
            'url': 'https://fastapi.tiangolo.com/',
        },
    },
]


app = FastAPI(
    title='Task App',
    summary='Some Description of my Task App',
    description='Detailed Description of my Application.',
    # ! not FastAPI or OpenAPI Version
    version='0.1.12b',
    terms_of_service='https://termsofservice.tasks-lamdallc.com',
    contact={
        'name': 'john elwis',
        'url': 'https://john-elwis.mydomain.com',
        'email': 'john-elwis-sysadmin@lamdallc.com',
    },
    license_info={
        'name': 'Apache 2.0',
        'identifier': 'MIT',
        'url': 'https://localhost:8000/license/mit',
    },
    tags_metadata=tags_metadata,
    openapi_tags=[
        {
            'name': 'user',
            'description': 'Some **U**ser _desc_',
            'externalDocs': {
                'description': '-hello-',
                'url': 'http://127.0.0.1:8000/',
            },
        },
        {
            'name': 'admin',
            'description': 'Some **Admin** user _desc_',
            'externalDocs': {
                'description': '-admin-',
                'url': 'http://127.0.0.1:8000/',
            },
        },
    ],
)


@app.get('/')
async def get_root():
    return {
        'routes': [
            '/',
        ]
    }
