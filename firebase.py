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
		#self.firebase.auth().signInAnonymously()


		self.db = self.firebase.database()

	def start(self):
		print("hello")
		restraunts = self.db.child("groups").child('2120b04c-bd1e-42c8-abf1-08fd4fde8133').child("restaurants").get()
		sols = []
		for i in restraunts.val().keys():
			mine = YelpFetch.YelpFetcher(['breakfast_brunch', 'chinese', 'diners', 'hotdogs', 'hotpot', 'italian', 'japanese', 'korean', 'mongolian', 'pizza', 'steak', 'sushi', 'tradamerican', 'vegetarian'])
			sols.append(mine.vectorize(mine.search_ID(i)))

		response_base = self.db.child("groups").child('2120b04c-bd1e-42c8-abf1-08fd4fde8133').child("games").child("0").child("responses").get()
		money = []
		category = []
		deliv = []
		if response_base.val() != None:
			for i in response_base.val().values():
				money.append(i[0])
				category.append(i[1])
				deliv.append(i[2])

		return sols, money, category, deliv
	# Fix authentication
	# only search good ids
	# add additional case for no categories

	def is_done(self, num_players):
		response_base = self.db.child("groups").child('2120b04c-bd1e-42c8-abf1-08fd4fde8133').child("games").child("0").child("responses").get()
		if response_base.val() == None:
			return False
		if len(response_base.val().keys()) >= num_players:
			return True
		else:
			return False


FBData().start()
print(FBData().is_done(1))