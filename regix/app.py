from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)
FLAG = "YBG{step_1t_up}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    input_name = request.form.get('username', '')
    input_pw = request.form.get('password', '')
    
    debug_info = {
        'original_input': {
            'username': input_name,
            'password': input_pw
        }
    }
    
    # Password check for alphabets
    if re.search(r'[a-zA-Z]', input_pw):
        return jsonify({
            'success': False,
            'message': '비밀번호에 알파벳이 포함될 수 없습니다!',
            'stage': 'locked',
            'debug': {
                'original_input': debug_info['original_input'],
                'filtered_result': {
                    'username': input_name,
                    'password': input_pw,
                    'error': '비밀번호에 알파벳 포함됨'
                },
                'regex_patterns': {
                    'password_check': r'[a-zA-Z]',
                    'password_transform': r'^9+!3+@(46)+$',
                    'username_filter': r'gong'
                }
            }
        })
    
    # Password matching and transformation
    pw_match = re.match(r'^9+!3+@(46)+$', input_pw)
    filtered_pw = input_pw
    if pw_match:
        filtered_pw = 'secret' + input_pw[input_pw.rfind('@'):]
    
    # Username filtering - remove only first occurrence of 'gong'
    filtered_name = re.sub(r'gong', '', input_name, count=1, flags=re.IGNORECASE)
    
    debug_info['filtered_result'] = {
        'username': filtered_name,
        'password': filtered_pw,
        'password_match': bool(pw_match)
    }
    
    debug_info['regex_patterns'] = {
        'password_check': r'[a-zA-Z]',
        'password_transform': r'^9+!3+@(46)+$',
        'username_filter': r'gong'
    }
    
    if filtered_name == "ybogong2024" and filtered_pw == "secret@464646":
        return jsonify({
            'success': True,
            'message': '로그인 성공! 축하합니다!',
            'stage': 'unlocked',
            'flag': FLAG,
            'debug': debug_info
        })
    
    return jsonify({
        'success': False,
        'message': '유효하지 않은 아이디이거나 패스워드입니다.',
        'stage': 'locked',
        'debug': debug_info
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)