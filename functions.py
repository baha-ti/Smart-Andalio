import functions_framework
from flask import Flask, request
from app import app as flask_app

@functions_framework.http
def app(request):
    """HTTP Cloud Function that serves the Flask application."""
    with flask_app.request_context(request.environ):
        return flask_app.full_dispatch_request() 