from __future__ import annotations

from decimal import Decimal, InvalidOperation
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional

from toolforge_weld.api_client import ToolforgeClient
from toolforge_weld.errors import ToolforgeError
from toolforge_weld.kubernetes_config import Kubeconfig, locate_config_file


class ToolforgeKubernetesError(ToolforgeError):
    """Base class for exceptions related to the Kubernetes client."""


class KubernetesConfigFileNotFoundException(ToolforgeKubernetesError):
    """Raised when a Kubernetes client is attempted to be created but the configuration file does not exist."""


class MountOption(Enum):
    """Represents the option to configure which (if any) NFS mounts a specific Kubernetes workload has access to."""

    ALL = "all"
    """Option for mounting all available mounts."""
    NONE = "none"
    """Option to disable any mounts."""

    def __str__(self) -> str:
        return self.value

    @classmethod
    def parse(cls, option: str) -> "MountOption":
        """Tries to parse a string into an option."""
        return cls(option)

    @classmethod
    def parse_labels(cls, labels: dict[str, str]) -> "MountOption":
        """Tries to parse Kubernetes labels into a mount option."""
        return cls(labels.get("toolforge.org/mount-storage", "all"))

    @property
    def supports_non_buildservice(self) -> bool:
        """Whether this option can be used on non-buildservice images."""
        return self == MountOption.ALL

    @property
    def labels(self) -> dict[str, str]:
        """The labels that enable this mount option on a Pod."""
        return {"toolforge.org/mount-storage": self.value}


def _format_labels(labels: Dict[str, str]) -> str:
    return ",".join([f"{k}={v}" for k, v in labels.items()])


class K8sClient(ToolforgeClient):
    """Kubernetes API client."""

    VERSIONS: ClassVar[Dict[str, str]] = {
        "configmaps": "v1",
        "cronjobs": "batch/v1",
        "deployments": "apps/v1",
        "endpoints": "v1",
        "events": "v1",
        "ingresses": "networking.k8s.io/v1",
        "jobs": "batch/v1",
        "limitranges": "v1",
        "pods": "v1",
        "replicasets": "apps/v1",
        "resourcequotas": "v1",
        "services": "v1",
    }

    def __init__(
        self,
        *,
        kubeconfig: Kubeconfig,
        user_agent: str,
        timeout: int = 10,
    ):
        """Constructor."""
        self.server = kubeconfig.current_server
        self.namespace = kubeconfig.current_namespace
        super().__init__(
            server=self.server,
            kubeconfig=kubeconfig,
            user_agent=user_agent,
            timeout=timeout,
        )

    @classmethod
    def from_file(cls, file: Path, **kwargs) -> "K8sClient":
        """Deprecated: use regular __init__ instead."""
        return cls(kubeconfig=Kubeconfig.load(path=file), **kwargs)

    @staticmethod
    def locate_config_file() -> Path:
        """Deprecated: use Kubeconfig.load instead."""
        return locate_config_file()

    def make_kwargs(self, url: str, **kwargs):
        """Setup kwargs for a Requests request."""
        kwargs = super().make_kwargs(url=url, **kwargs)
        version = kwargs.pop("version", "v1")
        if version == "v1":
            root = "api"
        else:
            root = "apis"

        # use "or" syntax in case namespace is present but set as None
        namespace = kwargs.pop("namespace", None) or self.namespace

        kwargs["url"] = "{}/{}/{}/namespaces/{}/{}".format(
            self.server, root, version, namespace, url
        )

        name = kwargs.pop("name", None)
        if name is not None:
            kwargs["url"] = "{}/{}".format(kwargs["url"], name)

        subpath = kwargs.pop("subpath", None)
        if subpath is not None:
            kwargs["url"] = "{}{}".format(kwargs["url"], subpath)

        return kwargs

    def get_object(
        self,
        kind: str,
        name: str,
        *,
        namespace: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get the object with the specified name and of the given kind in the namespace."""
        return self.get(
            kind,
            name=name,
            version=K8sClient.VERSIONS[kind],
            namespace=namespace,
        )

    def get_objects(
        self,
        kind: str,
        *,
        label_selector: Optional[Dict[str, str]] = None,
        field_selector: Optional[Dict[str, Any]] = None,
        namespace: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get list of objects of the given kind in the namespace."""
        params: Dict[str, Any] = {}

        if label_selector:
            params["labelSelector"] = _format_labels(label_selector)
        if field_selector:
            params["fieldSelector"] = field_selector

        return self.get(
            kind,
            params=params,
            version=K8sClient.VERSIONS[kind],
            namespace=namespace,
        )["items"]

    def delete_objects(
        self,
        kind: str,
        *,
        label_selector: Optional[Dict[str, str]] = None,
    ):
        """Delete objects of the given kind in the namespace."""
        if kind == "services":
            # Annoyingly Service does not have a Delete Collection option
            for svc in self.get_objects(kind, label_selector=label_selector):
                self.delete(
                    kind,
                    name=svc["metadata"]["name"],
                    version=K8sClient.VERSIONS[kind],
                )
        else:
            params: Dict[str, Any] = {}
            if label_selector:
                params["labelSelector"] = _format_labels(label_selector)

            self.delete(
                kind,
                params=params,
                version=K8sClient.VERSIONS[kind],
            )

    def create_object(self, kind: str, spec: Dict[str, Any]):
        """Create an object of the given kind in the namespace."""
        return self.post(
            kind,
            json=spec,
            version=K8sClient.VERSIONS[kind],
        )

    def replace_object(self, kind: str, spec: Dict[str, Any]):
        """Replace an object of the given kind in the namespace."""
        return self.put(
            kind,
            json=spec,
            name=spec["metadata"]["name"],
            version=K8sClient.VERSIONS[kind],
        )

    def delete_object(self, kind: str, name: str) -> None:
        self.delete(
            kind,
            name=name,
            version=K8sClient.VERSIONS[kind],
        )


# Copyright 2019 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
def parse_quantity(quantity: str | int | float | Decimal) -> Decimal:
    """
    Parse kubernetes canonical form quantity like 200Mi to a decimal number.
    Supported SI suffixes:
    base1024: Ki | Mi | Gi | Ti | Pi | Ei
    base1000: n | u | m | "" | k | M | G | T | P | E
    See https://github.com/kubernetes/apimachinery/blob/master/pkg/api/resource/quantity.go # noqa
    Input:
    quantity: string. kubernetes canonical form quantity
    Returns:
    Decimal
    Raises:
    ValueError on invalid or unknown input
    """

    if isinstance(quantity, (int, float, Decimal)):
        return Decimal(quantity)

    exponents = {
        "n": -3,
        "u": -2,
        "m": -1,
        "K": 1,
        "k": 1,
        "M": 2,
        "G": 3,
        "T": 4,
        "P": 5,
        "E": 6,
    }
    quantity = str(quantity)
    raw_number = quantity
    suffix = None

    if len(quantity) >= 2 and quantity[-1] == "i":
        if quantity[-2] in exponents:
            raw_number = quantity[:-2]
            suffix = quantity[-2:]
    elif len(quantity) >= 1 and quantity[-1] in exponents:
        raw_number = quantity[:-1]
        suffix = quantity[-1:]

    try:
        number = Decimal(raw_number)
    except InvalidOperation:
        raise ValueError("Invalid number format: {}".format(raw_number))

    if suffix is None:
        return number
    if suffix.endswith("i"):
        base = 1024
    elif len(suffix) == 1:
        base = 1000
    else:
        raise ValueError("{} has unknown suffix".format(quantity))

    # handly SI inconsistency
    if suffix == "ki":
        raise ValueError("{} has unknown suffix".format(quantity))
    if suffix[0] not in exponents:
        raise ValueError("{} has unknown suffix".format(quantity))

    exponent = Decimal(exponents[suffix[0]])
    return number * (base**exponent)
