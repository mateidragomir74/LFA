from parser import parse_nfa
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
import time

console = Console()

OBIECTE = {
    "library": "cheie",
    "lab":     "potiune",
}

CONDITII_IAU = {
    "lab": ("cheie", "Potiunea e incuiata cu un lacat! Iti trebuie o cheie."),
}

DESCRIERI = {
    "start":    "Esti la intrarea in casa vrajitorului.",
    "entrance": "Holul principal. Drumuri in toate directiile.",
    "lab":      "Laboratorul. Miroase a chimicale.",
    "library":  "Biblioteca. Rafturi uriase de carti pana in tavan.",
    "workshop": "Atelierul. Unelte si piese peste tot.",
    "garden":   "Gradina. Aer curat. Simti ca esti aproape de iesire.",
    "final":    "Ai iesit !",
}

OBIECTE_DESCRIERE = {
    "library": "[bold yellow]Vezi o CHEIE pe masa![/bold yellow]",
    "lab":     "[bold yellow]Vezi o POTIUNE inchisa cu lacat![/bold yellow]",
}


POZITII = {
    "final":    (0, 0),
    "garden":   (0, 4),
    "workshop": (2, 4),
    "library":  (2, 8),
    "lab":      (4, 4),
    "entrance": (4, 8),
    "start":    (4, 12),
}

CONEXIUNI = [
    ((0,0), (0,4),  "─"), 
    ((0,4), (2,4),  "│"), 
    ((2,4), (2,8),  "─"), 
    ((2,8), (4,8),  "│"), 
    ((4,4), (4,8),  "─"), 
    ((4,8), (4,12), "─"), 
]

ETICHETE = {
    "final":    (0, 0,  "FIN"),
    "garden":   (0, 4,  "  gdn"),
    "workshop": (2, 4,  "wsh"),
    "library":  (2, 8,  "  lib"),
    "lab":      (4, 4,  "lab"),
    "entrance": (4, 8,  "ent"),
    "start":    (4, 12, "str"),
}


def deseneaza_harta(stare_curenta, inventar):
    rows = 6
    cols = 28
    grid = [[" " for _ in range(cols)] for _ in range(rows)]

    for (r1,c1),(r2,c2),char in CONEXIUNI:
        if r1 == r2:
            for c in range(min(c1,c2)+1, max(c1,c2)):
                grid[r1][c] = char
        else:
            for r in range(min(r1,r2)+1, max(r1,r2)):
                grid[r][c1] = char

    for nume, (r, c) in POZITII.items():
        if nume == stare_curenta:
            grid[r][c] = "@"
        elif nume == "final":
            grid[r][c] = "X"
        else:
            grid[r][c] = "o"

    linii_lista = [list("".join(row)) for row in grid]
    for nome, (r, c, label) in ETICHETE.items():
        er = r + 1 if r < rows - 1 else r - 1
        for i, ch in enumerate(label):
            if c + i < cols and linii_lista[er][c+i] == " ":
                linii_lista[er][c+i] = ch

    linii_finale = ["".join(row) for row in linii_lista]

    text = Text()
    for linie in linii_finale:
        for ch in linie:
            if ch == "@":
                text.append(ch, style="bold yellow")
            elif ch == "X":
                text.append(ch, style="bold green")
            elif ch == "o":
                text.append(ch, style="white")
            elif ch in "─│":
                text.append(ch, style="dim white")
            else:
                text.append(ch, style="dim white")
        text.append("\n")

    text.append("\nInventar: ", style="dim")
    if inventar:
        for obj in inventar:
            text.append(f"[{obj}] ", style="bold cyan")
    else:
        text.append("gol", style="dim")

    return text


def joaca(start_state, final_states, transitions):
    stare_curenta = start_state
    inventar = set()
    obiecte_ramase = dict(OBIECTE)

    console.clear()
    console.print(Panel(
        "[bold cyan]DUNGEON QUEST[/bold cyan]\n"
        "[dim]Gaseste cheia din biblioteca, foloseste-o sa iei potiunea din lab,\n"
        "apoi iesi din dungeon![/dim]\n\n"
        "[dim]Comenzi:[/dim] [bold]west  east  north  south  iau  quit[/bold]",
        box=box.DOUBLE,
        style="cyan"
    ))
    time.sleep(1)

    while True:
        console.clear()

        harta = deseneaza_harta(stare_curenta, inventar)
        console.print(Panel(harta, title="[bold]Harta[/bold]", box=box.SIMPLE))
        console.print("[yellow]@[/yellow] tu   [white]o[/white] camera   [green]X[/green] iesire\n")

        descriere = DESCRIERI.get(stare_curenta, f"Esti in {stare_curenta}.")
        obiect_in_camera = obiecte_ramase.get(stare_curenta)
        if obiect_in_camera:
            descriere += "\n" + OBIECTE_DESCRIERE.get(stare_curenta, "")

        console.print(Panel(
            descriere,
            title=f"[bold]{stare_curenta}[/bold]",
            box=box.ROUNDED
        ))

        if stare_curenta in final_states:
            if "cheie" in inventar and "potiune" in inventar:
                console.print(Panel(
                    "[bold green]Ai iesit cu cheia si potiunea!\nAI CASTIGAT![/bold green]",
                    box=box.DOUBLE, style="green"
                ))
            else:
                lipsesc = []
                if "cheie" not in inventar: lipsesc.append("cheia")
                if "potiune" not in inventar: lipsesc.append("potiunea")
                console.print(Panel(
                    f"[bold red]Iti lipseste: {', '.join(lipsesc)}.\nAI PIERDUT![/bold red]",
                    box=box.DOUBLE, style="red"
                ))
            break

        disponibile = [k for k in transitions.get(stare_curenta, {}).keys() if k != "iau"]
        console.print(f"[dim]Mergi:[/dim] [bold]{' | '.join(disponibile)}[/bold]", end="")
        if obiect_in_camera:
            console.print(f"   [dim]Actiuni:[/dim] [bold yellow]iau[/bold yellow]")
        else:
            console.print()
        console.print()

        comanda = console.input("[bold yellow]> [/bold yellow]").strip().lower()
        console.print()

        if comanda == "quit":
            console.print("[dim]La revedere![/dim]")
            break

        elif comanda == "iau":
            obiect = obiecte_ramase.get(stare_curenta)
            if not obiect:
                console.print("[dim]Nu e nimic de luat aici.[/dim]")
                time.sleep(0.8)
            else:
                conditie = CONDITII_IAU.get(stare_curenta)
                if conditie:
                    item_necesar, mesaj_eroare = conditie
                    if item_necesar not in inventar:
                        console.print(f"[bold red]{mesaj_eroare}[/bold red]")
                        time.sleep(1.2)
                    else:
                        inventar.add(obiect)
                        del obiecte_ramase[stare_curenta]
                        console.print(f"[bold green]Ai luat {obiect}![/bold green]")
                        time.sleep(0.8)
                else:
                    inventar.add(obiect)
                    del obiecte_ramase[stare_curenta]
                    console.print(f"[bold green]Ai luat {obiect}![/bold green]")
                    time.sleep(0.8)

        elif stare_curenta in transitions and comanda in transitions[stare_curenta]:
            destinatii = transitions[stare_curenta][comanda]
            stare_noua = list(destinatii)[0]
            console.print(f"[dim]{stare_curenta}[/dim] [bold cyan]--{comanda}-->[/bold cyan] [bold]{stare_noua}[/bold]")
            time.sleep(0.6)
            stare_curenta = stare_noua

        else:
            console.print("[bold red]Nu poti merge in directia asta![/bold red]")
            time.sleep(0.8)


if __name__ == "__main__":
    reguli = console.input("[bold]Fisier cu reguli:[/bold] ").strip()
    sigma, states, start_state, final_states, transitions = parse_nfa(reguli)
    joaca(start_state, final_states, transitions)
