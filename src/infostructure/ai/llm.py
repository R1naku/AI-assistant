import requests


def generate_response(text):

    data = {
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ]
    }


    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json=data,
        timeout=60
    )


    return (
        response
        .json()
        ["choices"][0]
        ["message"]
        ["content"]
    )