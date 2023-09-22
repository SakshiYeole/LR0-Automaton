class LR0ParseTableElement:
    class ElementType:
        SHIFT = "SHIFT"
        REDUCE = "REDUCE"
        GOTO = "GOTO"
        ACCEPT = "ACCEPT"

    def __init__(self, element_type, reduction_production_rule, state_number):

        self.element_type = element_type
        self.reduction_production_rule = reduction_production_rule
        self.state_number = state_number
        if state_number is None:  # Reduce
            self.element_type = element_type
            self.reduction_production_rule = reduction_production_rule
        elif reduction_production_rule is None:  # Shift and Goto
            self.element_type = element_type
            self.stateNumber = state_number
        elif reduction_production_rule is None and state_number is None:  # Accept
            assert element_type == self.ElementType.ACCEPT
            self.element_type = element_type

    def __str__(self):
        if self.element_type == self.ElementType.REDUCE:
            assert self.reduction_production_rule is not None
            return f"Reduce: {str(self.reduction_production_rule)}"
        elif self.element_type == self.ElementType.SHIFT:
            return f"Shift: {str(self.state_number)}"
        elif self.element_type == self.ElementType.GOTO:
            return f"GOTO: {str(self.state_number)}"
        elif self.element_type == self.ElementType.ACCEPT:
            return f"Accept"
        return "NULL"


def main():
    e = LR0ParseTableElement(LR0ParseTableElement.ElementType.REDUCE, 'abc', 4)
    print(e)


if __name__ == "__main__":
    main()
