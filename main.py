import uvicorn

from utils.env_configuration import env_config


def main():
    host = env_config['app']['host']
    port = int(env_config['app']['port'])
    reload = bool(int(env_config['app']['reload']))
    workers = int(env_config['app']['workers'])
    uvicorn.run('app:app', host=host, port=port, reload=reload, workers=workers)


def main():
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    main()
