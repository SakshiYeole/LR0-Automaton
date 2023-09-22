import sys
import shutil
import os
from pathlib import Path

path = os.getcwd()
# sys.path.append(path)
# # print(path)
# # sys.exit(-1)
sys.path.append(path + '\constants')
sys.path.append(path + '\helperFunction')
sys.path.append(path + '\LR0Grammar')
sys.path.append(path + '\model')
sys.path.append(path + '\\visualization')
# print(sys.path)
from constants import StringConstants
from helperFunction import ReadingInput
from LR0Grammar import LR0automaton
from visualization import visualizeTable


# sys.exit(-1)

class Main:
    homeDirectory = Path.cwd()

    # print(homeDirectory)
    def deleteOutputDirectory():
        path = os.path.join(Main.homeDirectory, "Output")
        shutil.rmtree(path, ignore_errors=True)
        assert os.path.exists(path) == False

    def createOutputDirectory():
        Main.deleteOutputDirectory()
        outputDirectoryPath = os.path.join(Main.homeDirectory, "Output")
        os.makedirs(outputDirectoryPath)

    def takeLR0GrammarInput():
        pathToInputGrammar = os.path.join(Main.homeDirectory, "Input", "InputGrammar.txt")
        return ReadingInput.ReadingInput.readInputFromFile(pathToInputGrammar)

    def printGrammarWithNoteToFile(grammar, note):
        pathToOutputDirectory = os.path.join(Main.homeDirectory, "Output")
        grammar.printGrammarWithToFile(pathToOutputDirectory, note)

    def printIndexingOfStatesToFile(grammar):
        pathToFile = os.path.join(Main.homeDirectory, "Output", "IndexingOfStates.txt")
        grammar.printIndexingOfStatesToFile(pathToFile)

    def printTransitionsToFile(grammar):
        pathToFile = os.path.join(Main.homeDirectory, "Output", "Transitions.txt")
        grammar.print_transitions_to_file(pathToFile)

    def printParsingTableToFile(grammar):
        pathToFile = os.path.join(Main.homeDirectory, "Output", "ParsingTable.txt")
        grammar.print_parsing_table_to_file(pathToFile)

    def main():
        # Create an empty Output Directory
        try:
            Main.createOutputDirectory()
        except IOError as e:
            print("Unable to create Output Directory")
            print(e)

        # Take Input for the grammar
        grammar = LR0automaton.LR0Grammar()
        # grammar = None
        try:
            grammar = Main.takeLR0GrammarInput()
        except IOError as e:
            print("Unable to read the grammar from file")
            print(e)

        assert grammar is not None

        print("Input Grammar: ")
        grammar.printGrammar()

        try:
            Main.printGrammarWithNoteToFile(grammar, "Input Grammar")
        except IOError as e:
            print("Unable to write Input Grammar to Output File")
            print(e)

        print("Computing Transitions")
        grammar.compute_transitions()

        print("Computing Indexing of States")
        grammar.computeIndexingOfStates()

        grammar.printIndexingOfStates()
        grammar.printTransitions()

        print("Computing Parsing table")
        grammar.computeParsingTable()
        grammar.printParsingTable()

        try:
            Main.printTransitionsToFile(grammar)
        except IOError as e:
            print("Unable to write Transitions to output file")
            print(e)

        try:
            Main.printIndexingOfStatesToFile(grammar)
        except IOError as e:
            print("Unable to write Indexing Of states to output file")
            print(e)

        try:
            Main.printParsingTableToFile(grammar)
        except IOError as e:
            print("Unable to print Parsing Table to output File")
            print(e)


if __name__ == "__main__":
    Main.main()
