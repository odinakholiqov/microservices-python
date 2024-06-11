import sqlite3
from flask import Flask, request
import jwt
import os
import datetime

server = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@server.route("/")
def welcome():
    return "Auth Server"


@server.route("/login")
def login():
    auth = request.authorization
    print(auth)

    conn = get_db_connection()

    admin = conn.execute("SELECT * FROM users").fetchone()
    conn.close()

    if auth.username != admin["email"] or auth.password != admin["password"]:
        return "Invalid credentials", 401
    else:
        encoded_jwt = jwt.encode(
            {
                "username": admin["email"],
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(days=1),
                "iat": datetime.datetime.utcnow(),
                "is_admin": True,
            },
            os.environ.get("JWT_SECRET"),
            algorithm="HS256",
        )

        return encoded_jwt


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    encoded_jwt = encoded_jwt.split(" ")[1]

    if not encoded_jwt:
        return "Missing credentials", 401

    try:
        decoded_data = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms="HS256"
        )
    except:
        return "Not authorized", 403

    return decoded_data, 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
