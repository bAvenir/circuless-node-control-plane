from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from utils.config import settings

class Otel:
    def __init__(self, enabled: bool = True):
        self.service_name: str = "circ_node:" + settings.CLIENT_ID
        self.enabled: bool = enabled
        self.trace_provider: TracerProvider = None

    def setup_telemetry(self, app):
        """
        Configure OpenTelemetry with Zipkin exporter for traces.
        
        Args:
            app: FastAPI application instance
            service_name: Name of your service for identification in Zipkin
        """
        # Create a resource with service name
        resource = Resource(attributes={
            SERVICE_NAME: self.service_name
        })
        
        # Set up the tracer provider
        tracer_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer_provider)
        
        # Configure Zipkin exporter (default: http://localhost:9411)
        zipkin_exporter = ZipkinExporter(
            endpoint= settings.OTEL_ENDPOINT,
        )
        
        # Add BatchSpanProcessor to send spans in batches
        span_processor = BatchSpanProcessor(zipkin_exporter)
        tracer_provider.add_span_processor(span_processor)
        
        # Instrument FastAPI
        FastAPIInstrumentor.instrument_app(app)
        
        self.trace_provider = tracer_provider

        return


    def instrument_sqlalchemy(self, engine):
        """
        Instrument SQLAlchemy engine for automatic tracing.
        
        Args:
            engine: SQLAlchemy engine instance (AsyncEngine or Engine)
        """
        # For AsyncEngine, instrument the sync_engine
        if hasattr(engine, 'sync_engine'):
            SQLAlchemyInstrumentor().instrument(
                engine=engine.sync_engine,
                enable_commenter=True,
            )
        else:
            # For regular synchronous engine
            SQLAlchemyInstrumentor().instrument(
                engine=engine,
                enable_committer=True,
            )
        return

    def start_telemetry(self, app, engine):
        self.setup_telemetry(app)
        self.instrument_sqlalchemy(engine)
        print(f"✓ OpenTelemetry initialized with {settings.OTEL_EXPORTER} exporter")
        print(f"✓ Traces will be sent to {settings.OTEL_ENDPOINT}")
        return

    def stop_telemetry(self):
        self.trace_provider.shutdown()
        print("✓ OpenTelemetry shutdown complete")
        return