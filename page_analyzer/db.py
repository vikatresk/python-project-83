import psycopg2
from psycopg2.extras import NamedTupleCursor


def connect_db(db_url):
    return psycopg2.connect(db_url)


def close(conn):
    conn.close()


def get_url(conn, url_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        query = "SELECT * FROM urls WHERE id = (%s);"
        cur.execute(query, (url_id,))
        result = cur.fetchone()
    return result


def insert_url(conn, url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        query = "INSERT INTO urls (name) VALUES (%s) RETURNING id;"
        cur.execute(query, (url,))
        result = cur.fetchone()
    return result.id


def get_url_by_name(conn, url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        query = "SELECT * FROM urls WHERE name = (%s);"
        cur.execute(query, (url,))
        result = cur.fetchone()
    return result


def get_url_checks(conn, url_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        query = "SELECT * FROM url_checks WHERE url_id = (%s) ORDER BY id DESC;"
        cur.execute(query, (url_id,))
        result = cur.fetchall()
    return result


def insert_url_check(conn, url_id, url_info):
    url_info_data = (
        url_id,
        url_info["status_code"],
        url_info["h1"],
        url_info["title"],
        url_info["description"],
    )
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        query = """INSERT INTO url_checks (
                url_id,
                status_code,
                h1,
                title,
                description
                )
            VALUES (%s, %s, %s, %s, %s);
            """
        cur.execute(query, url_info_data)


def get_urls_with_latest_check(conn):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT id, name FROM urls ORDER BY id DESC;")
        urls = cur.fetchall()

        cur.execute(
            "SELECT DISTINCT ON (url_id) url_id, created_at, status_code FROM url_checks "
            "WHERE url_id IN (SELECT id FROM urls) "
            "ORDER BY url_id DESC;"
        )

        checks = {check.url_id: {
            'created_at': check.created_at,
            'status_code': check.status_code
            } for check in cur.fetchall()}

    return [
        {
            'id': url.id,
            'name': url.name,
            'created_at': checks.get(url.id, {}).get('created_at'),
            'status_code': checks.get(url.id, {}).get('status_code')
        }
        for url in urls
    ]
