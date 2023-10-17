import requests
from liveramp_automation.utils.allure import *
from liveramp_automation.utils.log import Logger


def request_post(url, headers, data=None, json=None, **kwargs):
    """Sends a POST request.

    :param url: URL for the request.
    :param headers: Headers for the request.
    :param data: Data for the request body.
    :param json: JSON for the request body.
    :param kwargs: Additional arguments for the request.
    :return: Response object.
    """
    Logger.info("Sending POST request to {}".format(url))
    allure_attach_text("Sending POST request to:", url)

    if data:
        Logger.info("Request data: {}".format(data))
        allure_attach_text("Request Data:", data)
    if json:
        Logger.info("Request JSON: {}".format(json))
        allure_attach_json("Request JSON:", json)
    try:
        response = requests.post(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("Response content: {}".format(response.text))
        allure_attach_text("Response content:", response.text)
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
        allure_attach_text("HTTP Error Exception:", str(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
        allure_attach_text("Request Timed Out:", str(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
        allure_attach_text("An Error Occurred", str(error))
    return response


def request_get(url, headers, data=None, json=None, **kwargs):
    """Sends a GET request.

    :param url: URL for the request.
    :param headers: Headers for the request.
    :param data: Data for the request body.
    :param json: JSON for the request body.
    :param kwargs: Additional arguments for the request.
    :return: Response object.
    """
    Logger.info("Sending GET request to {}".format(url))
    allure_attach_text("Sending GET request to:", url)

    if data:
        Logger.info("Request data: {}".format(data))
        allure_attach_text("Request Data:", data)
    if json:
        Logger.info("Request JSON: {}".format(json))
        allure_attach_json("Request JSON:", json)
    try:
        response = requests.get(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("Response content: {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
        allure_attach_text("HTTP Error Exception:", str(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
        allure_attach_text("Request Timed Out:", str(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
        allure_attach_text("An Error Occurred", str(error))
    return response


def request_options(url, headers, **kwargs):
    """Sends an OPTIONS request.

    :param url: URL for the request.
    :param headers: Headers for the request.
    :param kwargs: Additional arguments for the request.
    :return: Response object.
    """
    Logger.info("Sending OPTIONS request to {}".format(url))
    allure_attach_text("Sending OPTIONS request to:", url)
    try:
        response = requests.options(url=url, headers=headers, **kwargs)
        Logger.info("Response content: {}".format(response.text))
        allure_attach_text("Response content:", response.text)
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
        allure_attach_text("HTTP Error Exception:", str(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
        allure_attach_text("Request Timed Out:", str(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
        allure_attach_text("An Error Occurred", str(error))
    return response


def request_delete(url, headers, data=None, json=None, **kwargs):
    """Sends a DELETE request.

    :param url: URL for the request.
    :param headers: Headers for the request.
    :param data: Data for the request body.
    :param json: JSON for the request body.
    :param kwargs: Additional arguments for the request.
    :return: Response object.
    """
    Logger.info("Sending DELETE request to {}".format(url))
    allure_attach_text("Sending DELETE request to:", url)

    if data:
        Logger.info("Request data: {}".format(data))
        allure_attach_text("Request Data:", data)
    if json:
        Logger.info("Request JSON: {}".format(json))
        allure_attach_json("Request JSON:", json)
    try:
        response = requests.delete(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("Response content: {}".format(response.text))
        allure_attach_text("Response content:", response.text)
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
        allure_attach_text("HTTP Error Exception:", str(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
        allure_attach_text("Request Timed Out:", str(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
        allure_attach_text("An Error Occurred", str(error))
    return response


def request_head(url, headers, data=None, json=None, **kwargs):
    """Sends a HEAD request.

    :param url: URL for the request.
    :param headers: Headers for the request.
    :param data: Data for the request body.
    :param json: JSON for the request body.
    :param kwargs: Additional arguments for the request.
    :return: Response object.
    """
    Logger.info("Sending HEAD request to {}".format(url))
    allure_attach_text("Sending HEAD request to:", url)
    if data:
        Logger.info("Request data: {}".format(data))
        allure_attach_text("Request Data:", data)
    if json:
        Logger.info("Request JSON: {}".format(json))
        allure_attach_json("Request JSON:", json)
    try:
        response = requests.head(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("Response content: {}".format(response.text))
        allure_attach_text("Response content:", response.text)
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
        allure_attach_text("HTTP Error Exception:", str(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
        allure_attach_text("Request Timed Out:", str(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
        allure_attach_text("An Error Occurred", str(error))
    return response


def request_put(url, headers, data=None, json=None, **kwargs):
    """Sends a PUT request.

   :param url: URL for the request.
   :param headers: Headers for the request.
   :param data: Data for the request body.
   :param json: JSON for the request body.
   :param kwargs: Additional arguments for the request.
   :return: Response object.
   """
    Logger.info("Sending PUT request to {}".format(url))
    allure_attach_text("Sending PUT request to:", url)
    if data:
        Logger.info("Request data: {}".format(data))
        allure_attach_text("Request Data:", data)
    if json:
        Logger.info("Request JSON: {}".format(json))
        allure_attach_json("Request JSON:", json)
    try:
        response = requests.put(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("Response content: {}".format(response.text))
        allure_attach_text("Response content:", response.text)
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
        allure_attach_text("HTTP Error Exception:", str(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
        allure_attach_text("Request Timed Out:", str(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
        allure_attach_text("An Error Occurred", str(error))
    return response


def request_patch(url, headers, data=None, json=None, **kwargs):
    """Sends a PATCH request.

    :param url: URL for the request.
    :param headers: Headers for the request.
    :param data: Data for the request body.
    :param json: JSON for the request body.
    :param kwargs: Additional arguments for the request.
    :return: Response object.
    """
    Logger.info("Sending PATCH request to {}".format(url))
    allure_attach_text("Sending PATCH request to:", url)
    if data:
        Logger.info("Request data: {}".format(data))
        allure_attach_text("Request Data:", data)
    if json:
        Logger.info("Request JSON: {}".format(json))
        allure_attach_json("Request JSON:", json)
    try:
        response = requests.patch(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("Response content: {}".format(response.text))
        allure_attach_text("Response content:", response.text)
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
        allure_attach_text("HTTP Error Exception:", str(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
        allure_attach_text("Request Timed Out:", str(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
        allure_attach_text("An Error Occurred", str(error))
    return response
