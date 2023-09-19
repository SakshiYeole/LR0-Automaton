import graphviz

# Define the LR(0) automaton states and transitions
# list of dictionaries with two keys each. Each item in the list represent a state in DFA
# 1st key is the items matched to dictionary of production rules(each prodcution rule is a dict with items as strings and key as teh LHS of prodcution rule) in that state.
# 2nd key is transition matched to dictionary of transitions from that state to some other state on the key element
states = [
    {'items': ['S -> .E', 'E -> .E + T', 'E -> .T', 'T -> .T*F', 'T -> .F'], 'transitions': {'E': 1}},        # 0
    {'items': ['S -> E.'], 'transitions': {}},              # 1
    {'items': ['E -> .E+T', 'E -> .T'], 'transitions': {'E': 3, 'T': 2}}, #2
    {'items': ['E -> E.+T'], 'transitions': {'T': 4}},      # 3
    {'items': ['E -> E+.T'], 'transitions': {'T': 5}},      # 4
    {'items': ['T -> .T*F', 'T -> .F'], 'transitions': {'T': 6, 'F': 7}},   # 5
    {'items': ['T -> T.*F'], 'transitions': {'F': 8}},         # 6
    {'items': ['F -> .(E)', 'F -> .id'], 'transitions': {'E': 9, 'id': 10}},    # 7
    {'items': ['F -> (E.)'], 'transitions': {}},            # 8
    {'items': ['E -> E+.T.'], 'transitions': {}},    # 9
    {'items': ['T -> T.*F.'], 'transitions': {}},           # 10
]

def create_dfa(states):
    # Create a Graphviz Digraph object
    dot = graphviz.Digraph(format='png')

    # Add states and transitions to the graph
    for i, state in enumerate(states):
        items = '\n'.join(state['items'])
        dot.node(str(i), label=items, shape='box')
        for symbol, target_state in state['transitions'].items():
            dot.edge(str(i), str(target_state), label=symbol)

    # Save the generated graph to a file
    dot.save('LR0_automaton')

    # Render the graph to a PNG image
    dot.render('LR0_automaton', view=True)

def main():
    create_dfa(states)

if __name__ == "__main__":
    main()


