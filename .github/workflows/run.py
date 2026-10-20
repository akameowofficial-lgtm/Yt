import os, sys, json, urllib.request

skill, task = sys.argv[1], sys.argv[2]
system = open(f"/tmp/yt/skills/{skill}/SKILL.md").read()
voice = open("voice.md").read()

body = {
    "system_instruction": {"parts": [{"text": system + "\n\nCreator voice file:\n" + voice}]},
    "contents": [{"parts": [{"text": task}]}],
}
model = "gemini-2.5-flash"
req = urllib.request.Request(
    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    data=json.dumps(body).encode(),
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": os.environ["GEMINI_API_KEY"],
    },
)
r = json.load(urllib.request.urlopen(req))
print(r["candidates"][0]["content"]["parts"][0]["text"])
