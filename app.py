from flask import Flask, render_template, request, redirect
#import pandas as pd
from mongodb import MONGODB
from passlib.hash import pbkdf2_sha256
from movies import GET_REMMAND

app = Flask(__name__)

mongodb_url ='mongodb+srv://root:1234@mydb.1vno0ws.mongodb.net/?retryWrites=true&w=majority'
mongo_db = MONGODB(mongodb_url, 'recommandMovie')

@app.route('/') # localhost:5000에 get방식으로 요청, 5000뒤에 경로가 없을 때는 괄호 문자열 안에 '/' 만 추가
def index():
    query={
            "email":"1@naver.com"
        }
    result = mongo_db.find_data(collection='register', query=query)
    recommader = GET_REMMAND(userId=int(result[0]['userId']))
    mymovies = recommader.my_movies()
    print(mymovies.values)
    return render_template('index.html',data=mymovies.values)

@app.route('/register', methods=['GET','POST'])

def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        register_info = {
            "username":username,
            "email":email,
            "phone":phone,
            "password":pbkdf2_sha256.hash(password)
        }
        mongo_db.insert_data(collection='register', data=register_info)

        return redirect('/')
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    
    elif request.method == "POST":
        
        email = request.form["email"]
        password = request.form["password"]
        query={
            "email":email
        }
        result = mongo_db.find_data(collection='register', query=query)
        #print(result)
        if result == []:
            return redirect('/register')
        
        else:
            #print(result[0]['password'])
            result = pbkdf2_sha256.verify(password, result[0]['password'])
            print(result)
            if result:
                return redirect('/')
            else:
                return redirect('/register')
            
@app.route('/recommander', methods = ['GET', 'POST'])
def recommander():
    mymovie = request.form['mymovie']
    query = {
            "email":"1@naver.com"
        }
    result = mongo_db.find_data(collection='register', query=query)
    recommander = GET_REMMAND(userId=int(result[0]['userId']))
    # print(recommander)
    content_sim_dict = recommander.cosine_similarity(based="content_based" , target_movie=mymovie)
    print(content_sim_dict)
    recommand_movie = recommander.target_weighted_ranking_recommand(content_sim_dict['movieId'] ,content_sim_dict['content_similarity'],content_sim_dict['df'] , 5 )
    print(recommand_movie.values)
    return render_template('recommandmovie.html',movies=recommand_movie.values)
    
        
if __name__ == "__main__":
    app.run(debug=True)