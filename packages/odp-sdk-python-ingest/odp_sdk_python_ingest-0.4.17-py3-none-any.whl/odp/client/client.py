"""ODP Client."""
import time
import urllib.parse
from json import loads
from typing import BinaryIO, Dict, List

from requests.adapters import HTTPAdapter
from urllib3 import Retry

from odp.compute.blocks.aad_client_credentials import AadClientCredentials

DATASET_CONFIG = {
    "tabular": {
        "storage_class": "registry.hubocean.io/storageClass/tabular",
        "storage_controller": "registry.hubocean.io/storageController/storage-tabular",
    },
    "raw": {
        "storage_class": "registry.hubocean.io/storageClass/raw",
        "storage_controller": "registry.hubocean.io/storageController/storage-raw-cdffs",
    },
}


class OdpClient:
    """Class for ODP client, facilitating interactions with ODP."""

    MAX_RETRIES = 5
    BACKOFF_FACTOR = 5
    _api_base_url: str
    _DATASET_KIND = "catalog.hubocean.io/dataset"
    _azure_auth_block: AadClientCredentials
    _retry_status_codes = [410, 500]
    _requests_verify: bool

    def __init__(
        self,
        api_base_url: str,
        azure_auth_block: AadClientCredentials,
        prefect_user_uuid: str,
        requests_verify: bool = True,
    ):
        """Init function of the OdpClient class."""
        self._api_base_url = api_base_url
        self._azure_auth_block = azure_auth_block
        self._prefect_user_uuid = prefect_user_uuid
        self._requests_verify = requests_verify

    def _request(
        self,
        method: str,
        relative_url: str,
        json: Dict = None,
        params: Dict = None,
        headers: Dict = None,
        paginated: bool = False,
        files=None,
        data=None,
        new_line_json: bool = False,
    ):
        """
        Make an HTTP request.

        """
        if not json:
            json = {}
        with self._azure_auth_block.session() as session:
            retry = Retry(
                total=self.MAX_RETRIES,
                backoff_factor=self.BACKOFF_FACTOR,
                status_forcelist=self._retry_status_codes,
                raise_on_status=True,
            )
            session.mount("https://", HTTPAdapter(max_retries=retry))
            if not paginated:
                with session.request(
                    method=method,
                    url=urllib.parse.urljoin(self._api_base_url, relative_url),
                    headers=headers,
                    json=json,
                    params=params,
                    data=data,
                    files=files,
                    verify=self._requests_verify,
                ) as res:
                    if res.status_code not in self._retry_status_codes:
                        res.raise_for_status()
                    yield res
            else:
                if new_line_json:
                    with session.request(
                        method=method,
                        url=urllib.parse.urljoin(self._api_base_url, relative_url),
                        headers=headers,
                        json=json,
                        params=params,
                        verify=self._requests_verify,
                    ) as res:
                        if res.status_code not in self._retry_status_codes:
                            res.raise_for_status()
                        *items, last = res.iter_lines()
                        for item in items:
                            yield loads(item)
                        last_dict = loads(last)
                        json["cursor"] = last_dict.get("@@next", None)
                    while json["cursor"]:
                        with session.request(
                            method=method,
                            url=urllib.parse.urljoin(self._api_base_url, relative_url),
                            headers=headers,
                            json=json,
                            params=params,
                            verify=self._requests_verify,
                        ) as res:
                            if res.status_code not in self._retry_status_codes:
                                res.raise_for_status()
                            *items, last = res.iter_lines()
                            for item in items:
                                yield loads(item)
                            last_dict = loads(last)
                            json["cursor"] = last_dict.get("@@next", None)
                else:
                    with session.request(
                        method=method,
                        url=urllib.parse.urljoin(self._api_base_url, relative_url),
                        headers=headers,
                        json=json,
                        params=params,
                        data=data,
                        files=files,
                        verify=self._requests_verify,
                    ) as res:
                        if res.status_code not in self._retry_status_codes:
                            res.raise_for_status()
                        yield res
                        json["cursor"] = res.json().get("next", None)
                    while json["cursor"]:
                        with session.request(
                            method=method,
                            url=urllib.parse.urljoin(self._api_base_url, relative_url),
                            headers=headers,
                            json=json,
                            params=params,
                            data=data,
                            files=files,
                            verify=self._requests_verify,
                        ) as res:
                            json["cursor"] = res.json().get("next", None)
                            if res.status_code not in self._retry_status_codes:
                                res.raise_for_status()
                            yield res

    def _prefix_name_with_uuid(self, dataset_name: str):
        return f"{self._prefect_user_uuid}-{dataset_name}"

    def create_datapoints(self, datapoints: List[Dict], stage_id: str, dataset_name: str):
        """Method for creating objects in ODP."""
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/"
        data = {"data": datapoints}
        if stage_id:
            data["stage_id"] = stage_id
        return next(
            self._request(method="POST", relative_url=urllib.parse.urljoin(self._api_base_url, relative_url), json=data)
        )

    def list_datapoints(self, dataset_name: str, filters: List[Dict] = None, bbox: Dict = None):
        """Method for listing datapoints of a tabular dataset."""
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/list"
        body = {}
        if filters:
            body["filters"] = filters
        if bbox:
            body["bbox"] = bbox
        if not bbox or not filters:
            body = {"filters": None}
        return self._request(method="POST", relative_url=relative_url, json=body, paginated=True, new_line_json=True)

    def delete_datapoints(self, dataset_name: str, filters: List[Dict] = None, bbox: Dict = None):
        """Method for deleting datapoints."""
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/delete"
        body = {"filters": filters}
        if bbox:
            body["bbox"] = bbox
        return next(self._request(method="POST", relative_url=relative_url, json=body))

    def create_collection(
        self,
        collection_name: str,
        display_collection_name: str,
        collection_description: str,
        contact: str,
        organisation: str,
        published_date: str,
        website: str,
        license_name: str,
        license_text: str,
        license_href: str,
        labels: Dict = None,
        tags: List[str] = None,
    ):
        """Create collection."""
        body = {
            "kind": "catalog.hubocean.io/dataCollection",
            "version": "v1alpha3",
            "metadata": {
                "name": self._prefix_name_with_uuid(collection_name),
                "display_name": display_collection_name,
                "description": collection_description,
                "labels": labels,
            },
            "spec": {
                "distribution": {
                    "published_by": {
                        "contact": contact,
                        "organisation": organisation,
                    },
                    "published_date": published_date,
                    "website": website,
                    "license": {"name": license_name, "full_text": license_text, "href": license_href},
                },
                "tags": tags,
            },
        }

        return next(self._request(method="POST", relative_url="catalog", json=body))

    def delete_collection(self, collection_name: str):
        """Delete colletion."""
        relative_url = f"catalog/catalog.hubocean.io/dataCollection/{self._prefix_name_with_uuid(collection_name)}"
        return next(self._request(method="DELETE", relative_url=relative_url))

    def create_dataset(
        self,
        data_type: str,
        dataset_name: str,
        dataset_display_name: str,
        dataset_description: str,
        contact: str,
        organisation: str,
        documentation: List[str],
        collection_name: str = None,
        citation_cite_as: str = None,
        citation_doi: str = None,
        labels: Dict = None,
        tags: List = None,
        attributes: List = None,
    ):
        """Create or update dataset."""
        if not attributes:
            attributes = []
        try:
            storage_class = DATASET_CONFIG[data_type]["storage_class"]
            storage_controller = DATASET_CONFIG[data_type]["storage_controller"]
        except KeyError:
            raise ValueError("Incorrect value for the dataset type.")
        body = {
            "kind": "catalog.hubocean.io/dataset",
            "version": "v1alpha3",
            "metadata": {
                "labels": labels,
                "name": f"{self._prefix_name_with_uuid(dataset_name)}",
                "description": dataset_description,
                "display_name": dataset_display_name,
            },
            "spec": {
                "storage_class": storage_class,
                "storage_controller": storage_controller,
                "maintainer": {"contact": contact, "organisation": organisation},
                "documentation": documentation,
                "tags": tags,
                "citation": {"cite_as": citation_cite_as, "doi": citation_doi},
                "attributes": attributes,
            },
        }

        if collection_name:
            body["spec"][
                "data_collection"
            ] = f"catalog.hubocean.io/dataCollection/{self._prefix_name_with_uuid(collection_name)}"
        return next(self._request(method="POST", relative_url="catalog", json=body))

    def delete_dataset(self, dataset_name: str):
        """Delete dataset, the vacuum takes care of deleting schema and datapoints in the background."""
        relative_url = f"catalog/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}"
        return next(self._request(method="DELETE", relative_url=relative_url))

    def create_schema(self, dataset_name: str, schema: Dict):
        """Create schema."""
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/schema"
        return next(self._request(method="POST", relative_url=relative_url, json=schema))

    def delete_schema(self, dataset_name: str, delete_data: bool = False):
        """Delete schema of the specified dataset."""
        relative_url = (
            f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/schema?delete_data={delete_data}"
        )
        return next(self._request(method="DELETE", relative_url=relative_url))

    def create_file(self, file_name: str, dataset_name: str, mime_type: str, delay: int = 5):
        """Create a file in ODP."""
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}"
        time.sleep(delay)
        return next(
            self._request(method="POST", relative_url=relative_url, json={"name": file_name, "mime_type": mime_type})
        )

    def upload_file(self, file_name: str, dataset_name: str, file: BinaryIO, mime_type: str):
        """Upload a file to ODP."""
        headers = {"content-type": mime_type}
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/{file_name}"
        return next(self._request(method="PATCH", relative_url=relative_url, data=file, headers=headers))

    def get_file(self, file_name: str, dataset_name: str):
        """Retrieve the specified file."""
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/{file_name}"
        return next(self._request(method="GET", relative_url=relative_url))

    def list_files(self, dataset_name: str):
        """List files from a dataset."""
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/list"
        return self._request(method="POST", relative_url=relative_url, json={"mime_type": None}, paginated=True)

    def delete_file(self, file_name: str, dataset_name: str):
        """Delete the specified file."""
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/{file_name}"
        return next(self._request(method="DELETE", relative_url=relative_url))

    def stage_request(self, dataset_name: str):
        """Create a staging area for a dataset."""
        relative_url = f"/data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/stage"
        return next(self._request(method="POST", relative_url=relative_url, json={"action": "create"}))

    def commit_stage_request(self, dataset_name: str, stage_id: str):
        """Commit a staging area for a dataset."""
        relative_url = f"/data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/stage"
        return next(
            self._request(method="POST", relative_url=relative_url, json={"action": "commit", "stage_id": stage_id})
        )

    def get_staging_request_status(self, dataset_name: str, stage_id: str):
        """Get staging area's status."""
        relative_url = f"/data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/stage/{stage_id}"
        return next(self._request(method="GET", relative_url=relative_url))

    def list_staging_requests(self, dataset_name: str):
        """List staging requests."""
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/stage"
        return next(self._request(method="GET", relative_url=relative_url))

    def delete_staging_requests(self, dataset_name: str, stage_id: str, force_delete: bool = False):
        """Delete staging request. Use force_delete to delete a staging request in commit status."""
        relative_url = f"data/{self._DATASET_KIND}/{self._prefix_name_with_uuid(dataset_name)}/stage/{stage_id}"
        return next(self._request(method="DELETE", relative_url=relative_url, params={"force_delete": force_delete}))

    def _create_observable(
        self,
        ref_name: str,
        observable_name: str,
        observable_display_name: str,
        observable_description: str,
        observable_labels: Dict,
        observable_value: Dict,
        observable_cls: str,
    ):
        """Create dataset or collection observable."""
        relative_url = "/catalog"
        observable = {
            "kind": "catalog.hubocean.io/observable",
            "version": "v1alpha3",
            "metadata": {
                "name": self._prefix_name_with_uuid(observable_name),
                "display_name": observable_display_name,
                "description": observable_description,
                "labels": observable_labels,
            },
            "spec": {
                "ref": f"catalog.hubocean.io/{self._prefix_name_with_uuid(ref_name)}",
                "details": {
                    "value": observable_value,
                    "cls": observable_cls,
                },
            },
        }
        return next(self._request(method="POST", relative_url=relative_url, json=observable))

    def create_static_geometric_observable(
        self,
        ref_name: str,
        observable_name: str,
        observable_display_name: str,
        observable_description: str,
        observable_labels: Dict,
        observable_value: Dict,
    ):
        """Create geometric observable."""
        self._create_observable(
            ref_name=ref_name,
            observable_name=observable_name,
            observable_display_name=observable_display_name,
            observable_description=observable_description,
            observable_labels=observable_labels,
            observable_value=observable_value,
            observable_cls="odp.odcat.observable.observable.StaticGeometricCoverage",
        )

    def create_static_observable(
        self,
        ref_name: str,
        observable_name: str,
        observable_display_name: str,
        observable_description: str,
        observable_labels: Dict,
        observable_value: Dict,
    ):
        """Create geometric observable."""
        self._create_observable(
            ref_name=ref_name,
            observable_name=observable_name,
            observable_display_name=observable_display_name,
            observable_description=observable_description,
            observable_labels=observable_labels,
            observable_value=observable_value,
            observable_cls="odp.odcat.observable.observable.StaticCoverage",
        )
