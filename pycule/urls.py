"""URL routes for MCule API"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os
from typing import Optional


class MCuleRoutes:
    """
    Routes for MCule API service.
    """

    def __init__(self, base_url: Optional[str] = None) -> None:
        """
        Initialize the routes.
        Args:
            base_url (str, optional): base url for the service. If not provided it will default to
                the environment variable MCule or https://mcule.com
        """
        self._base_url = base_url if base_url else os.getenv("MCULE_BASE_URL", "https://mcule.com")
        self._update_routes()

    def _update_routes(self) -> None:
        """Update all the routes."""
        self.api_url = "{}/{}".format(self._base_url, "api/v1")
        self.database_url = "{}/{}".format(self.api_url, "database-files")
        self.compounddetails_url = "{}/{}/{}".format(self.api_url, "compound", "{mcule_id}")
        self.inchikeylookup_url = "{}/{}/{}".format(self.api_url, "lookup/inchikey", "{inchi_key}")
        self.singlequery_url = "{}/{}/{}/{}{}".format(
            self.api_url, "search", "lookup", "?query=", "{query}"
        )
        self.compoundavailability_url = "{}/{}/{}/{}".format(
            self.api_url, "compound", "{mcule_id}", "availability"
        )
        self.compoundprices_url = "{}/{}/{}/{}".format(
            self.api_url, "compound", "{mcule_id}", "prices"
        )
        self.multiplequeries_url = "{}/{}/{}/".format(self.api_url, "search", "exact")
        self.multiplequerieswithavailability_url = "{}/{}/{}/{}/".format(
            self.api_url, "search", "exact", "availability"
        )
        self.similaritysearch_url = "{}/{}/{}/".format(self.api_url, "search", "sim")
        self.substructuresearch_url = "{}/{}/{}/".format(self.api_url, "search", "sss")
        self.quoterequest_url = "{}/{}/".format(self.api_url, "iquote-queries")
        self.quoterequeststatus_url = "{}/{}/{}".format(
            self.api_url, "iquote-queries", "{quote_id}"
        )
        self.detailedquote_url = "{}/{}/{}".format(self.api_url, "iquotes", "{quote_id}")
        self.quotemissingstructures_url = "{}/{}/{}/{}".format(
            self.api_url, "iquotes", "{quote_id}", "missing"
        )
        self.downloadquote_url = "{}/{}/{}/{}".format(
            self.api_url, "iquotes", "{quote_id}", "{download_type}"
        )

    @property
    def base_url(self) -> str:
        """
        Get the base url for the MCule service.
        Returns:
            str: base url for the service
        """
        return self._base_url

    @base_url.setter
    def base_url(self, value: str) -> None:
        """
        Set the base url for the Mcule service.
        Args:
            value (str): bease url to set.
        """
        self._base_url = value
        self._update_routes()


class UltimateMCuleRoutes:
    """
    Routes for MCule Ultimate API service.
    """

    def __init__(self, base_url: Optional[str] = None) -> None:
        """
        Initialize the routes.
        Args:
            base_url (str, optional): base url for the service. If not provided it will default to
                the environment variable MCule or https://ultimateapp.mcule.com
        """
        self._base_url = (
            base_url
            if base_url
            else os.getenv("MCULE_ULTIMATE_BASE_URL", "https://ultimateapp.mcule.com")
        )
        self._update_routes()

    def _update_routes(self) -> None:
        """Update all the routes."""
        self.api_url = "{}/{}".format(self._base_url, "api/v1")
        self.search_url = "{}/{}/".format(self.api_url, "searches")
        self.pricing_url = "{}/{}/".format(self.api_url, "pricing")
        self.quoterequest_url = "{}/{}/".format(self.api_url, "iquote-queries")
        self.quotestatus_url = "{}/{}/{}/".format(self.api_url, "iquote-queries", "{quote_id}")
        self.detailedquote_url = "{}/{}/{}/".format(self.api_url, "iquotes", "{quote_id}")
        self.downloadquote_url = "{}/{}/{}/{}/".format(
            self.api_url, "iquotes", "{quote_id}", "{file_type}"
        )

    @property
    def base_url(self) -> str:
        """
        Get the base url for the MCule service.
        Returns:
            str: base url for the service
        """
        return self._base_url

    @base_url.setter
    def base_url(self, value: str) -> None:
        """
        Set the base url for the Mcule service.
        Args:
            value (str): bease url to set.
        """
        self._base_url = value
        self._update_routes()