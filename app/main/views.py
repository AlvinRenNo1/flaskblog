from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm
from flask_login import login_required
from ..decorators import confirmed_required


@main.route('/', methods=['GET', 'POST'])
@login_required
@confirmed_required
def index():
    return render_template('index.html')
