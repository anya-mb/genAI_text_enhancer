import json
from http import HTTPStatus

import json
import boto3


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


def get_text_and_operation(event):
    body = json.loads(event['body'])

    extracted_text = body['text']
    extracted_operation = body['operation']

    return extracted_text, extracted_operation


def is_not_valid(event):
    # The 'body' field is a stringified JSON, so parse it as well
    body = json.loads(event['body'])

    if validation_failure := validate_request(body):
        return validation_failure

    try:
        # Extract the 'text' field from the parsed body
        extracted_text = body['text']
        extracted_operation = body['operation']

        return False

    except Exception as e:
        return make_return(HTTPStatus.INTERNAL_SERVER_ERROR.value, f"Exception={e}")


def reverse_text_backend(text):
    reversed_dict = {
        # "operation": operation,
        "text": text[::-1]
    }

    return make_return(HTTPStatus.OK.value, json.dumps(reversed_dict, indent=2))


def summarize_text_backend(text, modelId='anthropic.claude-instant-v1'):
    boto3_bedrock = boto3.client('bedrock-runtime')

    prompt_data = f"Please summarize given text: {text}"

    # formatting body for claude
    # It is a bit picky and must end with "Assistant:"
    body = json.dumps({"prompt": "Human:" + prompt_data + "\nAssistant:", "max_tokens_to_sample": 300})

    # Choose the model
    accept = 'application/json'
    contentType = 'application/json'

    # invoke model and print out answer
    response = boto3_bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())


    summarized_dict = {
        # "operation": operation,
        "text": response_body['completion'] #"This is summarized text"
    }

    return make_return(HTTPStatus.OK.value, json.dumps(summarized_dict, indent=2))


def lambda_improve_text_backend(event, context):
    bad_validation_result = is_not_valid(event)

    if bad_validation_result:
        return bad_validation_result

    text, operation = get_text_and_operation(event)

    if operation == "reverse":
        reversed_result = reverse_text_backend(text)
        return reversed_result

    elif operation == "summarize":
        summarized_result = summarize_text_backend(text)
        return summarized_result
    else:
        return make_return(HTTPStatus.BAD_REQUEST.value, "Unknown operation")
