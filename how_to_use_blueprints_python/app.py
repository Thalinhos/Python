from flask import Flask # type: ignore
from saidaMultiProdutos.saidaMultiProdutos import smp

app = Flask(__name__)
app.register_blueprint(smp)


@app.route("/")
def hello_world():
    return 'testwe'

if __name__ == "__main__":
    app.run(debug=True)


