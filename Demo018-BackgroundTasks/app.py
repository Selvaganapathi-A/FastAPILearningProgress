from fastapi import BackgroundTasks, Depends, FastAPI, Query
from typing import Annotated

import asyncio
import random


app = FastAPI()


def get_random_number():
    return random.random() * 10


async def any_long_running_task(task_id: float, work: str):
    await asyncio.sleep(task_id)
    print(f'{task_id} - {work} Completed')


@app.get('/api')
async def get_root(
    backgroud_task: BackgroundTasks,
    task_id: Annotated[float, Depends(get_random_number)],
    work: Annotated[str | None, Query()] = None,
):
    if work is None:
        return {'request': 'request has no value'}
    backgroud_task.add_task(any_long_running_task, task_id, work)
    return {
        'route': '/',
        'message': '',
        'task completed after': task_id,
        'name': work,
    }
