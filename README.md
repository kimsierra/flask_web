# flask를 이용한 웹서버

가상환경을 구성 하기 위해서 

```powershell
python -m venv flask_web
cd flask_web

Scripts\activate

>>> (flask_web) C:\apps\flask_web>
```

.gitignore 파일 생성후

```powershell
/Lib
/Include
/Scripts
pyvenv.cfg
```

파이썬을 이용해서 웹서버를 구현하기 위해 flask 라이브러리 및 framework 를 사용한다.

pip를 이용해서 설치 한다.

```powershell
pip install flask 
```

라이브러리 설치 목록을 따로 만들어 관리하면 다른 곳에서 프로젝트를 구현할때 편리하다.

```powershell
pip freeze > requirements.txt
```

requirements.txt 에 있는 내용대로 라이브러리를 설치하는 방법은 다음과 같다.

```powershell
pip install -r requirements.txt
```

![image](https://github.com/kbigdata005/web_server/assets/139095086/ae2a74f9-df59-447e-b0ca-249d26dd935e)


위와 같은 구조로 웹서버를 만든다.

![image](https://github.com/kbigdata005/web_server/assets/139095086/15a7cc1e-aaa6-4129-9b7e-47ccc859d982)

다음과 같은 기능을 구현하기 위해

url : http://localhost:5000

method : GET 방식

data : Hello World!! 텍스트 데이터가 클라이언트에 전송되도록 한다.

app.py를 생성후 다음과 같이 코드를 추가한다.

```python
from flask import Flask , render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!!"

if __name__ == '__main__':
    app.run()
```

파이썬에서 index.html 템플릿 파일을 읽어서 문서데이터 변형후 클라이언트에 전송한다.

url : http://localhost:5000

method : GET 방식

data : Hello World!! 에 포함되어 있는 html 문서 데이터를 전송한다.

templates/index.html 파일을 생성후 다음과 같이 코드를 추가

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>웹페이지</title>
</head>
<body>
    <h1>Hello World!!</h1>
</body>
</html>
```

[app.py](http://app.py) 파일을 다음과 같이 수정한다.

```python
from flask import Flask , render_template
....

@app.route('/')
def index():
    
    return render_template('index.html')

...
```

jinja2 문법과 데이터를 연결하는 방법을 알아 보기 위해서 

app.py의 @app.route(’/’)을 다음과 같이 수정한다.

```python
...

@app.route('/')
def index():
    os_info = dict(request.headers)
    print(os_info) 
    return render_template('index.html',header=os_info )

...
```

index.html 또한 header값을 받아서 단순하게 화면에 보여주기 위해서 다음과 같이 수정한다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>웹페이지</title>
</head>
<body>
    <h1>Hello World!!</h1>
    <span> {{ header }} </span>
</body>
</html>
```

위의 코드와 같이  {{ }} 를 포함해서 {% %} , {# #} 등을 이용하여 jinja2 문법에 맞도로 작성을 하면

데이터 값을 탬플릿에 표현할 수 있다.

크롬 브라우저에서  GET 방식으로 요청 했을때 다음과 같은 결과를 볼 수 있다.

![image](https://github.com/kbigdata005/web_server/assets/139095086/b2855f1f-d297-43ad-a4f8-391b49daa147)

다음 과정은 요청 방식에 대해서 GET 방식과 POST 방식을 구분해서 받는 방법을 테스트 하기 위해

url : http://localhost:5000

method: GET 

에서는 위와 같은 페이지가 랜더링 되고

url: http://localhost:5000

method : POST 

일때는 다음과 같은  페이지가 랜더링 되도록 하기 위해 app.py를 다음과 같이 수정한다.

```python
....

@app.route('/' , methods=['GET','POST'])
def index():
    if request.method == "GET":
        os_info = dict(request.headers)
        print(os_info) 
        return render_template('index.html',header=os_info )
    
    elif request.method == "POST":
        return render_template('index.html',header= "안녕하세요 김태경입니다.!!!")
...
```

 [http://localhost:500](http://localhost:500) 으로 get방식으로 요청을 할때

즉 , query로 [http://localhost:5000?name=김태경](http://localhost:5000?name=김태경)&hello=안녕하세요

request 하였을때 

![image](https://github.com/kbigdata005/web_server/assets/139095086/82dd0a92-1bdc-4789-ba3e-f831ac8de359)

위와 같이 나타나기 위해서 

app.py를 수정한다.

```python
...

@app.route('/' , methods=['GET','POST'])
def index():
    if request.method == "GET":
        os_info = dict(request.headers)
        print(os_info) 
        name = request.args.get("name")
        print(name)
        hello = request.args.get("hello")
        print(hello)
        return render_template('index.html',header=f'{name}님 {hello}!!' )

...
```

##### 경로를 파라미터로 처리하는 방법

 url : http://localhost:5000/hello/name

method: GET 

![image](https://github.com/kbigdata009/flask_web/assets/153488538/d413f566-7aaa-4dbb-8317-37d44a9222d7)

 위와 같은 경로에서 name 경로부분에 일반적인 이름을 넣으면 화면에 다음과 같이 보여주게 하기 위하여 

main.py 부분에 다음과 같은 코드를 추가한다.

```python
....

@app.route('/hello/<name>')
def hello(name):
    # print(action , sound)
    action = request.args.get('action')
    sound = request.args.get('sound')
    return render_template('hello.html' 
                           , data = {"name":name ,
                                     "action":action,
                                     "sound":sound} )
...
```



templates/hello.html 파일을 생성 후 다음과 같은 코드를 추가한다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>웹페이지</title>
</head>
<body>
    <h1 style="color: red;">{{ data['name'] }} </h1>
    <span>{{ data['aciton'] }}와 같은 행동을 하고</span>
    <span>{{ data['sound'] }}와 소리를 낸다</span>
</body>
</html>
```





다음 과정은 요청 방식에 대해서 GET 방식과 POST 방식을 구분해서 받는 방법을 테스트 하기 위해

url : http://localhost:8000

method: GET 

에서는 위와 같은 페이지가 랜더링 되고 POST 방식을 구현해 보기위해 

url: http://localhost:8000/login

method : POST 

일때는 다음과 같은  페이지가 랜더링 되도록 하기 위해 main.py를 다음과 같이 수정한다.

```python
....

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
...
```

 http://localhost:500http://localhost:5000/login 으로 get방식으로 요청을 할때

username과 password를 입력하기 위한 페이지가 랜더링 되기 위해 

templates/login.html 파일을 생성후 다음과 같이 코드를 생성한다.



```html
<!DOCTYPE html> 
<html> 

<head> 
	<title>GeeksforGeeks Registration</title> 
	<link rel="stylesheet"
		href="style.css"> 
</head> 

<body> 
	<div class="main"> 
		<h1>GeeksforGeeks</h1> 
		<h3>Enter your login credentials</h3> 
		<form action="/login" method="post"> 
			<label for="first"> 
				Username: 
			</label> 
			<input type="text"
				id="first"
				name="username"
				placeholder="Enter your Username" required> 

			<label for="password"> 
				Password: 
			</label> 
			<input type="password"
				id="password"
				name="password"
				placeholder="Enter your Password" required> 

			<div class="wrap"> 
				<button type="submit"
						onclick="solve()"> 
					Submit 
				</button> 
			</div> 
		</form> 
		<p>Not registered? 
			<a href="#"
			style="text-decoration: none;"> 
				Create an account 
			</a> 
		</p> 
	</div> 
</body> 

</html>

```



다음과 같은 페이지가 랜더링 되는 것을 확인 할 수 있다.

![image](https://github.com/kbigdata005/web_server/assets/153488538/9489acb3-734f-4a65-8f68-557fa7efe13d)

위와 같이 사이트에서 username 부분과 password 부분에 해당하는 곳에 입력하고 submit 버튼을 누루면 

http://127.0.0.1:8000/login 으로 POST 방식으로 입력한 데이트와 함께 request 한다. 

username : moduedu@gmail , password :1234 를 입력후 Submit 버튼 클릭 

이러한 요청이 들어왔을때 서버에서 처리하기 위한 코드를 아래와 같이 작성한다.

main.py에 코드 추가

```python
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username , password)
        return "Success"
    elif request.method == 'GET':
        return render_template('login.html')
```



클라이언트 (즉 , 요청한 웹브라우저) 에서는 다음과 "Success" 라는 글씨가 페이지에 출력 되고 콘솔창에는 다음과 같은 메세시가 출력된다.

```powershell
moduedu 1234
127.0.0.1 - - [01/Feb/2024 16:31:42] "POST /register HTTP/1.1" 200 -
```



이러한 방식으로 

http://127.0.0.1:8000/regiter 경로로 POST 방식으로 요청을 하면 처리하는 기능을 구현하기 위해

다음과 같은 코드를 추가한다.



main.py

```python
@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
        
```



templatets/register.html

```html
<!DOCTYPE html> 
<html> 

<head> 
	<title>Ubion Registration</title> 
	<link rel="stylesheet"
		href="style.css"> 
</head> 

<body> 
	<div class="main"> 
		<h1>UBION</h1> 
		<h3>Enter your register Info</h3>
		<form action="/register" method="post"> 
			<label for="first"> 
				Username: 
			</label> 
			<input type="text"
				id="first"
				name="username"
				placeholder="Enter your Username" required> 

            <label for="first"> 
                Email: 
            </label> 
            <input type="text"
                id="first"
                name="email"
                placeholder="Enter your EMail" required>
            
            <label for="first"> 
                PHONE: 
            </label> 
            <input type="text"
                id="first"
                name="phone"
                placeholder="Enter your phonenumber" required>

			<label for="password"> 
				Password: 
			</label> 
			<input type="password"
				id="password"
				name="password"
				placeholder="Enter your Password" required> 

			<div class="wrap"> 
				<button type="submit"
						onclick="solve()"> 
					Submit 
				</button> 
			</div> 
		</form> 
		<p>Not registered? 
			<a href="#"
			style="text-decoration: none;"> 
				Create an account 
			</a> 
		</p> 
	</div> 
</body> 

</html>

```



main.py

```python
@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        print(username , password)
        return email
    elif request.method == 'GET':
        return render_template('register.html')
```

다음은 위와 같은 코드를 진행한 후 모습이다.

 

![image-20240201160736963](https://github.com/kbigdata005/web_server/assets/153488538/fa9616c1-4397-4029-8b58-99d7f11828b9)

Submit 버튼 클릭시 다음과 같은 페이지가 랜더링 된다.

![image-20240201160837094](https://github.com/kbigdata005/web_server/assets/153488538/c1f0e9f3-e7aa-4890-80b0-d160623e0e5b)





#### DataBase에 저장, 편집 등 기능 구현

DB를 활용하기 위하여 전에 구현하였던 회원가입과 로그인 코드를 활용하여 MongoDB에 저장하고 조회하는 기능을 구현한다.

(mongoDB는 cloud기반에 원격에 data 를 저장할 수 있는 계층형 DB로서 [MONOGDB](https://www.mongodb.com/ko-kr) 여기로 회원가입과 함께 database를 구축해야 한다. )

회원가입페이지에서 username, email, phone,password 를 입력하고 post 방식으로 http://localhost:5000/register 경로로 입력한

데이터와 함께 요청을 보냈을때 서버에서 username, email, phone,password 의 내용을 mongodb에 저장한다.

1. post 방식으로 http://localhost:5000/register 요청이 들어 왔을때 실행되기 위한 데코레이터 

   ```python
   @app.route('/register',  methods=['GET', 'POST'])
   ```

2. 기능구현을 위한 함수를 만들고 , 전달받은 데이터를 각각의 변수에 따로 저장한다.

   mongodb의 'ubion' schema에 users 라는 collection에 저장한다.

   ```python
   from flask import Flask , render_template
   from pymongo import MongoClient
   ...
   
   #mongodb connect
   mongodb_URI = "mongodb+srv://식으로 시작하는  mongodb 접속 주소"
   client = MongoClient(mongodb_URI)
   
   db = client.ubion
   
   ...
   
   
   @app.route('/register',methods=['GET', 'POST'])
   def register():
       if request.method == 'POST':
           users = db.users
           user = users.find_one({"email":email})
               if user == None:
                   hashed_pw = pbkdf2_sha256.hash(password+salt)
                   result = users.insert_one({
                       "username":username,
                       "email":email,
                       "phone":phone,
                       "password":hashed_pw
                   })
   
                   print(result)
                   return redirect("/login" )
   
               else:
                   return redirect("/register" )
       elif request.method == 'GET':
   
   ```



3. 가입하면서 작성한 항목 중에 email 을 중복되지 않게 하기위해 가입한 이메일이 있으면 다시 회원가입창을 보이게 하고 

이메일이 중복이 되지 않으면 mongoDB에  저장하고 login.html이 랜더링 되도록 한다.





4. Login 기능 구현 

로그인 페이지에서 email 과 password를 전달받아 서버에서 mongodb의 ubion 디비의 users 콜랙션에서 입력받은 email 로 조회하고 조회한 email 없으면 회원가입창으로 이동하고 만들고 , 

조회한 이메일이 있을때 입력받은 password와 database 에 조회한 password가 같으면 http://localhost:8000 으로 넘어가게 하고 비밀번호가 틀리면  다시 로그인 창으로 돌아 가도록 한다.

main.py 를 다음과 같은 코드를 추가한다.

```python
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.users
        user = user.find_one({"email":email })
            if user == None:
                return redirect("/register")
            else:
                result = pbkdf2_sha256.verify(password+salt, user['password'] )
                if result:
                    return redirect("/")
                else:
                    return redirect("/login")
    elif request.method == 'GET':
        return render_template('login.html')
    
```







http://localhost:5000/create_list 경로로 GET방식으로 요청했을때 게시판 작성 페이지가 랜더링 되도록 하기 위해

 main.py에 다음과 같은 코드를 추가한다.



```python
...

@app.route('/create_list', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('create_list.html')
    else:
        #create document
        lists = db.lists
        title = request.form['title']
        desc = request.form.get('desc')
        author = request.form.get('author')
        lists.insert_one({
                "title":title,
                "desc" : desc,
                "author":author
            })
        return redirect('/list')
    
    
...
```



templates/list.html 생성후 다음과 같은 코드를 추가한다.

```html
{% extends "layout_list.html" %}
{% block body %}  
        <!-- Masthead-->
        <header class="masthead bg-primary text-white text-center">
           <!-- Begin Page Content -->
           <div class="container">
           <div class="container-fluid">

            <!-- Page Heading -->
            <h1 class="h3 mb-2 text-gray-800">게시판</h1>
            <p class="mb-4">DataTables is a third party plugin that is used to generate the demo table below.
                For more information about DataTables, please visit the <a target="_blank"
                    href="https://datatables.net">official DataTables documentation</a>.</p>

            <!-- DataTales Example -->
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">게시판 리스트</h6>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>TITLE</th>
                                    <th>DESCRIPTION</th>
                                    <th>AUTHOR</th>
                                    <th>기타</th>
                                </tr>
                            </thead>
                            <tfoot>
                                <tr>
                                    <th>ID</th>
                                    <th>TITLE</th>
                                    <th>DESCRIPTION</th>
                                    <th>AUTHOR</th>
                                    <th>기타</th>
                                </tr>
                            </tfoot>
                            <tbody>
                                {% for data in list %}
                                <tr>
                                    <td>{{ loop.index }}</td>
                                    <td><a href="/detail/{{ data['_id'] }}">{{ data['title'] }}</a> </td>
                                    <td>{{ data['desc'] }}</td>
                                    <td> {{ data['author'] }}</td>
                                    <td> 
                                        <a href="/edit/{{ data['_id'] }}"><button class="btn btn-success">Edit</button></a>
                                        <a href="/delete/{{data['_id'] }}"><button class="btn btn-danger" onclick="return confirm('정말 삭제 하시겠습니까?')">Delete</button></a>

                                    </td>
                                    
                                </tr>
                                {% endfor %}
                               
                                
                            </tbody>
                        </table>
                        <a href="/create_list"><button class="btn-primary">Write</button></a>
                    </div>
                </div>
            </div>

        </div>
    </div>
        <!-- /.container-fluid -->
        </header>
   
{% endblock %}
 
        
```



위 코드에서 {% extends "layout_list.html" %} 부분은 다른 페이지에서 공통으로 들어가는 html 코드부분을 따로 파일로 만들어서 

import 하는 방식으로 적용함으로써 코드의 생산성을 향상시킨 부분이다. 



즉, jinja2 문법에서 html 을 상속받는 방법이다.

{% block body %} 

여기에 원하는 코드를 작성함으로써 list.html만에 페이지가 완성이 된다.

{% endblock %}

![image](https://github.com/kbigdata009/recommendations_web/assets/153488538/a7648e32-339a-4b5d-a9fb-54aeb57279ef)

과 같은 페이지가 랜더링 된다.

위에서 작성한 내용이 mongodb 에 저장되는 기능과 함께

http://localhost:5000/list 경로에 GET 방식으로 요청일 들어왔을때 mongodb에서 가져온 리스트 목록을 랜더링 하기 위해

main.py에 다음과 같은 코드를 추가한다.



mongodb에 저장하고 http://localhost:5000/list로 리다이렉트 하는 코드

```python
....
@app.route('/create_list', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('create_list.html')
    else:
        #create document
        lists = db.lists
        title = request.form['title']
        desc = request.form.get('desc')
        author = request.form.get('author')
        lists.insert_one({
                "title":title,
                "desc" : desc,
                "author":author
            })
        return redirect('/list')
....
```



http://localhost:5000/list  랜더링 되는 코드



```python
...

@app.route('/list', methods=['GET', 'POST'])
# @is_logged_in
def list():
    lists = db.lists
    results = lists.find()
    print(results)
    # for i in results:
    #     print(i)
    return render_template('list.html', list = results )
    

...
```



templates/list.html



```html
{% extends "layout_list.html" %}
{% block body %}  
        <!-- Masthead-->
        <header class="masthead bg-primary text-white text-center">
           <!-- Begin Page Content -->
           <div class="container">
           <div class="container-fluid">

            <!-- Page Heading -->
            <h1 class="h3 mb-2 text-gray-800">게시판</h1>
            <p class="mb-4">DataTables is a third party plugin that is used to generate the demo table below.
                For more information about DataTables, please visit the <a target="_blank"
                    href="https://datatables.net">official DataTables documentation</a>.</p>

            <!-- DataTales Example -->
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">게시판 리스트</h6>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>TITLE</th>
                                    <th>DESCRIPTION</th>
                                    <th>AUTHOR</th>
                                    <th>기타</th>
                                </tr>
                            </thead>
                            <tfoot>
                                <tr>
                                    <th>ID</th>
                                    <th>TITLE</th>
                                    <th>DESCRIPTION</th>
                                    <th>AUTHOR</th>
                                    <th>기타</th>
                                </tr>
                            </tfoot>
                            <tbody>
                                {% for data in list %}
                                <tr>
                                    <td>{{ loop.index }}</td>
                                    <td><a href="/detail/{{ data['_id'] }}">{{ data['title'] }}</a> </td>
                                    <td>{{ data['desc'] }}</td>
                                    <td> {{ data['author'] }}</td>
                                    <td> 
                                        <a href="/edit/{{ data['_id'] }}"><button class="btn btn-success">Edit</button></a>
                                        <a href="/delete/{{data['_id'] }}"><button class="btn btn-danger" onclick="return confirm('정말 삭제 하시겠습니까?')">Delete</button></a>

                                    </td>
                                    
                                </tr>
                                {% endfor %}
                               
                                
                            </tbody>
                        </table>
                        <a href="/create_list"><button class="btn-primary">Write</button></a>
                    </div>
                </div>
            </div>

        </div>
    </div>
        <!-- /.container-fluid -->
        </header>
   
{% endblock %}
 
        
```



다음과 같은 페이지가 랜더링 된다.

![image-20240206112327122](C:\Users\SAMSUNG\AppData\Roaming\Typora\typora-user-images\image-20240206112327122.png)



위 페이지에서 Edit와 Delete 기능을 만들기 위해 버튼을 클릭시 

Edit 페이지로 넘어 갈 수 있도록 main.py에 코드를 추가한다.



```python
...

@app.route('/edit/<id>' , methods=['GET', 'POST'])
def edit(list_id):
    if request.method == 'GET':
        lists = db.lists
        result = lists.find_one({'_id':bson.ObjectId(id)})
        print(result)
        return render_template('edit.html', data=result)

...
```



templates/edit.html 파일 생성후 코드 작성

```html
{% extends "layout_list.html" %}
{% block body %}  
        <!-- Masthead-->
        <header class="masthead bg-primary text-white text-center">
           <!-- Begin Page Content -->
           <div class="container">
           <div class="container-fluid">

            <!-- Page Heading -->
            <h1 class="h3 mb-2 text-gray-800">게시판</h1>
            <p class="mb-4">DataTables is a third party plugin that is used to generate the demo table below.
                For more information about DataTables, please visit the <a target="_blank"
                    href="https://datatables.net">official DataTables documentation</a>.</p>

            <!-- DataTales Example -->
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">게시판 편집</h6>
                </div>
                <div class="card-body">
                    <form action="/edit/{{ data['_id'] }}" method="post">
                       title :  <input type="text" name="title" placeholder="title" value="{{ data['title'] }}"><br>
                       desc  : <textarea name="desc" id="" cols="30" rows="10">{{ data['desc'] }}</textarea><br>
                       author : <input type="text" name="author" placeholder="author" value="{{ data['author'] }}"><br>
                       <input type="submit" value="편집제출">

                    </form>
                </div>
            </div>

        </div>
    </div>
        <!-- /.container-fluid -->
        </header>
   
{% endblock %}
 
        
```



![image](https://github.com/kbigdata009/recommendations_web/assets/153488538/7ce23fc5-3e04-4499-8813-a239012fc4de)

위와 같은 페이지에서 수정할 부분을 수정하고 편집제출을 누루면 mongodb가 없데이트 되도록 하는 코드 작성

```python
...

@app.route('/edit/<id>' , methods=['GET', 'POST'])
def edit(list_id):
    if request.method == 'GET':
        lists = db.lists
        result = lists.find_one({'_id':bson.ObjectId(id)})
        print(result)
        return render_template('edit.html', data=result)
    elif request.method == 'POST':
        lists = db.lists
        title = request.form['title']
        desc = request.form.get('desc')
        author = request.form.get('author')
        lists.update_one(
            {'_id' : bson.ObjectId(list_id)},
            {"$set": {
                "title":title,
                "desc" : desc,
                "author":author
            }},
            upsert=False

            )
        
        return redirect('/list')

...
```



GET방식으로  delete기능 구현

main.py 파일 코드 수정



```python
....

@app.route('/delete/<list_id>')
def delete(list_id):
    lists = db.lists
    lists.delete_one({"_id": bson.ObjectId(list_id) })
    return redirect('/list')

...
```



리스트에서 타이틀 제목을 클릭시 상세페이지가 랜더링 되기 위해

main.py 코드 추가

```python
# ids 를 parameter 처리
@app.route('/detail/<id>')
def detail(list_id):
    lists = db.lists
    result = lists.find_one({'_id':bson.ObjectId(id)})
    print(result)
    return render_template('detail.html', data=result)

```



templates/detail.html 작성

```python
{% extends "layout_list.html" %}
{% block body %}  
        <!-- Masthead-->
        <header class="masthead bg-primary text-white text-center">
           <!-- Begin Page Content -->
           <div class="container">
           <div class="container-fluid">

            <!-- Page Heading -->
            <h1 class="h3 mb-2 text-gray-800">게시판</h1>
            <p class="mb-4">DataTables is a third party plugin that is used to generate the demo table below.
                For more information about DataTables, please visit the <a target="_blank"
                    href="https://datatables.net">official DataTables documentation</a>.</p>

            <!-- DataTales Example -->
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">상세 페이지</h6>
                </div>
                <div class="card-body">
                     <!-- Basic Card Example -->
                     <div class="card shadow mb-4">
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">제목</h6>
                        </div>
                        <div class="card-body" style="color: black;">
                            {{ detail['title'] }}
                        </div>
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">내용</h6>
                        </div>
                        <div class="card-body" style="color: black;">
                            {{ detail['desc'] }}
                        </div>
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">글쓴이</h6>
                        </div>
                        <div class="card-body" style="color: black;">
                            {{ detail['author'] }}
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
        <!-- /.container-fluid -->
        </header>
   
{% endblock %}
 
        
```



