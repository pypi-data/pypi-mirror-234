import concurrent.futures as pyfutures
import copy
import os
from concurrent.futures import as_completed
from typing import Dict, List, Optional
import pandas as pd
from loguru import logger
from requests_futures.sessions import FuturesSession

from refuel.utils import format_filters, is_valid_uuid, normalize_sort_order


class RefuelClient:
    # Default config settings
    API_BASE_URL = "https://cloud-api.refuel.ai"
    API_KEY_ENV_VARIABLE = "REFUEL_API_KEY"
    TIMEOUT_SECS = 60
    DEFAULT_MAX_QUERY_ITEMS = 1000
    QUERY_STEP_SIZE = 100
    MAX_WORKERS = os.cpu_count()
    MAX_RETRIES = 3
    ADAPTER_KWARGS = {"max_retries": MAX_RETRIES}

    def __init__(
        self,
        api_key: str = None,
        api_base_url: str = API_BASE_URL,
        timeout: int = TIMEOUT_SECS,
        max_retries: int = MAX_RETRIES,
        max_workers: int = MAX_WORKERS,
        project: Optional[str] = None,
    ) -> None:
        """
        Args:
            api_key (str, optional): Refuel API Key. Defaults to None.
            api_base_url (str, optional): Base URL of the Refuel API endpoints. Defaults to API_BASE_URL.
            timeout (int, optional): Timeout (secs) for a given API call. Defaults to TIMEOUT_SECS.
            max_retries (int, optional): Max num retries. Defaults to MAX_RETRIES.
            max_workers (int, optional): Max number of concurrent tasks in the ThreadPoolExecutor
            project (str, optional): Name or ID of the Project you plan to use.
        """
        # initialize variables
        self._api_key = api_key or os.environ.get(self.API_KEY_ENV_VARIABLE)
        self._api_base_url = api_base_url
        self._timeout = timeout
        self._header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        # initialize request session
        adapter_kwargs = {"max_retries": max_retries}
        self._session = FuturesSession(
            max_workers=max_workers, adapter_kwargs=adapter_kwargs
        )
        self._project_id = None
        if project:
            if is_valid_uuid(project):
                self._project_id = project
            else:
                self._project_id = self._get_project_id_by_name(project)

    def _get(self, url: str, params: Dict = None) -> pyfutures.Future:
        return self._session.get(url, headers=self._header, params=params)

    def _post(
        self,
        url: str,
        data: str = None,
        params: dict = None,
        json: dict = None,
        files: List = None,
        headers: dict = None,
        empty_header=False,
    ) -> pyfutures.Future:
        if not headers and not empty_header:
            headers = self._header
        return self._session.post(
            url,
            headers=headers,
            timeout=self._timeout,
            data=data,
            params=params,
            json=json,
            files=files,
        )

    def _delete(self, url: str, params: Dict = None) -> pyfutures.Future:
        return self._session.delete(url, headers=self._header, params=params)

    def _item_count_helper(self, url: str, params: Dict = None) -> int:
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No item was logged"
            )
            return None

        # construct parallel requests
        request_params = copy.deepcopy(params)
        request_params["offset"] = 0
        request_params["max_items"] = 0

        response = self._get(url=url, params=request_params).result()
        if response.status_code != 200:
            logger.error(
                "Request failed with status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
        response_json = response.json()

        dataset_size = response_json.get("data", {}).get("total_count")
        return dataset_size or self.DEFAULT_MAX_QUERY_ITEMS

    def _query_helper(
        self, url: str, params: Dict = None, verbose: bool = False
    ) -> pd.DataFrame:
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No item was logged"
            )
            return None

        dataset_size = self._item_count_helper(url, params)
        max_items = min(
            params.get("max_items", self.DEFAULT_MAX_QUERY_ITEMS), dataset_size
        )
        offset = params.get("offset", 0)

        # construct parallel requests
        logger.info(f"Started fetching data. Will fetch {max_items} items ...")
        futures = []
        offset_starts = list(
            range(offset, offset + max_items, RefuelClient.QUERY_STEP_SIZE)
        )
        items_remaining = max_items

        for batch_num, offset_start in enumerate(offset_starts):
            num_to_fetch = min(items_remaining, RefuelClient.QUERY_STEP_SIZE)
            request_params = copy.deepcopy(params)
            request_params["offset"] = offset_start
            request_params["max_items"] = num_to_fetch
            future_obj = self._get(url=url, params=request_params)
            future_obj.batch_num = batch_num
            futures.append(future_obj)
            items_remaining -= num_to_fetch

        # parse response from each request
        batch_idx_to_items = {}
        num_fetched = 0
        for future in as_completed(futures):
            response = future.result()
            if response.status_code != 200:
                logger.error(
                    "Request failed with status code: {} received with response: {}",
                    response.status_code,
                    response.text,
                )
            else:
                json_response = response.json()
                result = json_response.get("data", [])
                items = result.get("items", [])
                batch_idx_to_items[future.batch_num] = items
                num_fetched += len(items)
                if verbose:
                    logger.info(f"Fetched {num_fetched} items so far.")

        sorted_by_batch_idx = [item[1] for item in sorted(batch_idx_to_items.items())]
        items = [item for sublist in sorted_by_batch_idx for item in sublist]
        logger.info(f"Completed fetching data. {len(items)} items were fetched.")
        return pd.DataFrame.from_records(items)

    def _get_dataset_id_by_name(self, dataset_name: str) -> str:
        for dataset in self.get_datasets():
            if dataset.get("dataset_name") == dataset_name:
                return dataset.get("id")
        logger.info(f"No dataset with name={dataset_name} found.")
        return None

    def _get_project_id_by_name(self, project_name: str) -> str:
        for project in self.get_projects():
            if project.get("project_name") == project_name:
                return project.get("id")
        logger.info(f"No project with name={project_name} found.")
        return None

    def _get_task_id_by_name(self, task_name: str, project: str) -> str:
        if is_valid_uuid(project):
            project_id = project
        elif project:
            project_id = self._get_project_id_by_name(project)
        else:
            project_id = None
        project_id = project_id or self._project_id
        if not project_id:
            logger.error(
                "Error retrieving task: must provide valid project name or ID!"
            )
            return None
        for task in self.get_tasks(project=project_id):
            if task.get("task_name") == task_name:
                return task.get("id")
        logger.info(f"No task with name={task_name} found.")
        return None

    # Datasets
    def get_datasets(self, project: Optional[str] = None) -> List:
        project_id = None
        # if a project parameter is provided, get the project_id
        if project:
            # check if the project_id is a valid UUID
            if is_valid_uuid(project):
                project_id = project
            else:
                project_id = self._get_project_id_by_name(project)

        # fallback to project provided during client initialization
        project_id = project_id or self._project_id

        response = self._get(
            url=self._api_base_url + "/datasets", params={"project_id": project_id}
        ).result()
        if response.status_code != 200:
            logger.error(
                "Request failed with status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
        else:
            return response.json().get("data", [])

    def get_dataset(self, dataset: str) -> Dict:
        dataset_id = None
        if is_valid_uuid(dataset):
            dataset_id = dataset
        else:
            dataset_id = self._get_dataset_id_by_name(dataset)

        if not dataset_id:
            logger.error("Must provide a valid dataset name or ID")
            return {}

        response = self._get(
            url=self._api_base_url + f"/datasets/{dataset_id}",
            params={"dataset_id": dataset_id},
        ).result()
        if response.status_code != 200:
            logger.error(
                "Request failed with status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
        else:
            return response.json().get("data", [])

    def upload_dataset(
        self,
        file_path: str,
        dataset_name: str,
        delimiter: str = ",",
        embedding_columns: List[str] = None,
    ) -> Dict:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
        }
        # Get presigned URL
        response = self._post(
            url=self._api_base_url + "/datasets/url",
            headers=headers,
        ).result()
        if response.status_code != 200:
            logger.error(
                "Status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
        response_unpacked = response.json().get("data", {})
        s3_path = response_unpacked["uri_path"]
        signed_url = response_unpacked["signed_url"]

        # upload file to presigned S3 URL
        with open(file_path, "rb") as f:
            files = {"file": ("dataset.csv", f)}
            response = self._post(
                url=signed_url["url"],
                data=signed_url["fields"],
                files=files,
                headers={},
                empty_header=True,
            ).result()
        if response.status_code != 204:
            logger.error(
                "Error uploading file to S3:\nStatus code: {} received with response: {}",
                response.status_code,
                response.text,
            )

        # Infer Schema from S3 path
        infer_schema_params = {"s3_path": s3_path}
        response = self._post(
            url=self._api_base_url + "/datasets/infer_schema",
            params=infer_schema_params,
            headers=headers,
        ).result()
        if response.status_code != 200:
            logger.error(
                "Failed to infer schema:\nStatus code: {} received with response: {}",
                response.status_code,
                response.text,
            )
        response_unpacked = response.json().get("data", {})
        dataset_schema = response_unpacked.get("schema_dict")

        # Ingest Dataset
        if not dataset_schema:
            logger.error("Failed to infer schema from dataset")
        ingest_params = {
            "s3_path": s3_path,
            "dataset_name": dataset_name,
        }
        data = {
            "schema_dict": dataset_schema,
            "embedding_columns": embedding_columns,
        }
        response = self._post(
            url=self._api_base_url + f"/datasets/ingest",
            params=ingest_params,
            json=data,
            headers=headers,
        ).result()
        if response.status_code != 200:
            logger.error(
                "Failed to ingest dataset:\nStatus code: {} received with response: {}",
                response.status_code,
                response.text,
            )

        dataset_response = response.json().get("data", {})
        dataset_id = dataset_response.get("id")
        # Associate dataset with project
        if self._project_id and dataset_id:
            url = (
                self._api_base_url
                + f"/datasets/{dataset_id}/projects/{self._project_id}"
            )
            response = self._post(
                url=url,
                params={},
                headers=headers,
            ).result()
            if response.status_code != 200:
                logger.error(
                    "Failed to ingest dataset into project:\nStatus code: {} received with response: {}",
                    response.status_code,
                    response.text,
                )
        return dataset_response

    def download_dataset(
        self,
        email_address: str,
        dataset: str,
        task: Optional[str] = None,
        project: Optional[str] = None,
    ) -> Dict:
        # Get dataset to be downloaded
        if is_valid_uuid(dataset):
            dataset_id = dataset
        else:
            dataset_id = self._get_dataset_id_by_name(dataset)
        if not dataset_id:
            logger.error("Must provide a valid dataset name or ID")
            return

        # Get task details if specified
        if is_valid_uuid(task):
            task_id = task
        elif task:
            task_id = self._get_task_id_by_name(task_name=task, project=project)
        else:
            task_id = None

        params = {
            "dataset_id": dataset_id,
            "email_address": email_address,
            "task_id": task_id,
        }
        response = self._get(
            url=self._api_base_url + f"/datasets/{dataset_id}/download", params=params
        ).result()
        if response.status_code != 200:
            logger.error(
                "Request failed with status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
        else:
            logger.info(
                "Dataset is being prepared for download. You will receive an email when it is ready."
            )
        return response.json()

    def get_items(
        self,
        dataset: str,
        offset: int = 0,
        max_items: int = 20,
        filters: List[Dict] = [],
        order_by: Optional[str] = None,
        order_direction: Optional[str] = "ASC",
        task: Optional[str] = None,
        project: Optional[str] = None,
    ) -> pd.DataFrame:
        dataset_id = None
        if is_valid_uuid(dataset):
            dataset_id = dataset
        else:
            dataset_id = self._get_dataset_id_by_name(dataset)
        if not dataset_id:
            logger.error("Must provide a valid dataset name or ID")
            return

        params = {
            "dataset_id": dataset_id,
            "offset": offset,
            "max_items": max_items,
            "filters": format_filters(filters),
            "expand": "true",
        }
        if order_by:
            params["order_by"] = order_by
            params["order_direction"] = normalize_sort_order(order_direction)

        # Get task details if specified
        if is_valid_uuid(task):
            task_id = task
        elif task:
            task_id = self._get_task_id_by_name(task_name=task, project=project)
        else:
            task_id = None
        # if task is provided, also return llm generated labels & confidence
        if task_id:
            params["task_id"] = task_id
            return self._query_helper(
                self._api_base_url + f"/tasks/{task_id}/datasets/{dataset_id}",
                params=params,
            )
        else:
            return self._query_helper(
                self._api_base_url + f"/datasets/{dataset_id}", params=params
            )

    # Projects
    def get_projects(self) -> List:
        response = self._get(url=self._api_base_url + "/projects").result()
        if response.status_code != 200:
            logger.error(
                "Request failed with status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
        else:
            return response.json().get("data", [])

    def get_project(self, project: str) -> Dict:
        project_id = None
        if is_valid_uuid(project):
            project_id = project
        else:
            project_id = self._get_project_id_by_name(project)
        if not project_id and self._project_id:
            project_id = self._project_id
        if not project_id:
            logger.error("Must provide a valid project name or ID")
            return
        response = self._get(
            url=self._api_base_url + f"/projects/{project_id}",
            params={"project_id": project_id},
        ).result()
        if response.status_code != 200:
            logger.error(
                "Request failed with status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
        else:
            return response.json().get("data", {})

    def create_project(self, project: str, description: str) -> Dict:
        response = self._post(
            url=self._api_base_url + f"/projects",
            params={"project_name": project, "description": description},
            headers=self._header,
        ).result()
        if response.status_code != 200:
            logger.error(
                "Failed to create project:\nStatus code: {} received with response: {}",
                response.status_code,
                response.text,
            )
            return {}
        return response.json().get("data", {})

    # Tasks
    def get_tasks(self, project: Optional[str] = None) -> List:
        # if a project parameter is provided, get the project_id
        if is_valid_uuid(project):
            project_id = project
        elif project:
            project_id = self._get_project_id_by_name(project)
        else:
            project_id = None
        # fallback to project provided during client initialization
        project_id = project_id or self._project_id

        if not project_id:
            logger.error(
                "Project name or ID must be provided to get all labeling tasks within a project"
            )
            return []

        response = self._get(
            url=self._api_base_url + f"/projects/{project_id}/tasks",
            params={"project_id": project_id},
        ).result()
        if response.status_code != 200:
            logger.error(
                "Request failed with status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
            return []
        else:
            return response.json().get("data", [])

    def get_task(
        self,
        task: str,
        project: Optional[str] = None,
    ) -> Dict:
        task_id = None
        if is_valid_uuid(task):
            task_id = task
        else:
            task_id = self._get_task_id_by_name(task_name=task, project=project)
        if not task_id:
            logger.error("Must provide a valid task name or ID")
            return
        params = {"task_id": task_id}
        response = self._get(
            url=self._api_base_url + f"/tasks/{task_id}", params=params
        ).result()
        if response.status_code != 200:
            logger.error(
                "Request failed with status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
        else:
            return response.json().get("data", {})

    def get_task_run(
        self,
        task: str,
        dataset: str,
        project: Optional[str] = None,
    ) -> Dict:
        task_id = None
        if is_valid_uuid(task):
            task_id = task
        else:
            task_id = self._get_task_id_by_name(task_name=task, project=project)
        if not task_id:
            logger.error("Must provide a valid task name or ID")
            return
        dataset_id = None
        if is_valid_uuid(dataset):
            dataset_id = dataset
        else:
            dataset_id = self._get_dataset_id_by_name(dataset)
        if not dataset_id:
            logger.error("Must provide a valid dataset name or ID")
            return
        params = {"task_id": task_id, "dataset_id": dataset_id}
        response = self._get(
            url=self._api_base_url + f"/tasks/{task_id}/runs/{dataset_id}",
            params=params,
        ).result()
        if response.status_code != 200:
            logger.error(
                "Request failed with status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
            return {}
        else:
            return response.json().get("data", {})

    def start_task_run(
        self,
        task: str,
        dataset: str,
        project: Optional[str] = None,
        num_items: Optional[int] = None,
    ) -> Dict:
        task_id = None
        if is_valid_uuid(task):
            task_id = task
        else:
            task_id = self._get_task_id_by_name(task_name=task, project=project)
        if not task_id:
            logger.error("Must provide a valid task name or ID")
            return
        dataset_id = None
        if is_valid_uuid(dataset):
            dataset_id = dataset
        else:
            dataset_id = self._get_dataset_id_by_name(dataset)
        if not dataset_id:
            logger.error("Must provide a valid dataset name or ID")
            return
        params = {
            "task_id": task_id,
            "dataset_id": dataset_id,
        }
        if num_items:
            params["num_items"] = num_items
        logger.info(
            "The labeling task is being run on the entire dataset. You can monitor progress with get_task_run(task_id, dataset_id)"
        )
        response = self._post(
            url=self._api_base_url + f"/tasks/{task_id}/runs/{dataset_id}",
            params=params,
            headers=self._header,
        ).result()

        if response.status_code != 200:
            logger.error(
                "Error starting task run:\nStatus code: {} received with response: {}",
                response.status_code,
                response.text,
            )
            return {}

        return response.json()

    def cancel_task_run(
        self,
        task: str,
        dataset: str,
        project: Optional[str] = None,
    ) -> Dict:
        task_id = None
        if is_valid_uuid(task):
            task_id = task
        else:
            task_id = self._get_task_id_by_name(task_name=task, project=project)
        if not task_id:
            logger.error("Must provide a valid task name or ID")
            return
        dataset_id = None
        if is_valid_uuid(dataset):
            dataset_id = dataset
        else:
            dataset_id = self._get_dataset_id_by_name(dataset)
        if not dataset_id:
            logger.error("Must provide a valid dataset name or ID")
            return

        params = {"task_id": task_id, "dataset_id": dataset_id, "cancel_run": True}

        response = self._post(
            url=self._api_base_url + f"/tasks/{task_id}/runs/{dataset_id}",
            params=params,
            headers=self._header,
        ).result()

        if response.status_code != 200:
            logger.error(
                "Error cancelling task run:\nStatus code: {} received with response: {}",
                response.status_code,
                response.text,
            )
            return {}
        return response.json()
