from bs4 import BeautifulSoup as BS


class parser:
    def loader(self):
        code = ''
        with open('images.html', 'r') as pic:
            for i in pic.read():
                code = code + i
        return code

    def finder(self, code):
        content = BS(code, 'lxml')
        return [image['src'] for image in content.findAll('img')]

    def run(self, bot, message):
        code = self.loader()
        links = self.finder(code)
        for link in links[:3]:
            bot.send_photo(message.chat.id, link)
