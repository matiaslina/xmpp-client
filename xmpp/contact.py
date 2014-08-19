
class Contact(object):

    def __init__(self, jid, data):
        self.jid = jid
        self.from = data.get("from", None)
        self.groups = data.get("groups", None)
        self.name = data.get("name", None)
        self.pending_in = data.get("pending_in", None)
        self.pending_out = data.get("pending_out", None)
        self.subscription = data.get("subscription", None)
        self.to = data.get("to", None)
        self.whitelisted = data.get("whitelisted", None)
