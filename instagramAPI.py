from instagram.client import InstagramAPI
import json
#(u'569470452.360cc24.08adf989f9f147afa7d72c181d53b7a9', 
#{u'username': u'ritvikupadhyaya', u'bio': u'', u'	website': u'', u'profile_picture': 
#u'https://igcdn-photos-e-a.akamaihd.net/hphotos-ak-xpf1/t51.2885-19/10802485_564679577009836_1705988990_a.jpg', 
#u'full_name': u'Ritvik Upadhyaya', u'id': u'569470452'})
#
#
access_token = "569470452.360cc24.08adf989f9f147afa7d72c181d53b7a9"
client_id = "360cc24cb8534f7cbbfb06d7ee1e26a3"
client_secret = "4e1026ba847841eab8797101ceb9680a"
api = InstagramAPI(access_token="569470452.360cc24.08adf989f9f147afa7d72c181d53b7a9", client_secret="4e1026ba847841eab8797101ceb9680a")
popular_media = api.media_popular(count=20)
# for media in popular_media:
#     print (media.images['standard_resolution'].url)


def getUserLikedInformation():
	userMediaValue, next_ = api.user_liked_media()
	while next_:
    		moreUserMedia, next_ = api.user_liked_media(with_next_url=next_)
    		userMediaValue.extend(moreUserMedia)
	for media in userMediaValue:
		if hasattr(media, 'location') and hasattr(media.location, 'point') and hasattr(media.location.point, 'latitude'):
			print (media.location.point.latitude)

getUserLikedInformation()
