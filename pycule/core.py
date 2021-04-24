"""Core MCule API module."""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import requests
import json
from typing import Optional

from urls import MCuleRoutes
from callbacks import search_result_on_success, default_on_success
from decorators import mcule_api_limits, response_handling

LOGGER = logging.getLogger("mcule:core")


class MCuleWrapper:
    """
    Python wrapper for MCule wrapper to access the API requests.
    """

    def __init__(
        self,
        authorisation_token: str,
        logger: Optional[logging.Logger] = None,
        base_url: Optional[str] = None,
    ):
        """
        MCuleWrapper constructor.
        Args:
            authorisation_token_key (str): an API token to access the service.
            logger (logging.Logger, optional): a logger.
                Defaults to None, a.k.a using a default logger.
            base_url (str, optional): base url for the service. If not provided it will default to
                the environment variable MCULE_BASE_URL or https://ultimateapp.mcule.com.
        """
        self._authorisation_token = authorisation_token
        self.logger = logger if logger else LOGGER
        self.headers = self._construct_headers()
        self.routes = MCuleRoutes(base_url)

    def set_base_url(self, base_url: str) -> None:
        """
        Set base url for the MCule service.
        Args:
            base_url (str): base url for the service to set.
        """
        self.routes.base_url = base_url

    def _construct_headers(self) -> dict:
        """
        Construct header, required for all requests.
        Returns:
            dict: dictionary containing the "Content-Type" and the
                "Authorization".
        """
        return {"Content-Type": "application/json", "Authorization": self._authorisation_token}

    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def exact_search(self, smiles: str) -> requests.models.Response:
        """
        Searches Mcule for exact match

        Args:
            smiles (str): a search for exact match to SMILES

        Returns:
            dict: dictionary containing the search response
        """
        data = {"query": {"type": "exact", "queries": [smiles]}}
        response = requests.post(
            self.routes.search_url, headers=self.headers, data=json.dumps(data), cookies={}
        )
        return response
