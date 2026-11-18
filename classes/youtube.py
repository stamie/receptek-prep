import ownclasses as ownclasses
import json
import re

class youtube:

    CONST = 'youtube'
    YOUTUBE_URL = 'https://youtu.be/'
    YOUTUBE_REGEXPS = {
        'start_json' : 'var ytInitialData = ',
        'end_json' : ';</script>'
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
    def loadAndSaveJson( fileName ):
        ret = False
        if ( re.search( 'html', fileName ) != None ) :
            fileName_ = re.sub( 'html', 'json', fileName )
            with open(fileName, "r", encoding="utf-8") as f:
                for row in f:
                    begin = re.search(youtube.YOUTUBE_REGEXPS['start_json'], row)
                    if (begin != None):
                        strToFile = row[begin.end():]
                        end = re.search(youtube.YOUTUBE_REGEXPS['end_json'], strToFile)
                        if (end != None):
                            strToFile = strToFile[0:end.start()]
                            with open(fileName_, "w") as f_:
                                f_.writelines(strToFile)
                                f_.close()
                                ret = fileName_
            f.close()
            return ret
        return None

    @staticmethod
    def getTitle( fileName ):
        if ( re.search( 'json', fileName ) != None and re.search( 'youtube', fileName ) != None) :
            with open(fileName, "r", encoding="utf-8") as f:
                datas = json.load(f)
                getDatas = datas['contents']['twoColumnWatchNextResults']['results']['results']['contents']
                if (getDatas != None):
                    print ('bejött')
                    for data_ in getDatas :
                        getData = data_['videoPrimaryInfoRenderer']['title']['runs']
                        if (getData != None):
                            for data in getData:
                                if (data['text'] != None):
                                    f.close()
                                    return data['text']
        return 'hibás'

    
Url = 'https://youtu.be/rA-wrhhiyAA'
UrlEredmeny = youtube.get_url( Url )
print(UrlEredmeny + ' helloka url')
fName = youtube.getHtml( UrlEredmeny )
fJson = youtube.loadAndSaveJson( fName )
title = youtube.getTitle(fJson)
print(title)

#print(eredmeny)  # Kimenet: https://youtu.be/abcd