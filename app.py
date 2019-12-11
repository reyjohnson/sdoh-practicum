import uuid
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)

app.secret_key = uuid.uuid4().hex

@app.route('/', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'GET':
        return render_template('form.html', questionnaire=load_questionnaire())

    if request.method == 'POST':
        print(request.form)
        return "OK", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)