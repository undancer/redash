from flask_babel import Babel


def init_app(app):
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
    babel = Babel(app)
