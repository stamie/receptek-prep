from youtube import youtube
from nosalty import nosalty

class urlconsts:
    URLS = { 
        'youtube' : youtube.YOUTUBE_URL,
        'nosalty' : nosalty.NOSALTY_URL,
        }
    @staticmethod
    def check_urls(inputString):
        for name, url in urlconsts.URLS.items():
            if url in inputString:
                cls = globals()[name]
                url_ = cls.get_url(inputString)
                return {'url': url_, 'name': name}          
        return {}



eredmeny = urlconsts.check_urls('hello https://nosalty.hu/abcd" hahó')
print(eredmeny)  