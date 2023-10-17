""" MCLI Abstraction for Clusters """
from __future__ import annotations

from dataclasses import dataclass


# TODO: Deprecate this in favor of ClusterDetails
@dataclass
class Cluster:
    """Configured MCLI cluster relating to specific kubernetes context
    """
    name: str
    kubernetes_context: str
    namespace: str
