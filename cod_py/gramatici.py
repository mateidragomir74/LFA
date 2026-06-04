
from collections import deque


def citeste_gramatica(fisier):
    vn, vt, start, productii = set(), set(), None, {}
    with open(fisier, 'r') as f:
        lines = [linie.strip() for linie in f]
    in_productii = False
    for linie in lines:
        if not linie or linie.startswith('#'):
            continue
        if linie.startswith('VN:'):
            vn = set(linie[3:].split())
        elif linie.startswith('VT:'):
            vt = set(linie[3:].split())
        elif linie.startswith('S:'):
            start = linie[2:].strip()
        elif linie.startswith('P:'):
            in_productii = True
        elif in_productii and '->' in linie:
            stanga, dreapta = linie.split('->', 1)
            neterminal = stanga.strip()
            alternative = dreapta.split('|')
            for alt in alternative:
                simboluri = alt.split()
                if not simboluri:
                    simboluri = ['eps']
                productii.setdefault(neterminal, []).append(simboluri)
    return vn, vt, start, productii


def genereaza_cuvinte(vn, start, productii, MAX_CUVINTE, MAX_LUNGIME):
    cuvinte = []
    vizitat = set()
    coada = deque([[start]])
    while coada and len(cuvinte) < MAX_CUVINTE:
        forma = coada.popleft()
        if tuple(forma) in vizitat:
            continue
        vizitat.add(tuple(forma))
        idx = next((i for i, s in enumerate(forma) if s in vn), None)
        if idx is None:
            cuvant = ''.join(s for s in forma if s != 'eps')
            if cuvant not in cuvinte:
                cuvinte.append(cuvant)
            continue
        neterminal = forma[idx]
        for productie in productii.get(neterminal, []):
            forma_noua = forma[:idx] + productie + forma[idx + 1:]
            if len(forma_noua) <= MAX_LUNGIME:
                coada.append(forma_noua)
    return cuvinte


if __name__ == "__main__":
    MAX_CUVINTE = int(input("cat cuvinte?:"))
    MAX_LUNGIME = int(input("cat lungime?:"))
    fisier = input("\nFisier cu gramatica: ").strip()
    vn, vt, start, productii = citeste_gramatica(fisier)
    print()
    print(f"Cuvinte generate (max {MAX_CUVINTE}):\n")
    cuvinte = genereaza_cuvinte(vn, start, productii, MAX_CUVINTE, MAX_LUNGIME)
    for i, cuvant in enumerate(cuvinte, 1):
        print(f"  {i:>2}. {cuvant or 'eps'}")
    print(f"\nTotal: {len(cuvinte)} cuvinte.")
