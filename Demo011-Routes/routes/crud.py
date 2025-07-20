from fastapi import APIRouter, Body
from typing import Annotated

import random


router: APIRouter = APIRouter()


@router.get('/')
async def read_all():
    return {
        'message': 'read all items',
        'items': [],
    }


@router.get('/{item_id}')
async def read(item_id: int):
    return {
        'message': 'read item',
        'particulars': {
            'item_id': item_id,
        },
    }


@router.post('/')
async def create(item: Annotated[str, Body()]):
    return {
        'message': 'create new item',
        'particulars': {
            'item_id': random.randint(0, 1000),
            'item': item,
        },
    }


@router.put('/{item_id}')
async def replace_existing_item(item_id: int, item: Annotated[str, Body()]):
    return {
        'message': 'replace item',
        'particulars': {
            'item_id': item_id,
            'item': item,
        },
    }


@router.patch('/{item_id}')
async def update_existing_item(item_id: int, item: Annotated[str, Body()]):
    return {
        'message': 'update item',
        'particulars': {
            'item_id': item_id,
            'item': item,
        },
    }


@router.delete('/{item_id}')
async def delete_item(item_id: int):
    return {
        'message': 'delete item',
        'particulars': {
            'item_id': item_id,
        },
    }
