from ssl import HAS_TLSv1_1
from unicodedata import name
from flask import Flask
from config import config
from flask_cors import CORS

from routes import api

app=Flask(__name__)

CORS(app,resources={"*": {"https://git.heroku.com/rest-api-t2.git"}})

def page_not_found(error):
    return "<h1> Page not found </h1>", 404
    
app.config.from_object(config['development'])

    #Blueprints
app.register_blueprint(api.main, url_prefix='/api')

app.register_error_handler(404,page_not_found)

if __name__=='__main__':

    
    app.run()
