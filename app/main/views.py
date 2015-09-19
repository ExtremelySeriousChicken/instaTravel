# This file will manage what happens when the users try to render a data

@main.route('/')
def index():
    render '<h1>Welcome!</h1>'
