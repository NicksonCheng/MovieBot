import os
import sys
import shutil
import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, PostbackEvent, TextMessage, VideoMessage, TextSendMessage, VideoSendMessage, PostbackAction, CarouselTemplate, ButtonsTemplate, TemplateSendMessage, TemplateAction, CarouselColumn, ButtonComponent, MessageTemplateAction, ImageCarouselColumn, PostbackTemplateAction, ImageCarouselTemplate
from pytube import YouTube

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
watch_more_type = ""
watch_more_text = ""
all_movie_infor = []
all_video_url = []
video_counter = 0


class MovieInfor:
    def __init__(self, name, image, date, outline, link, video, index):
        self.name = name
        self.image = image
        self.outline = outline
        self.date = date
        self.link = link
        self.idx = index
        self.video = video


class TVInfor:
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
        if(watch_type == "Movie"):
            string = "電影:"+text[0]+"\n"+text[1] + \
                "\n"+text[2] + '\n' + "連結:"+text[3]+"\n"
        elif(watch_type == "TV"):
            string = "電視劇::"+text[0]+"\n"+"介紹:"+text[1] + \
                "\n"+"評分:"+text[2]+"\n"+"連結:"+text[3]+"\n"
        elif(watch_type == "comic"):
            string = "漫畫:"+text[0]+"\n"+"介紹:"+text[1] + \
                "\n"+"人氣:"+text[2]+"\n"+"作者:"+text[3]+"\n"+"連結:"+text[4]+"\n"

    else:
        string = text
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=string))

    return "OK"


def downloadYoutube(url):
    global video_counter
    yt = YouTube(url)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first()
    if(not os.path.isdir("static")):
        os.makedirs("static")
    yt.download("static")
    videos = os.listdir("static")
    old_path = "static/"+videos[0]
    # print(old_path)
    new_path = "static/video"+str(len(all_video_url))+".mp4"

    try:
        os.rename(old_path, new_path)
    except Exception as e:
        # print("error")


def send_video_message(reply_token, movie_idx):
    global all_movie_infor
    global all_video_url
    video_url = all_movie_infor[int(movie_idx)].video
    if(video_url not in all_video_url):
        all_video_url.append(video_url)
        downloadYoutube(video_url)
    line_bot_api = LineBotApi(channel_access_token)
    message = VideoSendMessage(
        original_content_url="https://4f0651d08caa.ngrok.io/video" +
        str(len(all_video_url))+".mp4",
        preview_image_url=all_movie_infor[int(movie_idx)].image,

    )

    line_bot_api.reply_message(reply_token, message)


def send_button_message(userId, watch_type):
    global watch_more_type
    global watch_more_text
    view_text = ""
    view_img = ""
    act = []
    if(watch_type == "TV"):
        view_text = "get more TV?"
        view_img = "https://travel.ulifestyle.com.hk/cms/news_photo/1024x576/20200421184008__31112860324_47f1e039ef_b.jpg"
        acts = [MessageTemplateAction(label="回到主頁面", text="back"), MessageTemplateAction(
            label=watch_more_type, text=watch_more_text)]
    elif(watch_type == "Movie"):

        view_text = "get more Movie?"
        view_img = "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/18528023_10154290831916403_4058721277470459196_n.jpg?_nc_cat=110&ccb=2&_nc_sid=09cbfe&_nc_ohc=eILRNJk5cnwAX-hDsiM&_nc_ht=scontent-tpe1-1.xx&oh=049993d54a93ba1e5a470858cef73b33&oe=600831CF"
        acts = [MessageTemplateAction(label="回到主頁面", text="back"), MessageTemplateAction(
            label=watch_more_type, text=watch_more_text), MessageTemplateAction(
            label="收看預告", text="trailer")]
        if(watch_more_type == "no more"):
            del acts[1]
    else:
        view_text = "get more comic?"
        view_img = "https://p2.bahamut.com.tw/B/2KU/52/05bb4c851970ab2e9942f32c0118ff85.JPG?w=1000"
        acts = [MessageTemplateAction(label="回到主頁面", text="back"), MessageTemplateAction(
            label=watch_more_type, text=watch_more_text)]

    line_bot_api = LineBotApi(channel_access_token)

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
                    title='電影系列',
                    text='選擇你想要了解的電影',
                    actions=[
                         MessageTemplateAction(
                             label='熱售中',
                             text='current'

                         ),
                        MessageTemplateAction(
                             label='即將上映',
                             text='coming'

                         ),
                        MessageTemplateAction(
                             label='哈燒榜',
                             text='famous'
                         )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://travel.ulifestyle.com.hk/cms/news_photo/1024x576/20200421184008__31112860324_47f1e039ef_b.jpg',
                    title='電視劇系列',
                    text='選擇你想要追的電視劇?',
                    actions=[
                         MessageTemplateAction(
                             label='浪漫系列',
                             text='romance'

                         ),
                        MessageTemplateAction(
                             label='喜劇系列',
                             text='comedy'

                         ),
                        MessageTemplateAction(
                             label='恐怖系列',
                             text='horror'
                         )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://p2.bahamut.com.tw/B/2KU/52/05bb4c851970ab2e9942f32c0118ff85.JPG?w=1000',
                    title='動漫系列',
                    text='選擇你想看的漫畫?',
                    actions=[
                         MessageTemplateAction(
                             label='恐怖類型',
                             text='terror'

                         ),
                        MessageTemplateAction(
                             label='校園類型',
                             text='school'

                         ),
                        MessageTemplateAction(
                             label='格鬥類型',
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

        if(watch_type == "Movie"):
            data = "detail,"+infor.name+","+infor.date+"," + \
                infor.outline+","+infor.link+","+str(infor.idx)
            # print(data)
        elif(watch_type == "TV"):
            data = "detail,"+infor.name+","+infor.outline+","+infor.star+","+infor.link
        else:
            data = "detail@ "+infor.name+"@" + infor.outline+"@" + infor.popularity + \
                "@" + infor.author+"@"+infor.link
            # print(data)

        cols.append(
            ImageCarouselColumn(
                image_url=infor.image,
                action=PostbackTemplateAction(
                    label=infor.name[:10],
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


def crawlMovie(userId, reply_token, m_url, counter, m_type, m_text):

    send_text_message(reply_token, "系統處理中,請稍後~~", "general")
    global watch_more_type
    global watch_more_text
    watch_more_type = m_type
    watch_more_text = m_text
    basic_url = "https://www.vscinemas.com.tw/vsweb/"
    url = m_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = ""
    page_from = ""
    if(m_text == "load more famous"):
        page_from = "hot.aspx"
        movies = soup.find("ul", class_="hotList").find_all(
            "li", limit=counter)
    elif(m_text == "load more current"):
        page_from = "index.aspx"
        movies = soup.find("ul", class_="movieList").find_all(
            "li", limit=counter)
    else:
        page_from = "coming.aspx"
        movies = soup.find("ul", class_="movieList").find_all(
            "li", limit=counter)
    global all_movie_infor
    all_movie_infor = []
    for i in range(counter-3, counter, 1):
        # print(page_from)
        inn_url = url.replace(page_from, "") + \
            movies[i].find("figure").find("a").get('href')
        # print(inn_url)
        response = requests.get(inn_url)
        soup = BeautifulSoup(response.text, "html.parser")
        movie = soup.find("div", class_="movieMain")
        image = movie.find("img").get('src')[2:]
        image = basic_url+image
        name = movie.find("div", class_="titleArea").find("h1").text

        date = movie.find("div", class_="titleArea").find("time").text
        td = movie.find("div", class_="infoArea").find_all("td")
        outline = td[0].text+td[1].find("p").text+'\n'+td[2].text+td[3].find(
            "p").text+'\n'+td[4].text+td[5].text+"\n"+td[6].text+td[7].text+"\n"
        index = i-(counter-3)
        video = ""
        try:
            video = soup.find("iframe").get('src')
        except:
            video = "https://www.youtube.com/embed/-RAdHJ-aquE"

        # print(image)
        # print(name)
        # print(date)
        # print(outline)
        # print(video)
        all_movie_infor.append(MovieInfor(
            name, image, date, outline, inn_url, video, index))

    # print(all_movie_infor)
    send_image_carousel(all_movie_infor, userId, "Movie")


def crawlTV(userId, reply_token, TV_url, counter, m_type, m_text):
    send_text_message(reply_token, "系統處理中,請稍後~", "general")
    global watch_more_type
    global watch_more_text
    watch_more_type = m_type
    watch_more_text = m_text

    url = TV_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    TVs = soup.find(id='archive-content').find_all("article", limit=counter)
    all_infor = []
    for i in range(counter-3, counter, 1):
        image = TVs[i].find("img").get('src')
        name = TVs[i].find("div", "title").text
        if(name.find('：') != -1):
            name = name.split('：')[0]
        elif(name.find('/') != -1):
            name = name.split('/')[0]
        outline = TVs[i].find("div", "texto").text
        star = TVs[i].find("div", "rating").text
        link = TVs[i].find("a").get('href')
        # # print(f"type={star}\nimage={type(star)}")
        all_infor.append(TVInfor(name, image, outline, star, link))

    send_image_carousel(all_infor, userId, "TV")


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
        # print(name)

    send_image_carousel(all_infor, userId, "comic")


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
