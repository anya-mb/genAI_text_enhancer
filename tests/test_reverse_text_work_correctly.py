import json
from http import HTTPStatus
import pytest
from backend.main import lambda_reverse_text_backend


def test_lambda_reverse_text_backend():
    body = {
        "operation": "reverse",
        "text": "example"
    }
    event = {
        'body': json.dumps(body)  # Convert the dictionary to a JSON string
    }

    context = None  # context is often not needed for basic tests
    response = lambda_reverse_text_backend(event, context)

    status_code = HTTPStatus.OK.value
    body_text = {
        "operation": "reverse",
        "text": "elpmaxe"
    }

    expected_response = {
            "statusCode": status_code,
            "body": json.dumps(body_text, indent=2),
            "headers": {"content-type": "application/json"},
        }

    assert response == expected_response


def test_lambda_reverse_text_backend_with_invalid_text_input():
    # Example of invalid input
    body = {
            "operation": "reverse",
            "text": None
        }

    event = {
        'body': json.dumps(body)  # Convert the dictionary to a JSON string
    }
    context = None

    response = lambda_reverse_text_backend(event, context)
    status_code = response['statusCode']

    expected_status_code = HTTPStatus.BAD_REQUEST.value

    assert status_code == expected_status_code


def test_lambda_reverse_text_backend_with_unknown_operation():
    # Example of invalid input
    body = {
        "operation": "invalid_operation",
        "text": "example"
    }

    event = {
        'body': json.dumps(body)  # Convert the dictionary to a JSON string
    }
    context = None

    response = lambda_reverse_text_backend(event, context)
    status_code = response['statusCode']

    expected_status_code = HTTPStatus.BAD_REQUEST.value

    assert status_code == expected_status_code

def test_lambda_reverse_text_backend_with_invalid_body():
    # Example of invalid input
    body = {}

    event = {
        'body': json.dumps(body)  # Convert the dictionary to a JSON string
    }
    context = None

    response = lambda_reverse_text_backend(event, context)
    status_code = response['statusCode']

    expected_status_code = HTTPStatus.BAD_REQUEST.value

    assert status_code == expected_status_code