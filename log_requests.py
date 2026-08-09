import json

def log_request(req):
    with open("requests_log.json", "a") as f:
        f.write(req.json() + "\n")
