import pyrebase
import YelpFetch
import datetime

class FBData:
    def __init__(self, group):
        self.config = {
            "apiKey": "AIzaSyDtENByjPjjrXyoBWEr7Tr4to9ypS_EU38",
            "authDomain": "decisionkitchen.firebaseapp.com/",
            "databaseURL": "https://decisionkitchen.firebaseio.com/",
            "storageBucket": "decisionkitchen.appspot.com"
        }

        self.firebase = pyrebase.initialize_app(self.config)
        #self.firebase.auth().signInAnonymously()

        self.group = group
        self.db = self.firebase.database()

    def start(self):
        restraunts = self.db.child("groups").child(self.group).child("restaurants").get()
        sols = []
        if restraunts.val() != None:
            for i in restraunts.val().keys():
                mine = YelpFetch.YelpFetcher(['breakfast_brunch', 'chinese', 'diners', 'hotdogs', 'hotpot', 'italian', 'japanese', 'korean', 'mongolian', 'pizza', 'steak', 'sushi', 'tradamerican', 'vegetarian'])
                searched = mine.search_ID(i)
                if searched != None:
                    sols.append(mine.vectorize(searched))


        money_total = []
        category = []
        deliv = []
        for l in self.db.child("groups").child(self.group).child("games").child("0").child("responses").get().each():
            j = l.val()["value"]
            money = []
            if j != None:
                money.append(j[0])
                category.append(j[1])
                deliv.append(j[2])

            for i in range(len(money)):
                curr = 0
                count = 0
                print (money)
                for k in zip(money[i], [1,2,3,4]):
                    curr += k[0] * k[1]
                    if k[0] != 0:
                        count += 1
                if count != 0:
                    money[i] =  float(curr) / count
                else:
                    money[i] = 0
            if len(money) != 0:
                money = sum(money) / len(money)
            else:
                money = 0
            money_total.append(money)
        #Deliv is still bad
        return filter(lambda x: x != None, sols), sum(money_total) / len(money_total), category, deliv
    # Fix authentication
    # only search good ids
    # add additional case for no categories

    def is_done(self, num_players):
        response_base = self.db.child("groups").child(self.group).child("games").child("0").child("responses").get()
        if response_base.val() == None:
            return False
        if len(response_base.val().keys()) >= num_players:
            return True
        else:
            return False

    def push_update(self, top_restaurants):
        data = top_restaurants
        fetcher = YelpFetch.YelpFetcher([])
        restaurants = self.db.child("groups").child(self.group).child("restaurants").get().val()
        for restaurant in data:
            if restaurants == None or (not restaurant[0] in restaurants): # Push to firebase
                data = fetcher.search_ID(restaurant[0])
                self.db.child("groups").child(self.group).child("restaurants").child(data["id"]).set({
                    "address": data["location"]["address1"],
                    "city": data["location"]["city"],
                    "name": data["name"],
                    "id": data["id"],
                    "zip": data["location"]["zip_code"],
                    "state": data["location"]["state"]
                })

        self.db.child("groups").child(self.group).child("games").child("0").child("result").set(data)
        self.db.child("groups").child(self.group).child("games").child("0").child("meta").child("end").set(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + "Z")
        return True


#FBData("-KqJWkCu3YTpbMJi2u8U").start()
#print(FBData().push_update([[i for i in range(20)] for k in range(20)]))