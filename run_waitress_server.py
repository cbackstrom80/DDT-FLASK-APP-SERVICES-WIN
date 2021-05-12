import os
from waitress import serve
from splunk-otel-flask import app

serve(splunk-otel-flask.app, host='0.0.0.0', port=8080)