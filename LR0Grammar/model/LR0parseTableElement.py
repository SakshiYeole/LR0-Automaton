class LR0ParseTableElement:
    class ElementType:
        SHIFT = "SHIFT"
        REDUCE = "REDUCE"
        GOTO = "GOTO"
        ACCEPT = "ACCEPT"

    def __init__(self, element_type, productionRUle, stateNumber):
        if stateNumber == None:
            self.element_type = element_type
            self.reductionProductionRule = productionRUle
        elif productionRUle == None:
            self.element_type = element_type
            self.stateNumber = stateNumber
        elif productionRUle == None and stateNumber == None:
            assert element_type == self.ElementType.ACCEPT
            self.element_type = element_type

    # # shifting and goto
    # def __init__(self, elementType, stateNumber):
    #     self.element_type = elementType
    #     self.stateNumber = stateNumber

    # # accepting state only  
    # def __init__(self, elementType):
    #     assert elementType == self.ElementType.ACCEPT
    #     self.element_type = elementType
        
    def __str__(self):
        if self.element_type == self.ElementType.REDUCE:
            assert self.reduction_productionRule is not None
            return "Reduce: "+ str(self.reduction_productionRule)
        elif self.element_type == self.ElementType.SHIFT:
            return "Shift: " + str(self.stateNumber)
        elif self.element_type == self.ElementType.GOTO:
            return "GOTO: " + str(self.stateNumber)
        elif self.element_type == self.ElementType.ACCEPT:
            return "Accept"
        return "NULL"
    
def main():
    e = LR0ParseTableElement(LR0ParseTableElement.ElementType.SHIFT, None, 7)
    print(e)

if __name__ == "__main__":
    main()