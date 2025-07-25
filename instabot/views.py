from django.shortcuts import render
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from decouple import config

VERIFY_TOKEN = config('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = config('PAGE_ACCESS_TOKEN')

@csrf_exempt
def instagram_webhook(request):
    if request.method == 'GET':
        # Verification challenge from Meta
        verify_token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse("Invalid verification token", status=403)

    elif request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))

        for entry in payload.get('entry', []):
            for messaging in entry.get('messaging', []):
                sender_id = messaging['sender']['id']
                message_text = messaging.get('message', {}).get('text')

                if sender_id and message_text:
                    send_instagram_reply(sender_id, "Hello!")

        return HttpResponse("EVENT_RECEIVED", status=200)


def send_instagram_reply(recipient_id, message_text):
    url = f"https://graph.facebook.com/v19.0/me/messages"
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, params=params, headers=headers, json=data)
    return response.json()
