from parser import parse_pda



def accepta_cuvant(cuvant, start_state, final_states, start_stack, transitions):
    simboluri = cuvant.split() if cuvant.strip() else []
    stiva_dfs = [(start_state, 0, (start_stack,), [(start_state, 0, (start_stack,))])]
    vizitate = set()
    while stiva_dfs:
        stare, pos, stiva_pda, path = stiva_dfs.pop()
        if pos == len(simboluri):
            if (stare in final_states) or (not stiva_pda):
                return True, path
        config = (stare, pos, stiva_pda)
        if config in vizitate:
            continue
        vizitate.add(config)
        if not stiva_pda:
            continue
        top = stiva_pda[-1]
        tranzitii_posibile = []
        if pos < len(simboluri):
            simbol = simboluri[pos]
            cheie = (stare, simbol, top)
            for (dest, push) in transitions.get(cheie, []):
                tranzitii_posibile.append((dest, pos + 1, push))
        cheie_eps = (stare, 'eps', top)
        for (dest, push) in transitions.get(cheie_eps, []):
            tranzitii_posibile.append((dest, pos, push))
        for (dest, new_pos, push) in tranzitii_posibile:
            stiva_fara_top = stiva_pda[:-1]
            if push == 'eps':
                new_stiva = stiva_fara_top
            else:
                new_stiva = stiva_fara_top + tuple(push.split())
            new_path = path + [(dest, new_pos, new_stiva)]
            stiva_dfs.append((dest, new_pos, new_stiva, new_path))
    return False, []



if __name__ == "__main__":
    fisier = input("\nFisier cu definitia PDA: ").strip()
    sigma, stack_alphabet, states, start_state, final_states, start_stack, transitions = parse_pda(fisier)
    while True:
        cuvant = input("Cuvant (simboluri separate prin spatiu, sau 'exit'): ").strip()
        if cuvant.lower() == "exit":
            break
        rezultat, trace = accepta_cuvant(cuvant, start_state, final_states, start_stack, transitions)
        if rezultat:
            print(f"\n '{cuvant}' este ACCEPTAT")
        else:
            print(f"\n'{cuvant}' este RESPINS\n")