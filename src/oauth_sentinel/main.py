# Importing FastAPI to handle web requests and Requests to inspect the raw data coming
# in from our "Canary" hit.
# This is the Microsoft Authentication Library used to talk to the identity provider and
# eventually pull the "emergency brake" on any compromised accounts.
import msal  # noqa: F401
from fastapi import FastAPI, Request

# Initializes the app, giving it a professional title which shows up correctly in auto-
# generated documentation (/docs).
app = FastAPI(title="OAuth-Worm Sentinel")


# This is the "Tripwire" URL. I will register this as the Redirect URI in my decoy
# app. If a worm tries to authorize the decoy app, it will send the code here.
@app.get("/canary/callback")

# The function that executes when someone triggers the tripwire. I used async because
# I'll be making network calls to revoke tokens and send alerts.
async def canary_hit(request: Request):
    # Immediately captures the attacker's IP address. This is critical forensic data
    # for the "Audit" logs in the sentinel.
    assert request.client is not None, "Client connection required."
    client_ip = request.client.host
    # A loud console alert.
    print(f"!!! DEFCON 1: CANARY HIT FROM {client_ip} !!!")
    # Return a boring, "standard" message to the attacker so they don't realize they've
    # been caught by a sentinel
    return {"status": "authorized", "message": "Security Audit Logged"}
