import copy

class State:
    epsilon = '\u03B5'
    dotMarker = '\u2022'

    def __init__(self, non_closure_items, production_rules):
        self.items = set(non_closure_items)

        closure_items = set()
        for curr_item in self.items:
            curr_closure_items = curr_item.closure(production_rules)
            closure_items.update(curr_closure_items)
        
        self.items.update(closure_items)    

    def getItems(self):
        return copy.deepcopy(self.items)
    
    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, State):
            return False
        return self.items == other.items
    
    def __hash__(self) -> int:
        return hash(tuple(self.items))
    
    def __str__(self) -> str:
        stateStr = "State: \n"
        for item in self.items:
            stateStr += str(item) + "\n"
        return stateStr