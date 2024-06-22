import os
import json
import openai
from dotenv import load_dotenv
import chainlit as cl

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello! How can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    response = await generate_response(message.content)
    await cl.Message(content=response).send()

async def generate_response(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message['content'].strip()

def handler(event, context):
    # Parse the incoming request
    data = json.loads(event['body'])
    message = cl.Message(content=data['message'])

    # Trigger the chatbot event
    if 'on_message' in cl._events:
        cl._events['on_message'](message)

    # Return a response
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Message received'})
    }
