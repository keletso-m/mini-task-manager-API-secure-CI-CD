from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from .database import get_db
from .security_logger import log_security_event

auth_bp = Blueprint("auth", __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            if token.startswith("Bearer "):
                token = token[7:]

            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            current_user_id = data["user_id"]

        except jwt.ExpiredSignatureError:
            log_security_event("Expired token used")
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            log_security_event("Invalid token attempt")
            return jsonify({"message": "Invalid token"}), 401

        return f(current_user_id, *args, **kwargs)

    return decorated

# Registration endpoint
@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username and password required"}), 400

    username = data["username"]
    password = data["password"]

    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters"}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception:
        return jsonify({"message": "Username already exists"}), 409
    finally:
        conn.close()


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username and password required"}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (data["username"],)
    )

    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "user_id": user["id"],
            "exp": datetime.datetime.utcnow() +
                   datetime.timedelta(hours=current_app.config["JWT_EXPIRATION_HOURS"])
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"token": token}), 200
