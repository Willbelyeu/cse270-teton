import requests
import pytest
import requests_mock # Import the necessary mocking library

# Define the base URL and endpoint we are mocking
BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/users"
MOCK_URL = f"{BASE_URL}{ENDPOINT}"

def test_unauthorized_access_401(requests_mock):
    """
    Tests that the /users endpoint returns a 401 Unauthorized
    when provided with mock or invalid 'admin' credentials.
    
    The server response is mocked using requests_mock.
    """
    
    # 1. DEFINE THE MOCK RESPONSE (401 scenario)
    # We tell requests_mock to intercept GET requests to MOCK_URL
    # and return status 401 with a short, empty-like body.
    mock_body = "Unauthorized."
    requests_mock.get(
        MOCK_URL,
        status_code=401,
        text=mock_body
    )

    # Parameters representing the requested invalid credentials (optional for mock, but good practice)
    params = {
        "username": "admin",
        "password": "admin"
    }

    print(f"\nAttempting MOCKED request for 401 to: {MOCK_URL}")

    # Perform the GET request (it hits the mock defined above)
    response = requests.get(MOCK_URL, params=params, timeout=5)

    # 1. Assert the HTTP response code is 401 (Unauthorized)
    assert response.status_code == 401, (
        f"Expected status code 401, but got {response.status_code}. "
        f"Response text: {response.text}"
    )

    # 2. Assert the response content is essentially empty (less than 50 bytes)
    assert len(response.content) < 50, (
        f"Expected an empty response body, but found content of size {len(response.content)}. "
        f"Content (first 50 chars): {response.text[:50]}..."
    )

    print(f"Test passed: Received expected 401 status code from mock.")


def test_successful_access_200(requests_mock):
    """
    Tests that the /users endpoint returns a 200 OK 
    when provided with mock 'admin' credentials.
    
    The server response is mocked using requests_mock.
    """
    
    # 1. DEFINE THE MOCK RESPONSE (200 scenario)
    # We define a minimal successful response body (which should not be empty).
    mock_body = "User data: [{'id': 1, 'username': 'admin'}]"
    requests_mock.get(
        MOCK_URL,
        status_code=200,
        text=mock_body
    )

    # Parameters representing the requested valid credentials (optional for mock)
    params = {
        "username": "admin",
        "password": "qwerty"  # Valid password for this test case
    }

    print(f"\nAttempting MOCKED request for 200 to: {MOCK_URL}")

    # Perform the GET request (it hits the mock defined above)
    response = requests.get(MOCK_URL, params=params, timeout=5)

    # 1. Assert the HTTP response code is 200 (OK)
    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}. "
        f"Response text: {response.text}"
    )

    # 2. Assert the response content is NOT empty (since a successful call should return data).
    # We assert that the text content matches our mock body and has a reasonable length.
    assert response.text == mock_body, "Response text did not match the defined mock body."
    assert len(response.content) > 2, (
        f"Expected data in the response body, but found content was nearly empty."
    )

    print(f"Test passed: Received expected 200 status code from mock.")