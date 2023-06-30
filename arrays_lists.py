lista = [7,4,8,3,1,9]
lista2 = []
lista3 = []


def ordena_lista(lista):
    swap = True
    max_number = None 
    while swap:
        swap = False
        for i in range(len(lista)-1):
            if lista[i] > lista[i+1]:
                max_number = lista[i]
                lista[i] = lista[i+1]
                lista[i+1] = max_number
                swap = True
    return lista

lista2 += ordena_lista(lista) # passa a lista direto
lista3.append(ordena_lista(lista)) # passa a lista dentro da lista

print(lista2)
print(lista3)



