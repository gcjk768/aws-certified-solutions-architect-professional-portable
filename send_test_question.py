"""Post one quiz question into BOT_CHAT through the Bot API, using bot.py's own formatting.
The running bot (NAS) handles the answer buttons. Usage: python send_test_question.py [question-id]
Loads bot.env itself; prints nothing secret.
"""
import json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
for line in open(os.path.join(HERE, "bot.env"), encoding="utf-8"):
    if "=" in line and not line.lstrip().startswith("#"):
        k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
os.environ.setdefault("DATA_DIR", os.path.join(HERE, "data"))
import bot  # noqa: E402  (reads TELEGRAM_BOT_TOKEN/BOT_CHAT from env, loads questions.csv)

qid = sys.argv[1] if len(sys.argv) > 1 else next(i for i, q in bot.QUESTIONS.items() if q["domain"] == "SAP-C03 new topics")
q = bot.QUESTIONS[qid]
chat, thread = bot.BOT_CHAT
payload = {"chat_id": chat, "message_thread_id": thread, "parse_mode": "HTML", "text": bot.question_text(q),
           "reply_markup": bot.keyboard(q).to_dict()}
req = urllib.request.Request(f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
                             data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
try:
    r = json.load(urllib.request.urlopen(req, timeout=20))
    print("sent", qid, "to topic", thread, "message_id", r["result"]["message_id"])
except urllib.error.HTTPError as e:
    print("Telegram", e.code, re.sub(r"\d{8,10}:[A-Za-z0-9_-]{30,}", "<token>", e.read().decode())[:200])
    sys.exit(1)
