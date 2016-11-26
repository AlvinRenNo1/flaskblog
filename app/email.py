from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(recipients, **kwargs):
    app = current_app._get_current_object()
    msg = Message("账号确认", sender=app.config['MAIL_SENDER'], recipients=recipients)
    msg.body = "欢迎您, 新用户"
    msg.html = render_template('auth/confirm_email_body.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
