if __name__ == '__main__':
    from pathlib import Path

    import uvicorn

    uvicorn.run(
        'app:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
        reload_delay=10,
        reload_includes=[
            './app.py',
            './api_models.py',
            './routes/',
        ],
    )
