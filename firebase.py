import pyrebase
import YelpFetch

class FBData:
	def __init__(self):
		self.config = {
			"apiKey": "AIzaSyDtENByjPjjrXyoBWEr7Tr4to9ypS_EU38",
			"authDomain": "decisionkitchen.firebaseapp.com/",
			"databaseURL": "https://decisionkitchen.firebaseio.com/",
			"storageBucket": "decisionkitchen.appspot.com"
		}

		self.firebase = pyrebase.initialize_app(self.config)
		self.firebase.auth().signInAnonymously()


		self.db = self.firebase.database()

	def start(self):
		print("hello")
		users = self.db.child("groups").child('2120b04c-bd1e-42c8-abf1-08fd4fde8133').child("restaurants").get()
		sols = []
		for i in users.val().keys():
			mine = YelpFetch.YelpFetcher(['breakfast_brunch', 'chinese', 'diners', 'hotdogs', 'hotpot', 'italian', 'japanese', 'korean', 'mongolian', 'pizza', 'steak', 'sushi', 'tradamerican', 'vegetarian'])
			sols.append(mine.vectorize(mine.search_ID(i))[1])
		return sols
	# Fix authentication
	# only search good ids
	# add additional case for no categories



FBData().start()