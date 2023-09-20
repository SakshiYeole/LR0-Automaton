import copy

from model import Grammar as g
from model import productionRule as ProductionRule

class itemType:
        new_item = "new_item"
        derived_item = "derived_item"

class Item:
    dotMarker = '\u2022'
    # isreduction, 

    def __init__(self, LHS, RHS, item_type):
        self.LHS = LHS
        self.RHS = copy.deepcopy(RHS)
        if item_type == itemType.new_item:
            self.RHS.insert(0, self.dotMarker)

    def isReductionItem(self):
        return self.RHS.index(self.dotMarker)==(len(self.RHS)-1)
    
    def getSymbolNextToDotMarker(self):
        if self.isReductionItem():
            return None
        indexOfDotMarker = self.RHS.index(self.dotMarker)
        return self.RHS[indexOfDotMarker + 1]
    
    def getCorrespondingProductionRuleForReducingItem(self):
        production_rule = ProductionRule.ProductionRule(self.LHS)
        production_rule.addRHS(self.RHS)
        return production_rule
    
    def movingDotMarkerInItemAndReturn(self):
        if self.isReductionItem():
            print("Is a Reduction Item")
            return None
        newRHS = copy.deepcopy(self.RHS)
        indexOfDotMarker = self.RHS.index(self.dotMarker)
        self.RHS.remove(self.dotMarker)
        self.RHS.insert(indexOfDotMarker + 1, self.dotMarker)
        return Item(self.LHS, newRHS, itemType.derived_item)
    
    def closure(self, production_rules):
        closure_item = {self}
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
        return hash((self.LHS, tuple(self.RHS)))
    
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
    for i in  closure:
        print(i)

if __name__ == "__main__":
    main()