"""Mixin for a WorkflowDataTaskBase subclass which implements interservice bus access functionality."""
from typing import Any

from talus import DurableBlockingProducerWrapper

from dkist_processing_common._util.config import service_configuration


class InterserviceBusMixin:
    """Mixin for a WorkflowDataTaskBase subclass which implements interservice bus access functionality."""

    @staticmethod
    def _interservice_bus_parse_bindings(messages: list) -> list[dict[str, str]]:
        # @message_class decorated messages only
        # transform in to a single list
        all_bindings = []
        for m in messages:
            all_bindings += m.binding()
        # dedup
        result = []
        for binding in all_bindings:
            if binding not in result:
                result.append(binding)
        return result

    def interservice_bus_publish(self, messages: list[Any] | object):
        """Publish messages on the interservice bus."""
        if not isinstance(messages, list):
            messages = [messages]
        # @message_class decorated messages only
        bindings = self._interservice_bus_parse_bindings(messages=messages)
        with DurableBlockingProducerWrapper(
            producer_queue_bindings=bindings,
            publish_exchange=service_configuration.isb_exchange,
            rabbitmq_host=service_configuration.isb_mesh_service.host,
            rabbitmq_port=service_configuration.isb_mesh_service.port,
            rabbitmq_user=service_configuration.isb_username,
            rabbitmq_pass=service_configuration.isb_password,
            retry_delay=service_configuration.retry_config.retry_delay,
            retry_backoff=service_configuration.retry_config.retry_backoff,
            retry_jitter=service_configuration.retry_config.retry_jitter,
            retry_max_delay=service_configuration.retry_config.retry_max_delay,
            retry_tries=service_configuration.retry_config.retry_tries,
        ) as producer:
            for message in messages:
                producer.publish_message(message)
