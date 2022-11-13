from flask import Flask
from flask import request
import pandas as pd
import sys

import random
data=pd.read_csv('credentials.csv')
app = Flask(__name__)

@app.route("/status")
def status():
        return "1"
@app.route("/welcome/<name>")
def welcome(name):
        return "hello {}".format(name)

@app.route("/permissions/<username>/<password>", methods=["POST"])
def permissions(username, password):
    for i in data.index:
        if (data['username'][i]) == username and str((data['password'][i])) == password:
            return ('v1:'+ str(data['v1'][i])+',v2:'+str(data['v2'][i]))
    return ('Bad username or password')


@app.route("/v1/sentiment", methods=["GET"])
def v1_sentiment():
    user=request.headers.get("Authorization")
        #var = str(user).replace('=',',')
    username,password = user.split('=')
    user_permission= permissions(username,password)
    if user_permission=='Bad username or password':
        return 'utilisateur non autorisé'
    model_v1,model_v2=user_permission.split(',')

    if model_v1!='v1:1':

        return('seul le score des utilisateurs modele v1 est renvoyé')
   
    sentence=request.args.get('sentence')
    score= str(random.uniform(-1.0,1.0))
    return 'le score de votre sentence est :{}'.format(score)
@app.route("/v2/sentiment", methods=["GET"])
def v2_sentiment():
    user=request.headers.get("Authorization")
        #var = str(user).replace('=',',')
    username,password = user.split('=')
    user_permission= permissions(username,password)
    if user_permission=='Bad username or password':
        return 'utilisateur non autorisé'
    model_v1,model_v2=user_permission.split(',')

    if model_v2!='v2:1':

        return('seul le score des utilisateurs modele v2 est renvoyé')

    sentence=request.args.get('sentence')
    score= str(random.uniform(-1.0,1.0))
    return 'le score de votre sentence est :{}'.format(score)    
