from flask import Blueprint, render_template # type: ignore
from utils.utils import rawQuery

smp = Blueprint('saidaMultiProdutos', __name__, template_folder='./templates')

@smp.route('/retirarProdutos')
def showProductsToExtract():
    produtos = rawQuery("SELECT * FROM ProdutosTotal;")
    print(produtos)
    return render_template('saidaMultiProdutos.html', produtos=produtos)