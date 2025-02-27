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
from .config import config
from .tools import validate_url, normalize
from page_analyzer.exceptions import (
    InvalidURLError,
    URLTooLongError,
    URLValidationError,
)
from .html_parser import parse_page
from page_analyzer import db as db


app = Flask(__name__)
app.secret_key = config.SECRET_KEY
db_url = config.DATABASE_URL


@app.route('/')
def index():
    return render_template('index.html', )


@app.get("/urls")
def show_urls_page():
    with db.get_connection(db_url) as conn:
        urls_check = db.get_urls_with_latest_check(conn)
        return render_template("urls/index.html", urls_check=urls_check)


@app.get("/urls/<url_id>")
def show_url_page(url_id):
    with db.get_connection(db_url) as conn:
        url = db.get_url(conn, int(url_id))
        if not url:
            abort(404)
        checks = db.get_url_checks(conn, int(url_id))

    return render_template("urls/show.html", url=url, checks=checks)


@app.post("/urls")
def add_url():
    url = request.form.get("url")
    normal_url = normalize(url)

    try:
        validate_url(normal_url)
    except URLTooLongError:
        flash("URL превышает 255 символов", "danger")
        return render_template("index.html", url=normal_url), 422
    except InvalidURLError:
        flash("Некорректный URL", "danger")
        return render_template("index.html", url=normal_url), 422
    except URLValidationError as e:
        flash(str(e), "danger")
        return render_template("index.html", url=normal_url), 422

    with db.get_connection(db_url) as conn:
        url_info = db.check_url_exists(conn, normal_url)

    if url_info:
        flash("Страница уже существует", "info")
        url_id = url_info.id
    else:
        flash("Страница успешно добавлена", "success")
        with db.get_connection(db_url) as conn:
            url_id = db.insert_url(conn, normal_url)

    return redirect(url_for("show_url_page", url_id=url_id))


@app.post("/urls/<url_id>/check")
def check_url_page(url_id):
    with db.get_connection(db_url) as conn:
        url = db.get_url(conn, int(url_id))
    try:
        response = requests.get(url.name, timeout=50)
        response.raise_for_status()
    except requests.RequestException:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("show_url_page", url_id=url_id))

    url_info = parse_page(response.text, response.status_code)
    flash("Страница успешно проверена", "success")
    with db.get_connection(db_url) as conn:
        db.insert_check(conn, int(url_id), url_info)

    return redirect(url_for("show_url_page", url_id=url_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500
