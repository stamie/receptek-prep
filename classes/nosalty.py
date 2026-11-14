import ownclasses as ownclasses
class nosalty:
    
    NOSALTY_URL = 'https://nosalty.hu'

    @staticmethod
    def get_url( string_ ):
        url = ownclasses.urls.get_url( string_, nosalty.NOSALTY_URL, '"' )
        return url

#eredmeny = nosalty.get_url('https://nosalty.hu/abcd"')
#print(eredmeny)  # Kimenet: https://youtu.be/abcd

    