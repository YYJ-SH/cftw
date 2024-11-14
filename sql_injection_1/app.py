from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def execute_query(query):
    """DB 쿼리 실행 함수"""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result

@app.route('/')
def index():
    """로그인 페이지 렌더링"""
    return render_template('index.html')  # uid와 pwd 입력 폼 제공

@app.route('/login', methods=['POST'])
def login():
    """로그인 처리 및 결과 페이지 렌더링"""
    uid = request.form.get('uid')
    pwd = request.form.get('pwd')
    
    # 취약한 SQL 쿼리
    query = f"SELECT * FROM users WHERE uid='{uid}' and upw='{pwd}';"
    result = execute_query(query)
    
    if result:
        # 로그인 성공
        return render_template('result.html', message="Login successful!", result=result)
    else:
        # 로그인 실패
        return render_template('result.html', message="Login failed! Invalid UID or PWD.", result=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
