import os
import random
from datetime import datetime, timezone

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
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


def database():
    if supabase is None:
        return None, (jsonify(error="Database is not configured"), 503)
    return supabase, None


def api_error(error: APIError):
    if getattr(error, "code", None) == "23505":
        return jsonify(error="Registration already exists"), 409
    app.logger.exception("Supabase request failed")
    return jsonify(error="Database request failed"), 500


@app.route("/", methods=["GET"])
def index():
    return jsonify(message="QuadPulse Events API is running")


# ==========================================
# 1. PROFILES (STUDENT, FACULTY, ORG, ADMIN)
# ==========================================
@app.route("/api/profiles", methods=["GET", "OPTIONS"])
def list_profiles():
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response
    role = request.args.get("role")
    try:
        query = client.table("users").select("*")
        if role:
            query = query.eq("role", role.lower())
        result = query.execute()
        return jsonify(result.data)
    except APIError as error:
        return api_error(error)


# ==========================================
# 2. EVENTS (LIST WITH LIVE SEATS & CREATE)
# ==========================================
@app.route("/api/events", methods=["GET", "POST", "OPTIONS"])
def handle_events():
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response

    if request.method == "GET":
        try:
            events_res = (
                client.table("events")
                .select("*, users(id, campus_id, full_name, club_name)")
                .execute()
            )
            regs_res = client.table("registrations").select("event_id, is_waitlist").execute()

            booked_counts = {}
            waitlist_counts = {}
            for r in regs_res.data:
                eid = r["event_id"]
                if r.get("is_waitlist"):
                    waitlist_counts[eid] = waitlist_counts.get(eid, 0) + 1
                else:
                    booked_counts[eid] = booked_counts.get(eid, 0) + 1

            enriched = []
            for ev in events_res.data:
                booked = booked_counts.get(ev["id"], 0)
                cap = ev.get("capacity") or 0
                ev["registered_count"] = booked
                ev["waitlist_count"] = waitlist_counts.get(ev["id"], 0)
                ev["seats_left"] = max(0, cap - booked)
                enriched.append(ev)

            return jsonify(enriched)
        except APIError as error:
            return api_error(error)

    # POST: Create a new event with venue clash check
    payload = request.get_json(silent=True) or {}
    if not payload.get("title") or not payload.get("organizer_id"):
        return jsonify(error="JSON body must include title and organizer_id"), 400

    try:
        venue = payload.get("venue")
        event_date = payload.get("event_date")
        if venue and event_date:
            clash = (
                client.table("events")
                .select("id, title")
                .eq("venue", venue)
                .eq("event_date", event_date)
                .execute()
            )
            if clash.data:
                return jsonify(
                    error=f"Venue clash: '{clash.data[0]['title']}' is already scheduled at {venue} on {event_date}"
                ), 409

        new_event = {
            "organizer_id": payload["organizer_id"],
            "title": payload["title"],
            "capacity": int(payload.get("capacity", 50)),
            "status": payload.get("status", "pending_approval"),
            "category": payload.get("category", "Tech & Hackathons"),
            "venue": venue or "Main Campus Auditorium",
            "event_date": event_date or "TBD",
            "description": payload.get("description", ""),
            "faculty_approved": False,
        }
        result = client.table("events").insert(new_event).execute()
        return jsonify(result.data[0] if result.data else {}), 201
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


# ==========================================
# 3. REGISTRATIONS, QR PASSES & WAITLIST
# ==========================================
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
        # Check capacity to determine confirmed pass vs. waitlist
        ev_res = (
            client.table("events")
            .select("capacity")
            .eq("id", payload["event_id"])
            .maybe_single()
            .execute()
        )
        if not ev_res.data:
            return jsonify(error="Event not found"), 404

        capacity = ev_res.data.get("capacity") or 50
        confirmed_res = (
            client.table("registrations")
            .select("id")
            .eq("event_id", payload["event_id"])
            .eq("is_waitlist", False)
            .execute()
        )
        is_waitlist = len(confirmed_res.data) >= capacity
        pass_code = f"QP-2026-{random.randint(1000, 9999)}"

        new_reg = {
            "user_id": payload["user_id"],
            "event_id": payload["event_id"],
            "pass_code": pass_code,
            "pass_tier": payload.get("pass_tier", "General Student Pass"),
            "team_note": payload.get("team_note", ""),
            "is_waitlist": is_waitlist,
        }
        result = client.table("registrations").insert(new_reg).execute()
        registration = result.data[0] if result.data else {}
        return jsonify(registration), 201
    except APIError as error:
        return api_error(error)


@app.route("/api/registrations/<pass_code>", methods=["DELETE", "OPTIONS"])
def cancel_registration(pass_code):
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response
    try:
        existing = (
            client.table("registrations")
            .select("*")
            .eq("pass_code", pass_code)
            .maybe_single()
            .execute()
        )
        if not existing.data:
            return jsonify(error="Pass not found"), 404

        event_id = existing.data["event_id"]
        was_confirmed = not existing.data.get("is_waitlist")

        client.table("registrations").delete().eq("pass_code", pass_code).execute()

        # Auto-promote #1 waitlisted student if a confirmed spot freed up
        promoted = None
        if was_confirmed:
            waitlist = (
                client.table("registrations")
                .select("*")
                .eq("event_id", event_id)
                .eq("is_waitlist", True)
                .order("created_at")
                .limit(1)
                .execute()
            )
            if waitlist.data:
                upd = (
                    client.table("registrations")
                    .update({"is_waitlist": False})
                    .eq("id", waitlist.data[0]["id"])
                    .execute()
                )
                promoted = upd.data[0] if upd.data else None

        return jsonify(message="Registration cancelled", promoted=promoted)
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
            .order("created_at", desc=True)
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
            .select("*, users(id, campus_id, full_name, department, email, role)")
            .eq("event_id", event_id)
            .execute()
        )
        return jsonify(result.data)
    except APIError as error:
        return api_error(error)


# ==========================================
# 4. LIVE DOOR QR SCANNER VERIFICATION
# ==========================================
@app.route("/api/scanner/verify", methods=["POST", "OPTIONS"])
def verify_qr_pass():
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response

    payload = request.get_json(silent=True) or {}
    pass_code = (payload.get("pass_code") or "").strip().upper()
    if not pass_code:
        return jsonify(error="pass_code is required"), 400

    try:
        res = (
            client.table("registrations")
            .select("*, users(campus_id, full_name, department), events(title, venue)")
            .eq("pass_code", pass_code)
            .maybe_single()
            .execute()
        )
        if not res.data:
            return jsonify(valid=False, error="Invalid Pass Code"), 404

        reg = res.data
        if reg.get("is_waitlist"):
            return jsonify(valid=False, error="Pass is on Waitlist — Entry Denied"), 403

        if reg.get("checked_in"):
            return jsonify(
                valid=False,
                already_checked_in=True,
                error=f"Already checked in at {reg.get('checked_in_at')}",
                student=reg.get("users"),
            ), 409

        now_iso = datetime.now(timezone.utc).isoformat()
        client.table("registrations").update(
            {"checked_in": True, "checked_in_at": now_iso}
        ).eq("id", reg["id"]).execute()

        return jsonify(
            valid=True,
            message="Pass Verified & Attendance Logged",
            pass_code=pass_code,
            student=reg.get("users"),
            event=reg.get("events"),
            checked_in_at=now_iso,
        )
    except APIError as error:
        return api_error(error)


# ==========================================
# 5. FACULTY ENDORSEMENT & OD ATTENDANCE
# ==========================================
@app.route("/api/events/<event_id>/approve", methods=["PATCH", "OPTIONS"])
def approve_event(event_id):
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response
    payload = request.get_json(silent=True) or {}
    approved = payload.get("approved", True)
    new_status = "published" if approved else "rejected"
    try:
        res = (
            client.table("events")
            .update({"faculty_approved": approved, "status": new_status})
            .eq("id", event_id)
            .execute()
        )
        return jsonify(res.data[0] if res.data else {})
    except APIError as error:
        return api_error(error)


@app.route("/api/registrations/<reg_id>/od", methods=["PATCH", "OPTIONS"])
def verify_student_od(reg_id):
    if request.method == "OPTIONS":
        return "", 204
    client, error_response = database()
    if error_response:
        return error_response
    payload = request.get_json(silent=True) or {}
    od_status = payload.get("od_verified", True)
    try:
        res = (
            client.table("registrations")
            .update({"od_verified": od_status})
            .eq("id", reg_id)
            .execute()
        )
        return jsonify(res.data[0] if res.data else {})
    except APIError as error:
        return api_error(error)


if __name__ == "__main__":
    app.run(debug=True)