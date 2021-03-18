def addUser(UID, ChatID):
    print("Should add user with id " + str(UID) + " from ChatID " + str(ChatID))


def addSubscription(UID, URL):
    print("Should add subscription to " + URL + " to user " + str(UID))


def setFeedTime(UID, newFeedTime):
    print("Should set user with id " + str(UID) + " feed time to " + str(newFeedTime.hour) + ":" + str
        (newFeedTime.minute))