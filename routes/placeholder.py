from flask import Blueprint, render_template

placeholder_bp = Blueprint('placeholder', __name__)


@placeholder_bp.route('/placeholder')
def placeholder():
    return render_template('placeholder.html')
