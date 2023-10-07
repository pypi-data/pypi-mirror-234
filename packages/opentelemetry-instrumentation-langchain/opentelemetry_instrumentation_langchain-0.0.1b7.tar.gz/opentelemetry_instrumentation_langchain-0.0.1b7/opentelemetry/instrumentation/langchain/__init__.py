"""OpenTelemetry Langchain instrumentation"""
import logging
from typing import Collection
from wrapt import wrap_function_wrapper

from opentelemetry.trace import get_tracer

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import (
    _SUPPRESS_INSTRUMENTATION_KEY,
    unwrap,
)

from opentelemetry.instrumentation.langchain.task_wrapper import task_wrapper

logger = logging.getLogger(__name__)

_instruments = ("langchain >= 0.0.200",)
__version__ = "0.1.0"

WRAPPED_METHODS = [
    {
        "package": "langchain.chains.llm",
        "object": "LLMChain",
        "method": "run",
        "span_name": "llm_chain.run",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.chains.llm",
        "object": "LLMChain",
        "method": "arun",
        "span_name": "llm_chain.run",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.chains.llm",
        "object": "LLMChain",
        "method": "__call__",
        "span_name": "llm_chain.run",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.chains.llm",
        "object": "LLMChain",
        "method": "acall",
        "span_name": "llm_chain.run",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.chains.transform",
        "object": "TransformChain",
        "method": "run",
        "span_name": "transform_chain.run",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.chains.transform",
        "object": "TransformChain",
        "method": "arun",
        "span_name": "transform_chain.run",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.chains.transform",
        "object": "TransformChain",
        "method": "__call__",
        "span_name": "transform_chain.run",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.chains.transform",
        "object": "TransformChain",
        "method": "acall",
        "span_name": "transform_chain.run",
        "wrapper": task_wrapper,
    },
]


def _with_tracer_wrapper(func):
    """Helper for providing tracer for wrapper functions."""

    def _with_tracer(tracer, to_wrap):
        def wrapper(wrapped, instance, args, kwargs):
            return func(tracer, to_wrap, wrapped, instance, args, kwargs)

        return wrapper

    return _with_tracer


class LangchainInstrumentor(BaseInstrumentor):
    """An instrumentor for Langchain SDK."""

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, __version__, tracer_provider)
        for wrapped_method in WRAPPED_METHODS:
            wrap_package = wrapped_method.get("package")
            wrap_object = wrapped_method.get("object")
            wrap_method = wrapped_method.get("method")
            wrapper = wrapped_method.get("wrapper")
            wrap_function_wrapper(
                wrap_package,
                f"{wrap_object}.{wrap_method}" if wrap_object else wrap_method,
                wrapper(tracer, wrapped_method),
            )

    def _uninstrument(self, **kwargs):
        for wrapped_method in WRAPPED_METHODS:
            wrap_object = wrapped_method.get("object")
            unwrap(f"langchain.{wrap_object}", wrapped_method.get("method"))
