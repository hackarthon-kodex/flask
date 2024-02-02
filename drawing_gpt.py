from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# OpenAI API 키 설정


# 대화 내용을 저장할 리스트
conversations = []

@app.route('/chat', methods=['POST'])
def add_conversation():
    data = request.json
    conversation = data.get('conversation')
    if conversation:
        conversations.append(conversation)
        return jsonify({"message": "Conversation added successfully"}), 200
    else:
        return jsonify({"message": "No conversation provided"}), 400

@app.route('/summarize', methods=['GET'])
def summarize_conversation():
    # 모든 대화를 하나의 문자열로 결합
    full_conversation = " ".join(conversations)
    if not full_conversation:
        return jsonify({"message": "No conversations to summarize"}), 400

    # OpenAI API를 사용하여 대화 요약
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"너는 한글로 요약해서 대답하는 챗봇이야. 사용자가 한 말을 각자 한 문단의 일기형식으로 요약해서 말해.  육하원칙(누가, 무엇을, 왜, 언제, 어떻게, 어디서)에 해당하는 내용이 있다면 무조건 요약문에 포함시켜줘.",
        temperature=0.5,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text.strip()

    return jsonify({"summary": summary}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    # 클라이언트로부터 대화 데이터를 받습니다.
    
    isFinished = False
    while (isFinished == False):

        data = request.json
        conversation = data.get('conservation')

        # 대화 내용을 포함한 템플릿 생성
        prompt = f"너는 어린아이를 위한 챗봇이야. 아이 다루듯이 착하게 반말로 말해줘. 교육적인 말도 해줘. 대화 내용: {conversation}"
        print(prompt)

        # OpenAI API를 사용하여 대화 요약
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt},
                    {"role": "user", "content": conversation}],
            temperature=0.5,
            max_tokens=100
        )
        print(response)
        summary = response.choices[0].message['content'].strip()

    # 요약된 내용을 클라이언트에게 반환합니다.
    return jsonify({"summary": summary}), 200



if __name__ == '__main__':
    prompt = f"jjin start"
    app.run(host='192.168.56.1', port=5000)
