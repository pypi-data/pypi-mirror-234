import logging
import time
import json
from databricks.vector_search.exceptions import InvalidInputException
from databricks.vector_search.utils import OAuthTokenUtils
from databricks.vector_search.utils import RequestUtils
from databricks.vector_search.index import VectorSearchIndex
from mlflow.utils import databricks_utils


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


class VectorSearchClient:

    def __init__(
        self,
        workspace_url=None,
        personal_access_token=None,
        service_principal_client_id=None,
        service_principal_client_secret=None
    ):
        self.workspace_url = workspace_url
        self.personal_access_token = personal_access_token
        self.service_principal_client_id = service_principal_client_id
        self.service_principal_client_secret = service_principal_client_secret
        if not (
            self.service_principal_client_id and
            self.service_principal_client_secret
        ):
            if self.workspace_url is None:
                host_creds = databricks_utils.get_databricks_host_creds()
                self.workspace_url = host_creds.host
            if self.personal_access_token is None:
                host_creds = databricks_utils.get_databricks_host_creds()
                self.personal_access_token = host_creds.token

            host_creds = databricks_utils.get_databricks_host_creds()
            self.personal_access_token = host_creds.token
        self._control_plane_oauth_token = None
        self._control_plane_oauth_token_expiry_ts = None
        self.validate()

    def validate(self):
        if (self.service_principal_client_id and
                self.service_principal_client_secret and
                not self.workspace_url):
            raise InvalidInputException(
                "Service Principal auth flow requires workspace url"
            )
        if self.personal_access_token:
            print(
                """[WARNING] Personal access tokens should only be used for development.\nIf you are using vector search in production, please use our Service Principal flow."""
            )

    def _get_token_for_request(self):
        if self.personal_access_token:
            logging.info("[VectorSearchClient] Using PAT token")
            return self.personal_access_token
        if (
            self._control_plane_oauth_token
            and self._control_plane_oauth_token_expiry_ts
            and self._control_plane_oauth_token_expiry_ts - 100 > time.time()
        ):
            logging.info(f"[VectorSearchClient] Using existing unexpired OAUTH token. Expiry {self._oauth_token_expiry_ts}")
            return self._control_plane_oauth_token
        if self.service_principal_client_id and \
                self.service_principal_client_secret:
            logging.info(f"[VectorSearchClient] Getting new OAUTH token. Service Principal {self.service_principal_client_id}")
            authorization_details = []
            oauth_token_data = OAuthTokenUtils.get_oauth_token(
                workspace_url=self.workspace_url,
                service_principal_client_id=self.service_principal_client_id,
                service_principal_client_secret=self.service_principal_client_secret,
                authorization_details=authorization_details,
            )
            self._control_plane_oauth_token = oauth_token_data["access_token"]
            self._control_plane_oauth_token_expiry_ts = time.time() + oauth_token_data["expires_in"]
            return self._control_plane_oauth_token
        raise Exception("You must specify service principal or PAT token")

    def create_endpoint(self, name):
        logging.info(f"Creating endpoint: {name}")
        json_data = {"name": name}
        return RequestUtils.issue_request(
            url=f"{self.workspace_url}/api/2.0/vector-search/endpoints",
            token=self._get_token_for_request(),
            method="POST",
            json=json_data,
        )

    def get_endpoint(self, name):
        logging.info(f"Getting endpoint: {name}")
        return RequestUtils.issue_request(
            url=f"{self.workspace_url}/api/2.0/vector-search/endpoints/{name}",
            token=self._get_token_for_request(),
            method="GET",
        )

    def list_endpoints(self):
        logging.info(f"Listing all endpoints for Vector Search")
        return RequestUtils.issue_request(
            url=f"{self.workspace_url}/api/2.0/vector-search/endpoints",
            token=self._get_token_for_request(),
            method="GET",
        )

    def delete_endpoint(self, name):
        logging.info(f"Deleting endpoint: {name}")
        return RequestUtils.issue_request(
            url=f"{self.workspace_url}/api/2.0/vector-search/endpoints/{name}",
            token=self._get_token_for_request(),
            method="DELETE",
        )

    def create_delta_sync_index(
            self,
            endpoint_name,
            index_name,
            primary_key,
            source_table,
            pipeline_type,
            embedding_dimension=None,
            embedding_vector_column=None,
            embedding_source_column=None,
            ai_gateway_route_name=None,
            embedding_model_endpoint_name=None
    ):
        logging.info(f"Creating index {index_name} with endpoint: {endpoint_name}")
        assert pipeline_type, "Pipeline type cannot be None. Please use CONTINUOUS/TRIGGERED as the pipeline type."
        json_data = {
            "name": index_name,
            "index_type": "DELTA_SYNC",
            "primary_key": primary_key,
            "delta_sync_index_spec": {
                "source_table": source_table,
                "pipeline_type": pipeline_type.upper(),
            }
        }
        if embedding_vector_column:
            assert embedding_dimension, "Embedding dimension must be specified if source column is used"
            json_data["delta_sync_index_spec"]["embedding_vector_columns"] = [
                {
                    "name": embedding_vector_column,
                    "embedding_dimension": embedding_dimension
                }
            ]
        elif embedding_source_column:
            assert not (ai_gateway_route_name and embedding_model_endpoint_name), \
                "You cannot specify both AI Gateway route & Embedding Model Endpoint"
            assert ai_gateway_route_name or embedding_model_endpoint_name, \
                "You must specify either AI Gateway route or Embedding Model Endpoint"
            json_data["delta_sync_index_spec"]["embedding_source_columns"] = [
                {
                    "name": embedding_source_column,
                    "ai_gateway_route_name": ai_gateway_route_name,
                    "embedding_model_endpoint_name": embedding_model_endpoint_name
                }
            ]

        resp = RequestUtils.issue_request(
            url=f"{self.workspace_url}/api/2.0/vector-search/endpoints/{endpoint_name}/indexes",
            token=self._get_token_for_request(),
            method="POST",
            json=json_data,
        )

        index_url = resp.get('url') if \
            resp.get('url') else (
                self.workspace_url + f"/api/2.0/vector-search/endpoints/{endpoint_name}/indexes/{resp['name']}")
        return VectorSearchIndex(
            workspace_url=self.workspace_url,
            index_url=index_url,
            personal_access_token=self.personal_access_token,
            service_principal_client_id=self.service_principal_client_id,
            service_principal_client_secret=self.service_principal_client_secret,
            name=resp["name"],
            endpoint_name=endpoint_name
        )

    def create_direct_access_index(
            self,
            endpoint_name,
            index_name,
            primary_key,
            embedding_dimension,
            embedding_vector_column,
            schema
    ):
        logging.info(f"Creating direct access index {index_name} with endpoint: {endpoint_name}")
        assert schema, """
            Schema must be present when creating a direct vector index.
            Example schema: {"id": "integer", "text": "string", \
                "text_vector": "array<float>", "bool_val": "boolean", \
                    "float_val": "float", "date_val": "date"}"
        """
        json_data = {
            "name": index_name,
            "index_type": "DIRECT_ACCESS",
            "primary_key": primary_key,
            "direct_access_index_spec": {
                "embedding_vector_columns": [
                    {
                        "name": embedding_vector_column,
                        "embedding_dimension": embedding_dimension
                    }
                ],
                "schema_json": json.dumps(schema)
            },
            
        }
        resp = RequestUtils.issue_request(
            url=f"{self.workspace_url}/api/2.0/vector-search/endpoints/{endpoint_name}/indexes",
            token=self._get_token_for_request(),
            method="POST",
            json=json_data,
        )

        index_url = resp.get('url') if \
            resp.get('url') else (
                self.workspace_url + f"/api/2.0/vector-search/endpoints/{endpoint_name}/indexes/{resp['name']}")
        return VectorSearchIndex(
            workspace_url=self.workspace_url,
            index_url=index_url,
            personal_access_token=self.personal_access_token,
            service_principal_client_id=self.service_principal_client_id,
            service_principal_client_secret=self.service_principal_client_secret,
            name=resp["name"],
            endpoint_name=endpoint_name
        )

    def get_index(self, index_name, endpoint_name):
        resp = RequestUtils.issue_request(
            url=f"{self.workspace_url}/api/2.0/vector-search/endpoints/{endpoint_name}/indexes/{index_name}",
            token=self._get_token_for_request(),
            method="GET",
        )
        index_url = resp.get('url') if \
            resp.get('url') else (
                self.workspace_url + f"/api/2.0/vector-search/endpoints/{endpoint_name}/indexes/{resp['name']}")
        return VectorSearchIndex(
            workspace_url=self.workspace_url,
            index_url=index_url,
            personal_access_token=self.personal_access_token,
            service_principal_client_id=self.service_principal_client_id,
            service_principal_client_secret=self.service_principal_client_secret,
            name=index_name,
            endpoint_name=endpoint_name
        )