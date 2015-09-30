from instagram.client import InstagramAPI
from clarifai.client import ClarifaiApi
import requests
import json


access_token = "569470452.360cc24.08adf989f9f147afa7d72c181d53b7a9"
client_id = "360cc24cb8534f7cbbfb06d7ee1e26a3"
client_secret = "4e1026ba847841eab8797101ceb9680a"
tapDict = {}
finalReturnedList = []
api = InstagramAPI(access_token=access_token, client_secret=client_secret)
amadeus_api_key = 'RzGfJPsCmYIRlDmTi6Og2BAYAVviEAdh'
clarifai_api = ClarifaiApi()
# flights = Flights(amadeus_api_key)

#This method always grabs ALL the medias LIKED by the user
#Then stores it into UserMediaValue Array
#This function will take in two arrays - userMediaValue and locations
def getUserLikedInformation(userMediaValue, locations):
    mediaReceived, next_ = api.user_liked_media()

    while next_:
            moreUserMedia, next_ = api.user_liked_media(with_next_url=next_)
            mediaReceived.extend(moreUserMedia)
    userMediaValue.extend(mediaReceived)
    locations = prepareGeoTagList(userMediaValue, locations)

    return [userMediaValue, locations]

#This method grabs all the geolocations from all the media liked by the user
#So its a 2-d array of lattitude and longitude of all elements of userMediaValue
def prepareGeoTagList(userMediaValue, locations):
    for media in userMediaValue:
        if hasattr(media, 'location') and hasattr(media.location, 'point') and hasattr(media.location.point, 'latitude') and hasattr (media.location.point, 'longitude'):
            latData = media.location.point.latitude
            longData = media.location.point.longitude
            locations.append((latData,longData))
    return locations

#Takes in latitude and the longitude in that order and returns a json of all
#the airports close to the specified location
def AirportInformation(lati, longi):
    urlAirInfo = "https://api.sandbox.amadeus.com/v1.2/airports/nearest-relevant?apikey="+amadeus_api_key+"&latitude="+str(lati)+"&longitude="+str(longi)
    r = requests.get(urlAirInfo)
    jsonR = json.loads(r.text)
    return jsonR

# This function will return the index of the airport in aList
#This function will return -1 if it does not exixt
def gotAirport(air, aList):
    found = -1
    for airportIndex in range(len(aList)):
        if (air == aList[airportIndex]['airport']):
            return airportIndex
    return found

#If the number of likes associated with this airport is highest
#than any other in aList, then it returns the airport
def getMaxAirport(aList):
    highest = aList[0]

    for one in aList:
        if(one['num'] > highest['num']):
            highest = one
    return highest['airport']

#Grab all the airports in the airport list and return the airport with the max
#likes done close to it.
def areaCount(locations):
    airportList = list()
    for location in locations:
        answer = AirportInformation(location[0], location[1])
        for x in answer:
            num = gotAirport(x['airport'], airportList)
            if num == -1:
                 airportList.append({'airport' : x['airport'], 'num' : 0})
            else:
                airportList[num]['num'] += 1
    maxAirport = getMaxAirport(airportList);

    return maxAirport
        #now adding the data

#separate the likes, imagedata url from the media object for all the elements in the
#array with the given name
#returns the new list with 4 objects per element
def getLikeCount(arrayName):
    likeList = list()
    for photo in arrayName:
        likeList.append({'object': photo, 'likeNum' : photo.like_count,'type': photo.type, 'imageURL' : photo.images['standard_resolution'].url})
    return likeList

#Returns a new list with all the media arranged in descending order of likes
def sortLikes(arrayName):
    likeLists = list()

    likeLists = getLikeCount(arrayName)

    newList = sorted(likeLists, key=lambda member: member['likeNum'], reverse=True)

    newNewList = list()
    photoLength = 0
    if (len(newList) > 24):
        photoLength = 25
    else:
        len(newList)
    for i in range(photoLength):
        newNewList.append(newList[i])

    # print("size of Newnewlist")
    return newNewList

#Connects to the clarifai API and gets back all the tags the server returns
#for all the images liked by the user (userMediaValue)
#returns a 2d array of tag with how many time it came up in clarifai
#This function will take in userMediaValue and give
def sendImagesToClarifai(userMediaValue, tagDict):
    # multipleURL = "\"Authorization: Bearer Kab0erA7RqZeORbbIMiZtwLfd5Krur\""
    header1 = {'Authorization':'Bearer xFikphU34qMyB7dNSEDDYK2bz5Ao5k'}
    counter = 0
    urlArray = []
    resultArr = []
    sort = sortLikes(userMediaValue)
    for x in sort:
        if x['type'] == 'image':
            photoURL = x['imageURL']
            urlArray.append(photoURL)
            result = clarifai_api.tag_image_urls(photoURL)
            resultArr.append(result)
            counter+=1
    
    for x in xrange(0,counter):
        arrayOfTag = clarifaiTagUpdate(resultArr[x]['results'][0]['result']['tag']['classes'], tagDict)
    return [arrayOfTag, tagDict]

#search the tag in the taglist. return 1 if found, -1 otherwise
def foundTag(tag, tagList):
    for x in range(len(tagList)):
        if tag == tagList[x]['symbol']:
            tagList[x]['count'] += 1
            return tagList
    tagList.append({'symbol': tag, 'count': 1})
    return tagList

#Sort all the tags in the descending order of the number of times they come up
#in clarify. Should only be given something like the return value of sendImagesToClarifai
def clarifaiTagUpdate(returnArray, tagDict):
    for x in range(len(returnArray)):
        tagList = foundTag(returnArray[x], tagDict)
        
    # sorted_tapDict = sorted(tagDict.items(), key=lambda x: x[1], reverse=True)
    sorted_tapDict = sorted(tagDict, key=lambda member: member['count'], reverse=True)

    print sorted_tapDict
#The second pass at instagram to get the final results that qualify as pseudo random
#After the matching of tags from clarifai
#Returns the FINAL LIST that should be used for the second half of the 24 photos
def searchInstagram(userMediaValue, tagDict):
    result = sendImagesToClarifai(userMediaValue, tagDict)
    tagDictionaryToSearch = result[0]
    tagDict = result[1]
    semiFinalSearchArray = []
    for x in xrange(1,4):
        tagtosearch = tagDictionaryToSearch[x]
        print (tagtosearch)
        mediaReceived, next_ = api.tag_recent_media(tag_name = tagtosearch, count=20)
        semiFinalSearchArray.extend(moreUserMedia)
    finalReturnedList = sortLikes(semiFinalSearchArray)
    return [finalReturnedList, tagDict]


def amadeusAutoComplete(queryString):
    requestURl = "https://api.sandbox.amadeus.com/v1.2/airports/autocomplete?apikey=RzGfJPsCmYIRlDmTi6Og2BAYAVviEAdh&term="
    requestURl+=queryString
    r = requests.get(requestURl)
    jsonR = json.loads(r.text)
    return jsonR

#Enter the origin IATA code and the destination iATA code. Eg. flightInformation("BOS","NYC")
def flightInformation(origin,destination):
    requestURl = "https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?apikey=RzGfJPsCmYIRlDmTi6Og2BAYAVviEAdh&origin="+origin+"&destination="+destination
    r = requests.get(requestURl)
    jsonR = json.loads(r.text)
    print (jsonR)
    return jsonR
# getUserLikedInformation()
# prepareGeoTagList()
# areaCount()
# sendImagesToClarifai()

# Sort moved to send images to clarifai
# sort = sortLikes()
# print(sort)

# sortedLikeArr = userMediaValue.sort(key=getLikeCountFromJSON(), reverse = True)
# AirportInformation(LOCATIONS[0][0],LOCATIONS[0][1])
# areaCount()

#just for the push

