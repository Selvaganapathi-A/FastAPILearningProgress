from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, func, insert, select, update
from typing import Annotated

import api_models
import database
import database_models


@asynccontextmanager
async def application_initializer(app: FastAPI):
    await database.dropTables()
    await database.createTables()
    yield
    await database.dropTables()
    await database.ASYNCENGINE.dispose()


SessionDependency = Annotated[
    database.AsyncSession, Depends(database.session_dependency)
]


app: FastAPI = FastAPI(lifespan=application_initializer)


@app.post('/api/hero', response_model=api_models.HeroPublic)
async def create_hero(
    hero: api_models.HeroCreate, session: SessionDependency
) -> api_models.HeroPublic:
    print(hero)
    pk = await session.execute(
        insert(database_models.Hero).values(hero.model_dump())
    )
    await session.commit()

    return api_models.HeroPublic(
        pk=pk.lastrowid,
        name=hero.name,
        age=hero.age,
    )


@app.get('/api/hero')
async def read_all_hero(
    session: SessionDependency,
    offset: int = 0,
    limit: Annotated[int, Query(gt=0, le=20)] = 5,
):
    rowcount = await session.execute(
        select(func.count(database_models.Hero.pk))
    )
    total_records = rowcount.scalar_one()
    result = await session.execute(
        select(database_models.Hero.pk, database_models.Hero.name).slice(
            offset,
            offset + limit,
        )
    )
    return {
        'about': 'read all hero',
        'registered': total_records,
        'registered_list': result.mappings().fetchall(),
    }


@app.get('/api/hero/{hero_id}')
async def read_hero(hero_id: int, session: SessionDependency):
    result = await session.get(entity=database_models.Hero, ident=hero_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'reason': 'Hero not registered.'},
        )
    return {
        'about': 'read',
        'hero_id': hero_id,
        'hero': jsonable_encoder(result),
    }


@app.put('/api/hero/{hero_id}')
async def replace_hero(
    hero_id: int, hero: api_models.HeroCreate, session: SessionDependency
):
    await session.execute(
        update(database_models.Hero)
        .filter(database_models.Hero.pk == hero_id)
        .values(
            hero.model_dump(),
        ),
    )
    return {'about': 'replace', 'hero_id': hero_id, 'hero': hero}


@app.patch('/api/hero/{hero_id}')
async def modify_hero(
    hero_id: int, hero: api_models.HeroUpdate, session: SessionDependency
):
    await session.execute(
        update(database_models.Hero)
        .filter(database_models.Hero.pk == hero_id)
        .values(
            hero.model_dump(exclude_unset=True),
        ),
    )
    return {'about': 'modify', 'hero_id': hero_id, 'hero': hero}


@app.delete('/api/hero/{hero_id}')
async def delete_hero(hero_id: int, session: SessionDependency):
    result = await session.execute(
        delete(database_models.Hero).filter(database_models.Hero.pk == hero_id)
    )
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'reason': 'Hero not registered.'},
        )
    return {'about': 'delete', 'hero_id': hero_id}
