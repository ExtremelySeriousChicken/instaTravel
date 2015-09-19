# This file explains what happens when the main encounter a problem
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render'<h1>Page not found Boo Hoo 404!</h1>", 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render'<h1>There is something wrong with the server</h1>'. 500
