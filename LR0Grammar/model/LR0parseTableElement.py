class LR0ParseTableElement:
    class ElementType:
        SHIFT = "SHIFT"
        REDUCE = "REDUCE"
        GOTO =" GOTO"

    def __init__(self, element_type, stateOrProductionRUle):
        self.element_type = element_type
        if element_type == self.ElementType.SHIFT or element_type == self.ElementType.GOTO:
            self.state_number = stateOrProductionRUle
            self.reduction_productionRule = None
        elif element_type == self.ElementType.REDUCE:
            self.state_number = None
            self.reduction_productionRule = stateOrProductionRUle
        else:
            raise ValueError("Invalid element type")
        
    def __str__(self):
        if self.element_type == self.ElementType.REDUCE:
            assert self.reduction_productionRule is not None
            return "R: "+ str(self.reduction_productionRule)
        elif self.element_type == self.ElementType.SHIFT:
            return "S: " + str(self.state_number)
        elif self.element_type == self.ElementType.GOTO:
            return "GOTO: " + str(self.state_number)
        return "NULL"