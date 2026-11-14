import re
import urllib.request

class urls:
    @staticmethod
    def get_url( string_, URL, END_STRING ):
        found = re.search( URL, string_ )
        if ( found != None ):
            end_string_ = string_[found.end():]
            print(end_string_ + ' hello2')
            found2 = re.search( END_STRING, end_string_ )
            if ( found2 != None ):            
                return end_string_[: found2.start()]
            return end_string_
        return string_
    def wget( url, mentesi_hely ):
        urllib.request.urlretrieve(url, mentesi_hely)
        print("Sikeres letöltés az urllib-pel!")
    def setHtmlFileName( URL, CONST ):
        fileName = './htmls/' + CONST + '_' + URL + '.html'
        # fileName = re.sub( '.html.html', fileName )
        return fileName

class loadedPage:
    @staticmethod
    def getContentText( fileName ):
        with open(fileName, "r") as file_:
            ret = ''
            for row in file_:
                ret += ' ' + row.strip()
            return ret

        return ''

    
    

                
   


