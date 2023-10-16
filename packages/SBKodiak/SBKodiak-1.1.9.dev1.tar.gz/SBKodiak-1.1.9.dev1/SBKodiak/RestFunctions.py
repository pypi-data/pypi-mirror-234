import requests
import logging
import urllib3

from .KodiakGlobals import KodiakGlobals


# Disabling the certification warnings - Without this, every HTTPS request to kodiak will display a logging.warning
urllib3.disable_warnings()


def do_POST(json_msg, endpoint_url, header={}):
    """
    Common endpoint to POST the JSON to an endpoint

    :param json_msg: Json formatted message to send
    :param endpoint_url: URL to post to ( XXX.XXX.XXX.XXX/end/point )
    :param header: Header to include in request (optional)

    :return: Whatever is returned from the post request
    """

    print(f"DOING POST: {repr(json_msg)} to {endpoint_url} ")

    # Common requests python post
    response = requests.post(endpoint_url, json=json_msg, verify=False, headers=header)

    # Add the response to the list of responses - Debugging
    KodiakGlobals.last_response.append(repr(response.text))

    # log the response
    logging.debug(repr(response.text))
    logging.debug(response)

    print(repr(response.text))

    # return RAW response object
    return response


def do_GET(endpoint_url: str, header={}):
    """
    Common endpoint to GET response from an endpoint

    :param header: Optional header to send
    :param endpoint_url: URL to get to ( XXX.XXX.XXX.XXX/end/point )

    :return: Whatever is returned from the get request
    """

    # Common requests python post
    response = requests.get(endpoint_url, verify=False, headers=header)

    # Add the response to the list of responses - Debugging
    KodiakGlobals.last_response.append(repr(response.text))

    # Print the response
    logging.debug(response.text)

    # Returning raw response object
    return response

