from instagram.client import InstagramAPI
import amadeus
from amadeus import Flights


access_token = "569470452.360cc24.08adf989f9f147afa7d72c181d53b7a9"
client_id = "360cc24cb8534f7cbbfb06d7ee1e26a3"
client_secret = "4e1026ba847841eab8797101ceb9680a"
LOCATIONS = []

api = InstagramAPI(access_token=access_token, client_secret=client_secret)
amadeus_api_key = 'RzGfJPsCmYIRlDmTi6Og2BAYAVviEAdh'
flights = Flights(amadeus_api_key)

def getUserLikedInformation():
    userMediaValue, next_ = api.user_liked_media()

    while next_:
            moreUserMedia, next_ = api.user_liked_media(with_next_url=next_)
            userMediaValue.extend(moreUserMedia)

    for media in userMediaValue:
        if hasattr(media, 'location') and hasattr(media.location, 'point') and hasattr(media.location.point, 'latitude') and hasattr (media.location.point, 'longitude'):
            latData = media.location.point.latitude
            longData = media.location.point.longitude
            LOCATIONS.append((latData,longData))


def printUserData():
    for loc in LOCATIONS:
        print (loc[0], loc[1])

# def AirportInformation(lat, long):
# 	newarestAirportResponse = flights.nearest_relevant(LOCATIONS[0][0], LOCATIONS[0][1])

# AirportInformation(0,0)
getUserLikedInformation()
printUserData()
