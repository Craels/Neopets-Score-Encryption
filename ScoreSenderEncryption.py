import requests
import re
import os

class Encryption:
    def __init__(self):
        self.s = requests.session()
        self.enc = []
        self.keys = ''
        self.iv = None
        self.s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})

    def GrabSWF(self):
        resp = self.s.get('http://www.neopets.com/games/play_flash.phtml?va=&game_id=772&nc_referer=&age=0&hiscore=&sp=0&questionSet=&r=7582055&&width=580&height=580&quality=high&inpage=1')
        swfFile = self.getBetween(resp.text, 'include_movie\', \'', '.swf\');').replace('%2F', '/')
        resp = self.s.get('http://images.neopets.com/%s.swf' % swfFile)
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

    def getBetween(self, data, first, last):
        return data.split(first)[1].split(last)[0]
