import json
from http import HTTPStatus


KNOWN_OPERATIONS = ['reverse', 'summarize']


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


def validate_nad_get_text_and_operation(event, context):
    # The 'body' field is a stringified JSON, so parse it as well
    body = json.loads(event['body'])

    if validation_failure := validate_request(body):
        return validation_failure

    try:
        # Extract the 'text' field from the parsed body
        extracted_text = body['text']
        extracted_operation = body['operation']

        return extracted_text, extracted_operation

    except Exception as e:
        return make_return(HTTPStatus.INTERNAL_SERVER_ERROR.value, f"Exception={e}")


def lambda_reverse_text_backend(event, context):
    text, operation = validate_nad_get_text_and_operation(event, context)

    if operation != "reverse":
        return make_return(HTTPStatus.BAD_REQUEST.value, "Bad request exception: operation is not reverse, but invoked reverse lambda")

    reversed_dict = {
        "operation": operation,
        "text": text[::-1]
    }

    return make_return(HTTPStatus.OK.value, json.dumps(reversed_dict, indent=2))


def lambda_summarize_text_backend(event, context):
    text, operation = validate_nad_get_text_and_operation(event, context)

    if operation != "summarize":
        return make_return(HTTPStatus.BAD_REQUEST.value, "Bad request exception: operation is not summarize, but invoked summarize lambda")

    summarized_dict = {
        "operation": operation,
        "text": "This is summarized text"
    }

    print(f"{summarized_dict=}")

    return make_return(HTTPStatus.OK.value, json.dumps(summarized_dict, indent=2))
