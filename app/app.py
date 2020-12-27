import time
from flask import Flask
import sqlite3

from opentelemetry import trace
from opentelemetry.exporter.otlp.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor


app = Flask(__name__)
trace.set_tracer_provider(TracerProvider())

tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint="otel-agent:55680")
span_processor = BatchExportSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)

dbconn = sqlite3.connect(":memory:", check_same_thread=False)


class BarException(Exception):
    pass


@app.route("/hello")
def hello():
    time.sleep(0.2)
    cursor = dbconn.cursor()

    with tracer.start_as_current_span('batch-call-service'):
        call_service()
        call_service()

    cursor.execute("SELECT * FROM USERS WHERE id = 1")
    cursor.close()
    dbconn.commit()

    call_error()

    return 'world!'


def call_service():
    with tracer.start_as_current_span('call-service'):
        time.sleep(0.1)
        return "served"


def call_error():
    with tracer.start_as_current_span('call-error'):
        foo()


def foo():
    bar()


def bar():
    raise BarException('There is an error in the code!')


@app.before_first_request
def initialize_database():
    c = dbconn.cursor()

    # Create table
    c.execute("""
    CREATE TABLE users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username text
    );
    """)

    # Insert a row of data
    c.execute("INSERT INTO users (username) VALUES ('foo')")
    c.execute("INSERT INTO users (username) VALUES ('bar')")
    c.execute("INSERT INTO users (username) VALUES ('hash')")

    # Save (commit) the changes
    dbconn.commit()
