import json
import re

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .content import SITE_CONTENT, SOCIAL_LINKS


def shared_context():
    return {
        "site": SITE_CONTENT,
        "social_links": SOCIAL_LINKS,
    }


def home(request):
    context = shared_context()
    return render(request, "website/home.html", context)


def about(request):
    context = shared_context()
    return render(request, "website/about.html", context)


def services(request):
    context = shared_context()
    return render(request, "website/services.html", context)


def socials(request):
    context = shared_context()
    return render(request, "website/socials.html", context)


def build_knowledge_base():
    facts = [
        SITE_CONTENT["hero"]["subtitle"],
        SITE_CONTENT["main_work_intro"],
        SITE_CONTENT["service_intro"],
        f"Direct email contact is {SITE_CONTENT['brand']['email']}.",
        "Official social platforms are LinkedIn, X / Twitter, Instagram, and Facebook.",
    ]

    facts.extend(item["body"] for item in SITE_CONTENT["main_work"])
    facts.extend(item["body"] for item in SITE_CONTENT["about"])
    facts.extend(item["body"] for item in SITE_CONTENT["services"])
    facts.extend(item["answer"] for item in SITE_CONTENT["faqs"])
    return facts


def answer_question(message: str) -> str:
    text = message.lower().strip()
    if not text:
        return "Ask about Alphintra's company details, services, social links, or how to contact the team."

    if any(token in text for token in ["email", "contact", "call", "reach", "phone"]):
        return (
            f"You can contact Alphintra directly at {SITE_CONTENT['brand']['email']}. "
            "You can also use the official social links page for additional company contact points."
        )

    if any(token in text for token in ["social", "linkedin", "instagram", "facebook", "twitter", "x"]):
        labels = ", ".join(item["label"] for item in SOCIAL_LINKS)
        return f"Alphintra is available on these official platforms: {labels}."

    if any(token in text for token in ["service", "offer", "provide", "work", "build"]):
        services = ", ".join(item["title"] for item in SITE_CONTENT["services"])
        return f"Alphintra offers {services}."

    tokens = re.findall(r"[a-z0-9]+", text)
    knowledge = build_knowledge_base()
    scored = []
    for fact in knowledge:
      fact_lower = fact.lower()
      score = sum(1 for token in tokens if token in fact_lower)
      if score:
          scored.append((score, fact))

    if scored:
        scored.sort(key=lambda item: item[0], reverse=True)
        return scored[0][1]

    return (
        "I do not have a verified answer for that yet. Ask about Alphintra's services, company profile, "
        f"social links, or contact the team directly at {SITE_CONTENT['brand']['email']}."
    )


import urllib.request

@csrf_exempt
def chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed."}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    message = payload.get("message", "")
    session_id = payload.get("session_id", "")
    history = payload.get("history", [])

    data = json.dumps({
        "message": message,
        "session_id": session_id,
        "history": history
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://chatbot-backend-452555374554.us-central1.run.app/api/v1/chat",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            return JsonResponse(result)
    except Exception as e:
        # Fallback to local rule-based response if backend is offline
        return JsonResponse({"answer": answer_question(message)})
