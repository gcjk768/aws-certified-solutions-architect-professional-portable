"""Build one CSV of SAP practice questions from downloaded sources + authored banks.
Usage: python -I build_csv.py [sources_dir] [out.csv]   (defaults: ./sources, ./SAP-C03_practice_questions_2026.csv)
Also writes data/questions.csv in the quiz-bot schema. Exits non-zero if any row is malformed.
"""
import csv, html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "sources")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "SAP-C03_practice_questions_2026.csv")
LET = "ABCDEFGH"
rows = []

def have(name):
    ok = os.path.exists(os.path.join(SRC, name))
    if not ok: print("skip (missing)", name)
    return ok


def add(source, url, version, n_select, q, opts, ans, expl, topic=""):
    r = {"id": len(rows) + 1, "source": source, "source_url": url, "exam_version": version,
         "topic": topic, "select_count": n_select, "question": " ".join(q.split())}
    for L in LET:
        r["option_" + L] = " ".join(opts.get(L, "").split())
    r["correct_answer"] = ans
    r["explanation"] = " ".join(expl.split())
    rows.append(r)

def split_opts(block, pat):
    """block -> (question_text, {letter: text}) using regex pat that captures letter."""
    parts = re.split(pat, block, flags=re.M)
    q = parts[0]
    opts = {parts[i]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}
    return q, opts

if have("sap_sample.txt"):
    # 1. AWS official sample questions (PDF text)
    t = open(os.path.join(SRC, "sap_sample.txt"), encoding="utf-8").read()
    t = re.sub(r"[-�•▪]", "-", t)  # PDF bullet glyphs
    t = "\n".join(l for l in t.splitlines()
                  if not re.search(r"Sample Exam Questions|© 2022|SAP-C02\)\s*$", l))
    qpart, apart = t.split("\nAnswers", 1)
    qs = re.split(r"^\s*(\d+)\) ", qpart, flags=re.M)[1:]
    ans = dict(re.findall(r"^\s*(\d+)\) ([A-F](?:, [A-F])*) [–-] ", apart, flags=re.M))
    expl = dict(re.findall(r"^\s*(\d+)\) [A-F, ]+ [–-] (.*?)(?=^\s*\d+\) [A-F]|\Z)", apart, flags=re.M | re.S))
    for i in range(0, len(qs), 2):
        n, body = qs[i], qs[i + 1]
        q, opts = split_opts(body, r"^([A-F])\) ")
        m = re.search(r"Select (TWO|THREE)", q)
        add("AWS official SAP-C02 sample questions", "https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Sample-Questions.pdf",
            "SAP-C02", {"TWO": 2, "THREE": 3}.get(m.group(1) if m else "", 1), q, opts, ans[n].replace(" ", ""), expl[n])

if have("prashu_08-sap-practice-exam.md"):
    # 2. Prashu94 practice exam (25 MCQ) — covers SAP-C03 announced topics
    t = open(os.path.join(SRC, "prashu_08-sap-practice-exam.md"), encoding="utf-8").read()
    a = open(os.path.join(SRC, "prashu_08-sap-practice-exam-answers.md"), encoding="utf-8").read()
    key = {n: (x, why) for n, x, why in re.findall(r"^\| (\d+) \| ([A-D]) \| (.*?) \|$", a, flags=re.M)}
    qs = re.split(r"^(\d+)\. ", t, flags=re.M)[1:]
    for i in range(0, len(qs), 2):
        n, body = qs[i], qs[i + 1]
        q, opts = split_opts(body, r"^\s+([A-D])\. ")
        ver = "SAP-C03 (announced topic)" if re.search(r"SAP-C03|Clean Rooms|Lattice|ARC routing", body) else "SAP-C02"
        add("Prashu94/Notes SAP practice exam (GitHub)", "https://github.com/Prashu94/Notes/blob/main/Learning/aws-certification/04-sap/08-sap-practice-exam.md",
            ver, 1, q, opts, key[n][0], key[n][1])

# 3. Prashu94 short-answer exercises: SAP-C03 new skills (Q2-6) + SAP exercises (15)
def short_answer(path, url, version, topic):
    if not have(path): return
    t = open(os.path.join(SRC, path), encoding="utf-8").read()
    qsec = t.split("## Answers")[0]
    asec = t.split("## Answers")[1].split("\n## ")[0] if "## Answers" in t else ""
    if "## More exercises" in qsec: qsec = qsec.split("## More exercises")[1]
    elif "## Questions" in qsec: qsec = qsec.split("## Questions")[1]
    qd = dict(re.findall(r"^(\d+)\. (.*)$", qsec, flags=re.M))
    ad = dict(re.findall(r"^(\d+)\. (.*)$", asec, flags=re.M))
    for n in qd:
        if n in ad:
            add("Prashu94/Notes " + topic + " (GitHub)", url, version, "open", qd[n], {}, "", ad[n], topic)
short_answer("prashu_09-sap-c03-new-skills.md", "https://github.com/Prashu94/Notes/blob/main/Learning/aws-certification/04-sap/09-sap-c03-new-skills.md",
             "SAP-C03 (announced topic)", "SAP-C03 new skills exercises")
short_answer("prashu_07-sap-exercises.md", "https://github.com/Prashu94/Notes/blob/main/Learning/aws-certification/04-sap/07-sap-exercises.md",
             "SAP-C02", "SAP design exercises")

if have("sailor.md"):
    # 4. sailor.sh blog (10 MCQ with explanations)
    t = open(os.path.join(SRC, "sailor.md"), encoding="utf-8").read()
    for m in re.finditer(r"^## Question (\d+) — (.*?)\n(.*?)^### Answer: ([A-D])\n(.*?)^\* \* \*", t, flags=re.M | re.S):
        n, title, body, ansr, ex = m.groups()
        q, opts = split_opts(body.replace("**", ""), r"^([A-D])\. ")
        add("sailor.sh SAP-C02 practice questions (2026-04-17)", "https://sailor.sh/blog/sap-c02-practice-questions-with-answers/",
            "SAP-C02", 1, q, opts, ansr, ex.replace("**", "").replace("*   ", "- ").replace("Explanation: ", "", 1), title)

if have("certpunch.html"):
    # 5. CertPunch (258 MCQ with explanations) — structured HTML
    h = open(os.path.join(SRC, "certpunch.html"), encoding="utf-8").read()
    def clean(s): return html.unescape(re.sub(r"<[^>]+>", " ", s))
    for m in re.finditer(r'<li class="cpq-q" data-answer="([A-H,]+)" data-multi="(\d)">(.*?)</li>', h, flags=re.S):
        ansr, multi, body = m.groups()
        q = clean(re.search(r'<h3 class="cpq-qtitle"><span class="cpq-qnum">[^<]*</span>(.*?)</h3>', body, re.S).group(1))
        opts = {k: clean(v) for k, v in re.findall(r'data-key="([A-H])">.*?<span class="cpq-otext">(.*?)</span>', body, re.S)}
        ex = clean(re.search(r'<p class="cpq-expl">(.*?)</p>', body, re.S).group(1))
        add("CertPunch SAP-C02 free practice test (2026-07-30)", "https://certpunch.com/aws-certified-solutions-architect-professional-practice-test/",
            "SAP-C02", int(multi), q, opts, ansr, ex)

if have("trainer_sap.js"):
    # 5c. renehmj/aws-trainer SAP-C02 bank (MIT): JS array literal -> JSON (quote keys, drop comments and trailing commas)
    import json as _json
    t = open(os.path.join(SRC, "trainer_sap.js"), encoding="utf-8").read()
    t = t[t.index("= [") + 2 : t.rindex("]") + 1]
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"(?m)^\s*(\w+):", lambda m: '"%s":' % m.group(1), t)       # unquoted keys at line start
    t = re.sub(r"\{ id:", '{ "id":', t).replace(", text:", ', "text":')     # inline option objects
    t = re.sub(r",(\s*[}\]])", r"\1", t)
    for q in _json.loads(t):
        opts = {o["id"]: o["text"] for o in q["options"]}
        wrong = " ".join(f"{k}: {v}" for k, v in q.get("whyWrong", {}).items())
        ans = ",".join(q["correct"])
        add("renehmj/aws-trainer SAP-C02 bank (GitHub, MIT)", "https://github.com/renehmj/aws-trainer/blob/main/bank-sap-c02.js",
            "SAP-C02", len(q["correct"]), q["question"], opts, ans, q["explanation"] + " Why the others are wrong: " + wrong, q["domain"])

if have("src_www_mindmeshacademy_com_certifications_a.md"):
    # 5d. MindMesh Academy free SAP-C02 samples (Jina markdown)
    t = open(os.path.join(SRC, "src_www_mindmeshacademy_com_certifications_a.md"), encoding="utf-8").read()
    for m in re.finditer(r"^\d+\.\s+Question \d+ (.*?)\n(.*?)^Show answer and explanation\n\nCorrect answer:([A-E](?:,\s*[A-E])*)\n\n(.*?)(?=^\d+\.\s+Question|^## )", t, re.M | re.S):
        topic, body, ans, ex = m.groups()
        q, opts = split_opts(body, r"^\s*\*\s+([A-E])\.")
        add("MindMesh Academy free SAP-C02 samples", "https://www.mindmeshacademy.com/certifications/aws/aws-certified-solutions-architect-professional/practice-exam",
            "SAP-C02", len(ans.replace(" ", "").split(",")), q, opts, ans.replace(" ", ""), ex, topic.strip())

# 5b. Authored banks in banks/*.md (see AGENT.md for the format): header lines source/url/version, numbered questions, answer table
import glob
for _f in sorted(glob.glob(os.path.join(HERE, "banks", "*.md"))):
  t = open(_f, encoding="utf-8").read()
  hdr = dict(re.findall(r"^(source|url|version): (.*)$", t.split("\n## ", 1)[0], flags=re.M))
  qpart, apart = t.split("## Answers")
  key = {n: (x, why) for n, x, why in re.findall(r"^\| (\d+) \| ([A-E](?:,[A-E])*) \| (.*?) \|$", apart, flags=re.M)}
  section = ""
  for chunk in re.split(r"^(## .*)$", qpart, flags=re.M)[1:]:
      if chunk.startswith("## "):
          section = chunk[3:].strip(); continue
      qs = re.split(r"^(\d+)\. ", chunk, flags=re.M)[1:]
      for i in range(0, len(qs), 2):
          n, body = qs[i], qs[i + 1]
          q, opts = split_opts(body, r"^\s+([A-E])\. ")
          add(hdr.get("source", os.path.basename(_f)), hdr.get("url", "banks/" + os.path.basename(_f)),
              hdr.get("version", "SAP-C02"), len(key[n][0].split(",")), q, opts, key[n][0], key[n][1], section)

cols = ["id", "source", "source_url", "exam_version", "topic", "select_count", "question"] + \
       ["option_" + L for L in LET] + ["correct_answer", "explanation"]
with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(rows)

# self-check
from collections import Counter
print(Counter(r["source"] for r in rows))
bad = [r["id"] for r in rows if r["select_count"] != "open" and
       (not r["option_A"] or not r["option_B"] or not r["correct_answer"] or not r["question"])]
assert not bad, f"incomplete rows: {bad}"
for r in rows:
    if r["select_count"] != "open":
        assert all(r["option_" + L] for L in r["correct_answer"].split(",")), r["id"]
print("rows:", len(rows), "-> ", OUT)

# 6. Bot-schema copy for bot.py (same columns as the CCAR-P quiz bot): MCQ rows only.
SHORT = {"AWS official SAP-C02 sample questions": "AWS official sample",
         "CertPunch SAP-C02 free practice test (2026-07-30)": "CertPunch practice",
         "Prashu94/Notes SAP practice exam (GitHub)": "Prashu94 practice exam",
         "sailor.sh SAP-C02 practice questions (2026-04-17)": "sailor.sh scenarios",
         "Claude-written SAP-C03 new-topic bank (2026-10-14, unofficial)": "SAP-C03 new topics",
         "renehmj/aws-trainer SAP-C02 bank (GitHub, MIT)": "aws-trainer bank",
         "MindMesh Academy free SAP-C02 samples": "MindMesh samples"}
bot_path = os.path.join(HERE, "data", "questions.csv")
os.makedirs(os.path.dirname(bot_path), exist_ok=True)
with open(bot_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "domain", "question", "options", "correct", "explanation"])
    w.writeheader()
    n = 0
    for r in rows:
        if r["select_count"] == "open":
            continue
        n += 1
        opts = "\n".join(f"{L}. {r['option_' + L]}" for L in LET if r["option_" + L])
        # ponytail: domain = source bank; swap for the five SAP-C03 domains once AWS publishes the guide (2026-10-27)
        w.writerow({"id": f"SAP-{n:04d}", "domain": SHORT.get(r["source"], r["source"][:40]), "question": r["question"],
                    "options": opts, "correct": r["correct_answer"], "explanation": r["explanation"]})
print("bot rows:", n, "->", bot_path)
