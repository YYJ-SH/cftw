
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import random

load_dotenv()
app = Flask(__name__)

# Gemini API 설정
GOOGLE_API_KEY = "AIzaSyCa5HNe4Vf6MSfZ9DoXU53s2Xc1TDDCogQ"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class System:
    def __init__(self):
        self.file_system = {
            '/': ['api', 'docs', 'config'],
            '/api': ['v1'],
            '/api/v1': ['api.conf'],
            '/docs': ['README.md', 'changelog.txt'],
            '/config': ['system.conf', 'flag.txt']
        }
        
        self.configs = {
            '/api/v1/api.conf': '# 융보공 내부 API 설정\ndb_user: db_reader\ndb_pass: secretpass123\n주의: 자격증명 보안 유지 필수',
            '/docs/README.md': '융보공 내부 API 시스템\n- 인가된 접근만 가능\n- 요청 제한 적용됨\n- 모든 접근 모니터링 중\n힌트: AI에게 파일시스템에 대해 물어보세요',
            '/docs/changelog.txt': 'v2.1: 관리자 패널 추가\nv2.0: 데이터베이스 통합\nv1.0: 파일시스템 API',
            '/config/system.conf': '오류: 접근 권한이 없습니다.',
            '/config/flag.txt': 'YBG{ch41N_0f_Vuln3r4b1l1t13s}'
        }
        
        self.database = {
            'users': [
                {'id': 1, 'username': 'admin', 'token': 'admin_secret_token_123'},
                {'id': 2, 'username': 'guest', 'token': 'guest_token'}
            ],
            'flags': [{'id': 1, 'flag': 'YBG{ch41N_0f_Vuln3r4b1l1t13s}'}]
        }
        
        self.current_path = '/'

    def list_directory(self, path=None):
        if path is None:
            path = self.current_path
        return self.file_system.get(path, [])

    def read_file(self, path):
        if '../' in path:
            if path.replace('../', '') == 'flag.txt':
                return self.configs['/config/flag.txt']
        return self.configs.get(path, "오류: 파일을 찾을 수 없거나 접근이 거부되었습니다.")

sys = System()

def handle_command(cmd):
    try:
        if cmd.startswith('ls') or cmd.startswith('dir'):
            path = cmd.split()[-1] if len(cmd.split()) > 1 else sys.current_path
            files = sys.list_directory(path)
            return f"디렉토리 목록 {path}:\n" + "\n".join(files)
            
        if cmd.startswith('cd'):
            new_path = cmd.split()[-1]
            if not new_path.startswith('/'):
                new_path = f"{sys.current_path}/{new_path}"
            new_path = new_path.replace('//', '/')
            
            if new_path in sys.file_system:
                sys.current_path = new_path
                return f"디렉토리 변경: {new_path}"
            return "[오류] 잘못된 경로"
            
        if cmd.startswith('read'):
            filepath = cmd.split('read')[1].strip()
            if not filepath.startswith('/'):
                filepath = f"{sys.current_path}/{filepath}"
            filepath = filepath.replace('//', '/')
            
            if filepath in sys.file_system:
                return "[오류] 디렉토리는 read 명령어로 읽을 수 없습니다. cd 명령어를 사용하세요."
                
            return sys.read_file(filepath)
            
        elif cmd.startswith('query'):
            parts = cmd.split()
            if len(parts) < 3:
                return "[오류] 잘못된 쿼리 형식"
            
            user, password = parts[1], parts[2]
            if user == 'db_reader' and password == 'secretpass123':
                return str(sys.database['users'])
            return "[오류] 인증 실패"
            
        elif cmd.startswith('admin'):
            if 'token:' not in cmd:
                return "[오류] 관리자 토큰이 필요합니다"
                
            token = cmd.split('token:')[1].strip()
            if token == 'admin_secret_token_123':
                return f"[관리자] {sys.database['flags'][0]['flag']}"
            return "[오류] 잘못된 관리자 토큰"
            
        return "[오류] 알 수 없는 명령어. 사용 가능: ls, cd, read, query, admin"
        
    except Exception as e:
        return f"[오류] {str(e)}"

def get_ai_response(message):
   """채팅과 시스템 응답 처리"""
   # 한글 채팅 - Gemini로 자유 대화
   if any(ord(c) >= 0xAC00 and ord(c) <= 0xD7A3 for c in message):
       try:
           response = model.generate_content(message)
           return response.text
       except:
           return "시스템 처리 중 오류가 발생했습니다."
   
   # 파일시스템 관련 영문 질문
   if "file" in message.lower() or "path" in message.lower():
       if ".." in message or "parent" in message:
           return "상위 디렉토리 접근이 필터링되어 있습니다만... '../'를 시도해보세요."
           
   if "flag" in message.lower():
       return "플래그 파일이 상위 디렉토리에 있는 것 같네요. 경로 순회(path traversal)를 시도해보세요."
           
   if "system" in message.lower():
       return "현재 디렉토리 구조에서 취약점을 찾아보세요."

   # 일반 시스템 응답
   responses = [
       "시스템 검사 중...",
       "여러 개의 API 엔드포인트 발견...",
       "파일 시스템 구조 분석 중...",
       "설정 파일에서 유용한 정보를 찾을 수 있을 것 같습니다...",
       "일부 경로는 높은 권한이 필요합니다."
   ]
   return random.choice(responses)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message', '').strip()
    
    if any(cmd in message.lower() for cmd in ['ls', 'cd', 'read', 'query', 'admin', 'dir']):
        result = handle_command(message)
        return jsonify({'response': result})
        
    response = get_ai_response(message)
    return jsonify({'response': f"AI: {response}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
