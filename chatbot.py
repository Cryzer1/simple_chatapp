from chainlit import Chainlit

app = Chainlit()

@app.on_message
async def on_message(message):
    response = f"You said: {message.content}"
    await message.reply(response)

if __name__ == "__main__":
    app.run()
