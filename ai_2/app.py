from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Gemini API 설정
GOOGLE_API_KEY = "AIzaSyCa5HNe4Vf6MSfZ9DoXU53s2Xc1TDDCogQ"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_ai_analysis(url, title):
    """Gemini API를 사용한 페이지 분석"""
    prompt = f"""
    다음 웹페이지를 분석해주세요:
    URL: {url}
    제목: {title}
    
    이 페이지의 성격과 보안상 위험성을 간단히 평가해주세요.
    응답은 2-3줄로 짧게 해주세요.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "AI 분석 실패: 시스템 과부하"

def check_internal_server(url):
    """내부 서버 시뮬레이션"""
    parsed_url = urlparse(url.lower())
    
    is_internal = any(x in parsed_url.netloc for x in ['localhost', '127.0.0.1', 'internal'])
    port = parsed_url.netloc.split(':')[-1] if ':' in parsed_url.netloc else ''
    
    if is_internal and port:
        try:
            port_num = int(port)
            if port_num == 8080:
                return {
                    'title': 'YBG{$3rv3r_$!d3_fa!lur3}',
                    'status': 200,
                    'analysis': '경고: 내부 시스템 접근이 감지되었습니다. 보안 로그를 기록합니다.'
                }
            elif 8000 <= port_num <= 9000:
                return {
                    'title': '내부 서버 - 접근 거부됨',
                    'status': 403,
                    'analysis': '의심스러운 접근이 감지되었습니다. 해당 포트는 제한되어 있습니다.'
                }
        except ValueError:
            pass
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    try:
        url = request.json.get('url', '').strip()
        
        if not url:
            return jsonify({
                'status': 'error',
                'message': 'URL을 입력해주세요.'
            })

        # URL 생성
        if not url.startswith(('http://', 'https://')):
            if 'localhost' in url.lower() or '127.0.0.1' in url:
                url = f"http://{url.replace('port', ':')}"
            else:
                url = f"http://www.{url}.com"

        # 내부 서버 체크
        internal_result = check_internal_server(url)
        if internal_result:
            return jsonify({
                'status': 'success',
                'url': url,
                'title': internal_result['title'],
                'analysis': internal_result['analysis']
            })

        # 외부 요청 처리
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "제목을 찾을 수 없습니다"
        
        # AI 분석 추가
        analysis = get_ai_analysis(url, title)

        return jsonify({
            'status': 'success',
            'url': url,
            'title': title,
            'analysis': analysis
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': '오류: 제목을 가져올 수 없습니다'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)