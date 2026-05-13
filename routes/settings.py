from flask import Blueprint, jsonify, make_response, request
from flask_login import current_user
from data import db_session
from data.users import Users
from utils.theme import THEME_LIGHT, THEME_DARK

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/theme', methods=['POST'])
def set_theme():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        new_theme = 'light' if current_user.theme == 'dark' else 'dark'
        user = db_sess.query(Users).get(current_user.id)
        user.theme = new_theme
        db_sess.commit()
    else:
        current_theme = request.cookies.get('user_theme', 'light')
        new_theme = 'light' if current_theme == 'dark' else 'dark'

    if new_theme == 'light':
        theme_var = THEME_LIGHT
    else:
        theme_var = THEME_DARK

    resp = make_response(jsonify({
        'theme_name': new_theme,
        'variables': theme_var
    }))

    resp.set_cookie('user_theme', new_theme, max_age=365 * 24 * 60 * 60)
    return resp
