import ownclasses as ownclasses
import json
import re
from pathlib import Path

class youtube:

    CONST = 'youtube'
    YOUTUBE_URL = 'https://youtu.be/'
    YOUTUBE_REGEXPS = {
        'start_json' : 'var ytInitialData = ',
        'end_json' : ';</script>'
    }

    @staticmethod
    def get_url( string_ ):
        url = ownclasses.urls.get_url( string_ + '"', youtube.YOUTUBE_URL, '"' )
        pos = url.find('?')
        if pos > 0:
            url = url[0: pos]
        url = re.sub('</a>' , '', url)
        url = re.sub('</div>' , '', url)
            
        return url

    @staticmethod
    def getHtml( url ):
        url_ = youtube.YOUTUBE_URL + youtube.get_url( url )
        fileName = ownclasses.urls.setHtmlFileName( url, youtube.CONST )
        ownclasses.urls.wget( url_, fileName )
        return fileName

    @staticmethod
    def getContent( fileName ):
        try :
            if ( re.search( 'json', fileName ) != None and re.search( 'youtube', fileName ) != None) :
                with open(fileName, "r", encoding="utf-8") as f:
                    datas = json.load(f)
                    getDatas = datas['contents']['twoColumnWatchNextResults']['results']['results']['contents']
                    if (getDatas != None):
                        for data_ in getDatas :
                            secondary_info = data_.get("videoSecondaryInfoRenderer")
                            if secondary_info is not None:
                                secondary_info = secondary_info.get("attributedDescription")
                                if secondary_info is not None:
                                    getData = secondary_info.get('content')
                                    return getData
            return 'valami'
        except :
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
        try :
            if ( re.search( 'json', fileName ) != None and re.search( 'youtube', fileName ) != None) :
                with open(fileName, "r", encoding="utf-8") as f:
                    datas = json.load(f)
                    getDatas = datas['contents']['twoColumnWatchNextResults']['results']['results']['contents']
                    if (getDatas != None):
                        for data_ in getDatas :
                            getData = data_['videoPrimaryInfoRenderer']['title']['runs']
                            if (getData != None):
                                for data in getData:
                                    if (data['text'] != None):
                                        f.close()
                                        return data['text']
        except:
            return 'hibás'

    
# Url = 'hello https://youtu.be/_KA3Jk1al6U?is=o9F_40ZLBN6YSfLT'
# UrlEredmeny = youtube.get_url( Url )
# print(UrlEredmeny + ' helloka url')
# fName = youtube.getHtml( UrlEredmeny )
# fJson = youtube.loadAndSaveJson( fName )
# title = youtube.getTitle(fJson)
# print(title)

#print(eredmeny)  # Kimenet: https://youtu.be/abcd
inputFile = Path('../input.json')
output = []
errorOutput = []
with open(str(inputFile), "r", encoding="utf-8") as f:
    data = json.load(f)
    for d in data:
        yFile = Path(re.sub('https://youtu.be/', '../jsons/youtube_', d['url']) + '.json')
        content = youtube.getContent (str(yFile))
        if content == 'valami' :
            errorOutput.append({'title': d['title'], 'url': d['url']})
        else :
            output.append({'title': d['title'], 'url': d['url'], 'content' : content})
outputFile = Path('../ok.json')
with outputFile.open("w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

errorOutputFile = Path('../no_ok.json')
with errorOutputFile.open("w", encoding="utf-8") as f:
    json.dump(errorOutput, f, ensure_ascii=False, indent=2)


