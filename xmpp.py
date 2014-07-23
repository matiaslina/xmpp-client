import sleekxmpp

GTALK_SERVER = ('talk.google.com', 5222)

class Connection(sleekxmpp.ClientXMPP):

    def __init__(self, window=None):
        with open("./.account", "r") as account_file:
            mail = account_file.readline()
            mail = mail[0:len(mail)-1]
            password = account_file.readline()
            password = password[0:len(password)-1]
        print(mail)
        print(password)
        super(Connection, self).__init__(mail, password)

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)

        self.window = window

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            self.window.new_message_from_conn(msg['from'],msg['body'])
        else:
            print("[XMPP] Not chat or normal - ", msg['body'])


if __name__ == "__main__":
    conn = Connection()
    conn.connect(('talk.google.com', 5222))
    conn.process(block=False)
