import pytest
import requests

"""
HTTP methods as post, get

@Author: Efrat Cohen
@Date: 02.2023
"""


def post(url, json):
    """
    post http method to send data to a server to create/update a resource.

    @param: url - current post request url
    @param: json - current post request data json
    @return: post_response - post response
    """
    post_response = requests.post(url, json=json)
    pytest.logger.info("post http call response: " + str(post_response))
    return post_response


def get(url):
    """
    get http method to request data from a specified resource.

    @param: url - current get request url
    @return: get_response - get response
    """
    get_response = requests.get(url)
    pytest.logger.info("get http call response: " + str(get_response))
    return get_response
