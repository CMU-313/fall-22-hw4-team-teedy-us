import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"


    @app.route('/predict')
    def predict():
        #use entries from the query string here but could also use json
        Mjob_health = request.args.get('Mjob_health', None, type=int)
        Fjob_teacher = request.args.get('Fjob_teacher', None, type=int)
        studytime = request.args.get('studytime', None, type=int)
        higher_yes = request.args.get('higher_yes', None, type=int)
        health = request.args.get('health', None, type=int)
        absences = request.args.get('absences', None, type=int)

        if Mjob_health == None or Fjob_teacher == None or studytime == None or higher_yes == None or health == None or absences == None:
            return "Invalid Parameters or Missing Parameters", 400
        elif Mjob_health != 1 and Mjob_health != 0:
            return "Mjob_health has to be either 1 or 0", 400
        elif Fjob_teacher != 1 and Mjob_health != 0:
            return "Fjob_teacher has to be either 1 or 0", 400
        elif studytime < 1 or studytime > 4:
            return "studytime has to be between 1 and 4 inclusive", 400
        elif higher_yes != 1 and higher_yes != 0:
            return "higher_yes is to be either 1 or 0", 400
        elif health < 1 or health > 5:
            return "health has to be between 1 and 5 inclusive", 400
        elif absences < 0 or absences > 93:
            return "absences has to be between 0 and 93 inclusive", 400
    
        data = [[Mjob_health], [Fjob_teacher], [studytime], [higher_yes], [health], [absences]]
        query_df = pd.DataFrame({
            'Mjob': pd.Series(Mjob_health),
            'Fjob': pd.Series(Fjob_teacher),
            'studytime': pd.Series(studytime),
            'higher': pd.Series(higher_yes),
            'health': pd.Series(health),
            'absences': pd.Series(absences)
        })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        response = jsonify(np.ndarray.item(prediction))
        
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response, 200