from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

@app.route('/')
def index():
   return render_template('index.html', )

if __name__ == '__main__':
    app.run(debug=True)
