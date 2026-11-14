import ownclasses as ownclasses
import re

class youtube:

    CONST = 'youtube'
    YOUTUBE_URL = 'https://youtu.be/'
    YOUTUBE_REGEXPS = {
        'title' : "videoTitle",
        'content' : { "attributedDescription" : "content" }
    }

    @staticmethod
    def get_url( string_ ):
        url = ownclasses.urls.get_url( string_, youtube.YOUTUBE_URL, '"' )
        return url

    @staticmethod
    def getHtml( url ):
        url_ = youtube.YOUTUBE_URL + youtube.get_url( url )
        fileName = ownclasses.urls.setHtmlFileName( url, youtube.CONST )
        print(fileName + ' hello1')
        ownclasses.urls.wget( url_, fileName )
        return fileName

    @staticmethod
    def getContent( fileName ):
        str = ownclasses.loadedPage.getContentText( fileName )
        key_ = list(youtube.YOUTUBE_REGEXPS['content'].keys())[0]
        ls = re.findall(key_, str)
        print(ls)
        return 'valami'

    @staticmethod
    def getTitle( fileName ):
        return 'valami'
    
Url = 'https://youtu.be/rA-wrhhiyAA'
UrlEredmeny = youtube.get_url( Url )
print(UrlEredmeny + ' helloka url')
youtube.getHtml( UrlEredmeny )

#print(eredmeny)  # Kimenet: https://youtu.be/abcd