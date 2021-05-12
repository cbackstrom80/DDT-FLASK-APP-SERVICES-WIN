# DDT Flask on Azure App Services WIN

These instructions are intended to help get Flask with SPLUNK-OTEL up and running on an APP Services windows instance.  

This "Assumes":
     Windows APP Service Instance.
     HttpPlatformHandler is the method for serving up the app.  (Web.config included)
     Environment Variables 
        - OTEL_EXPORTER_JAEGER_ENDPOINT=https://ingest.us1.signalfx.com/v2/trace
        - OTEL_RESOURCE_ATTRIBUTES=eployment.environment=demo
        - SPLUNK_ACCESS_TOKEN=<your access token>


## Installation

    - Create APP Service
    - Add extension Python 3.6
    - SET ENV VARIABLES
    - Deploy from git or VS, cli etc.
    - Note: Verify your python path matches web.config (I.E.: "D:\home\Python364x64\python.exe")


## How it works


In the spirit of getting it running, I imported the splunk-otel library to use the start_tracing() class. However I found it easier to use the otel libs for manual instrumentation and static spans.  Because the App Service handler was not running the app with app.run(), I used a WSGI (Waitress) to "serve"  the app context/module.

```python
from splunk_otel.tracing import start_tracing
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
from flask import Flask
import requests
from waitress import serve
``` 
    

# Create app context  and use OTEL to instrument

##### I Reccomend checking out splunk-otel python libs and find start_tracing()  ( https://github.com/signalfx/splunk-otel-python/blob/main/splunk_otel/tracing.py)




```python
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



serve(app, host='0.0.0.0', port=os.environ["SERVER_PORT"])```




