def parse_dfa(filepath):
    sigma = set()
    states = set()
    start_state = None
    final_states = set()
    transitions = {}
    current_section = None
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    for line in lines:
        if line.startswith("sigma:"):
            elemente = line.replace("sigma:", "").split(",")
            sigma = {e.strip() for e in elemente if e.strip()}
        elif line.startswith("states:"):
            elemente = line.replace("states:", "").split(",")
            for element in elemente:
                componente = element.strip().split()
                if not componente:
                    continue
                nume_stare = componente[0]
                states.add(nume_stare)
                if 's' in componente[1:]:
                    start_state = nume_stare
                if 'f' in componente[1:]:
                    final_states.add(nume_stare)
        elif line.startswith("transitions:"):
            current_section = "transitions"
        elif current_section == "transitions":
            stanga, dreapta = line.split("->")
            parti = stanga.split(",")
            stare_sursa = parti[0].strip()
            simbol = parti[1].strip()
            stare_dest = dreapta.strip()
            if stare_sursa not in transitions:
                transitions[stare_sursa] = {}
            transitions[stare_sursa][simbol] = stare_dest
    return sigma, states, start_state, final_states, transitions

def parse_nfa(filepath):
    sigma = set()
    states = set()
    start_state = None
    final_states = set()
    transitions = {}
    current_section = None
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    for line in lines:
        if line.startswith("sigma:"):
            elemente = line.replace("sigma:", "").split(",")
            sigma = {e.strip() for e in elemente}
        elif line.startswith("states:"):
            elemente = line.replace("states:", "").split(",")
            for element in elemente:
                componente = element.strip().split()
                nume_stare = componente[0]
                states.add(nume_stare)
                if 's' in componente[1:]:
                    start_state = nume_stare
                if 'f' in componente[1:]:
                    final_states.add(nume_stare)
        elif line.startswith("transitions:"):
            current_section = "transitions"
        elif current_section == "transitions":
            stanga, dreapta = line.split("->")
            sursa_simbol = stanga.split(",")
            stare_sursa = sursa_simbol[0].strip()
            simbol = sursa_simbol[1].strip()
            stari_destinatie = {s.strip() for s in dreapta.split(",")}
            if stare_sursa not in transitions:
                transitions[stare_sursa] = {}
            if simbol not in transitions[stare_sursa]:
                transitions[stare_sursa][simbol] = set()
            transitions[stare_sursa][simbol].update(stari_destinatie)
    return sigma, states, start_state, final_states, transitions


def parse_pda(filepath):
    sigma = set()
    stack_alphabet = set()
    states = set()
    start_state = None
    final_states = set()
    start_stack = None
    transitions = {}
    current_section = None
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    for line in lines:
        if line.startswith("sigma:"):
            elemente = line.replace("sigma:", "").split(",")
            sigma = {e.strip() for e in elemente if e.strip()}
        elif line.startswith("stack_alphabet:"):
            elemente = line.replace("stack_alphabet:", "").split(",")
            stack_alphabet = {e.strip() for e in elemente if e.strip()}
        elif line.startswith("states:"):
            elemente = line.replace("states:", "").split(",")
            for element in elemente:
                componente = element.strip().split()
                if not componente:
                    continue
                nume_stare = componente[0]
                states.add(nume_stare)
                if 's' in componente[1:]:
                    start_state = nume_stare
                if 'f' in componente[1:]:
                    final_states.add(nume_stare)
        elif line.startswith("start_stack:"):
            start_stack = line.replace("start_stack:", "").strip()
        elif line.startswith("transitions:"):
            current_section = "transitions"
        elif current_section == "transitions":
            stanga, dreapta = line.split("->")
            parti_stanga = [p.strip() for p in stanga.split(",")]
            stare_sursa = parti_stanga[0]
            simbol_input = parti_stanga[1]
            top_stiva = parti_stanga[2]
            parti_dreapta = [p.strip() for p in dreapta.split(",")]
            stare_dest = parti_dreapta[0]
            push_string = parti_dreapta[1] if len(parti_dreapta) > 1 else "eps"
            cheie = (stare_sursa, simbol_input, top_stiva)
            if cheie not in transitions:
                transitions[cheie] = []
            transitions[cheie].append((stare_dest, push_string))
    return sigma, stack_alphabet, states, start_state, final_states, start_stack, transitions