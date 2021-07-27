"""Core MCule API module."""
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import requests
import json
from typing import Optional

from .urls import MCuleRoutes, UltimateMCuleRoutes
from .callbacks import default_on_success
from .decorators import mcule_api_limits, response_handling

LOGGER = logging.getLogger("mcule:core")


class MCuleWrapper:
    """
    Python wrapper for MCule API wrapper to access the API requests.
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
                the environment variable MCULE_BASE_URL or https://mcule.com
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
        return {
            "Content-Type": "application/json",
            "Authorization": "Token {}".format(self._authorisation_token),
        }

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def databasefiles(self) -> requests.models.Response:
        """
        Returns publicly available Mcule database files and URLs

        Returns:
            dict: dictionary containing the search response
        """
        response = requests.get(url=self.routes.database_url, headers=self.headers, cookies={})
        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def compounddetails(self, mcule_id: str) -> requests.models.Response:
        """
        Gets compound details from Mcule

        Args:
            mcule_id (str): Mcule ID of compound
        Returns:
            dict: dictionary containing the search response
        """
        response = requests.get(
            url=self.routes.compounddetails_url.format(mcule_id=mcule_id),
            headers=self.headers,
            cookies={},
        )
        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def inchikeylookup(self, inchi_key: str) -> requests.models.Response:
        """
        Searches Mcule using InChiKey

        Args:
            inchi_key (str): InChiKey of compound
        Returns:
            dict: dictionary containing the search response
        """
        print(self.routes.inchikeylookup_url.format(inchi_key=inchi_key))
        response = requests.get(
            url=self.routes.inchikeylookup_url.format(inchi_key=inchi_key),
            headers=self.headers,
            cookies={},
        )
        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def singlequerysearch(self, query: str) -> requests.models.Response:
        """
        Searches Mcule using an mcule ID, SMILES, InChI or InChIKey identifier.
        Retruns mcule id, smiles and URL for a compound

        Args:
            query (str): An mcule ID, SMILES, InChI or InChIKey identifier

        Returns:
            dict: dictionary containing the search response
        """

        response = requests.get(
            url=self.routes.singlequery_url.format(query=query),
            headers=self.headers,
            cookies={},
        )

        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def compoundavailability(self, mcule_id: str) -> requests.models.Response:
        """
        Searches Mcule for compound availability

        Args:
            mcule_id (str): Mcule compound ID
        Returns:
            dict: dictionary containing the search response
        """

        response = requests.get(
            url=self.routes.compoundavailability_url.format(mcule_id=mcule_id),
            headers=self.headers,
            cookies={},
        )

        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def compoundprices(self, mcule_id: str) -> requests.models.Response:
        """
        Get compound prices from Mcule

        Args:
            mcule_id (str): Mcule compound ID
        Returns:
            dict: dictionary containing the search response
        """

        response = requests.get(
            url=self.routes.compoundprices_url.format(mcule_id=mcule_id),
            headers=self.headers,
            cookies={},
        )

        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def compoundpricesamount(self, mcule_id: str, amount: float = 10) -> requests.models.Response:
        """
        Get compound prices from Mcule

        Args:
            mcule_id (str): Mcule compound ID
            amount (float): Amount required
        Returns:
            dict: dictionary containing the search response
        """

        response = requests.get(
            url=self.routes.compoundpricessetamount_url.format(mcule_id=mcule_id, amount=amount),
            headers=self.headers,
            cookies={},
        )

        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def multiplequeriessearch(self, queries: list) -> requests.models.Response:
        """
        Exact search of MCule fro multiple queries

        Args:
            queries (list): list of mcule ID, SMILES, InChI or InChIKey identifiers
        Returns:
            dict: dictionary containing the search response
        """
        data = {"queries": queries}
        response = requests.post(
            url=self.routes.multiplequeries_url,
            headers=self.headers,
            data=json.dumps(data),
            cookies={},
        )

        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def multiplequerieswithavailability(self, queries: list) -> requests.models.Response:
        """
        Exact search of MCule for multiple queries and availability

        Args:
            queries (list): list of mcule ID, SMILES, InChI or InChIKey identifiers
        Returns:
            dict: dictionary containing the search response
        """
        data = {"queries": queries}
        response = requests.post(
            url=self.routes.multiplequerieswithavailability_url,
            headers=self.headers,
            data=json.dumps(data),
            cookies={},
        )

        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def similaritysearch(
        self, query: str, limit: int = 3, threshold: float = 0.8
    ) -> requests.models.Response:
        """
        Similarity search of MCule for a compound

        Args:
            query (str): Mcule ID or SMILES
            limit (int): Maximum number of matches found, Default 3
            threshold (float): Similarity threshold. Default 0.8
        Returns:
            dict: dictionary containing the search response
        """
        data = {
            "query": query,
            "limit": limit,
            "threshold": threshold,
        }
        response = requests.post(
            url=self.routes.similaritysearch_url,
            headers=self.headers,
            data=json.dumps(data),
            cookies={},
        )

        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def substructuresearch(self, query: str) -> requests.models.Response:
        """
        Substructure search of MCule for a compound

        Args:
            query (str): Mcule ID or SMILES
        Returns:
            dict: dictionary containing the search response
        """
        data = {"query": query}
        response = requests.post(
            url=self.routes.substructuresearch_url,
            headers=self.headers,
            data=json.dumps(data),
            cookies={},
        )

        return response

    # Chcked all is working and good up unil here - getting a 400 validation error...
    # for quote request
    @response_handling(success_status_code=201, on_success=default_on_success)
    @mcule_api_limits
    def quoterequest(
        self, mcule_ids: list, delivery_country: str = "GB", amount: int = 1, **optional_args
    ) -> requests.models.Response:
        """
        Substructure search of MCule for a compound

        Args:
            Mandatory fields:
            mcule_ids: List of mcule IDs of structures you want get a quote for.
            delivery_country: ISO 3166-1 alpha-2 code of the delivery country. Defaults to GB
            amount: The amount or target concentration-volume pair (target_volume and target_cc) need to be specified. Defaults to 1

            Semi-optional - depends on info stored in MCule account
            customer_first_name: The customer's first name. It does not need to be specified if the user's first name is specified on the Edit profile page on mcule.com.
            customer_last_name: The customer's last name. It does not need to be specified if the user's last name is specified on the Edit profile page on mcule.com.


            Optional fields:
            amount: Preferred amount per molecule (mg). (default: 1)
            min_amount: Acceptable minimum amount (mg). (default: null)
            target_volume: The target volume (in ml), in case of solution based amount.
            target_cc: Target concentration (mM), in case of solution based amount.
            extra_amount: In case of solution based amount calculation the preferred extra amount (in mg) can be specified here.
            min_extra_amount: In case of solution based amount calculation the acceptable minimum extra amount (in mg) can be specified here.
            customer_email: The customer's email address. By default it will be filled with the email address associated with the user making the API request.
            delivery_time: Delivery time limit (working days). Door-to-door delivery time. Only offer molecules that are available within the specified number of working days. You can specify null if delivery time is not critical. (default: 21)
            purity: Required minimum purity (%). (default: null)
            higher_amounts: Set to true if you would like to get a quote for the compounds in the largest possible quantity in case they do not cost more than the specified amount. (default: false)
            item_filters: Per query item filters. Currently it supports only supplier filtering. See example below.

            Advanced optional fields:

            keep_original_salt_form: If false (by default), allow Mcule to deliver an alternative salt form if the original is not available. (default: false)
            keep_original_tautomer_form: If false (by default), allow Mcule to deliver compounds drawn in alternative tautomer forms. Alternative tautomer forms are perceived by the system based on IUPAC InChI identifiers. (default: false)
            keep_original_stereo_form: If false (by default), allow Mcule to deliver compounds drawn in alternative stereochemical forms. (default: false)
            deliver_multiple_salt_forms: Deliver multiple salt forms or tautomers of the same compound. If false and the input contains duplicates, only a single salt form / tautomer will be kept (only effective when alternative salt or tautomer forms are allowed). (default: false)


        Returns:
            dict: dictionary containing the search response
        """
        allowed_keywords = [
            "item_filters",
            "customer_first_name",
            "customer_last_name",
            "customer_email",
            "min_amount",
            "target_volume",
            "target_cc",
            "extra_amount",
            "min_extra_amount",
            "delivery_time",
            "purity",
            "higher_amouts",
            "keep_original_salt_form",
            "keep_original_tautomer_form",
            "keep_original_stereo_form",
            "deliver_multiple_salt_forms",
        ]

        optional_arguments = [
            (keyword, value)
            for keyword, value in zip(optional_args, optional_args.values())
            if keyword in allowed_keywords
        ]
        optional_dict = dict(optional_arguments)

        data = {
            "mcule_ids": mcule_ids,
            "delivery_country": delivery_country,
            "amount": amount,
        }

        if optional_dict:
            data.update(optional_dict)

        response = requests.post(
            url=self.routes.quoterequest_url,
            headers=self.headers,
            data=json.dumps(data),
            cookies={},
        )

        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def quoterequeststatus(self, quote_id: str) -> requests.models.Response:
        """
        Since processing a quote request and generating suitable
        quotes can take some time it is an asynchronous process.
        You can query the status of a quote request by calling
        the detail API endpoint of the quote request.
        It is returned in the api_url field when you create
        the quote request. You can also use the id field to
        construct the url of the API call. You can check the
        state field of the response whether the async quote
        request processing is finished.

         States:

        10 -> Pending: The quote query is queued but the processing
              has not started yet.
        20 -> Running: The processing of the quote query is in
              progress.
        30 -> Done: The processing of the quote query is finished.
              For one quote request query we might generate multiple
              quotes (this is what we call a group) or it is also
              possible that we could not generate any quotes for a
              particular quote request. If there are quotes they will
              appear under the group field where the quotes field
              contains a list of the generated quotes and some basic
              info about them. You can get detailed data of a
              particular quote by calling the endpoint specified in
              the api_url field.
        40 -> Error: An error happened during the processing of the
              quote query.


        Args:
            quote_id (str): Mcule quote ID
        Returns:
            dict: dictionary containing the search response
        """

        response = requests.get(
            url=self.routes.quoterequeststatus_url.format(quote_id=quote_id),
            headers=self.headers,
            cookies={},
        )

        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def detailedquote(self, quote_id: str) -> requests.models.Response:
        """
        Deatiled data re an individual quote

        Args:
            quote_id (str): Mcule quote ID
        Returns:
            dict: dictionary containing the search response
        """
        response = requests.get(
            url=self.routes.detailedquote_url.format(quote_id=quote_id),
            headers=self.headers,
            cookies={},
        )
        return response

    @response_handling(success_status_code=200, on_success=default_on_success)
    @mcule_api_limits
    def quotemissingstructures(self, quote_id: str) -> requests.models.Response:
        """
        Missing structures from quote along with reasons for exclusion

        Args:
            quote_id (str): Mcule quote ID
        Returns:
            dict: dictionary containing the search response
        """
        response = requests.get(
            url=self.routes.quotemissingstructures_url.format(quote_id=quote_id),
            headers=self.headers,
            cookies={},
        )
        return response

    # Need to figure this out still but for now, it's ggod to go
    # @response_handling(success_status_code=200, on_success=default_on_success)
    # @mcule_api_limits
    # def downloadquote(
    #     self, quote_id: str, download_type: str = "download-pd"
    # ) -> requests.models.Response:
    #     """
    #     Download .pdf of quote

    #     Args:
    #         quote_id (str): Mcule quote ID
    #         download_type: Can be either use 'download-pdf' or
    #                       'download-excel'. If no download_type
    #                        specified then 'donwload-pdf' used
    #     Returns:
    #         dict: dictionary containing the search response
    #     """
    #     response = requests.get(
    #         url=self.routes.downloadquote_url.format(
    #             quote_id=quote_id, download_type=download_type
    #         ),
    #         headers=self.headers,
    #         cookies={},
    #     )
    #     return response


class UltimateMCuleWrapper:
    """
    Python wrapper for MCule Ultimate API wrapper to access the API requests.
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
        self.routes = UltimateMCuleRoutes(base_url)

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
