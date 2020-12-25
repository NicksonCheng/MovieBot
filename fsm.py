from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_carousel, send_button_message, send_video_message, crawlMovie, crawlTV, crawlComic


class Movie:
    def __init__(self):
        self.detail_from_trailer = False

    def setUrl(self, url):
        self.url = url

    def setIdx(self, idx):
        self.idx = idx

    def setEvent(self, event):
        self.event = event

    def getUrl(self):
        return self.url

    def getIdx(self):
        return self.idx

    def getEvent(self):
        return self.event

    def change_detail_from(self, flag):
        self.detail_from_trailer = flag


class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):

        self.machine = GraphMachine(model=self, **machine_configs)
        self.current_counter = 0
        self.coming_counter = 1
        self.horror_counter = 3
        self.romance_counter = 3
        self.comedy_counter = 3
        self.fight_counter = 3
        self.school_counter = 3
        self.terror_counter = 3
        self.movie = Movie()

    def is_going_to_startPage(self, event):
        return True

    def is_going_to_current(self, event):

        text = event.message.text
        return text.lower() == "current" or text.lower() == "load more current"

    def is_going_to_coming(self, event):

        text = event.message.text
        return text.lower() == "coming" or text.lower() == "load more coming"

    def is_going_to_famous(self, event):

        text = event.message.text
        return text.lower() == "famous" or text.lower() == "load more famous"

    def is_going_to_comedy(self, event):
        text = event.message.text
        return text.lower() == "coming" or text.lower() == "load more coming"

    def is_going_to_horror(self, event):
        text = event.message.text
        return text.lower() == "horror" or text.lower() == "load more horror"

    def is_going_to_romance(self, event):
        text = event.message.text
        return text.lower() == "romance" or text.lower() == "load more romance"

    def is_going_to_comedy(self, event):
        text = event.message.text
        return text.lower() == "comedy" or text.lower() == "load more comedy"

    def is_going_to_horror(self, event):
        text = event.message.text
        return text.lower() == "horror" or text.lower() == "load more horror"

    def is_going_to_terror(self, event):
        text = event.message.text
        return text.lower() == "terror" or text.lower() == "load more terror"

    def is_going_to_school(self, event):
        text = event.message.text
        return text.lower() == "school" or text.lower() == "load more school"

    def is_going_to_fighting(self, event):
        text = event.message.text
        return text.lower() == "fighting" or text.lower() == "load more fighting"

    def is_going_to_MovieDetail(self, event):
        infor = event.postback.data

        text = infor.split(',')[0]
        return text.lower() == "detail"

    def is_going_to_TVDetail(self, event):
        infor = event.postback.data
        text = infor.split(',')[0]
        return text.lower() == "detail"

    def is_going_to_comicDetail(self, event):
        infor = event.postback.data
        text = infor.split('@')[0]
        return text.lower() == "detail"

    def is_going_to_trailer(self, event):
        text = event.message.text
        return text.lower() == "trailer"

    def is_going_to_final(self, event):
        return True

    def on_enter_startPage(self, event):
        userId = event.source.user_id
        send_button_carousel(userId)

    def on_enter_current(self, event):
        self.current_counter += 3
        self.movie.change_detail_from(False)
        userId = event.source.user_id
        reply_token = event.reply_token
        url = "https://www.vscinemas.com.tw/vsweb/film/index.aspx"
        # self.movie.setUrl(url)
        crawlMovie(userId, reply_token, url, self.current_counter,
                   "更多新片", "load more current")

    def on_enter_coming(self, event):
        self.coming_counter += 3
        self.movie.change_detail_from(False)
        userId = event.source.user_id
        reply_token = event.reply_token
        url = "https://www.vscinemas.com.tw/vsweb/film/coming.aspx"
        # self.movie.setUrl(url)
        crawlMovie(userId, reply_token, url, self.coming_counter,
                   "更多即將上映", "load more coming")

    def on_enter_famous(self, event):
        self.movie.change_detail_from(False)
        userId = event.source.user_id
        reply_token = event.reply_token
        url = "https://www.vscinemas.com.tw/vsweb/film/hot.aspx"
        # self.movie.setUrl(url)
        crawlMovie(userId, reply_token, url, 3,
                   "no more", "load more famous")

    def on_enter_romance(self, event):
        userId = event.source.user_id
        reply_token = event.reply_token
        url = 'https://www.movieffm.net/tvshows/?genres=romance&region&dtyear&cats&orderby'
        crawlTV(userId, reply_token, url, self.romance_counter,
                "更多愛情片", "load more romance")
        self.romance_counter += 3

    def on_enter_comedy(self, event):
        userId = event.source.user_id
        reply_token = event.reply_token
        url = 'https://www.movieffm.net/tvshows/?genres=comedy&region&dtyear&cats&orderby'
        crawlTV(userId, reply_token, url, self.comedy_counter,
                "更多喜劇片", "load more comedy")
        self.comedy_counter += 3

    def on_enter_horror(self, event):
        userId = event.source.user_id
        reply_token = event.reply_token
        url = 'https://www.movieffm.net/tvshows/?genres=horror&region&dtyear&cats&orderby'
        crawlTV(userId, reply_token, url, self.horror_counter,
                "更多恐怖片", "load more horror")
        self.horror_counter += 3

    def on_enter_terror(self, event):
        userId = event.source.user_id
        reply_token = event.reply_token
        url = 'https://www.mh5.tw/allcartoonlist?page=1&order=0&sort_type=2&class_id=15&ut_id=&area_id=3&status=all'
        crawlComic(userId, reply_token, url,
                   self.terror_counter, "更多恐怖漫畫", "load more terror")
        self.terror_counter += 3

    def on_enter_school(self, event):
        userId = event.source.user_id
        reply_token = event.reply_token
        url = 'https://www.mh5.tw/allcartoonlist?page=1&order=0&sort_type=2&class_id=3&ut_id=&area_id=3&status=all'
        crawlComic(userId, reply_token, url,
                   self.school_counter, "更多校園漫畫", "load more school")
        self.school_counter += 3

    def on_enter_fighting(self, event):
        userId = event.source.user_id
        reply_token = event.reply_token
        url = 'https://www.mh5.tw/allcartoonlist?page=1&order=0&sort_type=2&class_id=1&ut_id=&area_id=all&status=all'
        crawlComic(userId, reply_token, url,
                   self.fight_counter, "更多格鬥漫畫", "load more fighting")
        self.fight_counter += 3

    def on_enter_MovieDetail(self, event):
        print(event.reply_token)
        text = event.postback.data
        infor = event.postback.data.split(',')
        infor.pop(0)
        reply_token = event.reply_token
        userId = event.source.user_id
        self.movie.setIdx(infor[4])
        self.movie.setEvent(event)
        if(self.movie.detail_from_trailer == False):
            send_text_message(reply_token, infor, "Movie")
        send_button_message(userId, "Movie")

    def on_enter_TVDetail(self, event):
        text = event.postback.data
        infor = event.postback.data.split(',')
        infor.pop(0)
        reply_token = event.reply_token
        userId = event.source.user_id
        send_text_message(reply_token, infor, "TV")
        send_button_message(userId, "TV")

    def on_enter_comicDetail(self, event):
        text = event.postback.data
        infor = event.postback.data.split('@')

        infor.pop(0)
        reply_token = event.reply_token
        userId = event.source.user_id
        send_text_message(reply_token, infor, "comic")
        send_button_message(userId, "comic")

    def on_enter_trailer(self, event):
        reply_token = event.reply_token
        send_video_message(reply_token, self.movie.getIdx())
        self.movie.change_detail_from(True)
        self.go_back_detail(self.movie.getEvent())

    def on_enter_final(self, event):
        self.current_counter = 0
        self.coming_counter = 1
        self.horror_counter = 3
        self.romance_counter = 3
        self.comedy_counter = 3
        self.fight_counter = 3
        self.school_counter = 3
        self.terror_counter = 3
        self.go_back(event)
