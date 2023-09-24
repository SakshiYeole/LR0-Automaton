import copy

from model import Grammar as g
from model import productionRule as ProductionRule

class itemType:
        new_item = "new_item"
        derived_item = "derived_item"

class Item:
    dotMarker = '\u2022'
    end_of_line = "$"
    epsilon = '\u03B5'

    def __init__(self, LHS, RHS, item_type):
        self.LHS = LHS
        self.RHS = copy.deepcopy(RHS)
        self.RHs.remove(self.epsilon)
        if item_type == itemType.new_item:
            self.RHS.insert(0, self.dotMarker)

    def isReductionItem(self):
        if self.RHS:
            return self.RHS[len(self.RHS)-1]==self.dotMarker
        return False
    
    def isAcceptingItem(self):
        if self.isReductionItem():
            if len(self.RHS) > 2:
                secondLastSymbol = self.RHS[len(self.RHS) - 2]
                return secondLastSymbol.__eq__(self.end_of_line)
            
        return False

    def getSymbolNextToDotMarker(self):
        if self.isReductionItem():
            return None
        indexOfDotMarker = self.RHS.index(self.dotMarker)
        return str(self.RHS[indexOfDotMarker + 1])
    
    def getCorrespondingProductionRuleForReducingItem(self):
        production_rule = ProductionRule.ProductionRule(self.LHS)
        right = copy.deepcopy(self.RHS)
        right.remove(self.dotMarker)
        production_rule.addRHS(right)
        return production_rule
    
    def movingDotMarkerInItemAndReturn(self): 
        if self.isReductionItem():
            print("Is a Reduction Item")
            return None
        newRHS = copy.deepcopy(self.RHS)
        indexOfDotMarker = newRHS.index(self.dotMarker)
        newRHS.remove(self.dotMarker)
        newRHS.insert(indexOfDotMarker + 1, self.dotMarker)
        return Item(self.LHS, newRHS, itemType.derived_item)
    
    def closure(self, production_rules):
        closure_item = set()
        closure_item.add(self)
        addedNew = True
        while addedNew:
            addedNew = False
            toAdd = set()
            for currItem in closure_item:
                nextSymbolOfDotMarker = currItem.getSymbolNextToDotMarker()
                indexInProductionRule = next((i for i, rule in enumerate(production_rules) if rule.LHS == nextSymbolOfDotMarker), -1)
                if indexInProductionRule < 0:
                    continue
                production_rule = production_rules[indexInProductionRule]
                LHSOfproductionRule = production_rule.LHS
                for RHSOfProductionRule in production_rule.RHS:
                    itemForParticularRUle = Item(LHSOfproductionRule, RHSOfProductionRule, itemType.new_item)
                    if itemForParticularRUle not in closure_item:
                        addedNew = True
                        toAdd.add(itemForParticularRUle)
            
            if toAdd:
                closure_item.update(toAdd)
        return closure_item

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, Item):
            return False
        return self.LHS == other.LHS and self.RHS == other.RHS
    
    def __str__(self):
        return  f"{self.LHS} -> {self.RHS} "
    
    def __hash__(self) -> int:
        temp = str(self.LHS)
        temp += ''.join(str(i) for i in self.RHS)
        return hash(tuple(temp))
    
def main():
    dotMarker = '\u2022'
    
    t = g.Grammar()
    right = []
    right.append("(")
    right.append(dotMarker)
    right.append("E")
    right.append(")")
    i = Item("F", right, itemType.derived_item)
    print(f"Item: {i}")

    closure = set()
    closure = i.closure(t.getProductionRules())
    for i in closure:
        print(i)

if __name__ == "__main__":
    main()