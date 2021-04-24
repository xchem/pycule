"""Core MCule API module."""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import requests
import json
from typing import Optional

from .urls import MCuleRoutes
from .callbacks import search_result_on_success, default_on_success
from .decorators import mcule_api_limits, response_handling

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
            smiles (str): a search for exact match to SMILES. Can pass
                          in a list of SMILES strings

        Returns:
            dict: dictionary containing the search response
        """
        data = {"query": {"type": "exact", "queries": [smiles]}}
        response = requests.post(
            url=self.routes.search_url, headers=self.headers, data=json.dumps(data), cookies={}
        )
        return response

    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def similarity_search(
        self, smiles: str, limit: int, sim_threshold: float = 0.7
    ) -> requests.models.Response:
        """
        Searches Mcule using similarity

        Args:
            smiles (str): a search for similarity match to SMILES
            limit (int): Maximum number of matches returned
            sim_threshold (float): Minimum similarity threshold. Default is
                                   0.7

        Returns:
            dict: dictionary containing the search response
        """
        data = {
            "query": {
                "type": "sim",
                "query": smiles,
                "limit": limit,
                "sim_threshold": sim_threshold,
            }
        }
        response = requests.post(
            url=self.routes.search_url, headers=self.headers, data=json.dumps(data), cookies={}
        )
        return response

    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def substructure_search(self, smiles: str, limit: int) -> requests.models.Response:
        """
        Searches Mcule using substructure

        Args:
            smiles (str): a search for similarity match to SMILES
            limit (int): Maximum number of matches returned

        Returns:
            dict: dictionary containing the search response
        """
        data = {"query": {"type": "sss", "query": smiles, "limit": limit}}
        response = requests.post(
            url=self.routes.search_url, headers=self.headers, data=json.dumps(data), cookies={}
        )
        return response

    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def price_search_single(
        self, inchi_keys: list, amount: int = 1, currency: str = "USD", individual: bool = False
    ) -> requests.models.Response:
        """
        Searche Mcule for prices of compounds using a single amount for all
        the compounds eg. 1mg for all the compounds

        Args:
            inchi_keys (list): list of InChIKeys (returned from search results)
            amount (int): the amount value in mg. Default: 1, Min: 1, Max: 100.
            currency (str): Valid values are “USD”, “EUR”, “GBP”. The default is
            “USD”
            individual (bool): If true you will get individual prices for the compounds.
                               If false you will get “collective” prices for the compounds
                               which means you will get prices in the context when you
                               intend to “order” the compounds together.
                               These “collective” prices take into account possible price
                               jumps or other factors that might result in lower prices.
                               The default value is false.


        Returns:
            dict: dictionary containing the search response
        """
        data = {
            "compounds": compounds,
            "amount": amount,
            "currency": currency,
            "individual": individual,
        }
        response = requests.post(
            url=self.routes.pricing_url, headers=self.headers, data=json.dumps(data), cookies={}
        )

        return response

    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def price_search_multi(
        self, inchi_keys: list, amounts: list, currency: str = "USD", individual: bool = False
    ) -> requests.models.Response:
        """
        Searche Mcule for prices of compounds setting different amounts for
        the compounds

        Args:
            inchi_keys (list): list of InChIKeys (returned from search results)
            amounts (list): list of the amounts as values in mg. Default: 1, Min: 1,
                           Max: 100.
            currency (str): Valid values are “USD”, “EUR”, “GBP”. The default is
                            “USD”
            individual (bool): If true you will get individual prices for the compounds.
                               If false you will get “collective” prices for the compounds
                               which means you will get prices in the context when you
                               intend to “order” the compounds together.
                               These “collective” prices take into account possible price
                               jumps or other factors that might result in lower prices.
                               The default value is false.
        Returns:
            dict: dictionary containing the search response
        """
        compounds = [
            {"inchi_key": inchi, "amount": amount} for inchi, amount in zip(inchi_keys, amounts)
        ]
        data = {
            "compounds": compounds,
            "currency": currency,
            "individual": individual,
        }
        response = requests.post(
            url=self.routes.pricing_url, headers=self.headers, data=json.dumps(data), cookies={}
        )

        return response

    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def quote_request_single(
        self,
        inchi_keys: list,
        delivery_country: str,
        amount: int = 1,
        customer_email: str = None,
        currency: str = "USD",
        scheme: str = None,
        customer_name: str = None,
    ) -> requests.models.Response:
        """
        Get quotes for compounds from Mcule using different amounts

        Args:
            inchi_keys (list): list of InChIKeys (returned from search results)
            amounts (list): list of the amounts as values in mg. Default: 1, Min: 1,
                            Max: 100.
            delivery_country (str): ISO 3166-1 alpha-2 code of the delivery country.
            customer_email (str): The customer's email address. By default it will be filled with
                                  the email address associated with the user making the API request
                                  (defined by the token).
            currency (str): Valid values are “USD”, “EUR”, “GBP”. The default is “USD”.
            scheme (str): If you have access to predefined quote request schemes, you can specify
                          here which one you want to use. A quote query scheme is essentially a template
                          that contains predefined quote query parameters, or even include private parameters
                          that affect quote generation in various ways (e.g.: discounts, predefined custom prices).
                          These parameters can be customized for your use case. The scheme might already contain
                          mandatory fields like delivery_country. In this case you don't have to specify them again,
                          they will be applied from the scheme. Any explicitly specified public parameter during the
                          request will override the one that comes from the specified scheme.
            customer_name (str): The customer's full name. It is optional if the name of
                                 the user who is making the API request (defined by the token)
                                 is specified.
        Returns:
            dict: dictionary containing the search response
        """
        compounds = [
            {"inchi_key": inchi, "amount": amount} for inchi, amount in zip(inchi_keys, amounts)
        ]
        data = {
            "compounds": compounds,
            "amount": amount,
            "delivery_country": delivery_country,
            "customer_email": customer_email,
            "currency": currency,
            "scheme": scheme,
            "customer_name": customer_name,
        }
        response = requests.post(
            url=self.routes.quoterequest_url,
            headers=self.headers,
            data=json.dumps(data),
            cookies={},
        )

        return response

    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def quote_request_multi(
        self,
        inchi_keys: list,
        amounts: list,
        delivery_country: str,
        customer_email: str = None,
        currency: str = "USD",
        scheme: str = None,
        customer_name: str = None,
    ) -> requests.models.Response:
        """
        Get quotes for compounds from Mcule using different amounts

        Args:
            inchi_keys (list): list of InChIKeys (returned from search results)
            amounts (list): list of the amounts as values in mg. Default: 1, Min: 1,
                            Max: 100.
            delivery_country (str): ISO 3166-1 alpha-2 code of the delivery country.
            customer_email (str): The customer's email address. By default it will be filled with
                                  the email address associated with the user making the API request
                                  (defined by the token).
            currency (str): Valid values are “USD”, “EUR”, “GBP”. The default is “USD”.
            scheme (str): If you have access to predefined quote request schemes, you can specify
                          here which one you want to use. A quote query scheme is essentially a template
                          that contains predefined quote query parameters, or even include private parameters
                          that affect quote generation in various ways (e.g.: discounts, predefined custom prices).
                          These parameters can be customized for your use case. The scheme might already contain
                          mandatory fields like delivery_country. In this case you don't have to specify them again,
                          they will be applied from the scheme. Any explicitly specified public parameter during the
                          request will override the one that comes from the specified scheme.
            customer_name (str): The customer's full name. It is optional if the name of
                                 the user who is making the API request (defined by the token)
                                 is specified.
        Returns:
            dict: dictionary containing the search response
        """
        compounds = [
            {"inchi_key": inchi, "amount": amount} for inchi, amount in zip(inchi_keys, amounts)
        ]
        data = {
            "compounds": compounds,
            "delivery_country": delivery_country,
            "customer_email": customer_email,
            "currency": currency,
            "scheme": scheme,
            "customer_name": customer_name,
        }
        response = requests.post(
            url=self.routes.quoterequest_url,
            headers=self.headers,
            data=json.dumps(data),
            cookies={},
        )

        return response

    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def quote_status(
        self,
        quote_id: int,
    ) -> requests.models.Response:
        """
        Checks if asynchronous quote request has completed

        Args:
            id (int): id of quote request from quote_request_multi or
                      quote_request_single
        Returns:
            dict: dictionary containing the search response
        """

        response = requests.get(
            url=self.routes.quotestatus_url.format(quote_id=quote_id), headers=self.headers
        )

        return response

    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def detailed_quote(
        self,
        quote_id: int,
    ) -> requests.models.Response:
        """
        Retrieve detailed quote information for a quote request

        Args:
            id (int): id of quote request from quote_request_multi or
                      quote_request_single
        Returns:
            dict: dictionary containing the search response
        """
        response = requests.get(
            url=self.routes.detailedquote_url.format(quote_id=quote_id), headers=self.headers
        )

        return response

    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def excel_quote(
        self,
        quote_id: int,
        file_type: str = "excel",
    ) -> requests.models.Response:
        """
        Retrieve excel file (.xlsx) of quote for a quote request

        Args:
            id (int): id of quote request from quote_request_multi or
                      quote_request_single
            file_type (str): can be set to either "pdf" or "excel"
        Returns:
            file: returns either a .pdf or .xlsx file
        """
        response = requests.get(
            url=self.routes.downloadquote_url.format(quote_id=quote_id, file_type=file_type),
            headers=self.headers,
        )

        return response
