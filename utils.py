import os
import sys
import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, PostbackAction, CarouselTemplate, ButtonsTemplate, TemplateSendMessage, TemplateAction, CarouselColumn, ButtonComponent, MessageTemplateAction, ImageCarouselColumn, PostbackTemplateAction, ImageCarouselTemplate


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
watch_more_type = ""
watch_more_text = ""


class MovieInfor:
    def __init__(self, name, image, outline, star, link):
        self.name = name
        self.image = image
        self.outline = outline
        self.star = star
        self.link = link


class ComicInfor:
    def __init__(self, name, outline, popularity, image, author, link):
        self.name = name
        self.outline = outline
        self.popularity = popularity
        self.image = image
        self.author = author
        self.link = link


def send_text_message(reply_token, text, watch_type):
    string = ""
    if(type(text) == list):
        if(watch_type == "movie"):
            string = "電影:"+text[0]+"\n"+"介紹:"+text[1] + \
                "\n"+"評分:"+text[2]+"\n"+"連結:"+text[3]+"\n"
        elif(watch_type == "comic"):
            string = "漫畫:"+text[0]+"\n"+"介紹:"+text[1] + \
                "\n"+"人氣:"+text[2]+"\n"+"作者:"+text[3]+"\n"+"連結:"+text[4]+"\n"

    else:
        string = text
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=string))

    return "OK"


def send_button_message(userId, watch_type):
    global watch_more_type
    global watch_more_text
    view_text = ""
    view_img = ""
    if(watch_type == "movie"):
        view_text = "get more movie?"
        view_img = "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/18528023_10154290831916403_4058721277470459196_n.jpg?_nc_cat=110&ccb=2&_nc_sid=09cbfe&_nc_ohc=eILRNJk5cnwAX-hDsiM&_nc_ht=scontent-tpe1-1.xx&oh=049993d54a93ba1e5a470858cef73b33&oe=600831CF"
    else:
        view_text = "get more comic?"
        view_img = "https://p2.bahamut.com.tw/B/2KU/52/05bb4c851970ab2e9942f32c0118ff85.JPG?w=1000"
    line_bot_api = LineBotApi(channel_access_token)
    acts = [MessageTemplateAction(label="回到主頁面", text="back"), MessageTemplateAction(
        label=watch_more_type, text=watch_more_text)]

    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url=view_img,
            title="Watch More",
            text=view_text,
            actions=acts
        )
    )
    line_bot_api.push_message(userId, message)
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
                    title='Comic Menu',
                    text='Which comic would you like to watch?',
                    actions=[
                         MessageTemplateAction(
                             label='terror',
                             text='terror'

                         ),
                        MessageTemplateAction(
                             label='school',
                             text='school'

                         ),
                        MessageTemplateAction(
                             label='fighting',
                             text='fighting'
                         )
                    ]
                ),

            ]
        )
    )
    line_bot_api.push_message(userId, message)
    return "OK"


def send_image_carousel(all_infor, id, watch_type):

    line_bot_api = LineBotApi(channel_access_token)
    cols = []
    for infor in all_infor:
        data = ""
        if(watch_type == "movie"):
            data = "detail,"+infor.name+","+infor.outline+","+infor.star+","+infor.link
        else:
            data = "detail@ "+infor.name+"@" + infor.outline+"@" + infor.popularity + \
                "@" + infor.author+"@"+infor.link
            print(data)

        cols.append(
            ImageCarouselColumn(
                image_url=infor.image,
                action=PostbackTemplateAction(
                    label=infor.name,
                    data=data,
                    text="detail"
                )
            )
        )

    message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(columns=cols)
    )
    line_bot_api.push_message(id, message)
    return "OK"


def crawlMovie(userId, reply_token, movie_url, counter, m_type, m_text):
    send_text_message(reply_token, "系統處理中,請稍後~", "general")
    global watch_more_type
    global watch_more_text
    watch_more_type = m_type
    watch_more_text = m_text

    url = movie_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.find(id='archive-content').find_all("article", limit=counter)
    all_infor = []
    for i in range(counter-3, counter, 1):
        image = movies[i].find("img").get('src')
        name = movies[i].find("div", "title").text
        if(name.find('：') != -1):
            name = name.split('：')[0]
        elif(name.find('/') != -1):
            name = name.split('/')[0]
        outline = movies[i].find("div", "texto").text
        star = movies[i].find("div", "rating").text
        link = movies[i].find("a").get('href')
        # print(f"type={star}\nimage={type(star)}")
        all_infor.append(MovieInfor(name, image, outline, star, link))

    send_image_carousel(all_infor, userId, "movie")


def crawlComic(userId, reply_token, comic_url, counter, c_type, c_text):
    send_text_message(reply_token, "系統處理中,請稍後~", "general")
    global watch_more_type
    global watch_more_text
    watch_more_type = c_type
    watch_more_text = c_text
    url = comic_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    comics = soup.find("dl", class_="alllist").find_all("dt", limit=counter)
    all_infor = []

    for i in range(counter-3, counter, 1):
        inner_url = "https://www.mh5.tw" + \
            comics[i].find("div", class_="ti").find("a").get('href')
        response = requests.get(inner_url)
        soup = BeautifulSoup(response.text, "html.parser")
        comic = soup.find(id='setnmh-bookms')
        image = comic.find('img').get("src")
        name = comic.find("h1", class_="bookname").text
        name = name.replace('～', '')
        outline = comic.find("div", class_="ms").text
        if(len(outline) > 20):
            outline = outline[:20]
            outline = outline.replace('～', '')
            outline += "....."
        popularity = comic.find("div", class_="renqi").find("span").text
        author = comics[i].find("div", class_="who").find("a").text
        all_infor.append(ComicInfor(
            name, outline, popularity, image, author, inner_url))
        print(name)

    send_image_carousel(all_infor, userId, "comic")


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
