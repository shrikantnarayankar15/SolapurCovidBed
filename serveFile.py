from flask import Flask, render_template, request,make_response
# from predict_model import decode_sequence
app = Flask(__name__, template_folder='template')

@app.route('/', methods = ['POST', 'GET'])
def hello():
    csv = None
    with open('solapurMNC.txt', 'rb') as f:
        csv = f.read()
    resp = make_response(csv)
    resp.headers["Content-Disposition"] = "attachment; filename=export.txt"
    resp.headers["Content-Type"] = "text/csv"
    return resp

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)