class LR0ParseTableElement:
    class ElementType:
        SHIFT = "SHIFT"
        REDUCE = "REDUCE"
        GOTO = "GOTO"
        ACCEPT = "ACCEPT"

    # for reduction
    def __init__(self, element_type, productionRUle):
        self.element_type = element_type
        self.reductionProductionRule = productionRUle

    # shifting and goto
    def __init__(self, elementType, stateNumber):
        self.element_type = elementType
        self.stateNumber = stateNumber

    # accepting state only  
    def __init__(self, elementType):
        assert elementType == self.ElementType.ACCEPT
        self.element_type = elementType
        
    def __str__(self):
        if self.element_type == self.ElementType.REDUCE:
            assert self.reduction_productionRule is not None
            return "R: "+ str(self.reduction_productionRule)
        elif self.element_type == self.ElementType.SHIFT:
            return "S: " + str(self.state_number)
        elif self.element_type == self.ElementType.GOTO:
            return "GOTO: " + str(self.state_number)
        elif self.element_type == self.ElementType.ACCEPT:
            return "Accept"
        return "NULL"