import json
from http import HTTPStatus


KNOWN_OPERATIONS = ['reverse']


def make_return(status_code, body_text):
    return {
            "statusCode": status_code,
            "body": body_text,
            "headers": {"content-type": "application/json"},
        }


def validate_request(request_body):
    if 'operation' not in request_body:
        return make_return(HTTPStatus.BAD_REQUEST.value, "Bad request exception: operation is not in body")

    if 'text' not in request_body:
        return make_return(HTTPStatus.BAD_REQUEST.value, "Bad request exception: text is not in body")

    extracted_text = request_body['text']

    if type(extracted_text) != str:
        return make_return(HTTPStatus.BAD_REQUEST.value, "Bad request exception: text is not string")

    extracted_operation = request_body['operation']

    if extracted_operation not in KNOWN_OPERATIONS:
        return make_return(HTTPStatus.BAD_REQUEST.value, "Unknown operation")


def lambda_reverse_text_backend(event, context):
    # The 'body' field is a stringified JSON, so parse it as well
    body = json.loads(event['body'])

    if validation_failure := validate_request(body):
        return validation_failure

    try:
        # Extract the 'text' field from the parsed body
        extracted_text = body['text']
        extracted_operation = body['operation']

        reversed_dict = {
            "operation": extracted_operation,
            "text": extracted_text[::-1]
        }

        return make_return(HTTPStatus.OK.value, json.dumps(reversed_dict, indent=2))

    except Exception as e:
        return make_return(HTTPStatus.INTERNAL_SERVER_ERROR.value, f"Exception={e}")
