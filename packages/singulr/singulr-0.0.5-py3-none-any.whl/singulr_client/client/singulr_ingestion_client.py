import requests
import os
from typing import Optional, Dict, Union

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file


class SingulrClient(object):
    """
    A Python client for sending data to the Singulr API.
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the SingulrClient.

        :param base_url: The base URL of the Singulr API endpoint (default: "http://localhost:8080/api/ingestion/ingest").
        :param api_key: The API key for authentication (optional).
        """
        self.singulr_endpoint = base_url if base_url else os.environ["SINGULR_ENDPOINT"]
        self.api_key = api_key if api_key else None

    def _prepare_headers(self) -> Dict[str, str]:
        """
        Prepare HTTP headers for requests.

        :return: A dictionary of HTTP headers.
        """
        headers = {
            'Content-Type': 'application/json',
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def ingest_payload(self, ingestion_payload: Dict[str, Union[str, int, float, bool]]) -> Union[requests.Response, None]:
        """
        Send a payload to the Singulr ingestion endpoint.

        :param ingestion_payload: The payload to be ingested as a dictionary.
        :return: The HTTP response object if successful, otherwise None.
        """
        try:
            # Make an HTTP POST request to the Java REST endpoint with the data
            response = requests.post(self.singulr_endpoint, json=ingestion_payload)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Return the response
                return response
            else:
                raise ValueError(f"HTTP POST request failed with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


if __name__ == '__main__':
    ic = SingulrClient()
    import json

    # Example usage with JSON data
    with open("b.json", "r") as file:
        data = json.load(file)
    ic.ingest_payload(data)
