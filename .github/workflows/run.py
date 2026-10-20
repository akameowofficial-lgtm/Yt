import os, sys, json, urllib.request, urllib.error

KEY = os.environ["GEMINI_API_KEY"]
BASE = "https://generativelanguage.googleapis.com/v1beta"
HEADERS = {"Content-Type": "application/json", "x-goog-api-key": KEY}

skill, task = sys.argv[1], sys.argv[2]
system = open("/tmp/yt/skills/" + skill + "/SKILL.md").read()
voice = open("voice.md").read()

req = urllib.request.Request(BASE + "/models?pageSize=100", headers=HEADERS)
try:
    data = json.load(urllib.request.urlopen(req))
except urllib.error.HTTPError as e:
    print("LIST MODELS FAILED:", e.code, e.read().decode())
    sys.exit(1)

names = []
for m in data.get("models", []):
    n = m["name"]
    ok = "generateContent" in m.get("supportedGenerationMethods", [])
    bad = any(x in n for x in ["image", "tts", "live", "audio", "robotics"])
    if ok and "flash" in n and not bad:
        names.append(n)
names.sort(key=lambda n: (0 if "lite" in n else 1, n))
print("Models available:", names, file=sys.stderr)

text = system + "\n\nCreator voice file:\n" + voice
body = {
    "system_instruction": {"parts": [{"text": text}]},
    "contents": [{"parts": [{"text": task}]}],
}

last = ""
for name in names[:5]:
    req = urllib.request.Request(
        BASE + "/" + name + ":generateContent",
        data=json.dumps(body).encode(),
        headers=HEADERS,
    )
    try:
        r = json.load(urllib.request.urlopen(req))
        print(r["candidates"][0]["content"]["parts"][0]["text"])
        sys.exit(0)
    except urllib.error.HTTPError as e:
        last = name + ": " + str(e.code) + " " + e.read().decode()
        print("Failed:", last, file=sys.stderr)

print("ALL MODELS FAILED:", last)
sys.exit(1)
