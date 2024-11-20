from flask import Flask, render_template, jsonify

app = Flask(__name__)

FLAG = "YBG{cl1ent_s1de_1s_n0t_s4fe}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_flag')
def get_flag():
    return jsonify({'flag': FLAG})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)