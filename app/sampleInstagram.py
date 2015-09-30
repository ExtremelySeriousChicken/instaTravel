from instagram.client import InstagramAPI

def setup():

    api = InstagramAPI(client_id='360cc24cb8534f7cbbfb06d7ee1e26a3', client_secret='4e1026ba847841eab8797101ceb9680a')
    popular_media = api.media_popular(count=20)
    returnThis = list()
    for media in popular_media:
        returnThis.append(media.images['standard_resolution'].url)
    print (returnThis)
    return returnThis

#just for the push