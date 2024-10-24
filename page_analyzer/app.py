from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

@app.route('/')
def index():
   return "Hello there, it's the first Flask app"

if __name__ == '__main__':
    app.run(debug=True)
