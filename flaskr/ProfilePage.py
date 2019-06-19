from flask import Blueprint, flash, g, request, session, url_for
bp = Blueprint('profilePage',__name__, url_prefix='profile')

# @bp.route('/profile', methods = ['GET', 'POST', 'PUT'])
# def profile():
#     req = request.get_json()
