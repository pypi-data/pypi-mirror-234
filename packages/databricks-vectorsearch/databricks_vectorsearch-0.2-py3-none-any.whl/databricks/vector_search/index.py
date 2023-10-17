import logging
import json
import time
from databricks.vector_search.utils import OAuthTokenUtils
from databricks.vector_search.utils import RequestUtils


class VectorSearchIndex:
    def __init__(
        self,
        workspace_url=None,
        index_url=None,
        personal_access_token=None,
        name=None,
        endpoint_name=None,
        service_principal_client_id=None,
        service_principal_client_secret=None,
    ):
        self.workspace_url = workspace_url
        self.index_url = index_url
        self.name = name
        self.endpoint_name = endpoint_name
        self.personal_access_token = personal_access_token
        self.service_principal_client_id = service_principal_client_id
        self.service_principal_client_secret = service_principal_client_secret
        if (self.service_principal_client_id and
                self.service_principal_client_secret):
            assert self.workspace_url, "Service Principal auth flow requires workspace url"
        self._write_oauth_token = None
        self._write_oauth_token_expiry_ts = None

    def _get_token_for_request(self):
        if self.personal_access_token:  # PAT flow
            logging.info("[VectorSearchIndex] Using PAT token")
            return self.personal_access_token
        if (
            self._write_oauth_token
            and self._write_oauth_token_expiry_ts
            and self._write_oauth_token_expiry_ts - 100 > time.time()
        ):
            logging.info(f"[VectorSearchIndex] Using existing unexpired OAUTH token. Expiry {self._write_oauth_token_expiry_ts}")
            return self._write_oauth_token
        if self.service_principal_client_id and \
                self.service_principal_client_secret:
            logging.info(f"[VectorSearchIndex] Getting new OAUTH token. SP CLIENT ID {self.service_principal_client_id}")
            write_authorization_details = [{
                "type": "unity_catalog_permission",
                "securable_type": "table",
                "securable_object_name": self.name,
                "operation": "WriteVectorIndex"
            }]
            oauth_token_data = OAuthTokenUtils.get_oauth_token(
                workspace_url=self.workspace_url,
                service_principal_client_id=self.service_principal_client_id,
                service_principal_client_secret=self.service_principal_client_secret,
                authorization_details=json.dumps(write_authorization_details)
            )
            self._write_oauth_token = oauth_token_data["access_token"]
            self._write_oauth_token_expiry_ts = time.time() + oauth_token_data["expires_in"]
            return self._write_oauth_token
        raise Exception("You must specify service principal or PAT token")

    def upsert(self, inputs):
        assert type(inputs) == list, "inputs must be of type: List of dicts"
        assert all(
            type(i) == dict for i in inputs
        ), "inputs must be of type: List of dicts"
        upsert_payload = {"inputs_json": json.dumps(inputs)}
        return RequestUtils.issue_request(
            url=f"{self.index_url}/upsert-data",
            token=self._get_token_for_request(),
            method="POST",
            json=upsert_payload
        )

    def delete(self, primary_keys):
        delete_payload = {"primary_keys": primary_keys}
        return RequestUtils.issue_request(
            url=f"{self.index_url}/delete-data",
            token=self._get_token_for_request(),
            method="POST",
            json=delete_payload
        )

    def describe(self):
        return RequestUtils.issue_request(
            url=f"{self.workspace_url}/api/2.0/vector-search/endpoints/{self.endpoint_name}/indexes/{self.name}",
            token=self._get_token_for_request(),
            method="GET",
        )

    def similarity_search(
        self,
        columns,
        query_text=None,
        query_vector=None,
        filters=None,
        num_results=5,
    ):
        json_data = {
            "num_results": num_results,
            "columns": columns,
            "filters_json": json.dumps(filters) if filters else None,
        }
        if query_text:
            json_data["query"] = query_text
            json_data["query_text"] = query_text
        if query_vector:
            json_data["query_vector"] = query_vector

        return RequestUtils.issue_request(
            url=f"{self.index_url}/query",
            token=self._get_token_for_request(),
            method="GET",
            json=json_data
        )