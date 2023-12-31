# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
import os, openai, requests

initialize_app()


@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    print(req.data)
    return https_fn.Response("Hello world!")



openai.api_key = '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'

MODEL = "gpt-3.5-turbo"
PROMPT = "Tell me a dad joke"

def chat_with_gpt111(request):
    request_json = request #request.get_json()
    message = request_json['message'] if 'message' in request_json else 'Tell me a unique, random fact in less than 50 words.'
    
    messages=[
        {"role": "system", "content": "You are a helpful assistant named Jarvis."},
        {"role": "user", "content": message}
    ]
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        max_tokens=100,
        temperature=0.7,
        top_p=1.0,
    )
    response = response['choices'][0]['message']['content']
    return response
    


def handleWebhook111(request):
    req = request.get_json()
    print(req)

    responseText = ""
    intent = req["queryResult"]["intent"]["displayName"]

    if intent == "Default Welcome Intent":
        #responseText = "Hello from a GCF Webhook"
        responseText = chat_with_gpt(request)
    elif intent == "get-agent-name":
        responseText = "My name is Flowhook"
    else:
        responseText = f"There are no fulfillment responses defined for Intent {intent}"
    
    message = {'message': req['queryResult']['queryText']}
    responseText = chat_with_gpt(message)
    print({'message': message, 'response': responseText})

    # You can also use the google.cloud.dialogflowcx_v3.types.WebhookRequest protos instead of manually writing the json object
    res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}

    return res

