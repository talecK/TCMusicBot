from converters import json_response

def response(messages, data=None, status=200):

    response_data = {}

    if messages:
        if not isinstance(messages,list):
            messages = [messages]

        response_data["messages"] = messages

    if data:
        response_data["data"] = data

    prepared_response = json_response(response_data)
    prepared_response.status_code = status

    return prepared_response
