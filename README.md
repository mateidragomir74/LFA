# Laboratoare Theory of Computation

## cod_py

### parser.py
Citeste fisierele de definitie pentru DFA, NFA si PDA.
Nu se ruleaza direct, e importat de celelalte fisiere.

---

### dfa.py
Simuleaza un DFA si verifica daca un cuvant e acceptat.

**Input:** numele unui fisier de definitie DFA, apoi cuvinte cu simbolurile separate prin spatiu.
**Output:** `ACCEPTAT` sau `RESPINS` pentru fiecare cuvant introdus.

```
Fisier cu definitia DFA: input.txt
Cuvant: a b a
'a b a' este ACCEPTAT
```

Format fisier:
```
sigma: a, b
states: q0 s, q1, q2 f
transitions:
q0, a -> q1
q1, b -> q2
```

---

### nfa.py
Simuleaza un NFA cu epsilon-tranzitii.

**Input:** numele unui fisier de definitie NFA, apoi cuvinte cu simbolurile separate prin spatiu.
**Output:** `ACCEPTAT` sau `RESPINS` pentru fiecare cuvant introdus.

```
Fisier cu definitia NFA: input.txt
Cuvant: a b
'a b' este ACCEPTAT
```

Format fisier (acelasi ca DFA, cu `eps` pentru epsilon-tranzitii):
```
sigma: a, b, eps
states: q0 s, q1, q2 f
transitions:
q0, a -> q1, q2
q1, eps -> q2
```

---

### pda.py
Simuleaza un PDA prin DFS nedeterminist.

**Input:** numele unui fisier de definitie PDA, apoi cuvinte cu simbolurile separate prin spatiu.
**Output:** `ACCEPTAT` sau `RESPINS` pentru fiecare cuvant introdus.

```
Fisier cu definitia PDA: input.txt
Cuvant: a a b b
'a a b b' este ACCEPTAT
```

Format fisier:
```
sigma: a, b, eps
stack_alphabet: A, Z
states: q0 s, q1, q2 f
start_stack: Z
transitions:
q0, a, Z -> q1, A Z
q1, b, A -> q1, eps
q1, eps, Z -> q2, Z
```

---

### gramatici.py
Citeste o gramatica formala si genereaza cuvinte din limbajul ei prin BFS.

**Input:** numarul maxim de cuvinte, lungimea maxima a unei forme sententiale, numele fisierului cu gramatica.
**Output:** lista cuvintelor generate de gramatica.

```
cat cuvinte?: 5
cat lungime?: 20
Fisier cu gramatica: gramatica.txt

Cuvinte generate (max 5):
   1. ab
   2. aabb
   3. aaabbb
```

Format fisier:
```
VN: S
VT: a b
S: S
P:
S -> a S b | a b
```

---

### jocdungeoncugrafici.py
Joc dungeon bazat pe NFA cu grafici, generat cu AI.
Harta jocului e definita printr-un fisier NFA starile sunt camere, tranzitiile sunt directii de mers.

**Input:** numele fisierului cu harta (format NFA), apoi comenzi de miscare.
**Output:** interfata grafica in terminal cu harta, inventar si descrierea camerei curente.

Comenzi disponibile: `north` `south` `east` `west` `iau` `quit`

Obiectiv: ia cheia din biblioteca, foloseste-o sa iei potiunea din lab, apoi iesi din dungeon cu ambele obiecte.

**Dependinte:**
```bash
pip install rich
```
