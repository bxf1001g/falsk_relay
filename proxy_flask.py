import sys
sys.stdout.reconfigure(line_buffering=True)
import os, json, requests
from flask import Flask, request, Response, abort


FIREBASE_BASE  = os.environ.get("FIREBASE_BASE",  "https://relay-test1001-default-rtdb.asia-southeast1.firebasedatabase.app")
RELAY_PATH     = os.environ.get("RELAY_PATH",     "/relay.json")
SECRET_TOKEN   = os.environ.get("SECRET_TOKEN",   "R3LAY123SECRET")
FIREBASE_AUTH  = os.environ.get("FIREBASE_AUTH",  "")  # e.g. "?auth=XXXX" if needed

def fb_url():
    return FIREBASE_BASE + RELAY_PATH + FIREBASE_AUTH

app = Flask(__name__)

@app.get("/")
def root():
    return "Relay proxy OK\n"

def check():
    if request.args.get("key") != SECRET_TOKEN:
        abort(403)

@app.get("/relay")
def relay_get():
    check()
    r = requests.get(fb_url(), timeout=8)
    r.raise_for_status()
    return Response(r.text.strip() + "\n", mimetype="text/plain")

@app.get("/set")
def relay_set():
    check()
    val = (request.args.get("value") or "").upper()
    if val not in ("ON", "OFF"):
        return Response("ERROR: value must be ON or OFF\n", status=400)
    r = requests.put(fb_url(), json=val, timeout=8)
    r.raise_for_status()
    return Response("OK\n", mimetype="text/plain")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))

    app.run(host="0.0.0.0", port=port)
