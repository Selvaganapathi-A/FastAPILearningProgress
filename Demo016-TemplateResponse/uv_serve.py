if __name__ == '__main__':
    from pathlib import Path

    current_dir = str(Path(__file__).parent)
    import uvicorn

    uvicorn.run(
        'app:app',
        reload=True,
        reload_delay=0,
        reload_dirs=[
            current_dir,
        ],
        # workers=4,
    )
