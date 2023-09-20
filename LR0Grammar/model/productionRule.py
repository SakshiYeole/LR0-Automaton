class ProductionRule:           #Tested

    def __init__(self, LHS):
        self.LHS = LHS
        self.RHS = []
    
    def __str__(self):
        return  f"{self.LHS} -> {self.RHS} "
    
    def addRHS(self, RHS):
        self.RHS.append(RHS)
    
    def addRHSall(self,RHSall):
        for i in RHSall:
            self.addRHS(i)
    
    def getLHS(self):
        return self.LHS
    
    def getRHS(self):
        return self.RHS
    
    def setnewRHS(self, RHS):
        self.RHS.clear()
        self.addRHSall(RHS)

    def printProductionRule(self):
        print(f"{self.LHS} -> ")
        s = ""
        for right in self.RHS:
            s = s + " " + right + " |"
        s.replace(s[len(s)-1], "")
        print(s)

    def __eq__(self, other):
        if other == None:
            return False
        return self.LHS == other.LHS
