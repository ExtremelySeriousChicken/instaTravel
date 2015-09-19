from . import app
@app.route('/')
def index():
    return '<h1>Welcome!</h1>'