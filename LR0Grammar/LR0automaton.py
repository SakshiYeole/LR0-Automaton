import sys
import os
import copy
from collections import deque

from visualization import visualizeTable

path = os.getcwd() + '\LR0Grammar'
sys.path.append(path + '\model')
sys.path.append(path + '\..\constants')
sys.path.append(path + '\..\\visualization')
from constants import StringConstants
from model import item
from model import state
from model import Grammar
from model import LR0parseTableElement

class LR0Grammar(Grammar.Grammar):
    end_of_line = "$"

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
        rightOfItem.append(self.end_of_line)
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

    def compute_transitions(self):
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
        index = index + 1

        for fromState, transitions in self.transitions.items():
            if fromState not in self.stateIndexing:
                self.stateIndexing[fromState] = index
                # index += 1
                index = index + 1

            for transitionString, toState in transitions.items():
                if toState not in self.stateIndexing:
                    self.stateIndexing[toState] = index
                    # index += 1
                    index = index + 1

    def getStateIndexing(self):
        return copy.deepcopy(self.stateIndexing)

    def getStateFromIndex(self, index):
        for state, integer in self.stateIndexing.items():
            if index == integer:
                return state
        return None

    def addToParseTable(self, state_number, shift_state_number, production_rule, transition_string, element_type):
        self.parseTable[state_number][transition_string] = LR0parseTableElement.LR0ParseTableElement(
            element_type, production_rule, shift_state_number)

    def parseTableIsNonEmptyForStateAndTransitionString(self, state_number, transition_string):
        return transition_string in self.parseTable[state_number]

    def createEmptyParsingTable(self):
        for i in range(len(self.stateIndexing)):
            map = {}
            self.parseTable.append(map)

    def computeParsingTable(self):
        if not self.transitions:
            print("Compute the transitions before running this function")
            sys.exit(-1)

        self.createEmptyParsingTable()

        for i in range(len(self.stateIndexing)):
            from_state = self.getStateFromIndex(i)
            from_state_int = i

            # check if it is accepting
            if from_state.isAcceptingState():
                for terminal in super().getTerminalSymbols():
                    self.addToParseTable(from_state_int, None, None, terminal, LR0parseTableElement.LR0ParseTableElement.ElementType.ACCEPT)

                continue

            # check if the fromstate is a reducing state
            if from_state.isReducingState():
                reducing_items = from_state.getItemsWhichAreReducingItems()
                if len(reducing_items) > 1:
                    # reduce-reduce conflict
                    print("Reduce - Reduce conflict: ", reducing_items)
                    sys.exit(-1)
                try:
                    reducing_item = next(iter(reducing_items))
                    productionrule_foritem = reducing_item.getCorrespondingProductionRuleForReducingItem()

                    # for all terminal symbols, reduction
                    for terminal in super().getTerminalSymbols():
                        self.addToParseTable(from_state_int, None, productionrule_foritem, terminal, LR0parseTableElement.LR0ParseTableElement.ElementType.REDUCE)
                    continue
                except StopIteration:
                    pass

            for transition_string, to_state in self.transitions[from_state].items():
                to_state_int = self.stateIndexing[to_state]

                if self.parseTableIsNonEmptyForStateAndTransitionString(from_state_int, transition_string):
                    # shift-reduce conflict
                    print("Shift - Reduce conflict: ", from_state_int, " state and symbol ", transition_string)
                    sys.exit(-1)

                if super().isTerminalSymbol(transition_string):
                    # shift
                    self.addToParseTable(from_state_int, to_state_int, None, transition_string, LR0parseTableElement.LR0ParseTableElement.ElementType.SHIFT)
                elif super().isNonterminalSymbol(transition_string):
                    # goto
                    self.addToParseTable(from_state_int, to_state_int, None, transition_string, LR0parseTableElement.LR0ParseTableElement.ElementType.GOTO)

    def printIndexingOfStates(self):
        if not self.stateIndexing:
            print("Compute the indexing before running this function")
            sys.exit(-1)

        print("Total States: ", len(self.stateIndexing))
        print("Indexing of states: ")
        for state, value in self.stateIndexing.items():
            print(f"{value} :-\n{state} ")

    def printIndexingOfStatesToFile(self, path_to_file):
        with open(path_to_file, 'w') as writer:
            if not self.stateIndexing:
                writer.write("Compute the indexing before running this function\n")
                sys.exit(-1)

            writer.write(f"Total States: {len(self.stateIndexing)}\n")
            writer.write("Indexing of maps: \n")

            for state, index in self.stateIndexing.items():
                writer.write(f"{index} :- \n{state}\n")

            writer.write("\n")

    def printTransitions(self):
        if not self.stateIndexing:
            print("Compute the indexing before running this function")
            sys.exit(-1)

        for from_state, transition_map in self.transitions.items():
            from_state_index = self.stateIndexing[from_state]

            for transition_string, to_state in transition_map.items():
                to_state_index = self.stateIndexing[to_state]

                print("From State: ", from_state_index)
                print("Transition String: ", transition_string)
                print("To State: ", to_state_index)
                print()

        print()

    def print_transitions_to_file(self, path_to_file):
        with open(path_to_file, 'w') as writer:
            if not self.stateIndexing:
                writer.write("Compute the indexing before running this function\n")
                sys.exit(-1)

            writer.write("Following are the Transitions: \n")

            str_to_write = ''

            for state, transition_map in self.transitions.items():
                from_state = self.stateIndexing[state]

                for transition_string, to_state in transition_map.items():
                    to_state_value = self.stateIndexing[to_state]

                    str_to_write += "From State: " + str(from_state) + "\n"
                    str_to_write += "Transition String: " + transition_string + "\n"
                    str_to_write += "To State: " + str(to_state_value) + "\n"
                    str_to_write += "\n"

            writer.write(str_to_write)

    def print_parsing_table_to_file(self, path_to_file):
        header_symbols1 = []
        header_symbols1 = super().getTerminalSymbols()         # ACTION
        header_symbols1.extend(super().getNonTerminalSymbols())#GOTO
        visualizeTable.visualizeTableToFile(self.parseTable, path_to_file, header_symbols1)

    def printParsingTable(self):
        header_symbols2 = []
        header_symbols2 = super().getTerminalSymbols()         # ACTION
        header_symbols2.extend(super().getNonTerminalSymbols())#GOTO
        visualizeTable.visualizeTable(self.parseTable, header_symbols2)

    def findLengthOfMaxTableElement(self):
        max_length = float('-inf')

        for map_elem in self.parseTable:
            for element in map_elem.values():
                max_length = max(max_length, len(str(element)))

        return max_length


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

    t.addRule("E' -> E")
    t.addRule("E -> E + T | T")
    t.addRule("T -> T * F | F")
    t.addRule("F -> ( E ) | id")

    # t.printGrammar()

    t.compute_transitions()
    t.computeIndexingOfStates()
    # t.printIndexingOfStates()
    # t.printTransitions()
    t.computeParsingTable()
    # print(t.parseTable)
    for i in t.parseTable:
        for key, value in i.items():
            print(f"{key} {value}", end=" ")
        print()
        print()


if __name__ == "__main__":
    main()
