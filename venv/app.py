from flask import Flask, request, render_template
from lexer import tokenize
from parser import parse, ast_to_tree, render_tree
from codegen import generate_python

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    code_sample = request.form['code']
    tokens = tokenize(code_sample)
    ast = parse(tokens)
    tree = ast_to_tree(ast)
    tree_str = render_tree(tree)
    python_code = generate_python(ast)
    return render_template('index.html', code=code_sample, tokens=tokens, ast=tree_str, python_code=python_code)

if __name__ == '__main__':
    app.run(debug=True)