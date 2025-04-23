"""Module to test exceptions and warnings."""
import pytest

from sprynger import Metadata, init
from sprynger.exceptions import (
    APIError,
    MissingAPIKeyError,
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    InvalidRequestError,
    InternalServerError,
)

def test_empty_response():
    """Test the empty response."""
    init()
    with pytest.warns(UserWarning, match='No results where found. Check the query.'):
        Metadata(doi='does_not_exist', refresh=True)


def test_authentication_error():
    """Test the authentication error."""
    init(api_key='does_not_exist')
    with pytest.raises(AuthenticationError, match='Authentication failed. Check your API key.'):
        Metadata('10.1007/s10660-023-09761-x', refresh=True)


def test_api_error():
    """Test the API error."""
    with pytest.raises(APIError) as exc_info:
        raise APIError(500, "Test API error")
    assert exc_info.value.status_code == 500
    assert exc_info.value.message == "Test API error"
    assert str(exc_info.value) == "500: Test API error"


def test_missing_api_key_error():
    """Test the missing API key error."""
    with pytest.raises(MissingAPIKeyError) as exc_info:
        raise MissingAPIKeyError()
    assert exc_info.value.message == "API key is missing. Please provide a valid API key."
    assert str(exc_info.value) == "API key is missing. Please provide a valid API key."


def test_rate_limit_error():
    """Test the rate limit error."""
    with pytest.raises(RateLimitError) as exc_info:
        raise RateLimitError(429, "Too many requests")
    assert exc_info.value.status_code == 429
    assert exc_info.value.message == "Too many requests"
    assert str(exc_info.value) == "429: Too many requests"


def test_resource_not_found_error():
    """Test the resource not found error."""
    with pytest.raises(ResourceNotFoundError) as exc_info:
        raise ResourceNotFoundError(404, "Resource not found")
    assert exc_info.value.status_code == 404
    assert exc_info.value.message == "Resource not found"
    assert str(exc_info.value) == "404: Resource not found"


def test_invalid_request_error():
    """Test the invalid request error."""
    with pytest.raises(InvalidRequestError) as exc_info:
        raise InvalidRequestError(400, "Bad request")
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "Bad request"
    assert str(exc_info.value) == "400: Bad request"


def test_internal_server_error():
    """Test the internal server error."""
    with pytest.raises(InternalServerError) as exc_info:
        raise InternalServerError(500, "Server error")
    assert exc_info.value.status_code == 500
    assert exc_info.value.message == "Server error"
    assert str(exc_info.value) == "500: Server error"
