"""Prometheus client logic"""

from __future__ import annotations

from typing import Dict, Set, Tuple

from prometheus_client import REGISTRY, CollectorRegistry, Gauge


class PrometheusConfig:

    _registries: Set[CollectorRegistry] = {REGISTRY}
    _thresholds: Dict[Tuple[str, str], float] = {}

    @classmethod
    def add_registry(cls, registry: CollectorRegistry) -> None:
        cls._registries.add(registry)

    @classmethod
    def set_asset_metric_threshold(cls, asset: str, metric: str, threshold: float) -> None:
        cls._thresholds[(asset, metric)] = threshold


class AssetMetricHeartbeat(PrometheusConfig):

    asset_metric_last_timestamp = Gauge(
        "asset_metric_last_timestamp",
        "This is a generated metric for the last timestamp of a message",
        ["workload", "asset", "metric"],
    )
    asset_metric_threshold_in_sec = Gauge(
        "asset_metric_threshold_in_sec",
        "This is a generated metric for the duration of seconds until the associated metric becomes stale",
        ["workload", "asset", "metric"],
    )

    _current_registries: Set[CollectorRegistry] = {REGISTRY}

    def __init__(self, workload: str) -> None:
        self._default_threshold: int = 5 * 60  # seconds
        self.workload: str = workload
        for registry in self._registries:
            if registry not in self._current_registries:
                self._current_registries.add(registry)
                registry.register(self.asset_metric_last_timestamp)
                registry.register(self.asset_metric_threshold_in_sec)

    def set_asset_metric_timestamp(self, asset: str, metric: str) -> None:
        self.asset_metric_last_timestamp.labels(
            workload=self.workload, asset=asset, metric=metric
        ).set_to_current_time()
        self.asset_metric_threshold_in_sec.labels(
            workload=self.workload, asset=asset, metric=metric
        ).set(self._thresholds.setdefault((asset, metric), self._default_threshold))
