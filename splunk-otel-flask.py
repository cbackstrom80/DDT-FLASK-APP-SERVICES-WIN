#### HACK FOR STDIO ERROR #####
import os, sys
for _name in ('stdin', 'stdout', 'stderr'):
    if getattr(sys, _name) is None:
        setattr(sys, _name, open(os.devnull, 'r' if _name == 'stdin' else 'w'))
del _name # clean up this module's name space a little (optional)



from splunk_otel.tracing import start_tracing
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
from flask import Flask
import requests
from waitress import serve  

# Create app context  and use OTEL to instrument


start_tracing(service_name='digitaldrivethru')
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)


@app.route('/')
def hello_world():
	tracer = trace.get_tracer(__name__)
	with tracer.start_as_current_span("Get Reccomedations"):
		r = requests.get("http://www.splunk.com")
		with tracer.start_as_current_span("digital-drive-thru-flask"):
                	print("deepbrew")


	return r.url



serve(app, host='0.0.0.0', port=os.environ["SERVER_PORT"])