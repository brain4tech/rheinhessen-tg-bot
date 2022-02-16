import json
from time import time
import os


class UserIdList:
    """A datastructure (dict) of user-id specific data structured with the chat-id"""

    def __init__(self, file_name_):
        self._id_list = {}
        self._file_name = os.path.join("data", file_name_)

        try:
            with open(self._file_name, "r") as file:
                self._id_list = json.loads(file.read())
        except Exception:
            pass

    def __call__(self):
        return self._id_list

    def __contains__(self, key):
        return key in self._id_list

    def __str__(self):
        return str(self._id_list)

    def save(self, file_name_: str = ""):
        """safe the id_list"""
        if file_name_:
            with open(file_name_, "w") as file:
                file.write(json.dumps(self._id_list))

        elif self._file_name:
            with open(self._file_name, "w") as file:
                file.write(json.dumps(self._id_list))

    def register(self, chat_id, user_id, user_data):
        """registers a new user in a group"""

        chat_id = str(chat_id)
        user_id = str(user_id)

        if chat_id in self._id_list:
            self._id_list[chat_id][user_id] = user_data
        else:
            self._id_list[chat_id] = {}
            self._id_list[chat_id][user_id] = user_data

        self.save()

    def unregister(self, chat_id, user_id):
        """unregisters a user from a group"""

        chat_id = str(chat_id)
        user_id = str(user_id)

        if chat_id in self._id_list:
            self._id_list[chat_id].pop(user_id, None)

            if not self._id_list[chat_id]:
                self._id_list.pop(chat_id, None)

        self.save()

    def getList(self, chat_id=None):
        if chat_id:
            try:
                return self._id_list[chat_id]
            except Exception:
                return None

        return self._id_list


class UserIdTimestampList(UserIdList):

    def __init__(self, file_name_, time_interval_=None):
        super().__init__(file_name_)
        self.__time_interval = time_interval_

    def getExpiredUsers(self, custom_interval=None):
        timeup_list = []

        timestamp = int(time())

        interval = custom_interval if custom_interval else self.__time_interval

        for chat in self._id_list:
            for user in self._id_list[chat]:
                if timestamp - self._id_list[chat][user] >= interval:
                    timeup_list.append([chat, user])

        return timeup_list
