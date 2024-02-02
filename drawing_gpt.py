from flask import Flask, request, jsonify, redirect, url_for
import openai, time

app = Flask(__name__)

# 객체 4개 목록은 초반에 return 되어 클라이언트에서 관리된다고 가정
# 클라이언트에서 질문 키워드를 넘겨줌
# 주고 받은 내용 한 번에 클라 -> 백 전달하여 요약 

# OpenAI API 키 설정


@app.route('/api/chat/system', methods=['POST'])
def from_system():
    data = request.json
    issue = data.get('input_issue')

    # 대화 내용을 포함한 템플릿 생성
    prompt = f"너는 어린아이를 위한 챗봇이야. 아이 다루듯이 착하게 반말로 말해줘. 교육적인 말도 해줘. 대화 내용: 아이가 {issue} 그림을 그렸는데, 자연스럽게 물어봐줘"

    # OpenAI API를 사용하여 대화 요약
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.5,
        max_tokens=100
    )

    # 요약된 내용을 클라이언트에게 반환합니다.
    return jsonify({"system": response.choices[0].message['content'].strip()}), 200



@app.route('/api/chat/kid', methods=['POST'])
def from_kid():
    data = request.json
    system = data.get('system')
    conversation = data.get('conversation')


    # 대화 내용을 포함한 템플릿 생성
    prompt = f"너는 어린아이를 위한 챗봇이야. 아이 다루듯이 착하게 반말로 말해줘. 교육적인 말도 해줘. 대화 내용: {system}에 대해 {conversation} 이렇게 답장했는데, 요약해줘!"


    # OpenAI API를 사용하여 대화 요약
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt},
                {"role": "user", "content": conversation}],
        temperature=0.5,
        max_tokens=100
    )
    summary = response.choices[0].message['content'].strip()
    return jsonify({"summary": summary}), 200



if __name__ == '__main__':
    app.run(host='192.168.56.1', port=5000)
