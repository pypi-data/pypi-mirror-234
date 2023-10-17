import datetime


class Messenger:
    def __init__(self):
        self.messages = {}
        self.admin_messages = []
        self.info = []
        self.warnings = []
        self.errors = []
        self.seq_list = []

    def add_message(self, message):
        json_msg = {
            "message": message,
            "time_stamp": datetime.datetime.now(),
        }
        if type(message["to"]) == list:
            message["to"] = tuple((message["to"][0], message["to"][1]))
        if type(message["from"]) == list:
            message["from"] = tuple((message["from"][0], message["from"][1]))

        if message["to"] == "Broadcast":
            if message["to"] not in self.messages:
                self.messages[message["to"]] = [json_msg]
            else:
                self.messages[message["to"]].append(json_msg)

        elif "self" not in message:
            if message["from"] not in self.messages:
                self.messages[message["from"]] = [json_msg]
            else:
                self.messages[message["from"]].append(json_msg)
        else:
            if message["to"] not in self.messages:
                self.messages[message["to"]] = [json_msg]
            else:
                self.messages[message["to"]].append(json_msg)

    def get_messages(self):
        return self.messages

    def add_info(self, message):
        json_msg = {
            "message": message,
            "time_stamp": datetime.datetime.now(),
            "state": "INFO"
        }
        self.seq_list.append(json_msg)
        self.info.append(json_msg)

    def get_info(self):
        return self.info

    def add_warning(self, message):
        json_msg = {
            "message": message,
            "time_stamp": datetime.datetime.now(),
            "state": "WARNING"
        }
        self.seq_list.append(json_msg)
        self.warnings.append(json_msg)

    def get_warnings(self):
        return self.warnings

    def add_error(self, message):
        json_msg = {
            "message": message,
            "time_stamp": datetime.datetime.now(),
            "state": "ERROR"
        }
        self.seq_list.append(json_msg)
        self.errors.append(json_msg)

    def get_errors(self):
        return self.errors
