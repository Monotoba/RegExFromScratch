class State:
    def __init__(self, is_final=False):
        self.is_final = is_final
        self.transitions = {}
