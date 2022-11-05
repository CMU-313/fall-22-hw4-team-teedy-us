from flask import Flask

from app.handlers.routes import configure_routes

# we are looking to use the reasons, activities, and absences attributes to predict

def test_predict_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict?reasons="home"&absences=2&activies=yes'
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.get_data() == b'1\n' #will change this number to what we should actually be predicting

def test_predict_missing_queries():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict?reasons="home"&absences=2'
    
    response = client.get(url)
    assert response.status_code == 400 #should return bad request 400

def test_predict_missing_queries():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict?reasons="home"&absences=2'

    response = client.get(url)
    assert response.status_code == 400 #should return bad request 400

def test_predict_extra_queries():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict?reasons="home"&absences=2&activies=yes&school=GP'

    response = client.get(url)
    assert response.status_code == 400 #should return bad request 400
