
import json

class UserIdList:
    """A list (dict) of user-id's sorted after the chat-id"""
    def __init__(self, save_path_: str = ""):
        self.__id_list = {}
        self.__save_path = "data/id_list.json"

        if save_path_:
            self.__save_path = save_path_        

        try:
            with open(self.__save_path, "r") as file:
                self.__id_list = json.loads(file.read())
        except Exception:
            pass

    def __call__(self):
        return self.__id_list
    
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
