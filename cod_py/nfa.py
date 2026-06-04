from parser import parse_nfa
from collections import deque

def calc_eps(stari_curente, transitions):
    stari = set(stari_curente)
    coada = deque(stari_curente)
    while coada:
        stare = coada.popleft()
        for urmatoare in transitions.get(stare, {}).get('eps', set()):
            if urmatoare not in stari:
                stari.add(urmatoare)
                coada.append(urmatoare)
    return stari


def accepta_cuvant(cuvant, start_state, final_states, transitions):
    stari_curente = calc_eps({start_state}, transitions)
    for simbol in cuvant.split():
        stari_urmatoare = set()
        for stare in stari_curente:
            stari_urmatoare.update(
                transitions.get(stare, {}).get(simbol, set())
            )
        if not stari_urmatoare:
            return False
        stari_curente = calc_eps(stari_urmatoare, transitions)
    return bool(stari_curente & final_states)



if __name__ == "__main__":
    fisier = input("\nFisier cu definitia NFA: ").strip()
    sigma, states, start_state, final_states, transitions = parse_nfa(fisier)
    while True:
        cuvant = input("Cuvant (simboluri separate prin spatiu, sau 'exit'): ").strip()
        if cuvant.lower() == "exit":
            break
        rezultat = accepta_cuvant(cuvant, start_state, final_states, transitions)
        if rezultat:
            print(f"'{cuvant}' este ACCEPTAT\n")
        else:
            print(f"'{cuvant}' este RESPINS\n")
