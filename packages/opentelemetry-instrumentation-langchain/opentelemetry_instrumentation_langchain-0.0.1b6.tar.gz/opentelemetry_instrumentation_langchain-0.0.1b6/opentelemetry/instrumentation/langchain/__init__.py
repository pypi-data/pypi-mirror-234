"""OpenTelemetry Langchain instrumentation"""
import logging
from typing import Collection
from wrapt import wrap_function_wrapper

from opentelemetry import context as context_api
from opentelemetry.trace import get_tracer, SpanKind
from opentelemetry.trace.status import Status, StatusCode

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import (
    _SUPPRESS_INSTRUMENTATION_KEY,
    unwrap,
)

from opentelemetry.semconv.ai import SpanAttributes, LLMRequestTypeValues, TraceloopSpanKindValues

logger = logging.getLogger(__name__)

_instruments = ("langchain >= 0.0.200",)
__version__ = "0.1.0"

WRAPPED_METHODS = [
    {
        "object": "LLMChain",
        "method": "run",
        "span_name": "llm_chain.run"
    },
    {
        "object": "LLMChain",
        "method": "arun",
        "span_name": "llm_chain.run"
    },
    {
        "object": "LLMChain",
        "method": "__call__",
        "span_name": "llm_chain.run"
    },
    {
        "object": "LLMChain",
        "method": "acall",
        "span_name": "llm_chain.run"
    },
    {
        "object": "TransformChain",
        "method": "run",
        "span_name": "transform_chain.run"
    },
    {
        "object": "TransformChain",
        "method": "arun",
        "span_name": "transform_chain.run"
    },
    {
        "object": "TransformChain",
        "method": "__call__",
        "span_name": "transform_chain.run"
    },
    {
        "object": "TransformChain",
        "method": "acall",
        "span_name": "transform_chain.run"
    },
]


def _with_tracer_wrapper(func):
    """Helper for providing tracer for wrapper functions."""

    def _with_tracer(tracer, to_wrap):
        def wrapper(wrapped, instance, args, kwargs):
            return func(tracer, to_wrap, wrapped, instance, args, kwargs)

        return wrapper

    return _with_tracer


@_with_tracer_wrapper
def _wrap(tracer, to_wrap, wrapped, instance, args, kwargs):
    """Instruments and calls every function defined in TO_WRAP."""
    if context_api.get_value(_SUPPRESS_INSTRUMENTATION_KEY):
        return wrapped(*args, **kwargs)

    name = to_wrap.get("span_name")
    with tracer.start_as_current_span(name) as span:
        span.set_attribute(
            SpanAttributes.TRACELOOP_SPAN_KIND,
            TraceloopSpanKindValues.TASK.value,
        )
        span.set_attribute(SpanAttributes.TRACELOOP_ENTITY_NAME, name)

        return wrapped(*args, **kwargs)


class LangchainInstrumentor(BaseInstrumentor):
    """An instrumentor for Langchain SDK."""

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, __version__, tracer_provider)
        for wrapped_method in WRAPPED_METHODS:
            wrap_object = wrapped_method.get("object")
            wrap_method = wrapped_method.get("method")
            wrap_function_wrapper(
                "langchain", f"{wrap_object}.{wrap_method}", _wrap(tracer, wrapped_method)
            )

    def _uninstrument(self, **kwargs):
        for wrapped_method in WRAPPED_METHODS:
            wrap_object = wrapped_method.get("object")
            unwrap(f"langchain.{wrap_object}", wrapped_method.get("method"))
