from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_carousel, send_button_message, crawlMovie, crawlComic


class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.horror_counter = 3
        self.romance_counter = 3
        self.comedy_counter = 3
        self.fight_counter = 3
        self.school_counter = 3
        self.terror_counter = 3

    def is_going_to_startPage(self, event):
        return True

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

    def is_going_to_movieDetail(self, event):
        infor = event.postback.data
        text = infor.split(',')[0]
        return text.lower() == "detail"

    def is_going_to_comicDetail(self, event):
        infor = event.postback.data
        text = infor.split('@')[0]
        return text.lower() == "detail"

    def is_going_to_final(self, event):
        return True

    def on_enter_startPage(self, event):
        userId = event.source.user_id
        send_button_carousel(userId)

    def on_enter_romance(self, event):
        userId = event.source.user_id
        reply_token = event.reply_token
        url = 'https://www.movieffm.net/movies/?genres=romance&region&dtyear&cats&orderby=view'
        crawlMovie(userId, reply_token, url, self.romance_counter,
                   "更多愛情片", "load more romance")
        self.romance_counter += 3

    def on_enter_comedy(self, event):
        userId = event.source.user_id
        reply_token = event.reply_token
        url = 'https://www.movieffm.net/movies/?genres=comedy&region&dtyear&cats&orderby=view'
        crawlMovie(userId, reply_token, url, self.comedy_counter,
                   "更多喜劇片", "load more comedy")
        self.comedy_counter += 3

    def on_enter_horror(self, event):
        userId = event.source.user_id
        reply_token = event.reply_token
        url = 'https://www.movieffm.net/movies/?genres=horror&region&dtyear&cats&orderby=view'
        crawlMovie(userId, reply_token, url, self.horror_counter,
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

    def on_enter_movieDetail(self, event):
        text = event.postback.data
        infor = event.postback.data.split(',')
        infor.pop(0)
        reply_token = event.reply_token
        userId = event.source.user_id
        send_text_message(reply_token, infor, "movie")
        send_button_message(userId, "movie")

    def on_enter_comicDetail(self, event):
        text = event.postback.data
        infor = event.postback.data.split('@')

        infor.pop(0)
        reply_token = event.reply_token
        userId = event.source.user_id
        send_text_message(reply_token, infor, "comic")
        send_button_message(userId, "comic")

    def on_enter_final(self, event):
        self.horror_counter = 3
        self.romance_counter = 3
        self.comedy_counter = 3
        self.fight_counter = 3
        self.school_counter = 3
        self.terror_counter = 3
        self.go_back(event)
