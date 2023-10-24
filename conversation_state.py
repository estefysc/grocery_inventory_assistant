class ConversationState:
    def __init__(self):
        self.stage = "greeting"
        self.user_intent = None
        self.item_to_update = None
        self.quantity = None
        self.consumption_rate = None

    def reset(self):
        self.stage = "greeting"
        self.user_intent = None
        self.item_to_update = None
        self.quantity = None
        self.consumption_rate = None
