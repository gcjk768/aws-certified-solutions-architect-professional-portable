"""Parsers for online SAP-C02/C03 sources downloaded into sources/online/ (research agent, 2026-10-16).
Each parser reads one file layout and calls add(source, url, version, n_select, q, opts, ans, expl, topic).
Missing files are skipped. Personal use: nothing here is redistributed."""
import hashlib, html, json, os, re

LET = "ABCDEFGH"


def _clean(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("**", "").strip()


def _hash_pos(text, n):
    return int(hashlib.md5(text.encode()).hexdigest(), 16) % n


def parse_all(ON, add):
    # open-exam-prep.com: Next.js RSC payload with "initialQuestions":[{question, options, correctAnswer (index), explanation, category}]
    f = os.path.join(ON, "open-exam-prep_aws-solutions-architect-pro.html")
    if os.path.exists(f):
        h = open(f, encoding="utf-8", errors="replace").read()
        chunks = re.findall(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)', h)
        txt = json.loads('"' + "".join(chunks) + '"')
        i = txt.find('"initialQuestions":')
        if i >= 0:
            for q in json.JSONDecoder().raw_decode(txt, i + len('"initialQuestions":'))[0]:
                ca = q["correctAnswer"]
                ans = ",".join(LET[k] for k in (ca if isinstance(ca, list) else [ca]))
                opts = {LET[k]: o for k, o in enumerate(q["options"])}
                why = q.get("explanation", "") + (" Exam tip: " + q["examTip"] if q.get("examTip") else "")
                add("open-exam-prep.com free SAP practice", "https://open-exam-prep.com/practice/aws-solutions-architect-pro", "SAP-C02",
                    len(ans.split(",")), q["question"], opts, ans, why, q.get("category", ""))
        else:
            print("open-exam-prep: initialQuestions not found; page layout changed?")

    # certsafari.com: schema.org Quiz JSON-LD; acceptedAnswer (one or a list) is listed first, so spread by a stable hash
    f = os.path.join(ON, "certsafari_aws-solutions-architect-professional_practice-questions.html")
    if os.path.exists(f):
        h = open(f, encoding="utf-8", errors="replace").read()
        for blob in re.findall(r"<script[^>]*ld\+json[^>]*>(.*?)</script>", h, re.S):
            for node in json.loads(blob).get("@graph", []):
                for q in node.get("hasPart", []) if node.get("@type") == "Quiz" else []:
                    acc = q["acceptedAnswer"]
                    accs = acc if isinstance(acc, list) else [acc]
                    sug = q.get("suggestedAnswer", [])
                    texts = [s["text"] for s in sug]
                    for a in accs:
                        texts.insert(_hash_pos(q["text"] + a["text"], len(texts) + 1), a["text"])
                    right = {a["text"] for a in accs}
                    opts = {LET[k]: t for k, t in enumerate(texts)}
                    ans = ",".join(LET[k] for k, t in enumerate(texts) if t in right)
                    comment = {x["text"]: x.get("comment", {}).get("text", "") for x in accs + sug}
                    why = " ".join(f"{LET[k]}: {comment[t]}" for k, t in enumerate(texts) if comment.get(t))
                    add("certsafari.com free SAP samples", "https://www.certsafari.com/aws/solutions-architect-professional/practice-questions",
                        "SAP-C02", len(accs), q["text"], opts, ans, why)

    # certland.net: <article> per question, "Qn." stem, <li> options (✓ = correct), no explanations
    f = os.path.join(ON, "certland_sap-c02_practice-questions.html")
    if os.path.exists(f):
        h = open(f, encoding="utf-8", errors="replace").read()
        for art in re.findall(r"<article.*?</article>", h, re.S):
            m = re.search(r"<h2[^>]*>.*?Q\d+\.</span>(.*?)</h2>", art, re.S)
            if not m:
                continue
            opts, ans = {}, []
            for k, li in enumerate(re.findall(r"<li[^>]*>(.*?)</li>", art, re.S)):
                spans = re.findall(r"<span[^>]*>(.*?)</span>", li, re.S)
                if len(spans) < 2:
                    continue
                opts[LET[k]] = _clean(spans[-1])
                if "✓" in spans[0]:
                    ans.append(LET[k])
            ex = re.search(r"Explanation</p>\s*<p[^>]*>(.*?)</p>", art, re.S)
            if opts and ans:
                add("certland.net free SAP samples", "https://certland.net/exams/aws-certified-solutions-architect-professional-sap-c02/practice-questions/",
                    "SAP-C02", len(ans), _clean(m.group(1)), opts, ",".join(ans), _clean(ex.group(1)) if ex else "")

    # PatrickWiloak (CC BY 4.0): "### Question N" / "**Scenario:** ..." / "A. ..." / <details> "**Correct: A**" "**Why:** ..."
    f = os.path.join(ON, "PatrickWiloak_cloud-data-ai-security-zero-to-hero_practice-questions_aws-solutions-architect-professional.md")
    if os.path.exists(f):
        t = open(f, encoding="utf-8").read()
        for m in re.finditer(r"^### Question (\d+)\n(.*?)(?=^### Question \d+|\Z)", t, re.M | re.S):
            body = m.group(2)
            qpart, _, apart = body.partition("<details>")
            opts = {L: x.strip() for L, x in re.findall(r"^([A-H])\. (.*)$", qpart, re.M)}
            am = re.search(r"\*\*Correct: ([A-H](?:,\s*[A-H])*)\*\*", apart)
            why = re.search(r"\*\*Why:\*\* (.*?)(?=\n\*\*Key Concept|\n</details>|\Z)", apart, re.S)
            stem = qpart.split("\nA. ", 1)[0].replace("**Scenario:**", "").strip()
            if opts and am:
                ans = am.group(1).replace(" ", "")
                add("PatrickWiloak practice questions (GitHub, CC BY 4.0)", "https://github.com/PatrickWiloak/cloud-data-ai-security-zero-to-hero",
                    "SAP-C02", len(ans.split(",")), stem, opts, ans, _clean(why.group(1)) if why else "")

    # Whizlabs blog: "Question No: #n" / Domain / "Question Text:" + <ul> requirements / <ol> unlettered options / "Correct Answer: B" / "Explanation:"
    f = os.path.join(ON, "whizlabs_blog_aws-solutions-architect-professional-exam-questions.html")
    if os.path.exists(f):
        h = open(f, encoding="utf-8", errors="replace").read()
        blocks = re.split(r"Question No: #\d+", h)[1:]
        for b in blocks:
            dom = re.search(r"<b>Domain:</b>(.*?)</span>", b, re.S)
            qt = re.search(r"<b>Question Text: </b>(.*?)<ol>", b, re.S) or re.search(r"Sub Topic:</b>.*?</p>(.*?)<ol>", b, re.S)
            ol = re.search(r"<ol>(.*?)</ol>", b, re.S)
            ca = re.search(r"Correct Answer:\s*(?:</b>|</strong>)?\s*(?:<[^>]+>\s*)*([A-H](?:\s*,\s*[A-H])*)", _clean(b) if False else b)
            ex = re.search(r"Explanation:\s*(?:</b>|</strong>)?(.*?)(?=Question No: #|<h4|\Z)", b, re.S)
            if not (qt and ol and ca):
                continue
            items = [_clean(x) for x in re.findall(r"<li[^>]*>(.*?)</li>", ol.group(1), re.S)]
            opts = {LET[k]: x for k, x in enumerate(items) if x}
            ans = ca.group(1).replace(" ", "")
            add("Whizlabs blog SAP sample questions", "https://www.whizlabs.com/blog/aws-solutions-architect-professional-exam-questions/", "SAP-C02",
                len(ans.split(",")), _clean(qt.group(1)), opts, ans, _clean(ex.group(1))[:1200] if ex else "", _clean(dom.group(1)) if dom else "")

    # examcert.app blog widget: <div class="sq-question" data-correct="A"> / <h3>Question n</h3> / <p>stem</p> / sq-option data-letter / sq-explanation
    f = os.path.join(ON, "examcert-app_sap-c02-practice-questions-2026_blog.html")
    if os.path.exists(f):
        h = open(f, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r'<div class="sq-question" data-correct="([A-H,]+)"[^>]*>(.*?)(?=<div class="sq-question"|\Z)', h, re.S):
            ans, b = m.group(1).replace(" ", ""), m.group(2)
            stem = re.search(r"</h3>\s*<p[^>]*>(.*?)</p>", b, re.S)
            opts = {L: re.sub(r"^[A-H]\.\s*", "", _clean(x)) for L, x in re.findall(r'<div class="sq-option" data-letter="([A-H])"[^>]*>(.*?)</div>', b, re.S)}
            ex = re.search(r'<div class="sq-explanation"[^>]*>(.*?)</div>', b, re.S)
            if stem and opts:
                add("examcert.app SAP-C02 blog questions", "https://www.examcert.app/blog/aws-sap-c02-practice-questions-2026/", "SAP-C02",
                    len(ans.split(",")), _clean(stem.group(1)), opts, ans, _clean(ex.group(1)) if ex else "")

    # Digital Cloud Training: accordion "Question n: stem" / <p><strong>A.</strong> ...</p> / "The correct answer is C." / "Explanation:" per-option
    f = os.path.join(ON, "digitalcloud-training_sap-free-practice-questions.html")
    if os.path.exists(f):
        h = open(f, encoding="utf-8", errors="replace").read()
        text = _clean(re.sub(r"<p><strong>([A-H])\.</strong>", r" OPT_\1 ", h))
        for m in re.finditer(r"Question (\d+): (.*?)(?=Question \d+: |\Z)", text, re.S):
            body = m.group(2)
            stem = body.split(" OPT_A ", 1)[0].strip()
            opts = {L: x.strip() for L, x in re.findall(r"OPT_([A-H]) (.*?)(?= OPT_[A-H] |Show Answer|The correct answer)", body, re.S)}
            ca = re.search(r"The correct answers? (?:is|are) ([A-H](?:\s*(?:,|and)\s*[A-H])*)", body)
            ex = re.search(r"Explanation:\s*(.*?)(?=References?:|Question \d+:|\Z)", body, re.S)
            if opts and ca:
                ans = ",".join(re.findall(r"[A-H]", ca.group(1)))
                add("Digital Cloud Training free SAP questions", "https://digitalcloud.training/aws-solutions-architect-professional-free-practice-questions/",
                    "SAP-C02", len(ans.split(",")), stem[:1500], opts, ans, _clean(ex.group(1))[:1500] if ex else "")

    # techpracticeexams.com blog: <h2>Question n</h2> / <p><strong>stem</strong></p> / <ul><li>A) ...</li></ul> / "Answer: B — ..." / prose
    f = os.path.join(ON, "techpracticeexams_sap-c02-practice-questions-1_blog.html")
    if os.path.exists(f):
        h = open(f, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"Question (\d+)</h2>(.*?)(?=<h2[^>]*>\s*Question \d+</h2>|\Z)", h, re.S):
            b = m.group(2)
            stem = re.search(r"<p><strong>(.*?)</strong></p>", b, re.S)
            opts = {L: _clean(x) for L, x in re.findall(r"<li>\s*([A-H])\)\s*(.*?)</li>", b, re.S)}
            ca = re.search(r"Answer:\s*([A-H](?:\s*,\s*[A-H])*)", _clean(b))
            ex = re.search(r"Answer:.*?</p>(.*)", b, re.S)
            if stem and opts and ca:
                ans = ca.group(1).replace(" ", "")
                add("techpracticeexams.com SAP-C02 blog questions", "https://techpracticeexams.com/blog/sap-c02-practice-questions-1", "SAP-C02",
                    len(ans.split(",")), _clean(stem.group(1)), opts, ans, _clean(ex.group(1))[:1500] if ex else "")
