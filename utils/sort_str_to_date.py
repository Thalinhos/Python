produtos = db.query_raw("SELECT * FROM ProdutoEntrada;")
for produto in produtos:
    produto['entryDate'] = datetime.strptime(produto['entryDate'], '%d/%m/%Y %H:%M:%S') #strToDate
produtos_ordenados = sorted(produtos, key=lambda x: x['entryDate'], reverse=True) #sortBy'entryDate' in python