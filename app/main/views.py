from datetime import datetime
from flask import render_template, session, redirect, url_for, abort

from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():

        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False), current_time=datetime.utcnow())
# 在蓝本中url_for()函数的使用方法不同，Flask会为蓝本中的全部端点加上一个命名空间，这样就可以在不同的蓝本中
# 使用相同的断电名定义视图函数，而不会产生冲突，所以视图函数index()注册的端点名是main.index,简写为.index


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
