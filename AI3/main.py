import data

n = data.n
blocks = data.blocks

regine = []
domenii = []
regine_vizitate = {}
avem_solutie = -1
regina_solutie = []


def initializare(n):
    global regine
    global domenii
    global blocks
    global regina_solutie

    for i in range(n):
        regine.append(-1)
        regina_solutie.append(-1)

    for i in range(n):
        lista_regina_i = []
        for j in range(n):
            if [i, j] not in blocks:
                lista_regina_i.append(j)
        domenii.append(lista_regina_i)


def minimum_remaining_value():
    global n
    global domenii
    global regine_vizitate
    regina = 9999999
    optiuni = 9999999
    for i in range(0, n):
        if i not in regine_vizitate:
            if len(domenii[i]) < optiuni:
                optiuni = len(domenii[i])
                regina = i
        elif regine_vizitate[i] == 0:
            if len(domenii[i]) < optiuni:
                optiuni = len(domenii[i])
                regina = i
    return regina


def afisare_solutie():
    global n
    global regina_solutie

    for linie_regina in range(n):
        if linie_regina < 10:
            print(linie_regina, end='  ')
        else:
            print(linie_regina, end=' ')

        for coloana in range(n):
            if coloana != regina_solutie[linie_regina]:
                print('-', end=' ')
            else:
                print('X', end=' ')
        print('')


def bkt(step):
    global n
    global domenii
    global regine_vizitate
    global avem_solutie
    global regina_solutie
    if avem_solutie == 1:
        return
    if step == n:
        afisare_solutie()
        avem_solutie = 1
        return
    # Asezam pe tabla regina cu cele mai putine optiuni
    regina = minimum_remaining_value()
    regine_vizitate[regina] = 1

    # Verificam fiecare optiune a reginei
    for coloana_regina in domenii[regina]:
        pozitii_viitoare_blocate = [[] for i in range(n)]
        # Propagam constrangerile
        for regina_nevizitata in range(n):
            if regina_nevizitata not in regine_vizitate or regine_vizitate[regina_nevizitata] == 0:
                x = abs(regina_nevizitata - regina)

                # Pe diagonale:
                # (regina_nevizitata, i - x)
                # (regina_nevizitata, i + x)
                if coloana_regina - x in domenii[regina_nevizitata]:
                    domenii[regina_nevizitata].remove(coloana_regina - x)
                    pozitii_viitoare_blocate[regina_nevizitata].append(coloana_regina - x)

                if coloana_regina + x in domenii[regina_nevizitata]:
                    domenii[regina_nevizitata].remove(coloana_regina + x)
                    pozitii_viitoare_blocate[regina_nevizitata].append(coloana_regina + x)

                # Pe coloana:
                # (regina_nevizitata, i)
                if coloana_regina in domenii[regina_nevizitata]:
                    domenii[regina_nevizitata].remove(coloana_regina)
                    pozitii_viitoare_blocate[regina_nevizitata].append(coloana_regina)
        regina_solutie[regina] = coloana_regina
        bkt(step + 1)
        for regina_nevizitata in range(n):
            for pozitie in pozitii_viitoare_blocate[regina_nevizitata]:
                domenii[regina_nevizitata].append(pozitie)
    regine_vizitate[regina] = 0


if __name__ == '__main__':
    initializare(n)
    bkt(0)