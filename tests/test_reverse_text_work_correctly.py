import json
from http import HTTPStatus
import pytest
from backend.main import lambda_improve_text_backend


def test_lambda_improve_text_backend():
    body = {
        "operation": "reverse",
        "text": "example"
    }
    event = {
        'body': json.dumps(body)  # Convert the dictionary to a JSON string
    }

    context = None  # context is often not needed for basic tests
    response = lambda_improve_text_backend(event, context)

    # what is expected
    status_code = HTTPStatus.OK.value
    body_text = {
        # "operation": "reverse",
        "text": "elpmaxe"
    }

    expected_response = {
        "statusCode": status_code,
        "body": json.dumps(body_text, indent=2),
        "headers": {"content-type": "application/json"},
    }

    assert response == expected_response, f"{response=}, {expected_response=}"


@pytest.mark.parametrize("body", [
    {"operation": "reverse", "text": None},
    {"operation": "invalid_operation", "text": "example"},
    {},
    {"text": "example"},
    {"operation": "reverse"}
])
def test_lambda_reverse_text_backend_invalid_input(body):
    expected_status_code = HTTPStatus.BAD_REQUEST.value

    event = {
        'body': json.dumps(body)  # Convert the dictionary to a JSON string
    }
    context = None

    response = lambda_improve_text_backend(event, context)
    status_code = response['statusCode']

    assert status_code == expected_status_code
