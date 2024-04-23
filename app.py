from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/') # localhost:5000에 get방식으로 요청, 5000뒤에 경로가 없을 때는 괄호 문자열 안에 '/' 만 추가
def index():
    print(request.headers)
    return render_template('index.html',data=request.headers)

if __name__ == "__main__":
    app.run(debug=True)