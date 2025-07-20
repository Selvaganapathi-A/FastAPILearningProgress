from enum import StrEnum
from fastapi import FastAPI, Path
from typing import Annotated


app: FastAPI = FastAPI()


@app.get('/items/{itemid}')
async def get_item_id(itemid: int):
    return {'message': 'Read Path Parameter', 'response': {'Item ID': itemid}}


@app.get('/files/{filepath:path}')
async def read_path(filepath: str):
    return {
        'message': 'Read Path Parameter',
        'response': {'Filepath': filepath},
    }


# path parameter type convert like (slug, str, int, float, path, etc...)
@app.get('/images/{image:str}')
async def read_image(image: str):
    return {'message': 'Read Path Parameter', 'response': {'image': image}}


# ! ------------ Enumerators in Path ----------------- !"


class Device(StrEnum):
    Nokia = 'nokia'
    Sony = 'sony'
    Blackberry = 'blackberry'
    Microsoft = 'microsoft'
    RedMI = 'redmi'
    XioMI = 'xiomi'
    Nothing = 'nothing'


@app.get('/devices/{device}')
async def read_avilablity(device: Device):
    if device.value in ('nokia', 'sony', 'blackberry'):
        return {
            'message': 'Read Path Parameter as Enum Object',
            'response': {
                'Device': device,
                'status': 'discontinued a decade ago.',
            },
        }
    elif device == Device.Microsoft:
        return {
            'message': 'Read Path Parameter as Enum Object',
            'response': {'Device': device, 'status': 'US Only.'},
        }
    elif device.name in ('XioMI', 'RedMI'):
        return {
            'message': 'Read Path Parameter as Enum Object',
            'response': {'Device': device, 'status': 'China Exports.'},
        }
    else:
        return {
            'message': 'Read Path Parameter as Enum Object',
            'response': {'Device': device.name, 'status': 'Unknown.'},
        }


""" Advanced Path Params """


@app.get('/product/{category}')
async def product_category(
    category: Annotated[
        int,
        Path(
            title='Some Title',
            description='Some Other Description about Path.',
            # * validators
            ge=100,
            lt=1000,
            # * tags to be used in api docs [redoc, docs(swagger)]
            tags=['product', 'category'],
        ),
    ],
) -> dict[str, str]:
    if 100 <= category < 250:
        return {'Category': 'Environmental Friendly'}
    elif 250 <= category < 500:
        return {'Category': 'Handle With Care'}
    elif 500 <= category < 750:
        return {'Category': 'Dangereous Chemical'}
    elif 750 <= category < 1000:
        return {'Category': 'Use Only in Research Facilities'}
    else:
        return {'Category': 'Unknown Category'}
