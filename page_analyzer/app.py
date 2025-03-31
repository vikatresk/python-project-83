from flask import (
    Flask,
    request,
    abort,
    redirect,
    url_for,
    flash
)
from flask import render_template
import requests
from .tools import validate_url, normalize
from .html_parser import parse_page
from page_analyzer import db as db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")


@app.route('/')
def index():
    return render_template('index.html', )


@app.get("/urls")
def show_urls_page():
    with db.connect_db(app.config["DATABASE_URL"]) as conn:
        urls_check = db.get_urls_with_latest_check(conn)
        result = render_template("urls/index.html", urls_check=urls_check)
    db.close(conn)
    return result    


@app.get("/urls/<int:url_id>")
def show_url_page(url_id):
    with db.connect_db(app.config["DATABASE_URL"]) as conn:
        url = db.get_url(conn, url_id)
        if not url:
            abort(404)
        checks = db.get_url_checks(conn, url_id)
        result = render_template("urls/show.html", url=url, checks=checks)
    db.close(conn)
    return result


@app.post('/urls')
def add_url():
    with db.connect_db(app.config["DATABASE_URL"]) as conn:
        input_url = request.form['url']
        is_valid, error_message = validate_url(input_url)

        if not is_valid:
            flash(error_message, 'danger')
            return render_template('index.html',), 422

        normal_url = normalize(input_url)
        url_info = db.get_url_by_name(conn, normal_url)

        if url_info:
            flash("Страница уже существует", "info")
            url_id = url_info.id

        else:
            url_id = db.insert_url(conn, normal_url)
            flash("Страница успешно добавлена", "success")

        result = redirect(url_for("show_url_page", url_id=url_id))
    db.close(conn)
    return result


@app.post("/urls/<int:url_id>/check")
def check_url_page(url_id):
    with db.connect_db(app.config["DATABASE_URL"]) as conn:
        url = db.get_url(conn, url_id)
        try:
            response = requests.get(url.name, timeout=50)
            response.raise_for_status()
            url_info = parse_page(response.text, response.status_code)
            db.insert_url_check(conn, url_id, url_info)
            flash("Страница успешно проверена", "success")
        except requests.RequestException:
            flash("Произошла ошибка при проверке", "danger")
        result = redirect(url_for("show_url_page", url_id=url_id))
    db.close(conn)
    return result
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500
