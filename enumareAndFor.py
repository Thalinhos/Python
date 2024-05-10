alunos = [
    {'nome': 'henrique', 'notas': [6, 4, 4, 6, 10]},
    {'nome': 'zodd', 'notas': [6, 4, 4, 6, 9]},
    {'nome': 'thalisson', 'notas': [6, 5, 4, 6, 9]},
    {'nome': 'william', 'notas': [6, 4.9, 3.4, 6.35, 9]},
    ]

for indice, valor in enumerate(alunos):
    media = 0
    for nota in valor['notas']:
        media = media + nota
    media = round(media / len(valor['notas']), 2)

    if media >= 5.90:
        print(valor['nome'], 'Está Aprovado', media)
    else:
        print(valor['nome'], 'Reprovado', media)



