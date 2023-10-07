""" Prometheus client """

import asyncio
import os
import threading
import time
from typing import Optional

import structlog
from prometheus_client import CollectorRegistry, push_to_gateway, start_http_server
from pydantic import BaseModel

from kelvin.sdk.pubsub import PrometheusConfig

logger = structlog.get_logger(__name__)


ENV_EDGETELEMETRY_IP = "KELVIN_EDGETELEMETRY_IP"
ENV_EDGETELEMETRY_PORT = "KELVIN_EDGETELEMETRY_PORT"


class PrometheusHttpServerConfig(BaseModel):
    port: int


class PrometheusPushGatewayConfig(BaseModel):
    ip: str
    port: str
    sleep_rate: float = 10
    timeout: float = 10


class PrometheusConfiguration(BaseModel):
    """Prometheus Configuration"""

    http_server: Optional[PrometheusHttpServerConfig]
    push_gateway: Optional[PrometheusPushGatewayConfig]


class HeartbeatConfig(BaseModel):
    enabled: bool = False


class Telemetry(BaseModel):
    heartbeat: HeartbeatConfig = HeartbeatConfig()
    prometheus: Optional[PrometheusConfiguration]


class PrometheusHttpServer:
    def __init__(self, port: int = 8000) -> None:
        try:
            start_http_server(port)
        except Exception as e:
            logger.exception(
                "Failed to start Prometheus http server on given port",
                exception=e,
                port=port,
            )


class PrometheusPushGateway:
    def __init__(
        self, ip: str, port: str, job: str, sleep_rate: float, timeout: float, event_loop: bool
    ) -> None:
        self.registry: CollectorRegistry = CollectorRegistry()
        self.gateway: str = f"{ip}:{port}"
        self.job: str = job
        self.sleep_rate: float = sleep_rate
        self.timeout: float = timeout
        PrometheusConfig.add_registry(self.registry)
        if event_loop:
            loop = asyncio.get_event_loop()
            loop.create_task(self._push_service_async())
        else:
            t = threading.Thread(target=self._push_service)
            t.daemon = True
            t.start()

    def push_to_gateway(self) -> None:
        try:
            push_to_gateway(
                gateway=self.gateway,
                job=self.job,
                registry=self.registry,
                timeout=self.timeout,
            )
        except Exception as e:
            logger.exception(
                "Failed to push Prometheus metrics to gateway",
                gateway=self.gateway,
                exception=e,
            )

    def _push_service(self) -> None:
        while True:
            self.push_to_gateway()
            time.sleep(self.sleep_rate)

    async def _push_service_async(self) -> None:
        while True:
            self.push_to_gateway()
            await asyncio.sleep(self.sleep_rate)


class PrometheusClient:

    _http_server: Optional[PrometheusHttpServer]
    _push_gateway: Optional[PrometheusPushGateway]
    _push_gateway_job: str = "workload"
    heartbeat_enabled: bool = False
    http_server: Optional[PrometheusHttpServerConfig] = None
    push_gateway: Optional[PrometheusPushGatewayConfig] = None

    def __init__(self, event_loop: bool = True) -> None:
        if self.http_server is not None:
            self._http_server = PrometheusHttpServer(self.http_server.port)

        ip = os.environ.get(ENV_EDGETELEMETRY_IP)
        port = os.environ.get(ENV_EDGETELEMETRY_PORT)
        if ip is not None and port is not None:
            self.push_gateway = PrometheusPushGatewayConfig(ip=ip, port=port)
        if self.heartbeat_enabled and self.push_gateway is not None:
            self._push_gateway = PrometheusPushGateway(
                self.push_gateway.ip,
                self.push_gateway.port,
                self._push_gateway_job,
                self.push_gateway.sleep_rate,
                self.push_gateway.timeout,
                event_loop,
            )

    @classmethod
    def assign_config(cls, config: Telemetry) -> None:
        cls.heartbeat_enabled = config.heartbeat.enabled
        if config.prometheus is not None:
            cls.http_server = config.prometheus.http_server
            cls.push_gateway = config.prometheus.push_gateway

    @classmethod
    def assign_workload(cls, workload: str) -> None:
        cls._push_gateway_job = workload
