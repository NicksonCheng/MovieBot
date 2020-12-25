import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "startPage", "current", "coming", "famous", "romance",
            "comedy", "horror", "terror", "school", "fighting", "MovieDetail", "TVDetail", "comicDetail", "trailer", "final"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "startPage",
            "conditions": "is_going_to_startPage",
        },
        # --------------enter movie,TV or comic------------------
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "current",
            "conditions": "is_going_to_current",
        },
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "coming",
            "conditions": "is_going_to_coming",
        },
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "famous",
            "conditions": "is_going_to_famous",
        },
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "coming",
            "conditions": "is_going_to_coming",

        },
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "romance",
            "conditions": "is_going_to_famous",
        },
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "romance",
            "conditions": "is_going_to_romance",
        },
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "comedy",
            "conditions": "is_going_to_comedy",
        },
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "horror",
            "conditions": "is_going_to_horror",
        },
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "terror",
            "conditions": "is_going_to_terror",
        },
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "school",
            "conditions": "is_going_to_school",
        },
        {
            "trigger": "advance",
            "source": "startPage",
            "dest": "fighting",
            "conditions": "is_going_to_fighting",
        },


        # --------------------choose type--------------------
        {
            "trigger": "advance",
            "source": "current",
            "dest": "MovieDetail",
            "conditions": "is_going_to_MovieDetail",

        },
        {
            "trigger": "advance",
            "source": "coming",
            "dest": "MovieDetail",
            "conditions": "is_going_to_MovieDetail",

        },
        {
            "trigger": "advance",
            "source": "famous",
            "dest": "MovieDetail",
            "conditions": "is_going_to_MovieDetail",

        },
        {
            "trigger": "advance",
            "source": "romance",
            "dest": "TVDetail",
            "conditions": "is_going_to_TVDetail",

        },
        {
            "trigger": "advance",
            "source": "comedy",
            "dest": "TVDetail",
            "conditions": "is_going_to_TVDetail",

        },
        {
            "trigger": "advance",
            "source": "horror",
            "dest": "TVDetail",
            "conditions": "is_going_to_TVDetail",

        },
        {
            "trigger": "advance",
            "source": "terror",
            "dest": "comicDetail",
            "conditions": "is_going_to_comicDetail",

        },
        {
            "trigger": "advance",
            "source": "school",
            "dest": "comicDetail",
            "conditions": "is_going_to_comicDetail",

        },
        {
            "trigger": "advance",
            "source": "fighting",
            "dest": "comicDetail",
            "conditions": "is_going_to_comicDetail",

        },




        # ------------------------load more--------------------------
        {
            "trigger": "advance",
            "source": "MovieDetail",
            "dest": "current",
            "conditions": "is_going_to_current",

        },
        {
            "trigger": "advance",
            "source": "MovieDetail",
            "dest": "coming",
            "conditions": "is_going_to_coming",

        },
        {
            "trigger": "advance",
            "source": "MovieDetail",
            "dest": "famous",
            "conditions": "is_going_to_famous",

        },
        {
            "trigger": "advance",
            "source": "TVDetail",
            "dest": "romance",
            "conditions": "is_going_to_romance",

        },
        {
            "trigger": "advance",
            "source": "TVDetail",
            "dest": "comedy",
            "conditions": "is_going_to_comedy",

        },
        {
            "trigger": "advance",
            "source": "TVDetail",
            "dest": "horror",
            "conditions": "is_going_to_horror",

        },
        {
            "trigger": "advance",
            "source": "comicDetail",
            "dest": "terror",
            "conditions": "is_going_to_terror",

        },
        {
            "trigger": "advance",
            "source": "comicDetail",
            "dest": "school",
            "conditions": "is_going_to_school",

        },
        {
            "trigger": "advance",
            "source": "comicDetail",
            "dest": "fighting",
            "conditions": "is_going_to_fighting",

        },
        # ----------------------trailer------------------------------------
        {
            "trigger": "advance",
            "source": "MovieDetail",
            "dest": "trailer",
            "conditions": "is_going_to_trailer",

        },

        # ---------------go to finite state-------------------------------
        {
            "trigger": "advance",
            "source": "MovieDetail",
            "dest": "final",
            "conditions": "is_going_to_final",

        },
        {
            "trigger": "advance",
            "source": "TVDetail",
            "dest": "final",
            "conditions": "is_going_to_final",

        },
        {
            "trigger": "advance",
            "source": "comicDetail",
            "dest": "final",
            "conditions": "is_going_to_final",

        },
        {
            "trigger": "advance",
            "source": "trailer",
            "dest": "final",
            "conditions": "is_going_to_trailer",

        },

        {"trigger": "go_back", "source": ["final"], "dest": "startPage"},
        {"trigger": "go_back_detail", "source": [
            "trailer"], "dest": "MovieDetail"},

    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():

    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        print(f"\nFSM STATE: {machine.state}")
        #print(f"REQUEST BODY: \n{body}")
        if(event.type == "message"):
            if(event.message.text.lower() != "detail"):  # avoid to finite state
                response = machine.advance(event)
        else:
            response = machine.advance(event)
            print(response)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="localhost", port=port, debug=True)

# test
