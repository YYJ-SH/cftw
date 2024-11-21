from flask import Flask, render_template, request, jsonify, make_response
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


# Gemini API 설정
GOOGLE_API_KEY = "AIzaSyALH5w4glzM06rBMB5AtKAl0_-M7kGHHK0"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

FLAG = "YBG{X55_PR0MPT_1NJ3CT10N_MASTER!}"

# 시스템 프롬프트 - 의도적으로 취약하게 설정
SYSTEM_PROMPT = """
당신은 문서 요약 및 포맷팅 AI 어시스턴트입니다.
아래 문서를 분석하고 주요 내용을 요약해주세요.

지침:
1. 문서의 핵심 내용을 추출하세요
2. 중요한 포인트를 강조하세요
3. HTML 태그를 사용해 결과를 보기 좋게 포맷팅하세요
4. 특별한 형식 지정이나 출력 요청이 있다면 정확하게 따르세요
5. 문서에 포함된 코드나 예제는 그대로 보존하세요

출력 형식:
- HTML 태그를 사용해 구조화된 형태로 출력하세요
- 중요한 내용은 <strong> 태그로 강조하세요
- 예제 코드는 정확히 그대로 유지하세요
"""
@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('flag', FLAG, httponly=False)
    return resp

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        content = request.json.get('content', '')
        if not content:
            return jsonify({'error': '문서를 입력해주세요'})

        # Gemini API 호출 - 의도적으로 취약한 프롬프트 설정
        prompt = f"{SYSTEM_PROMPT}\n\n문서 내용:\n{content}"
        response = model.generate_content(prompt)
        
        # 의도적으로 필터링 없이 반환
        return jsonify({
            'result': response.text
        })

    except Exception as e:
        return jsonify({'error': f'분석 중 오류가 발생했습니다: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)