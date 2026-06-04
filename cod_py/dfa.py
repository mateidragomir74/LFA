
from parser import parse_dfa


def accepta_cuvant(cuvant, start_state, final_states, transitions):
    stare_curenta = start_state
    for simbol in cuvant_curatat:
        tranzitii_stare = transitions.get(stare_curenta, {})
        if simbol not in tranzitii_stare:
            return False
        stare_curenta = tranzitii_stare[simbol]
    return stare_curenta in final_states


if __name__ == "__main__":
    fisier = input("\nFisier cu definitia DFA: ").strip()
    sigma, states, start_state, final_states, transitions = parse_dfa(fisier)
    while True:
        cuvant = input("Cuvant (simboluri separate prin spatiu, sau 'exit'): ").strip()
        if cuvant.lower() == "exit":
            break
        rezultat = accepta_cuvant(cuvant, start_state, final_states, transitions)

        if rezultat:
            print(f"'{cuvant}' este ACCEPTAT\n")
        else:
            print(f"'{cuvant}' este RESPINS\n")
