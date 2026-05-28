import os
import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

SERVICE_PRIORITY = {
    "CRITICAL": ["hospital", "ambulance_service", "police", "towing_service"],
    "MODERATE": ["police", "hospital", "towing_service", "car_repair"],
    "MINOR":    ["police", "car_repair", "tire_shop", "towing_service"],
}

EMERGENCY_NUMBERS = {
    "IN": {"police": "100", "ambulance": "108", "unified": "112", "fire": "101"},
    "US": {"police": "911", "ambulance": "911", "unified": "911", "fire": "911"},
    "GB": {"police": "999", "ambulance": "999", "unified": "999", "fire": "999"},
    "DEFAULT": {"police": "112", "ambulance": "112", "unified": "112", "fire": "112"},
}


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.1,
        convert_system_message_to_human=True
    )


def classify_severity(description: str) -> dict:
    llm = get_llm()

    system_prompt = """You are RoadSoS, an AI emergency triage assistant for road accidents.

Analyse the accident description and return ONLY a valid JSON object — no markdown, no explanation, no backticks.

JSON schema:
{
  "severity": "CRITICAL" | "MODERATE" | "MINOR",
  "severity_reason": "one sentence explaining your classification",
  "priority_services": ["ordered list of services needed, most urgent first"],
  "first_aid_tip": "2-3 clear numbered first-aid steps for this accident",
  "call_action": "short urgent instruction e.g. Call 112 immediately",
  "confidence": "high" | "medium" | "low"
}

Severity rules:
- CRITICAL: unconscious person, heavy bleeding, suspected spinal injury, fire, multiple casualties
- MODERATE: injuries but conscious, vehicle badly damaged, single casualty
- MINOR: no injuries, minor damage, breakdown, tyre puncture

Service types: hospital, ambulance_service, police, towing_service, car_repair, tire_shop
Always include police in priority_services."""

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Accident: {description}")
        ])

        raw = response.content.strip()
        raw = re.sub(r"^```(?:json)?", "", raw).strip()
        raw = re.sub(r"```$", "", raw).strip()

        result = json.loads(raw)

        if result.get("severity") not in SERVICE_PRIORITY:
            result["severity"] = "MODERATE"
        if not result.get("priority_services"):
            result["priority_services"] = SERVICE_PRIORITY[result["severity"]]

        return result

    except Exception as e:
        print(f"[Classifier error] {e}")
        return {
            "severity": "MODERATE",
            "severity_reason": "Could not analyse — defaulting to moderate",
            "priority_services": SERVICE_PRIORITY["MODERATE"],
            "first_aid_tip": "1. Call 112 immediately.\n2. Do not move injured persons.\n3. Keep them warm and still until help arrives.",
            "call_action": "Call 112 immediately",
            "confidence": "low"
        }


def get_emergency_numbers(country_code: str) -> dict:
    return EMERGENCY_NUMBERS.get(country_code.upper(), EMERGENCY_NUMBERS["DEFAULT"])