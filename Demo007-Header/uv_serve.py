if __name__ == '__main__':
    from pathlib import Path

    import uvicorn

    uvicorn.run(
        'app:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
        reload_delay=0,
        reload_dirs=[str(Path(__file__).parent.resolve())],
    )
