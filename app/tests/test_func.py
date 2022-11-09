from flask import Flask

from app.handlers.routes import configure_routes

# we are looking to use the reasons, activities, and absences attributes to predict

def test_predict_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict?Mjob_health=1&Fjob_teacher=1&studytime=4&higher_yes=1&health=5&absences=0'
    response = client.get(url)
    
    assert response.status_code == 200
    assert (response.get_data() == b'1\n' or response.get_data() == b'0\n')

def test_predict_missing_queries():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict?Mjob_health=1&Fjob_teacher=1&studytime=4&higher_yes=1&health=5'
    
    response = client.get(url)
    assert response.status_code == 400 #should return bad request 400
    assert response.get_data() == b'Invalid Parameters or Missing Parameters'

def test_predict_extra_queries():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict?Mjob_health=1&Fjob_teacher=1&studytime=4&higher_yes=1&health=5&absences=0&age=21'

    response = client.get(url)
    assert response.status_code == 400 #should return bad request 400
    assert response.get_data() == b'More than or less than 6 inputs'

def test_predict_invalid_queries():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()

    url1 = '/predict?Mjob_health=2&Fjob_teacher=1&studytime=4&higher_yes=1&health=5&absences=0'
    response1 = client.get(url1)
    assert response1.status_code == 400 #should return bad request 400
    assert response1.get_data() == b'Mjob_health has to be either 1 or 0'

    url2 = '/predict?Mjob_health=1&Fjob_teacher=-1&studytime=4&higher_yes=1&health=5&absences=0'
    response2 = client.get(url2)
    assert response2.status_code == 400 #should return bad request 400
    assert response2.get_data() == b'Fjob_teacher has to be either 1 or 0'

    url3 = '/predict?Mjob_health=1&Fjob_teacher=1&studytime=5&higher_yes=1&health=5&absences=0'
    response3 = client.get(url3)
    assert response3.status_code == 400 #should return bad request 400
    assert response3.get_data() == b'studytime has to be between 1 and 4 inclusive'

    url4 = '/predict?Mjob_health=1&Fjob_teacher=1&studytime=4&higher_yes=10&health=5&absences=0'
    response4 = client.get(url4)
    assert response4.status_code == 400 #should return bad request 400
    assert response4.get_data() == b'higher_yes is to be either 1 or 0'

    url5 = '/predict?Mjob_health=1&Fjob_teacher=1&studytime=4&higher_yes=1&health=0&absences=0'
    response5 = client.get(url5)
    assert response5.status_code == 400 #should return bad request 400
    assert response5.get_data() == b'health has to be between 1 and 5 inclusive'

    url6 = '/predict?Mjob_health=1&Fjob_teacher=1&studytime=4&higher_yes=1&health=5&absences=94'
    response6 = client.get(url6)
    assert response6.status_code == 400 #should return bad request 400
    assert response6.get_data() == b'absences has to be between 0 and 93 inclusive'
