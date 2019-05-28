from flask import Flask, render_template, request


import src.app.backend as backend


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    names = backend.read_names()
    return render_template('home.html', names=names)


@app.route('/save', methods=['POST'])
def save():
    attending = request.form.to_dict().keys()
    names = backend.read_names()
    attendance = [
        1 if str(person) in attending else 0
        for person in range(len(names))]
    backend.update_attendance(attendance)
    return ('', 204)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080)
