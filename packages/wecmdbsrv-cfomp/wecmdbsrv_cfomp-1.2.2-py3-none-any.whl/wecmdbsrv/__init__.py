import os
import logging
from flask import Flask


class DefaultConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'JqjQoDgepSTEzlv0IuZGVw==')
    WEWORK_TOKEN = os.environ.get('WEWORK_TOKEN')
    WEWORK_ENCODING_AES_KEY = os.environ.get('WEWORK_ENCODING_AES_KEY')
    WEWORK_CORPID = os.environ.get('WEWORK_CORPID')
    WEWORK_AGENTID = os.environ.get('WEWORK_AGENTID')
    WEWORK_SECRET = os.environ.get('WEWORK_SECRET')
    ES_HOSTS = os.environ.get('ES_HOSTS', 'localhost').split()
    ES_SIZE = os.environ.get('ES_SIZE', 20)
    ES_TIMEOUT = os.environ.get('ES_TIMEOUT')
    EXTERNAL_URL = os.environ.get('EXTERNAL_URL')
    URL_PREFIX = os.environ.get('URL_PREFIX', '/wecmdbsrv')


def create_flask_app(**kwargs):
    app = Flask(
        __name__,
        static_url_path=os.environ.get('URL_PREFIX', '/wecmdbsrv')
    )
    app.config.from_object(DefaultConfig)
    app.config.from_envvar("PROJECT_SETTING", silent=True)
    app.config.update(kwargs)
    from .views import basic, host, oauth
    app.register_blueprint(basic.bp, url_prefix=app.config['URL_PREFIX'])
    app.register_blueprint(host.bp, url_prefix=app.config['URL_PREFIX'])
    app.register_blueprint(oauth.bp, url_prefix=app.config['URL_PREFIX'])
    return app


app = create_flask_app()

# make app to use gunicorn logger handler
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run(debug=True)
