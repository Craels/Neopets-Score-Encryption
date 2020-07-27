import requests
import re
import os

class Encryption:
    def __init__(self):
        self.s = requests.session()
        self.enc = []
        self.keys = ''
        self.iv = None
        self.s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'})

    def GrabSWF(self):
        resp = self.s.get('http://www.neopets.com/games/play_flash.phtml?va=&game_id=/games/play_flash.phtml?va=&game_id=500&nc_referer=&age=0&hiscore=0&sp=1&questionSet=&r=3066612&&width=500&height=500&quality=high&inpage=1')
        resp = self.s.get('http://images.neopets.com/games/gaming_system/np8_include_v29.swf')
        with open('enc.swf', 'wb') as f:
            f.write(resp.content)
        os.system('flare enc.swf')

    def parseEnc(self):
        with open('enc.flr', 'r') as f:
            out = f.read()
            for data in re.findall(r'this.aDecimals.push\(\[(.*?)\]\);', out):
                for x in data.split(','):
                    self.enc.append(x)
        for data in self.enc:
            self.keys += chr(int(data))
        iv = re.findall(r'__get__iVID = function \(\) {\n(.*?);', out)
        self.iv = iv[0].replace('return', '').strip()

    def cleanUp(self):
        if os.path.exists('enc.swf'):
            os.remove('enc.swf')
        if os.path.exists('enc.flr'):
            os.remove('enc.flr')
