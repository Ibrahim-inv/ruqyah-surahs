# -*- coding: utf-8 -*-
"""يبني صفحتي «سور الرقية» و«المسبحة».

الاستخدام: python3 build.py <مجلد quran> <مجلد المستودع> [<مجلد مخرجات الأداة>]
- المستودع: index.html و tasbih.html بهيكل كامل لغيت هب.
- مجلد الأداة (اختياري): النسختان بلا هيكل لنشرهما أداةً على كلود.
"""
import json, html, sys, os

SRC = sys.argv[1]
REPO = sys.argv[2]
ART = sys.argv[3] if len(sys.argv) > 3 else None

PAGES_BASE = "https://ibrahim-inv.github.io/ruqyah-surahs/"
BASMALA = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

def ar(n):
    return str(n).translate(AR_DIGITS)

def load(s):
    d = json.load(open(os.path.join(SRC, f"s{s}.json"), encoding="utf-8"))["data"]
    out = []
    for a in d["ayahs"]:
        t = a["text"].replace("﻿", "").strip()
        if s != 1 and a["numberInSurah"] == 1 and t.startswith(BASMALA):
            t = t[len(BASMALA):].strip()
        out.append((a["numberInSurah"], t))
    return out

def pick(s, start, end):
    return [a for a in load(s) if start <= a[0] <= end]

# ---------- المشترك ----------
FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri+Quran&family=Noto+Naskh+Arabic:wght@400;500;700&display=swap">'''

TOKENS = '''
:root {
  --bg: #f3f4ee; --card: #fbfcf8; --fg: #1e2924; --muted: #66716a; --line: #d6dbd1;
  --accent: #0f5e4a; --accent-soft: #e2efe9; --gold: #a5833a;
  --font-quran: "Amiri Quran", "Scheherazade New", "KFGQPC Uthman Taha Naskh", "Noto Naskh Arabic", serif;
  --font-ui: "Noto Naskh Arabic", "Geeza Pro", "Tahoma", serif;
  --qsize: 1.7rem;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #121816; --card: #1a211e; --fg: #e7eae3; --muted: #9aa59d; --line: #2b3531;
    --accent: #7fd3b4; --accent-soft: #1f2f29; --gold: #d2b36c; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #121816; --card: #1a211e; --fg: #e7eae3; --muted: #9aa59d; --line: #2b3531;
  --accent: #7fd3b4; --accent-soft: #1f2f29; --gold: #d2b36c; color-scheme: dark;
}
* { box-sizing: border-box; }
'''

def wrap_standalone(page, description):
    """يغلّف صفحة الأداة بهيكل كامل لغيت هب."""
    i = page.index("</style>") + len("</style>")
    head = page[:i].replace('<meta charset="utf-8">\n', "", 1).replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "", 1)
    body = page[i:]
    return ("<!doctype html>\n<html lang=\"ar\" dir=\"rtl\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            f"<meta name=\"description\" content=\"{html.escape(description)}\">\n"
            "<meta name=\"color-scheme\" content=\"light dark\">\n"
            + head +
            "\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>\n</head>\n<body>"
            + body + "\n</body>\n</html>\n")

# ---------- صفحة السور ----------
def build_ruqyah(tasbih_href):
    items = [
        ("fatiha",  "سورة الفاتحة",       "٧ آيات",             [("", load(1))],            False, ""),
        ("kursi",   "آية الكرسي",         "البقرة ٢٥٥",         [("", pick(2, 255, 255))],  False, ""),
        ("baqara1", "أوائل سورة البقرة",  "الآيات ١ إلى ٥",     [("", pick(2, 1, 5))],      True,  ""),
        ("baqara2", "خواتيم سورة البقرة", "الآيتان ٢٨٥ و٢٨٦",   [("", pick(2, 285, 286))],  False, ""),
        ("sihr",    "آيات السحر",         "الأعراف ويونس وطه",  [
            ("سورة الأعراف، الآيات ١١٧ إلى ١٢٢", pick(7, 117, 122)),
            ("سورة يونس، الآيات ٧٩ إلى ٨٢",      pick(10, 79, 82)),
            ("سورة طه، الآيات ٦٥ إلى ٦٩",        pick(20, 65, 69)),
        ], False, "الآيات التي يوصي بها ابن باز وغيره لإبطال السحر، وليست في نسخ رقية التعطيل المتداولة."),
        ("anfal",   "سورة الأنفال",       "٧٥ آية",             [("", load(8))],            True,  ""),
        ("saffat",  "سورة الصافات",       "١٨٢ آية",            [("", load(37))],           True,  ""),
        ("haqqa",   "سورة الحاقة",        "٥٢ آية",             [("", load(69))],           True,  ""),
        ("zalzala", "سورة الزلزلة",       "٨ آيات",             [("", load(99))],           True,  ""),
        ("qaria",   "سورة القارعة",       "١١ آية",             [("", load(101))],          True,  "وردت في نسخة الرقية الشاملة فقط"),
        ("dukhan",  "سورة الدخان",        "٥٩ آية",             [("", load(44))],           True,  ""),
        ("kafirun", "سورة الكافرون",      "٦ آيات",             [("", load(109))],          True,  ""),
        ("ikhlas",  "سورة الإخلاص",       "٤ آيات",             [("", load(112))],          True,  ""),
        ("falaq",   "سورة الفلق",         "٥ آيات",             [("", load(113))],          True,  ""),
        ("nas",     "سورة الناس",         "٦ آيات",             [("", load(114))],          True,  ""),
    ]

    def render_ayat(ayahs):
        return " ".join(
            f'<span class="a">{html.escape(t)}</span> <span class="n" aria-label="آية {ar(n)}">{ar(n)}</span>'
            for n, t in ayahs)

    sections = []
    total = len(items)
    total_ayahs = 0
    for i, (sid, title, meta, passages, bas, note) in enumerate(items):
        nxt = items[i + 1] if i + 1 < total else None
        note_html = f'<span class="note">{html.escape(note)}</span>' if note else ""
        bas_html = f'<p class="basmala">{BASMALA}</p>' if bas else ""
        body = []
        for label, ayahs in passages:
            total_ayahs += len(ayahs)
            if label:
                body.append(f'<p class="plabel">{html.escape(label)}</p>')
            body.append(f'<p class="ayat">{render_ayat(ayahs)}</p>')
        next_html = (f'<button type="button" class="next" data-next="{nxt[0]}">التالي: {html.escape(nxt[1])}</button>'
                     if nxt else '<button type="button" class="next" data-next="hisn">التالي: التحصين</button>')
        sections.append(f'''
<section class="surah" id="{sid}">
  <h2 class="head-wrap">
    <button type="button" class="head" id="h-{sid}" aria-expanded="false" aria-controls="b-{sid}">
      <span class="idx">{ar(i + 1)}</span>
      <span class="name">{html.escape(title)}</span>
      <span class="meta">{html.escape(meta)}</span>
      <span class="chev" aria-hidden="true"></span>
    </button>
  </h2>
  <div class="body" id="b-{sid}" hidden>
    {note_html}
    {bas_html}
    {''.join(body)}
    <div class="foot">
      <label class="read"><input type="checkbox" id="r-{sid}" data-read="{sid}"> قرأتها</label>
      {next_html}
    </div>
  </div>
</section>''')

    css = TOKENS + '''
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font-family: var(--font-ui); font-size: 1rem; line-height: 1.7;
  padding-block: 0 4rem;
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
}
.page { max-width: 46rem; margin: 0 auto; min-width: 0; }
header.top { text-align: center; padding-block: 2rem 1rem; }
header.top h1 { font-family: var(--font-quran); font-weight: 400; font-size: 2.4rem; margin: 0; color: var(--accent); text-wrap: balance; line-height: 1.4; }
header.top p { margin: .4rem 0 0; color: var(--muted); font-size: .95rem; }
.navlink { display: inline-block; margin-top: .8rem; font-size: .95rem; color: var(--accent); text-decoration: none; border: 1px solid var(--line); background: var(--card); border-radius: 2rem; padding: .3rem 1rem; }
.navlink:hover { border-color: var(--accent); }
.toolbar {
  position: sticky; top: env(safe-area-inset-top, 0px); z-index: 2;
  display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: .5rem .75rem;
  background: var(--bg); border-bottom: 1px solid var(--line); padding-block: .6rem; margin-bottom: 1rem;
}
.toolbar .group { display: flex; align-items: center; gap: .4rem; }
.toolbar button { font: inherit; font-size: .9rem; color: var(--fg); background: var(--card); border: 1px solid var(--line); border-radius: .5rem; padding: .3rem .7rem; cursor: pointer; }
.toolbar button:hover { border-color: var(--accent); }
.toolbar button:focus-visible, .head:focus-visible, .next:focus-visible, .read input:focus-visible, .navlink:focus-visible, .start button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.progress { color: var(--muted); font-size: .9rem; font-variant-numeric: tabular-nums; }
.list { display: flex; flex-direction: column; gap: .7rem; }
.surah { min-width: 0; }
.head-wrap { margin: 0; font-size: 1rem; }
.head {
  width: 100%; display: grid; grid-template-columns: auto 1fr auto auto; align-items: center; gap: .75rem;
  text-align: right; font: inherit; color: var(--fg); cursor: pointer;
  background: var(--card); border: 1px solid var(--line); border-radius: .6rem; padding: .7rem 1rem;
  transition: border-color .15s, background .15s;
}
.head:hover { border-color: var(--accent); }
.head[aria-expanded="true"] { background: var(--accent-soft); border-color: var(--accent); }
.idx { display: inline-grid; place-items: center; width: 1.9rem; height: 1.9rem; border-radius: 50%; border: 1px solid var(--gold); color: var(--gold); font-size: .85rem; font-variant-numeric: tabular-nums; }
.surah.read .idx { background: var(--gold); color: var(--card); }
.name { font-family: var(--font-quran); font-size: 1.45rem; line-height: 1.3; min-width: 0; }
.meta { color: var(--muted); font-size: .85rem; white-space: nowrap; }
.chev { width: .55rem; height: .55rem; border-right: 2px solid var(--muted); border-bottom: 2px solid var(--muted); transform: rotate(45deg); transition: transform .2s; margin-left: .2rem; }
.head[aria-expanded="true"] .chev { transform: rotate(-135deg); }
.body { background: var(--card); border: 1px solid var(--line); border-top: 0; border-radius: 0 0 .6rem .6rem; margin-top: -.35rem; padding: 1.4rem 1.25rem 1rem; }
.note { display: block; color: var(--muted); font-size: .85rem; margin-bottom: .8rem; }
.plabel { color: var(--accent); font-size: .9rem; margin: 1.2rem 0 .3rem; }
.plabel:first-of-type { margin-top: 0; }
.basmala { font-family: var(--font-quran); font-size: calc(var(--qsize) * 1.05); text-align: center; margin: 0 0 1rem; color: var(--accent); line-height: 2; }
.ayat { font-family: var(--font-quran); font-size: var(--qsize); line-height: 2.25; text-align: justify; margin: 0; min-width: 0; overflow-wrap: anywhere; }
.n { display: inline-grid; place-items: center; min-width: 1.35em; height: 1.35em; padding: 0 .2em; border: 1px solid var(--gold); border-radius: 50%; color: var(--gold); font-family: var(--font-ui); font-size: .5em; line-height: 1; vertical-align: .35em; margin: 0 .15em; font-variant-numeric: tabular-nums; }
.foot { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: .6rem; border-top: 1px dashed var(--line); margin-top: 1.4rem; padding-top: .9rem; }
.read { display: inline-flex; align-items: center; gap: .4rem; cursor: pointer; color: var(--muted); }
.read input { accent-color: var(--accent); width: 1.1rem; height: 1.1rem; }
.next { font: inherit; font-size: .95rem; color: var(--card); background: var(--accent); border: 0; border-radius: .5rem; padding: .45rem .9rem; cursor: pointer; }
.hisn { margin-top: 2.2rem; min-width: 0; }
.hisn h2 { font-family: var(--font-quran); color: var(--accent); text-align: center; font-weight: 400; font-size: 2rem; margin: 0 0 .2rem; line-height: 1.4; }
.hisn .lead { text-align: center; color: var(--muted); font-size: .9rem; margin: 0 0 1rem; }
.hisn h3 { font-size: .85rem; font-weight: 500; color: var(--muted); letter-spacing: .02em; margin: 1.2rem 0 .5rem; }
.hisn .cards { display: flex; flex-direction: column; gap: .7rem; }
.dhikr { background: var(--card); border: 1px solid var(--line); border-radius: .6rem; padding: 1rem 1.1rem; display: flex; flex-direction: column; gap: .45rem; min-width: 0; }
.dhikr .t { font-family: var(--font-quran); font-size: calc(var(--qsize) * .82); line-height: 2; margin: 0; overflow-wrap: anywhere; }
.dhikr .rep { color: var(--gold); font-size: .85rem; }
.dhikr .src, .hisn .src { color: var(--muted); font-size: .85rem; margin: 0; }
.tahrij { margin-top: .2rem; margin-bottom: 1.8rem; }
.tahrij .start { display: flex; justify-content: center; margin-top: 1rem; }
.start button { font: inherit; font-size: 1rem; color: var(--card); background: var(--accent); border: 0; border-radius: .5rem; padding: .55rem 1.3rem; cursor: pointer; }
footer.bottom { color: var(--muted); font-size: .85rem; text-align: center; margin-top: 2.5rem; line-height: 1.8; }
@media (max-width: 480px) {
  .head { grid-template-columns: auto 1fr auto; }
  .meta { grid-column: 2; grid-row: 2; }
  .chev { grid-column: 3; grid-row: 1 / span 2; }
  .name { font-size: 1.3rem; }
}
@media (prefers-reduced-motion: reduce) { .chev, .head { transition: none; } }
'''

    page = f'''<meta charset="utf-8">
<title>سور الرقية</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<style>
/* صفحة قراءة: عمود واحد، كل سورة شريط عنوان يُفتح على نصها. */{css}</style>

<div class="page" dir="rtl" lang="ar">
  <header class="top">
    <h1>سور الرقية</h1>
    <p>التحريج، ثم السور والمقاطع المتداولة في رقية التعطيل بترتيبها المشهور مع آيات السحر، ثم التحصين. اضغط على السورة لتُفتح للقراءة.</p>
    <a class="navlink" href="{tasbih_href}">المسبحة: عدّاد الأذكار</a>
  </header>

  <div class="toolbar">
    <div class="group">
      <button type="button" id="font-down" aria-label="تصغير الخط">أ−</button>
      <button type="button" id="font-up" aria-label="تكبير الخط">أ+</button>
    </div>
    <span class="progress" id="progress"></span>
    <div class="group">
      <button type="button" id="open-all">فتح الكل</button>
      <button type="button" id="close-all">طي الكل</button>
    </div>
  </div>

  <section class="hisn tahrij" id="tahrij">
    <h2>التحريج</h2>
    <p class="lead">يُقرأ مرة واحدة قبل البدء بالسور.</p>
    <div class="cards">
      <div class="dhikr">
        <p class="t">دَخَلْتُ عَلَى جَسَدِي بِلَا إِلَٰهَ إِلَّا اللَّهُ، أُنَاشِدُ كُلَّ مَنْ دَخَلَ جَسَدِي مِنَ الشَّيَاطِينِ وَمِنَ السِّحْرِ وَالْحَسَدِ وَالْعَيْنِ تَرْكَ جَسَدِي طَاعَةً لِلَّهِ وَلِرَسُولِهِ، لَا تُؤْذُونِي وَلَا أُوذِيكُمْ</p>
        <p class="src">الصيغة الأولى في الرقية المتداولة.</p>
      </div>
      <div class="dhikr">
        <p class="t">أُحَرِّجُ عَلَى مَنْ حَلَّ بِجَسَدِي وَزَوْجِي وَأَبْنَائِي، أُحَرِّجُ عَلَيْكُمْ تَرْكَ هَذَا الْمَكَانِ طَاعَةً لِلَّهِ</p>
        <p class="src">الصيغة الثانية في الرقية المتداولة، وتشمل الأهل والمكان.</p>
      </div>
    </div>
    <p class="src" style="margin-top:.8rem">الصيغتان من اجتهاد الرقاة لا من المأثور. ومخاطبة الجن وردت عن ابن تيمية مع المصروع الحاضر، وقيّدها ابن باز بترك المبالغة، وقصرها إسلام ويب على الأمر بالمعروف والنهي عن المنكر.</p>
    <div class="start"><button type="button" id="start-ruqyah">ابدأ الرقية من الفاتحة</button></div>
  </section>

  <main class="list" id="list">
{''.join(sections)}
  </main>

  <section class="hisn" id="hisn">
    <h2>التحصين</h2>
    <p class="lead">يُقرأ بعد الانتهاء من السور، أو في الصباح والمساء.</p>
    <h3>صيغة التحصين في الرقية المتداولة</h3>
    <div class="cards">
      <div class="dhikr">
        <p class="t">تَحَصَّنْتُ بِلَا إِلَٰهَ إِلَّا اللَّهُ، تَحَصَّنْتُ بِرَبِّ الْفَلَقِ مِنْ شَرِّ مَا خَلَقَ</p>
        <p class="src">صيغة الرقية المتداولة. معناها صحيح، ولم أجد لها أصلًا مأثورًا عن النبي صلى الله عليه وسلم.</p>
      </div>
    </div>
    <h3>أذكار التحصين الثابتة في السنة</h3>
    <div class="cards">
      <div class="dhikr">
        <p class="t">بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ</p>
        <span class="rep">ثلاث مرات صباحًا ومساءً</span>
        <p class="src">أبو داود 5088، والترمذي 3388، وصححه الألباني.</p>
      </div>
      <div class="dhikr">
        <p class="t">أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ</p>
        <span class="rep">ثلاث مرات في المساء</span>
        <p class="src">صحيح مسلم 2708 و2709.</p>
      </div>
      <div class="dhikr">
        <p class="t">أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ الَّتِي لَا يُجَاوِزُهُنَّ بَرٌّ وَلَا فَاجِرٌ، مِنْ شَرِّ مَا خَلَقَ وَذَرَأَ وَبَرَأَ، وَمِنْ شَرِّ مَا يَنْزِلُ مِنَ السَّمَاءِ وَمِنْ شَرِّ مَا يَعْرُجُ فِيهَا، وَمِنْ شَرِّ مَا ذَرَأَ فِي الْأَرْضِ وَمِنْ شَرِّ مَا يَخْرُجُ مِنْهَا، وَمِنْ شَرِّ فِتَنِ اللَّيْلِ وَالنَّهَارِ، وَمِنْ شَرِّ كُلِّ طَارِقٍ إِلَّا طَارِقًا يَطْرُقُ بِخَيْرٍ يَا رَحْمَنُ</p>
        <p class="src">مسند أحمد 3/419 من حديث عبدالرحمن بن خنبش، وحسّن إسناده العراقي.</p>
      </div>
      <div class="dhikr">
        <p class="t">آية الكرسي، وسورة الإخلاص والفلق والناس</p>
        <span class="rep">المعوذات ثلاث مرات صباحًا ومساءً، وآية الكرسي عند النوم</span>
        <p class="src">البخاري 2311، وأبو داود 5082 والترمذي 3575 وحسّنه.</p>
      </div>
    </div>
  </section>

  <footer class="bottom">
    النص برواية حفص عن عاصم بالرسم العثماني من مشروع «تنزيل».<br>
    الترتيب هنا ترتيب الرقية المتداولة لا ترتيب المصحف، وليس لتخصيص هذه السور أصل في النص.
  </footer>
</div>

<script>
(function () {{
  var root = document.documentElement;
  root.setAttribute('dir', 'rtl'); root.setAttribute('lang', 'ar');
  var TOTAL = {total};
  var AR = ['٠','١','٢','٣','٤','٥','٦','٧','٨','٩'];
  function ar(n) {{ return String(n).replace(/\\d/g, function (d) {{ return AR[+d]; }}); }}
  function load(k, fb) {{ try {{ var v = localStorage.getItem(k); return v === null ? fb : JSON.parse(v); }} catch (e) {{ return fb; }} }}
  function save(k, v) {{ try {{ localStorage.setItem(k, JSON.stringify(v)); }} catch (e) {{}} }}

  var size = load('ruqyah.size', 1.7);
  function applySize() {{ root.style.setProperty('--qsize', size + 'rem'); }}
  applySize();
  document.getElementById('font-up').addEventListener('click', function () {{ size = Math.min(3, +(size + 0.15).toFixed(2)); applySize(); save('ruqyah.size', size); }});
  document.getElementById('font-down').addEventListener('click', function () {{ size = Math.max(1.1, +(size - 0.15).toFixed(2)); applySize(); save('ruqyah.size', size); }});

  function setOpen(sec, open) {{
    sec.querySelector('.head').setAttribute('aria-expanded', open ? 'true' : 'false');
    sec.querySelector('.body').hidden = !open;
  }}
  var sections = Array.prototype.slice.call(document.querySelectorAll('.surah'));
  sections.forEach(function (sec) {{
    sec.querySelector('.head').addEventListener('click', function () {{
      var open = this.getAttribute('aria-expanded') === 'true';
      setOpen(sec, !open);
      if (!open) sec.scrollIntoView({{ block: 'start', behavior: 'smooth' }});
    }});
    sec.querySelector('.next').addEventListener('click', function () {{
      var target = document.getElementById(this.getAttribute('data-next'));
      setOpen(sec, false);
      if (target.classList.contains('surah')) setOpen(target, true);
      target.scrollIntoView({{ block: 'start', behavior: 'smooth' }});
    }});
  }});
  document.getElementById('open-all').addEventListener('click', function () {{ sections.forEach(function (s) {{ setOpen(s, true); }}); }});
  document.getElementById('close-all').addEventListener('click', function () {{ sections.forEach(function (s) {{ setOpen(s, false); }}); }});
  document.getElementById('start-ruqyah').addEventListener('click', function () {{
    setOpen(sections[0], true); sections[0].scrollIntoView({{ block: 'start', behavior: 'smooth' }});
  }});

  var read = load('ruqyah.read', {{}});
  function updateProgress() {{
    var n = sections.filter(function (s) {{ return read[s.id]; }}).length;
    document.getElementById('progress').textContent = 'قرأت ' + ar(n) + ' من ' + ar(TOTAL);
  }}
  sections.forEach(function (sec) {{
    var box = sec.querySelector('input[data-read]');
    box.checked = !!read[sec.id]; sec.classList.toggle('read', box.checked);
    box.addEventListener('change', function () {{
      read[sec.id] = this.checked; if (!this.checked) delete read[sec.id];
      sec.classList.toggle('read', this.checked); save('ruqyah.read', read); updateProgress();
    }});
  }});
  updateProgress();

  var h = (location.hash || '').replace('#', '');
  var target = h && document.getElementById(h);
  if (target && target.classList.contains('surah')) {{ setOpen(target, true); target.scrollIntoView(); }}
  else setOpen(sections[0], true);
}})();
</script>
'''
    return page, total_ayahs

# ---------- صفحة المسبحة ----------
ADHKAR = [
    ("istighfar", "الاستغفار", "أَسْتَغْفِرُ اللَّهَ"),
    ("hawqala",   "الحوقلة", "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ"),
    ("hayy",      "دعاء الاستغاثة", "يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ، أَصْلِحْ لِي شَأْنِي كُلَّهُ، وَلَا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ وَلَا أَدْنَى مِنْ ذَلِكَ"),
    ("malik",     "من الفاتحة", "يَا مَالِكَ يَوْمِ الدِّينِ، إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ"),
    ("salat",     "الصلاة على النبي", "اللَّهُمَّ صَلِّ وَسَلِّمْ وَبَارِكْ عَلَى نَبِيِّنَا مُحَمَّدٍ"),
]

def build_tasbih(index_href):
    data_js = json.dumps([{"id": i, "label": l, "text": t} for i, l, t in ADHKAR], ensure_ascii=False)
    dots = "".join(f'<span class="dot" data-i="{i}"></span>' for i in range(len(ADHKAR)))
    css = TOKENS + '''
html, body { height: 100%; }
body {
  margin: 0; background: var(--bg); color: var(--fg); font-family: var(--font-ui); line-height: 1.6;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  overflow: hidden;
}
.app { height: 100%; max-width: 40rem; margin: 0 auto; display: flex; flex-direction: column; min-width: 0; }
.bar { display: flex; align-items: center; justify-content: space-between; gap: .5rem; padding-block: .7rem .3rem; }
.bar h1 { font-family: var(--font-quran); font-weight: 400; font-size: 1.7rem; margin: 0; color: var(--accent); }
.bar a, .bar button { font: inherit; font-size: .9rem; color: var(--accent); background: var(--card); border: 1px solid var(--line); border-radius: 2rem; padding: .25rem .9rem; text-decoration: none; cursor: pointer; }
.bar a:hover, .bar button:hover { border-color: var(--accent); }
.niyya { background: var(--accent-soft); border: 1px solid var(--line); border-radius: .7rem; padding: .8rem 1rem; margin-top: .4rem; font-size: .95rem; }
.niyya p { margin: 0; }
.niyya .k { color: var(--accent); font-weight: 500; }
.niyya .m { color: var(--muted); font-size: .85rem; margin-top: .3rem; }
.surface {
  flex: 1; min-height: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: .6rem;
  text-align: center; cursor: pointer; user-select: none; -webkit-user-select: none; touch-action: none; padding-block: .5rem;
}
.dots { display: flex; gap: .45rem; }
.dot { width: .55rem; height: .55rem; border-radius: 50%; border: 1px solid var(--gold); }
.dot.on { background: var(--gold); }
.label { color: var(--muted); font-size: .9rem; margin: 0; }
.text { font-family: var(--font-quran); font-size: clamp(1.4rem, 5.5vw, 2.1rem); line-height: 1.9; margin: 0; max-width: 32rem; text-wrap: balance; }
.ring { position: relative; width: min(58vw, 15rem); aspect-ratio: 1; max-width: 100%; }
.ring svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.ring .track { fill: none; stroke: var(--line); stroke-width: 6; }
.ring .bar2 { fill: none; stroke: var(--accent); stroke-width: 6; stroke-linecap: round; transition: stroke-dashoffset .15s; }
.ring.hundred .bar2 { stroke: var(--gold); }
.count { position: absolute; inset: 0; display: grid; place-items: center; font-size: clamp(2.6rem, 12vw, 4.2rem); font-variant-numeric: tabular-nums; line-height: 1; }
.count.pop { animation: pop .18s ease-out; }
@keyframes pop { 0% { transform: scale(1); } 40% { transform: scale(1.12); } 100% { transform: scale(1); } }
.sub { color: var(--muted); font-size: .9rem; margin: 0; font-variant-numeric: tabular-nums; }
.hint { color: var(--muted); font-size: .8rem; margin: 0; }
.controls { display: flex; justify-content: space-between; align-items: center; gap: .5rem; padding-block: .5rem 1rem; }
.controls button { font: inherit; font-size: .95rem; color: var(--fg); background: var(--card); border: 1px solid var(--line); border-radius: .6rem; padding: .5rem 1rem; cursor: pointer; min-width: 5.5rem; }
.controls button:hover { border-color: var(--accent); }
.controls button.warn { color: var(--card); background: #a84b3c; border-color: #a84b3c; }
.controls .total { color: var(--muted); font-size: .85rem; font-variant-numeric: tabular-nums; }
button:focus-visible, a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { .count.pop { animation: none; } .ring .bar2 { transition: none; } }
'''
    page = f'''<meta charset="utf-8">
<title>المسبحة</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<style>
/* شاشة واحدة: الذكر في الوسط وحلقة المئة حوله، اللمس يعدّ والسحب ينقل. */{css}</style>

<div class="app" dir="rtl" lang="ar">
  <header class="bar">
    <a href="{index_href}">سور الرقية</a>
    <h1>المسبحة</h1>
    <button type="button" id="niyya-btn" aria-expanded="true" aria-controls="niyya">النية</button>
  </header>
  <div class="niyya" id="niyya">
    <p><span class="k">استحضر النية:</span> الصدقة، وبنية الفرج وتيسير الأمر، وأن يُسخِّر الله لك من هو أقوى منك.</p>
    <p class="m">بالمئات، ولو استطعت بالآلاف.</p>
  </div>

  <main class="surface" id="surface" aria-live="polite">
    <div class="dots" id="dots">{dots}</div>
    <p class="label" id="label"></p>
    <p class="text" id="text"></p>
    <div class="ring" id="ring">
      <svg viewBox="0 0 120 120" aria-hidden="true">
        <circle class="track" cx="60" cy="60" r="54"></circle>
        <circle class="bar2" id="bar" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29"></circle>
      </svg>
      <div class="count" id="count">٠</div>
    </div>
    <p class="sub" id="sub"></p>
    <p class="hint">اضغط في أي مكان للعدّ، واسحب للانتقال إلى الذكر التالي</p>
  </main>

  <footer class="controls">
    <button type="button" id="prev">السابق</button>
    <span class="total" id="total"></span>
    <button type="button" id="reset">تصفير</button>
    <button type="button" id="next">التالي</button>
  </footer>
</div>

<script>
(function () {{
  var root = document.documentElement;
  root.setAttribute('dir', 'rtl'); root.setAttribute('lang', 'ar');
  var ADHKAR = {data_js};
  var AR = ['٠','١','٢','٣','٤','٥','٦','٧','٨','٩'];
  var C = 339.29;
  function ar(n) {{ return String(n).replace(/\\d/g, function (d) {{ return AR[+d]; }}); }}
  function load(k, fb) {{ try {{ var v = localStorage.getItem(k); return v === null ? fb : JSON.parse(v); }} catch (e) {{ return fb; }} }}
  function save(k, v) {{ try {{ localStorage.setItem(k, JSON.stringify(v)); }} catch (e) {{}} }}

  var counts = load('tasbih.counts', {{}});
  var cur = Math.min(ADHKAR.length - 1, Math.max(0, load('tasbih.current', 0)));
  var niyyaOpen = load('tasbih.niyya', true);

  var $ = function (id) {{ return document.getElementById(id); }};
  var elCount = $('count'), elBar = $('bar'), elRing = $('ring'), elSub = $('sub'), elTotal = $('total');
  var dots = Array.prototype.slice.call(document.querySelectorAll('.dot'));

  function render(anim) {{
    var d = ADHKAR[cur], n = counts[d.id] || 0;
    $('label').textContent = d.label;
    $('text').textContent = d.text;
    elCount.textContent = ar(n);
    var inHundred = n === 0 ? 0 : (n % 100 === 0 ? 100 : n % 100);
    elBar.setAttribute('stroke-dashoffset', (C * (1 - inHundred / 100)).toFixed(2));
    elRing.classList.toggle('hundred', n > 0 && n % 100 === 0);
    elSub.textContent = 'المئات المكتملة: ' + ar(Math.floor(n / 100)) + (n >= 1000 ? ' · تجاوزت الألف' : '');
    var all = 0; ADHKAR.forEach(function (x) {{ all += counts[x.id] || 0; }});
    elTotal.textContent = 'المجموع ' + ar(all);
    dots.forEach(function (el, i) {{ el.classList.toggle('on', i === cur); }});
    if (anim) {{ elCount.classList.remove('pop'); void elCount.offsetWidth; elCount.classList.add('pop'); }}
  }}

  function count() {{
    var d = ADHKAR[cur];
    counts[d.id] = (counts[d.id] || 0) + 1;
    save('tasbih.counts', counts);
    render(true);
    try {{ if (navigator.vibrate) navigator.vibrate(counts[d.id] % 100 === 0 ? [40, 60, 40] : 12); }} catch (e) {{}}
  }}
  function go(delta) {{
    cur = (cur + delta + ADHKAR.length) % ADHKAR.length;
    save('tasbih.current', cur);
    render(false);
  }}

  // اللمس يعدّ، السحب ينقل
  var sx = 0, sy = 0, st = 0, moved = false, active = false;
  var surf = $('surface');
  surf.addEventListener('pointerdown', function (e) {{
    if (e.button !== undefined && e.button !== 0) return;
    active = true; moved = false; sx = e.clientX; sy = e.clientY; st = Date.now();
  }});
  surf.addEventListener('pointermove', function (e) {{
    if (!active) return;
    if (Math.abs(e.clientX - sx) > 10 || Math.abs(e.clientY - sy) > 10) moved = true;
  }});
  function finish(e) {{
    if (!active) return; active = false;
    var dx = e.clientX - sx, dy = e.clientY - sy;
    var ax = Math.abs(dx), ay = Math.abs(dy);
    if (ax > 45 || ay > 45) {{
      // في الاتجاه العربي: السحب لليسار أو للأعلى = التالي
      if (ax >= ay) go(dx < 0 ? 1 : -1); else go(dy < 0 ? 1 : -1);
    }} else if (!moved) {{
      count();
    }}
  }}
  surf.addEventListener('pointerup', finish);
  surf.addEventListener('pointercancel', function () {{ active = false; }});
  surf.addEventListener('contextmenu', function (e) {{ e.preventDefault(); }});

  // لوحة المفاتيح
  document.addEventListener('keydown', function (e) {{
    if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') return;
    if (e.code === 'Space' || e.code === 'Enter') {{ e.preventDefault(); count(); }}
    else if (e.code === 'ArrowLeft') go(1);
    else if (e.code === 'ArrowRight') go(-1);
  }});

  $('next').addEventListener('click', function () {{ go(1); }});
  $('prev').addEventListener('click', function () {{ go(-1); }});

  // تصفير على خطوتين
  var resetBtn = $('reset'), armed = null;
  resetBtn.addEventListener('click', function () {{
    if (armed) {{
      clearTimeout(armed); armed = null;
      delete counts[ADHKAR[cur].id]; save('tasbih.counts', counts);
      resetBtn.textContent = 'تصفير'; resetBtn.classList.remove('warn'); render(false);
    }} else {{
      resetBtn.textContent = 'تأكيد التصفير'; resetBtn.classList.add('warn');
      armed = setTimeout(function () {{ armed = null; resetBtn.textContent = 'تصفير'; resetBtn.classList.remove('warn'); }}, 3000);
    }}
  }});

  // النية
  var nb = $('niyya-btn'), nbox = $('niyya');
  function applyNiyya() {{ nbox.hidden = !niyyaOpen; nb.setAttribute('aria-expanded', niyyaOpen ? 'true' : 'false'); }}
  applyNiyya();
  nb.addEventListener('click', function () {{ niyyaOpen = !niyyaOpen; save('tasbih.niyya', niyyaOpen); applyNiyya(); }});

  render(false);
}})();
</script>
'''
    return page

# ---------- الإخراج ----------
RUQYAH_DESC = "صفحة قراءة لسور الرقية المتداولة بترتيبها، كل سورة تُفتح بالضغط عليها"
TASBIH_DESC = "مسبحة أذكار: اضغط للعدّ واسحب للانتقال إلى الذكر التالي"

# نسخة غيت هب: روابط نسبية
ruqyah_page, n_ayahs = build_ruqyah("tasbih.html")
tasbih_page = build_tasbih("index.html")
open(os.path.join(REPO, "index.html"), "w", encoding="utf-8").write(wrap_standalone(ruqyah_page, RUQYAH_DESC))
open(os.path.join(REPO, "tasbih.html"), "w", encoding="utf-8").write(wrap_standalone(tasbih_page, TASBIH_DESC))
print("repo pages written; ayahs on ruqyah page:", n_ayahs)

# نسخة الأداة: روابط إلى الموقع العام
if ART:
    os.makedirs(ART, exist_ok=True)
    rp, _ = build_ruqyah(PAGES_BASE + "tasbih.html")
    tp = build_tasbih(PAGES_BASE)
    open(os.path.join(ART, "ruqyah-surahs.html"), "w", encoding="utf-8").write(rp)
    open(os.path.join(ART, "tasbih.html"), "w", encoding="utf-8").write(tp)
    print("artifact pages written to", ART)
