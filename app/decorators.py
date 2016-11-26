from functools import wraps
from flask import abort, redirect, url_for, render_template
from flask_login import current_user
from .models import Permission
from .email import send_email

# 这是最基本的装修器
def confirmed_required(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            token = current_user.generate_confirmation_token()
            send_email([current_user.email], token=token)
            return render_template('auth/confirm_required.html')
        return fn(*args, **kwargs)
    return decorated_function


# 带参数的装饰器最外一层函数将在解释器载入时执行
def permission_required(permission):
    def decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return fn(*args, **kwargs)
        return decorated_function
    return decorator


def only_user(login_name):
    def decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            if not current_user.confirmed or current_user.login_name != login_name:
                abort(403)
            return fn(*args, **kwargs)
        return decorated_function
    return decorator
