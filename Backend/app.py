import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from postgrest import APIError
from supabase import Client, create_client

load_dotenv()

app = Flask(__name__)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_PUBLISHABLE_KEY")
supabase: Client | None = (
    create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None
)


@app.after_request
def allow_cross_origin_requests(response):
    """Allow browser clients hosted on any origin to call this API."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


def database():
    if supabase is None:
        return None, (jsonify(error="Database is not configured"), 503)
    return supabase, None


def api_error(error: APIError):
    # Postgres unique_violation is the expected duplicate-registration case.
    if getattr(error, "code", None) == "23505":
        return jsonify(error="Registration already exists"), 409
    app.logger.exception("Supabase request failed")
    return jsonify(error="Database request failed"), 500


@app.route("/", methods=["GET"])
def index():
    return jsonify(message="Events API is running")


@app.route("/api/events", methods=["GET", "OPTIONS"])
def list_events():
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response
    try:
        result = client.table("events").select("*").execute()
        return jsonify(result.data)
    except APIError as error:
        return api_error(error)


@app.route("/api/events/<event_id>", methods=["GET", "OPTIONS"])
def get_event(event_id):
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response
    try:
        result = client.table("events").select("*").eq("id", event_id).maybe_single().execute()
        if not result.data:
            return jsonify(error="Event not found"), 404
        return jsonify(result.data)
    except APIError as error:
        return api_error(error)


@app.route("/api/registrations", methods=["POST", "OPTIONS"])
def create_registration():
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not payload.get("user_id") or not payload.get("event_id"):
        return jsonify(error="JSON body must include user_id and event_id"), 400
    try:
        result = (
            client.table("registrations")
            .insert({"user_id": payload["user_id"], "event_id": payload["event_id"]})
            .execute()
        )
        registration = result.data[0] if result.data else {}
        return jsonify(registration), 201
    except APIError as error:
        return api_error(error)


@app.route("/api/me/registrations", methods=["GET", "OPTIONS"])
def list_user_registrations():
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify(error="user_id query parameter is required"), 400
    try:
        result = (
            client.table("registrations")
            .select("*, events(*)")
            .eq("user_id", user_id)
            .execute()
        )
        return jsonify(result.data)
    except APIError as error:
        return api_error(error)


@app.route("/api/events/<event_id>/registrations", methods=["GET", "OPTIONS"])
def list_event_registrations(event_id):
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response
    try:
        result = (
            client.table("registrations")
            .select("*, users(id, email, role)")
            .eq("event_id", event_id)
            .execute()
        )
        return jsonify(result.data)
    except APIError as error:
        return api_error(error)


if __name__ == "__main__":
    app.run(debug=True)
