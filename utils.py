import os
import sys
import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, CarouselTemplate, TemplateSendMessage, CarouselColumn, MessageTemplateAction, ImageCarouselColumn


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_button_carousel(userId):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/18528023_10154290831916403_4058721277470459196_n.jpg?_nc_cat=110&ccb=2&_nc_sid=09cbfe&_nc_ohc=eILRNJk5cnwAX-hDsiM&_nc_ht=scontent-tpe1-1.xx&oh=049993d54a93ba1e5a470858cef73b33&oe=600831CF',
                    title='Movie Menu',
                    text='Which movie would you like to watch?',
                    actions=[
                         MessageTemplateAction(
                             label='romance',
                             text='romance'

                         ),
                        MessageTemplateAction(
                             label='comedy',
                             text='comedy'

                         ),
                        MessageTemplateAction(
                             label='horror',
                             text='horror'
                         )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://p2.bahamut.com.tw/B/2KU/52/05bb4c851970ab2e9942f32c0118ff85.JPG?w=1000',
                    title='Movie Menu',
                    text='Which movie would you like to watch?',
                    actions=[
                         MessageTemplateAction(
                             label='romance',
                             text='romance'

                         ),
                        MessageTemplateAction(
                             label='comedy',
                             text='comedy'

                         ),
                        MessageTemplateAction(
                             label='horror',
                             text='horror'
                         )
                    ]
                ),

            ]
        )
    )
    line_bot_api.push_message(userId, message)
    return "OK"


def send_image_carousel(names, images):
    line_bot_api = LineBotApi(access_token)
    cols = []
    for i, url in enumerate(images):
        cols.append(
            ImageCarouselColumn(
                image_url=url,
                action=MessageTemplateAction(
                    label=names[i],
                    text=names[i]
                )
            )
        )
    message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(columns=cols)
    )
    line_bot_api.push_message(id, message)
    return "OK"


def crawlHorrorMovie():
    url = 'https://www.movieffm.net/movies/?genres=horror&region&dtyear&cats&orderby=view'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.find(id='archive-content').find_all("article", limit=3)
    images = []
    names = []
    outline = []
    for movie in movies:
        img = movie.find("img").get('src')
        name = movie.find("div", "title").text
        print(f"{name}\n")
        names.append(name)
        images.append(img)
    send_image_carousel(names, images)


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
