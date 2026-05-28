import os
import json
import time
from flask import Flask, render_template, request, jsonify, render_template_string
from dotenv import load_dotenv
from severity_classifier import classify_severity, get_emergency_numbers
from places_service import get_all_nearby
from offline_cache import save_to_cache, get_from_cache
from rag_engine import get_qa_chain, ask

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


@app.route("/")
def index():
    return render_template("index.html", GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY)



@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        # "service": "RoadSoS",
        "gemini_key_set": bool(os.getenv("GEMINI_API_KEY")),
        "maps_key_set": bool(os.getenv("GOOGLE_MAPS_API_KEY")),
    })


@app.route("/severity", methods=["POST"])
def severity():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    description = (data.get("description") or "").strip()
    # if not description:
    #     return jsonify({"error": "Field 'description' is required"}), 400
    # if len(description) < 10:
    #     return jsonify({"error": "Description too short"}), 400
    if not description or len(description) < 10:
        return jsonify({"error": "Please describe the accident in more detail"}), 400

    country_code = data.get("country_code", "IN")

    start = time.time()
    result = classify_severity(description)
    elapsed_ms = int((time.time() - start) * 1000)

    result["emergency_numbers"] = get_emergency_numbers(country_code)
    result["processing_time_ms"] = elapsed_ms

    # print(f"[/severity] '{description[:60]}' → {result['severity']} ({elapsed_ms}ms)")
    return jsonify(result)


@app.route("/test")
def test():
    cases = [
        {
            "label": "Critical — unconscious rider",
            "description": "Two bikes collided head-on. One rider is unconscious and bleeding heavily from the head.",
            "expected": "CRITICAL"
        },
        {
            "label": "Minor — parking lot scrape",
            "description": "Minor scrape in parking lot. No injuries. Small dent on bumper. Both drivers are fine.",
            "expected": "MINOR"
        },
        {
            "label": "Moderate — airbag deployed",
            "description": "Car hit road divider at 60kmph. Airbag deployed. Driver conscious but has cuts on face. Car cannot move.",
            "expected": "MODERATE"
        },
    ]

    results = []
    for case in cases:
        result = classify_severity(case["description"])
        results.append({
            "label": case["label"],
            "expected": case["expected"],
            "got": result["severity"],
            "passed": result["severity"] == case["expected"],
            # "reason": result.get("severity_reason", ""),
            # "services": result.get("priority_services", []),
            # "first_aid": result.get("first_aid_tip", "")[:100] + "...",
            # "call_action": result.get("call_action", ""),
        })

    all_passed = all(r["passed"] for r in results)
    return app.response_class(
        response=json.dumps({
            "status": "PASS" if all_passed else "PARTIAL", "results": results
        }, indent=2),
        mimetype="application/json"
    )


# Stubs for future days
@app.route("/nearby", methods=["POST"])
def nearby():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
 
    description = (data.get("description") or "").strip()
    lat = data.get("lat")
    lng = data.get("lng")
    country_code = data.get("country_code", "IN")
 
    if not description:
        return jsonify({"error": "Field 'description' is required"}), 400
    if lat is None or lng is None:
        return jsonify({"error": "Fields 'lat' and 'lng' are required"}), 400
 
    try:
        lat = float(lat)
        lng = float(lng)
    except (ValueError, TypeError):
        return jsonify({"error": "lat and lng must be numbers"}), 400
 
    # print(f"[/nearby] Classifying: '{description[:60]}'")
    severity_result = classify_severity(description)
    priority_services = severity_result.get("priority_services", ["hospital", "police"])
 
    # print(f"[/nearby] Fetching places for: {priority_services}")
    # Try live Places API first
    services = get_all_nearby(lat, lng, priority_services)
    offline_mode = False

    # If Places API returned nothing, fall back to SQLite cache
    if not services:
        print("[/nearby] Places API returned nothing — trying offline cache")
        services = get_from_cache(lat, lng, priority_services)
        offline_mode = True
    else:
        # Save fresh results to cache for future offline use
        save_to_cache(lat, lng, services)

    total_contacts = sum(len(v) for v in services.values())
 
    return jsonify({
        "severity":          severity_result.get("severity"),
        "severity_reason":   severity_result.get("severity_reason"),
        "first_aid_tip":     severity_result.get("first_aid_tip"),
        "call_action":       severity_result.get("call_action"),
        "priority_services": priority_services,
        "emergency_numbers": get_emergency_numbers(country_code),
        "services":          services,
        "total_contacts":    total_contacts,
        "user_location":     {"lat": lat, "lng": lng},
        "offline_mode":      offline_mode,
    })

@app.route("/chat", methods=["POST"])
def chat():
    """
    RAG first-aid chatbot.
    Answers follow-up questions using the knowledge base.
 
    Request:  { "question": "How do I do CPR?" }
    Response: { "answer": "...", "sources": ["first_aid.txt"] }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
 
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Field 'question' is required"}), 400
 
    try:
        qa_chain = get_qa_chain()
        result = ask(qa_chain, question)
        return jsonify(result)
    except Exception as e:
        print(f"[/chat] Error: {e}")
        return jsonify({
            "answer": "I'm having trouble answering right now. Please call 112 immediately for emergency help.",
            "sources": []
        })
 


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error — check your .env file"}), 500


if __name__ == "__main__":
    print("\n🚨 RoadSoS starting...")
    print("   Gemini key set:", bool(os.getenv("GEMINI_API_KEY")))
    print("   Maps key set:  ", bool(os.getenv("GOOGLE_MAPS_API_KEY")))
    print("\n   → http://localhost:5000/health")
    print("   → http://localhost:5000/test")
    print("   → http://localhost:5000/\n")
    app.run(debug=True, port=5000)