
import json
from time import time

class UserIdList:
    """A list (dict) of user-id's sorted after the chat-id"""
    def __init__(self, save_path_: str = "", time_interval_ = 30):
        self.__id_list = {}
        self.__save_path = "data/id_list.json"
        self.__time_interval = time_interval_

        if save_path_:
            self.__save_path = save_path_        

        try:
            with open(self.__save_path, "r") as file:
                self.__id_list = json.loads(file.read())
        except Exception:
            pass

    def __call__(self):
        return self.__id_list
    
    def __contains__(self, key):
        return key in self.__id_list
    
    def __str__(self):
        return str(self.__id_list)
    
    def save(self, save_path_: str = ""):
        """safe the id_list"""
        if save_path_:
            with open(save_path_, "w") as file:
                file.write(json.dumps(self.__id_list))

        elif self.__save_path:
            with open(self.__save_path, "w") as file:
                file.write(json.dumps(self.__id_list))

    
    def register(self, chat_id, user_id, user_timestamp):
        """registers a new user in a group"""

        chat_id = str(chat_id)
        user_id = str(user_id)

        if chat_id in self.__id_list:
            self.__id_list[chat_id][user_id] = user_timestamp
        else:
            self.__id_list[chat_id] = {}
            self.__id_list[chat_id][user_id] = user_timestamp
        
        self.save()

    def unregister (self, chat_id, user_id):
        """unregisters a user from a group"""

        chat_id = str(chat_id)
        user_id = str(user_id)

        if chat_id in self.__id_list:
            self.__id_list[chat_id].pop(user_id, None)
        
            if not self.__id_list[chat_id]:
                self.__id_list.pop(chat_id, None)
        
        self.save()
    
    def timeUp(self, custom_interval = None):
        timeup_list = []
        
        timestamp = int(time())

        interval = custom_interval if custom_interval else self.__time_interval

        for chat in self.__id_list:
            for user in self.__id_list[chat]:
                if timestamp - self.__id_list[chat][user] >= interval:
                    timeup_list.append([chat, user])
        
        return timeup_list

