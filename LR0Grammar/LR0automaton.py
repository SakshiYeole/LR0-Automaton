# the final output DFA must be a list of states, where each item in list a dictionary
# 1st key is the items matched to dictionary of production rules(each prodcution rule is a dict with items as strings and key as teh LHS of prodcution rule) in that state.
# 2nd key is transition matched to dictionary of transitions from that state to some other state on the key element
# states = [
#     {'items': ['S -> .E', 'E -> .E + T', 'E -> .T', 'T -> .T*F', 'T -> .F'], 'transitions': {'E': 1}},        # 0
#     {'items': ['S -> E.'], 'transitions': {}},              # 1
#     {'items': ['E -> .E+T', 'E -> .T'], 'transitions': {'E': 3, 'T': 2}}, #2
#     {'items': ['E -> E.+T'], 'transitions': {'T': 4}},      # 3
#     {'items': ['E -> E+.T'], 'transitions': {'T': 5}},      # 4
#     {'items': ['T -> .T*F', 'T -> .F'], 'transitions': {'T': 6, 'F': 7}},   # 5
#     {'items': ['T -> T.*F'], 'transitions': {'F': 8}},         # 6
#     {'items': ['F -> .(E)', 'F -> .id'], 'transitions': {'E': 9, 'id': 10}},    # 7
#     {'items': ['F -> (E.)'], 'transitions': {}},            # 8
#     {'items': ['E -> E+.T.'], 'transitions': {}},    # 9
#     {'items': ['T -> T.*F.'], 'transitions': {}},           # 10
# ]
import os
import sys
import copy
from pathlib import Path
from enum import Enum
import shutil
import subprocess
from collections import deque

sys.path.append('E:\Acads\Semester 7\CD\Lab\lab6\model')
from model import productionRule as pr
from model import item
from model import state
from model import Grammar
from model import LR0parseTableElement

class LR0Grammar(Grammar):

    def __init__(self):
        super().__init__()
        self.transitions = {}
        self.initialState = None
        self.parseTable = []
        self.stateIndexing = {}

    def findInitialItem(self):
        firstSymbol = super().getFirstSymbol()
        newNameForFirstSymbol = super().findNewName(firstSymbol)
        rightOfItem = [firstSymbol]
        return item.Item(newNameForFirstSymbol, rightOfItem, item.itemType.new_item)
    
    def findInitialItemSet(self):
        initial_Item = self.findInitialItem()
        InitialItem_set = {initial_Item}
        return InitialItem_set
    
    def addToTransitions(self, from_state, transition_string, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][transition_string] = to_state

    def checkStateAlreadyServed(self, state):
        return state in self.transitions
    
    def computeTransitions(self):
        initial_item_Set = self.findInitialItemSet()
        self.initialState = state.State(initial_item_Set, super().getProductionRules())

        new_states_created = deque()
        new_states_created.append(self.initialState)

        while new_states_created:
            curr_state = new_states_created.popleft()

            # check if the state is already served
            if self.checkStateAlreadyServed(curr_state):
                continue
            string_transition_possible = set()
            for item in curr_state.getItems():
                if not item.isReductionItem():
                    string_transition_possible.add(item.getSymbolNextToDotMarker())

            for transitionString in string_transition_possible:
                non_closure_items_for_new_state = set()
                for item in curr_state.getItems():
                    if not item.isReductionItem() and item.getSymbolNextToDotMarker() == transitionString:
                        non_closure_items_for_new_state.add(item.movingDotMarkerInItemAndReturn())

                newstate = state.State(non_closure_items_for_new_state, super().getProductionRules())
                new_states_created.append(newstate)
                self.addToTransitions(curr_state, transitionString, newstate)

    def computeIndexingOfStates(self):
        index = 0
        self.stateIndexing[self.initialState] = index
        index += 1

        for fromState, transitions in self.transitions.items():
            if fromState not in self.stateIndexing:
                self.stateIndexing[fromState] = index
                index += 1

            for transitionString, toState in transitions.items():
                if toState not in self.stateIndexing:
                    self.stateIndexing[toState] = index
                    index =+ 1
    def createEmptyParsingTable(self):
        for i in range(len(self.stateIndexing)):
            map = {}
            self.parseTable.append(map)
    
    def addToParsetableReduce(self, state_number, production_rule, transition_string):
        self.parseTable[state_number][transition_string]= LR0parseTableElement("REDUCE", production_rule)

    def addToParseTableShiftGoto(self, state_number, shift_state_number, transition_string, element_type):
        self.parseTable[state_number][transition_string] = LR0parseTableElement(element_type, state_number)

    def parseTableIsNonEmptyForStateAndTransitionString(self, state_number, transition_string):
        return transition_string in self.parseTable[state_number]

    # def computeParsingTable(self):
    #     if not self.transitions:
    #         print("Compute teh transitions before runnimg tis function")
    #         sys.exit(-1)

    #     self.createEmptyParsingTable()

    #     for from_state, transition_map in self.transitions.items():
    #         from_state_int = self.stateIndexing[from_state]

    #         # check if teh fromstate is a reducing state
    #         if from_state.isReducingState():
    #             reducing_items = from_state.getItemsWhichAreReducingItems()
    #             if len(reducing_items) > 1:
    #                 # reduce-reduce conflict
    #                 print("Reduce - Reduce conflict: ", reducing_items)
    #                 sys.exit(-1)

    #             reducing_item = next(iter(reducing_items))
    #             productionrule_foritem = reducing_item.getgetCorrespondingProductionRuleForReducingItem()

    #             # for all terminal symbols, reduction
    #             for terminal in super().get

    def indexingStates(self):
        result = {}
        index = 0

        for from_state, transition_map in self.transitions.items():
            if from_state not in result:
                result[from_state] = index
                index += 1

            for to_state in transition_map.values():
                if to_state not in result:
                    result[to_state] = index
                    index += 1
        
        print("Total States: ", len(result))
        print("Indexing of maps: ")
        for state, index in result.items():
            print(f"{index} :- ")
            print(state)

        return result
    
    def printTransitions(self):
        stateIndexing = self.indexingStates()

        for from_state, transition_map in self.transitions.items():
            from_state_index = stateIndexing[from_state]

            for transition_string, to_state in transition_map.items():
                to_state_index = stateIndexing[to_state]

                print("From State: ", from_state_index)
                print("Transition String: ", transition_string)
                print("To State: ", to_state_index)
                print()
        
        print()
        
class ReadingInput:
    def readInputFromFile(path):
        with open(path, 'r') as file:
            grammar = Grammar()
            startSymbol = file.readline().strip()
            grammar.setFirstSymbol(startSymbol)

            nonTerminalString = file.readline().strip()
            nonTeminals = nonTerminalString.split()
            grammar.addAllNonTerminalSymbolFromIterator(nonTeminals)

            terminalString = file.readline().strip()
            terminals = terminalString.split()
            grammar.addAllTerminalSymbolFromIterator(terminals)

            for line in file:
                input_line = line.strip()
                if not input_line:
                    continue
                grammar.addRule(input_line)

        return grammar

def main():

    dotMarker = '\u2022'

    # Testing
    t = LR0Grammar()
    t.setFirstSymbol("E")
    t.addNonterminalSymbol("E")
    t.addNonterminalSymbol("T")
    t.addNonterminalSymbol("F")

    t.addTerminalSymbol("+")
    t.addTerminalSymbol("*")
    t.addTerminalSymbol("(")
    t.addTerminalSymbol(")")
    t.addTerminalSymbol("F")

    # t.addRule("E' -> E")
    t.addRule("E -> E + T | T")
    t.addRule("T -> T * F | F")
    t.addRule("F -> ( E ) | id")

    t.printGrammar()

    t.computeTransitions()
    t.printTransitions()

if __name__ == "__main__":
    main()