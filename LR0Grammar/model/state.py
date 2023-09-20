import copy

from model import Grammar as g
from model import item

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
    
    def getItemsWhichAreReducingItems(self):
        result = set()
        for item in self.items:
            if item.isReductionItem():
                result.add(item)
        return result
        
    def idReducingState(self):
        reduction_items = self.getItemsWhichAreReducingItems()
        return not reduction_items
        # checks if the set is empty

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
    
def main():
    dotMarker = '\u2022'
    t = g.Grammar()
    t.addRule("E' -> E")
    t.addRule("E -> E + T | T")
    t.addRule("T -> T * F | F")
    t.addRule("F -> ( E ) | id")
    t.printGrammar()

    t = g.Grammar()
    right = []
    right.append("(")
    right.append(dotMarker)
    right.append("E")
    right.append(")")
    i = item.Item("F", right, item.itemType.derived_item)
    print(f"Item: {i}")

    closure = set()
    closure = i.closure(t.getProductionRules())
    for i in  closure:
        print(i)

    inititemset = set()
    inititemset.add(i)

    s1 = State(inititemset, t.getProductionRules())
    print(s1)
    s2 = State(inititemset, t.getProductionRules())
    print(s2)

    print(s1==s2)

    states = set()
    states.add(s1)
    states.add(s2)
    print(f"states size: {len(states)}")

if __name__ == "__main__":
    main()