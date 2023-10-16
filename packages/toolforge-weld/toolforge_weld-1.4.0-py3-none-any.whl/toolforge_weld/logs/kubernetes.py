from typing import Dict, Iterator, Optional

from dateutil.parser import parse as parse_date

from toolforge_weld.kubernetes import K8sClient
from toolforge_weld.logs.source import LogEntry, LogSource

KUBERNETES_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class KubernetesSource(LogSource):
    def __init__(self, *, client: K8sClient) -> None:
        super().__init__()
        self.client = client

    def _get_pod_logs(
        self,
        *,
        pod_name: str,
        container_name: str,
        follow: bool,
        lines: Optional[int],
    ) -> Iterator[LogEntry]:
        params = {
            "container": container_name,
            "follow": follow,
            "pretty": True,
            "timestamps": True,
        }
        if lines:
            params["tailLines"] = lines

        for line in self.client.get_raw_lines(
            "pods",
            name=pod_name,
            subpath="/log",
            params=params,
            version=K8sClient.VERSIONS["pods"],
            timeout=None if follow else self.client.timeout,
        ):
            datetime, message = line.split(" ", 1)
            yield LogEntry(
                pod=pod_name,
                container=container_name,
                datetime=parse_date(datetime),
                message=message,
            )

    def query(
        self, *, selector: Dict[str, str], follow: bool, lines: Optional[int]
    ) -> Iterator[LogEntry]:
        # FIXME: in follow mode, might want to periodically query
        # if there are new pods
        pods = self.client.get_objects(
            "pods",
            label_selector=selector,
        )

        if not pods:
            return []

        # TODO: this needs multi-threading or some other trickery (asyncio?)
        # to work in follow mode with multiple containers
        for pod in pods:
            container_name = pod["spec"]["containers"][0]["name"]
            for entry in self._get_pod_logs(
                pod_name=pod["metadata"]["name"],
                container_name=container_name,
                follow=follow,
                lines=lines,
            ):
                yield entry
