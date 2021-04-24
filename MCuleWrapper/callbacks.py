"""Callbacks for Mcule API."""
import logging
import requests

LOGGER = logging.getLogger("mcule:callbacks")


def search_result_on_success(response: requests.models.Response) -> dict:
    """
    Process the successful response of requests returning the exact search
    results.
    Args:
        response (requests.models.Response): response from an API request.
    Returns:
        dict: dictionary representing the response.
    """
    response_dict = response.json()
    return {
        "compound_id": response_dict["results"][0]["compound"]["idx"],
        "response": response_dict,
    }


def default_on_success(response: requests.models.Response) -> dict:
    """
    Process the successful response.
    Args:
        response (requests.models.Response): response from an API request.
    Returns:
        dict: dictionary representing the response.
    """
    response_dict = response.json()
    return {"response": response_dict}
