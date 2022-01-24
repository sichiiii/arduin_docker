from flask import Flask

app = Flask(__name__)


if __name__ == "__main__":

    from routes import *
    
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.secret_key = 'some_secret'
    
    app.run(debug=True, host='0.0.0.0')
