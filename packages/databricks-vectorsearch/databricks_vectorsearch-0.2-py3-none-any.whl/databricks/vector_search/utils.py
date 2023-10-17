import requests
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


class OAuthTokenUtils:

    @staticmethod
    def get_oauth_token(
        workspace_url,
        service_principal_client_id,
        service_principal_client_secret,
        authorization_details=None,
    ):
        authorization_details = authorization_details or []
        url = workspace_url + "/oidc/v1/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            "grant_type": "client_credentials",
            "scope": "all-apis",
            "authorization_details": authorization_details
        }
        logging.info(f"Issuing request to {url} with data {data} and headers {headers}")
        response = requests.request(
            url=url,
            auth=(service_principal_client_id, service_principal_client_secret),
            headers=headers,
            method="POST",
            data=data
        )
        try:
            response.raise_for_status()
        except Exception as e:
            logging.warn(f"Error retrieving OAuth Token {e}")
            raise Exception(
                f"Response content {response.content}, status_code {response.status_code}"
            )
        return response.json()


class RequestUtils:

    @staticmethod
    def issue_request(url, token, method, params=None, json=None, verify=True):
        headers = dict()
        headers["Authorization"] = f"Bearer {token}"
        logging.info(f"Issuing request to {url} with method {method} and \
            json {json} and headers {headers} and verify {verify}")
        response = requests.request(
            url=url,
            headers=headers,
            method=method,
            params=params,
            json=json,
            verify=verify
        )
        try:
            response.raise_for_status()
        except Exception as e:
            logging.warn(f"Error processing request {e}")
            raise Exception(
                f"Response content {response.content}, status_code {response.status_code}"
            )
        return response.json()
