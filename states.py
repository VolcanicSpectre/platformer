from abc import abstractclassmethod


class State:
    
    @abstractclassmethod
    def handle_inputs(events): pass
    
    @abstractclassmethod
    def update(dt): pass


class


