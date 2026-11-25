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
inputFile = Path('../ok.json')
output = []
errorOutput = []
OsszetevokStr = ['összetevők', 'hozzávalók']
kategoriak = ['#']
alapanyagJsonba =[]
egysegek = ['g ', 'kg ', 'gramm ', 'evőkanál ', 'tk ', 'l ', 'ml ', 'csésze ', 'uncia ', 'db ', 'mk ', 'ek ', 'bögre ', 'dl ', 'teáskanál ']
isNotAlapanyag = ['ratkozz fel a csatornára', 'attints a csengőre', '#']
with open(str(inputFile), "r", encoding="utf-8") as f:
    data = json.load(f)
    for d in data:
        content = str(d['content'])
        bool = False
        for osszStr in OsszetevokStr :
            if re.search(osszStr, content.lower()) is not None:
                start = re.search(osszStr, content.lower())
                content = content[start.end():]
                alapanyagok = content.split('\n')
                alapanyagokTomb = []
                for alapanyag in alapanyagok:
                    pattern = re.compile(r"\d")
                    alapanyag = re.sub(pattern, '', alapanyag).strip().strip(".").strip(":").lower()
                    alapanyag = re.sub('/', '', alapanyag).strip().strip(".").strip(":")
                    alapanyag = re.sub('-', '', alapanyag).strip().strip(".").strip(":")

                    for egyseg in egysegek :
                        if re.match(egyseg, alapanyag) is not None :
                           end = re.match(egyseg, alapanyag)
                           alapanyag = alapanyag[end.end():].strip()
                    if alapanyag != '':
                        alapanyagokTomb.append(alapanyag)
                        if alapanyag not in alapanyagJsonba:
                            alapanyagJsonba.append(alapanyag)
                output.append({'title': d['title'], 'url': d['url'], 'alapanyagok': alapanyagokTomb, 'content' : d['content']})
                bool =True
                break
        if bool is False :
            errorOutput.append({'title': d['title'], 'url': d['url'], 'content' : d['content']})
    


outputFile = Path('../ok_1.json')
with outputFile.open("w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

errorOutputFile = Path('../no_ok_1.json')
with errorOutputFile.open("w", encoding="utf-8") as f:
    json.dump(errorOutput, f, ensure_ascii=False, indent=2)
alapanyagokFile = Path('../alapanyag.json')
with alapanyagokFile.open('w', encoding="utf-8") as f:
    json.dump(alapanyagJsonba, f, ensure_ascii=False, indent=2)
