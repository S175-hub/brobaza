import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, current_user
from data import db_session
from data.users import Users
from routes.api import api_bp
from routes.comments import comment_bp
from routes.create import create_bp
from routes.feed import feed_bp
from routes.follow import follow_bp
from routes.likes import like_bp
from routes.login import login_bp
from routes.placeholder import placeholder_bp
from routes.post import post_bp
from routes.profile import profile_bp
from routes.profile_edit import profile_edit_bp
from routes.profile_setup import profile_setup_bp
from routes.register import register_bp
from routes.settings import settings_bp
from ui.emojis import EMOJI_LIST
from ui.icons import LIKE_ICON_EMPTY, LIKE_ICON_FILLED, BACK_ICON, COMMENT_ICON
from ui.menu import SIDEBAR_MENU
from utils.theme import THEME_DARK, THEME_LIGHT

load_dotenv()


def create_app():
    app = Flask(__name__)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'data', 'database.db')
    db_session.global_init(DB_PATH)
    return app


app = create_app()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove_session()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(int(user_id))


@app.context_processor
def inject_sidebar():
    return {"SIDEBAR_MENU": SIDEBAR_MENU}


@app.context_processor
def inject_emojis():
    return dict(EMOJI_LIST=EMOJI_LIST)


@app.context_processor
def inject_icons():
    return dict(
        LIKE_ICON_EMPTY=LIKE_ICON_EMPTY,
        LIKE_ICON_FILLED=LIKE_ICON_FILLED,
        BACK_ICON=BACK_ICON,
        COMMENT_ICON=COMMENT_ICON
    )


@app.context_processor
def inject_theme():
    if current_user.is_authenticated:
        theme_name = current_user.theme
    else:
        theme_name = request.cookies.get('user_theme', 'light')

    current_theme_var = THEME_LIGHT if theme_name == 'light' else THEME_DARK

    return dict(THEME=current_theme_var, THEME_NAME=theme_name)


app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(profile_setup_bp)
app.register_blueprint(feed_bp)
app.register_blueprint(create_bp)
app.register_blueprint(post_bp)
app.register_blueprint(follow_bp)
app.register_blueprint(like_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(profile_edit_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(placeholder_bp)
app.register_blueprint(api_bp)
app.register_blueprint(comment_bp)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.route('/')
def index():
    return redirect(url_for('feed.feed'))


# if __name__ == '__main__':
#     db_session.global_init('data/database.db')
#     app.run(port=8080, host='127.0.0.1', debug=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
