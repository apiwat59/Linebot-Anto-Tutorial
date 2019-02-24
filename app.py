from flask import Flask, request
import antolib
from linebot import (
    LineBotApi, WebhookHandler,
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError,
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

line_bot_api = LineBotApi('NncLrzt2hAfj8NpyPP7DzQ9YS9IhGaH/ybNBFoEe3lrCq5Q+/dilnweOmLEpXOlMUcm/6l7r6vcE9DsvRus3tktCzArA9Qleo8xdSrIv3KmqRfIJzc3C4eyrWLFPAbGde1886PU2IzVdfXiH5wZOKwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7f04aa5a1efcc3f532f512ec9db25d07')

app = Flask(__name__)

# username of anto.io account
user = 'apiwatpanyoi'
# key of permission, generated on control panel anto.io
key = 'ZM1xFGrwpWxe3ty5AbCzVAytrowGCBaz28pH6t5c'
# your default thing.
thing = 'gasza1'

anto = antolib.Anto(user, key, thing)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if(message == 'ON1'):
        anto.pub('gasza1', 1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ON1SUCESS"))
    elif(message == 'OFF1'):
        anto.pub('gasza1', 0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="OFF1SUCESS"))
    elif(message == 'channel2 on'):
        anto.pub('myChannel2', 1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn On channel2"))
    elif(message == 'channel2 off'):
        anto.pub('myChannel2', 0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn Off channel2"))
    
if __name__ == "__main__":
    anto.mqtt.connect()
    app.run(debug=True)
