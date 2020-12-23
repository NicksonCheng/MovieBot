from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_carousel, crawlHorrorMovie


class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_startPage(self, event):
        text = event.message.text
        return True

    def is_going_to_romance(self, event):
        text = event.message.text
        return text.lower() == "romance"

    def is_going_to_comedy(self, event):
        text = event.message.text
        return text.lower() == "comedy"

    def is_going_to_horror(self, event):
        text = event.message.text
        return text.lower() == "horror"

    def on_enter_startPage(self, event):
        userId = event.source.user_id

        send_button_carousel(userId)

    def on_enter_romance(self, event):
        print("I'm entering romance")
        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger romance")
        self.go_back()

    def on_enter_comedy(self, event):
        print("I'm entering comedy")
        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger comedy")
        self.go_back()

    def on_enter_horror(self, event):
        print("I'm entering horror")
        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger horror")
        crawlHorrorMovie()
        self.go_back()

    def on_exit_romance(self):
        print("Leaving romance")

    def on_exit_comedy(self):
        print("Leaving comedy")

    def on_exit_horror(self):
        print("Leaving horror")
