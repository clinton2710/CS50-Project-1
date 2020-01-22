from flask import Flask, g, redirect, url_for, session, render_template, request, flash
from functools import wraps





def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))    
    return decorated_function     