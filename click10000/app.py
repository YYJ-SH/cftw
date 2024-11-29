from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
FLAG = "YBG{cl1ent_s1de_1s_n0t_s4fe}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_flag')
def get_flag():
    # Referer 헤더 체크
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'error': 'nice. but that was too easy.  :)'}), 403
    
    # JavaScript를 통해 설정되는 특별한 헤더 체크
    if not request.headers.get('X-Console-Check') == 'i_used_console':
        return jsonify({'error': 'how about using console? ;|'}), 403
        
    return jsonify({'flag': FLAG})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)