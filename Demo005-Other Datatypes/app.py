from datetime import date, datetime, time, timedelta
from decimal import Decimal
from fastapi import FastAPI, status
from uuid import UUID


app: FastAPI = FastAPI()


app: FastAPI = FastAPI()


@app.get('/', status_code=status.HTTP_200_OK)
async def root(
    unique_id: UUID,
    created: datetime,
    modified: date,
    last_access_time: time,
    last_downtime: timedelta,
    image: bytes,
    weight: Decimal,
):
    print('UUID', unique_id)
    print('datetime', created)
    print('date', modified)
    print('time', last_access_time)
    print('timedelta', last_downtime)
    print('bytes', image)
    print('Decimal', weight)
    return {
        'message': 'The Following datatypes are converted automatically.',
        'Datatypes': {
            'UUID': unique_id,
            'datetime': created,
            'date': modified,
            'time': last_access_time,
            'timedelta': last_downtime,
            'bytes': image,
            'Decimal': weight,
        },
    }


"""

# print(UUID(bytes=b'1234123412341234').hex)
# print(datetime.now().isoformat())
# print(date.today().isoformat())
# print(time(23, 50, 50).isoformat())
# print(timedelta(days=23, seconds=50, microseconds=50))



Extra datatypes other than native common datatypes

    Request:
        http://127.0.0.1:8000/?unique_id=31323334313233343132333431323334&
        created=2025-05-10T21:59:41.260168&modified=2025-05-10&
        last_access_time=21:59:41.260168&last_downtime=4 days&
        image=skdfjskdjfhksdjf&weight=32.123

    Response
                   unique_id 31323334-3132-3334-3132-333431323334
                     created 2025-05-10 21:59:41.260168
                    modified 2025-05-10
            last_access_time 21:59:41.260168
               last_downtime 4 days, 0:00:00
                       image b'skdfjskdjfhksdjf'
                      weight 32.123
"""
