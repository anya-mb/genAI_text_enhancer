import json
from http import HTTPStatus


def lambda_reverse_text_backend(event, context):
    # The 'body' field is a stringified JSON, so parse it as well
    body = json.loads(event['body'])

    try:
        # Extract the 'text' field from the parsed body
        extracted_text = body['text']
        reversed_dict = {
            "operation": "reverse",
            "text": extracted_text[::-1]
        }

        response = {
            "statusCode": HTTPStatus.OK.value,
            "body": json.dumps(reversed_dict, indent=2),
            "headers": {"content-type": "application/json"},
        }

    except Exception as e:
        response = {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR.value,
            "body": f"Exception={e}",
            "headers": {"content-type": "text/plain"},
        }
    return response
