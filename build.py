#!/usr/bin/env python3
"""Kept Hour static site generator. One command, whole site."""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://orionarchitekton.github.io/kept-hour"
UPDATED = "2026-09-26"

ROLES = [
    ("software-engineer", "Software engineer", 128000, 45),
    ("registered-nurse", "Registered nurse", 86000, 42),
    ("teacher", "Teacher", 64000, 50),
    ("accountant", "Accountant", 78000, 45),
    ("project-manager", "Project manager", 98000, 48),
    ("marketing-manager", "Marketing manager", 88000, 46),
    ("sales-representative", "Sales representative", 72000, 45),
    ("customer-support", "Customer support specialist", 48000, 40),
    ("electrician", "Electrician", 68000, 42),
    ("plumber", "Plumber", 67000, 42),
    ("hvac-technician", "HVAC technician", 62000, 42),
    ("truck-driver", "Truck driver", 56000, 55),
    ("warehouse-associate", "Warehouse associate", 40000, 40),
    ("retail-manager", "Retail manager", 52000, 48),
    ("restaurant-manager", "Restaurant manager", 54000, 50),
    ("chef", "Chef", 56000, 50),
    ("graphic-designer", "Graphic designer", 62000, 42),
    ("ux-designer", "UX designer", 98000, 42),
    ("data-analyst", "Data analyst", 86000, 42),
    ("product-manager", "Product manager", 135000, 48),
    ("lawyer", "Lawyer", 145000, 55),
    ("paralegal", "Paralegal", 62000, 42),
    ("pharmacist", "Pharmacist", 132000, 40),
    ("physical-therapist", "Physical therapist", 98000, 40),
    ("dental-hygienist", "Dental hygienist", 87000, 36),
    ("social-worker", "Social worker", 58000, 42),
    ("hr-generalist", "HR generalist", 70000, 42),
    ("recruiter", "Recruiter", 68000, 45),
    ("financial-analyst", "Financial analyst", 96000, 48),
    ("operations-manager", "Operations manager", 92000, 48),
    ("construction-manager", "Construction manager", 104000, 50),
    ("carpenter", "Carpenter", 58000, 42),
    ("mechanic", "Mechanic", 52000, 42),
    ("police-officer", "Police officer", 72000, 46),
    ("firefighter", "Firefighter", 58000, 56),
    ("paramedic", "Paramedic", 50000, 48),
    ("journalist", "Journalist", 55000, 45),
    ("copywriter", "Copywriter", 68000, 40),
    ("real-estate-agent", "Real estate agent", 62000, 45),
    ("insurance-agent", "Insurance agent", 64000, 42),
    ("executive-assistant", "Executive assistant", 70000, 45),
    ("office-administrator", "Office administrator", 48000, 40),
    ("barista", "Barista", 32000, 32),
    ("server", "Restaurant server", 34000, 30),
    ("delivery-driver", "Delivery driver", 38000, 40),
    ("pharmacy-technician", "Pharmacy technician", 40000, 40),
    ("medical-assistant", "Medical assistant", 42000, 40),
    ("veterinary-technician", "Veterinary technician", 40000, 40),
    ("librarian", "Librarian", 62000, 40),
    ("architect", "Architect", 92000, 48),
]

# Effective combined income-tax load used as a planning default, not a filing number.
# Rent is a typical 1-bedroom asking rent, 2025–26 planning range, labeled as such.
CITIES = [
    ("new-york-ny", "New York, NY", "United States", 0.30, 4200),
    ("los-angeles-ca", "Los Angeles, CA", "United States", 0.28, 2800),
    ("chicago-il", "Chicago, IL", "United States", 0.27, 2100),
    ("houston-tx", "Houston, TX", "United States", 0.24, 1600),
    ("phoenix-az", "Phoenix, AZ", "United States", 0.24, 1700),
    ("philadelphia-pa", "Philadelphia, PA", "United States", 0.27, 1800),
    ("san-antonio-tx", "San Antonio, TX", "United States", 0.24, 1400),
    ("san-diego-ca", "San Diego, CA", "United States", 0.28, 2800),
    ("dallas-tx", "Dallas, TX", "United States", 0.24, 1700),
    ("austin-tx", "Austin, TX", "United States", 0.24, 1900),
    ("san-jose-ca", "San Jose, CA", "United States", 0.29, 3200),
    ("jacksonville-fl", "Jacksonville, FL", "United States", 0.23, 1500),
    ("fort-worth-tx", "Fort Worth, TX", "United States", 0.24, 1500),
    ("columbus-oh", "Columbus, OH", "United States", 0.26, 1400),
    ("charlotte-nc", "Charlotte, NC", "United States", 0.25, 1600),
    ("indianapolis-in", "Indianapolis, IN", "United States", 0.25, 1300),
    ("san-francisco-ca", "San Francisco, CA", "United States", 0.32, 3600),
    ("seattle-wa", "Seattle, WA", "United States", 0.26, 2400),
    ("denver-co", "Denver, CO", "United States", 0.26, 2000),
    ("washington-dc", "Washington, DC", "United States", 0.30, 2600),
    ("boston-ma", "Boston, MA", "United States", 0.28, 3000),
    ("nashville-tn", "Nashville, TN", "United States", 0.23, 1800),
    ("detroit-mi", "Detroit, MI", "United States", 0.26, 1300),
    ("portland-or", "Portland, OR", "United States", 0.28, 1900),
    ("las-vegas-nv", "Las Vegas, NV", "United States", 0.23, 1600),
    ("memphis-tn", "Memphis, TN", "United States", 0.24, 1200),
    ("louisville-ky", "Louisville, KY", "United States", 0.26, 1200),
    ("baltimore-md", "Baltimore, MD", "United States", 0.28, 1700),
    ("milwaukee-wi", "Milwaukee, WI", "United States", 0.26, 1300),
    ("albuquerque-nm", "Albuquerque, NM", "United States", 0.25, 1300),
    ("tucson-az", "Tucson, AZ", "United States", 0.24, 1400),
    ("fresno-ca", "Fresno, CA", "United States", 0.27, 1600),
    ("sacramento-ca", "Sacramento, CA", "United States", 0.28, 2000),
    ("atlanta-ga", "Atlanta, GA", "United States", 0.26, 1800),
    ("miami-fl", "Miami, FL", "United States", 0.24, 2400),
    ("raleigh-nc", "Raleigh, NC", "United States", 0.25, 1600),
    ("omaha-ne", "Omaha, NE", "United States", 0.26, 1300),
    ("minneapolis-mn", "Minneapolis, MN", "United States", 0.27, 1600),
    ("cleveland-oh", "Cleveland, OH", "United States", 0.26, 1200),
    ("tampa-fl", "Tampa, FL", "United States", 0.23, 1800),
    ("remote-us", "Remote, United States", "United States", 0.26, 1800),
    ("london-uk", "London, UK", "United Kingdom", 0.32, 2200),
    ("toronto-ca", "Toronto, Canada", "Canada", 0.30, 2200),
    ("vancouver-ca", "Vancouver, Canada", "Canada", 0.30, 2400),
    ("sydney-au", "Sydney, Australia", "Australia", 0.32, 2400),
    ("melbourne-au", "Melbourne, Australia", "Australia", 0.32, 2000),
]

SALARIES = [35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000,
            85000, 90000, 100000, 110000, 120000, 130000, 150000, 175000, 200000, 250000]
HOUR_OPTS = [35, 40, 45, 50, 55, 60]

MEETINGS = [3, 5, 8, 10, 12, 15, 20]


def money(n: float, digits: int = 0) -> str:
    if digits:
        return f"${n:,.{digits}f}"
    return f"${n:,.0f}"


def rate(n: float) -> str:
    return f"${n:,.2f}"


def hours_label(h: float) -> str:
    if abs(h - round(h)) < 0.05:
        return f"{h:.0f}"
    return f"{h:.1f}"


CSS = r"""
:root {
  --ink: #1a1814;
  --muted: #5c564c;
  --cream: #f7f3ea;
  --paper: #fffdf8;
  --line: #e4dccb;
  --rust: #b04a2a;
  --rust-deep: #8a3820;
  --moss: #2f4a3f;
  --gold: #c4954a;
  --shadow: 0 18px 40px rgba(26, 24, 20, 0.08);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background:
    radial-gradient(1200px 500px at 90% -10%, rgba(196,149,74,.18), transparent 60%),
    radial-gradient(900px 400px at -10% 20%, rgba(176,74,42,.08), transparent 55%),
    var(--cream);
  font: 18px/1.55 "Iowan Old Style", "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
}
a { color: var(--rust-deep); }
a:hover { color: var(--rust); }
.wrap { width: min(1080px, calc(100% - 32px)); margin: 0 auto; }
header.site {
  display: flex; align-items: center; justify-content: space-between;
  padding: 22px 0 8px;
}
.brand { display: flex; gap: 10px; align-items: center; text-decoration: none; color: var(--ink); font-weight: 700; letter-spacing: .04em; }
.brand img { width: 36px; height: 36px; border-radius: 50%; }
.brand span { font-family: "Avenir Next", "Segoe UI", sans-serif; font-size: 14px; letter-spacing: .16em; text-transform: uppercase; }
nav.site a { margin-left: 16px; text-decoration: none; font-family: "Avenir Next", "Segoe UI", sans-serif; font-size: 14px; letter-spacing: .04em; }
.hero { padding: 28px 0 10px; }
.kicker { font-family: "Avenir Next", "Segoe UI", sans-serif; letter-spacing: .18em; text-transform: uppercase; font-size: 12px; color: var(--rust); font-weight: 700; }
h1 { font-size: clamp(40px, 6vw, 68px); line-height: .98; letter-spacing: -0.03em; margin: 10px 0 14px; font-weight: 600; }
.lede { font-size: 22px; max-width: 42rem; color: var(--muted); }
.card {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 18px;
  box-shadow: var(--shadow);
  padding: 22px;
}
.grid { display: grid; gap: 16px; }
.grid-2 { grid-template-columns: 1.1fr .9fr; }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }
label { display: block; font-family: "Avenir Next", "Segoe UI", sans-serif; font-size: 13px; letter-spacing: .04em; text-transform: uppercase; color: var(--muted); margin: 10px 0 6px; }
input, select {
  width: 100%; font: 18px/1.3 Georgia, serif; padding: 12px 12px;
  border: 1px solid var(--line); border-radius: 10px; background: #fff; color: var(--ink);
}
button, .btn {
  display: inline-block; background: var(--rust); color: #fffdf8; border: 0; border-radius: 999px;
  padding: 12px 18px; font-family: "Avenir Next", "Segoe UI", sans-serif; font-size: 15px;
  letter-spacing: .03em; text-decoration: none; cursor: pointer;
}
button:hover, .btn:hover { background: var(--rust-deep); color: white; }
.btn.moss { background: var(--moss); }
.stat { padding: 8px 0; }
.stat b { display: block; font-size: 34px; letter-spacing: -0.03em; line-height: 1.05; }
.stat span { color: var(--muted); font-size: 14px; font-family: "Avenir Next", "Segoe UI", sans-serif; }
.note { font-size: 14px; color: var(--muted); }
.share-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
.pill {
  border: 1px solid var(--line); background: #fff; color: var(--ink); border-radius: 999px;
  padding: 8px 12px; font-family: "Avenir Next", "Segoe UI", sans-serif; font-size: 13px;
  text-decoration: none; cursor: pointer;
}
h2 { font-size: 32px; letter-spacing: -0.02em; margin: 36px 0 10px; }
h3 { margin: 0 0 6px; font-size: 20px; }
.list a { display: block; padding: 8px 0; border-bottom: 1px solid var(--line); text-decoration: none; }
.prose { max-width: 42rem; }
.prose p { margin: 0 0 14px; }
footer.site { margin: 48px 0 28px; padding-top: 18px; border-top: 1px solid var(--line); color: var(--muted); font-size: 14px; }
table { width: 100%; border-collapse: collapse; background: var(--paper); }
th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--line); }
th { font-family: "Avenir Next", "Segoe UI", sans-serif; font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.banner {
  margin-top: 18px; padding: 16px 18px; border-left: 4px solid var(--gold); background: #fff8ea;
}
.warn { background: #fff4ee; border-left-color: var(--rust); }
@media (max-width: 800px) {
  .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
  nav.site { display: none; }
  h1 { font-size: 40px; }
}
"""

JS = r"""
function money(n, d) {
  d = d == null ? 0 : d;
  return n.toLocaleString("en-US", {style:"currency", currency:"USD", maximumFractionDigits:d, minimumFractionDigits:d});
}
function readNum(id, fallback) {
  const el = document.getElementById(id);
  if (!el) return fallback;
  const v = parseFloat(String(el.value).replace(/[^0-9.]/g, ""));
  return isFinite(v) ? v : fallback;
}
function compute() {
  const salary = readNum("salary", 85000);
  const hours = Math.max(1, readNum("hours", 45));
  const weeks = Math.max(1, readNum("weeks", 50));
  const tax = Math.min(0.6, Math.max(0, readNum("tax", 25) / 100));
  const commute = Math.max(0, readNum("commute", 0));
  const days = Math.max(0, readNum("days", 5));
  const meetingHrs = Math.max(0, readNum("meetings", 0));
  const grossH = salary / (hours * weeks);
  const netH = grossH * (1 - tax);
  const commuteYearHrs = (commute / 60) * days * weeks;
  const commuteCost = commuteYearHrs * netH;
  const meetingYear = meetingHrs * weeks;
  const meetingCost = meetingYear * netH;
  const trueHours = hours + (commute / 60) * (days / 5) * (days ? 5 : 0);
  // commute is daily round trip, so add daily commute hours onto the weekly hour count
  const weeklyCommute = (commute / 60) * days;
  const trueWeekly = hours + weeklyCommute;
  const trueNet = (salary * (1 - tax)) / (trueWeekly * weeks);
  const evening = Math.max(0, hours - 40) * weeks;
  const set = (id, text) => { const n = document.getElementById(id); if (n) n.textContent = text; };
  set("out-gross", money(grossH, 2));
  set("out-net", money(netH, 2));
  set("out-true", money(trueNet, 2));
  set("out-evening", evening.toFixed(0) + " hours");
  set("out-commute", money(commuteCost, 0) + " / " + commuteYearHrs.toFixed(0) + " h");
  set("out-meetings", money(meetingCost, 0));
  set("out-annual-net", money(salary * (1 - tax), 0));
  const share = document.getElementById("share-text");
  if (share) {
    share.value = "My kept hour is " + money(netH, 2) + " after tax. Evenings already sold this year: " + evening.toFixed(0) + " hours. " + location.href;
  }
  const params = new URLSearchParams({s: salary, h: hours, w: weeks, t: Math.round(tax*100), c: commute, d: days, m: meetingHrs});
  const url = location.pathname + "?" + params.toString();
  const link = document.getElementById("perm");
  if (link) link.textContent = url;
  history.replaceState(null, "", url);
}
function bootFromQuery() {
  const q = new URLSearchParams(location.search);
  const map = {s:"salary", h:"hours", w:"weeks", t:"tax", c:"commute", d:"days", m:"meetings"};
  Object.keys(map).forEach(k => { if (q.has(k)) { const el = document.getElementById(map[k]); if (el) el.value = q.get(k); } });
}
function copyShare() {
  const t = document.getElementById("share-text");
  if (!t) return;
  navigator.clipboard.writeText(t.value).then(() => {
    const b = document.getElementById("copy-btn");
    if (b) { const old = b.textContent; b.textContent = "Copied"; setTimeout(() => b.textContent = old, 1200); }
  });
}
document.addEventListener("DOMContentLoaded", () => {
  bootFromQuery();
  document.querySelectorAll("input,select").forEach(el => el.addEventListener("input", compute));
  compute();
  const b = document.getElementById("copy-btn");
  if (b) b.addEventListener("click", copyShare);
});
"""


def head(title: str, desc: str, path: str, extra: str = "") -> str:
    canon = f"{SITE}{path}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{SITE}/favicon.png">
<style>{CSS}</style>
{extra}
</head>
<body>
<div class="wrap">
<header class="site">
  <a class="brand" href="{SITE}/"><img src="{SITE}/favicon.png" alt=""> <span>Kept Hour</span></a>
  <nav class="site">
    <a href="{SITE}/">Calculator</a>
    <a href="{SITE}/salary/">Salaries</a>
    <a href="{SITE}/jobs/">Jobs</a>
    <a href="{SITE}/cities/">Cities</a>
    <a href="{SITE}/meetings/">Meetings</a>
    <a href="{SITE}/compare/">Offers</a>
    <a href="{SITE}/newsletter/">Brief</a>
  </nav>
</header>
"""


FOOT = f"""
<footer class="site">
  <p>Kept Hour is a planning tool, not tax, legal, or financial advice. Tax loads and rents are labeled defaults so you can see the shape of a year, then replace them with your own numbers. Figures update in the browser. No account. No tracking pixels.</p>
  <p>Built {UPDATED}. <a href="{SITE}/about/">About</a> · <a href="{SITE}/privacy/">Privacy</a> · <a href="{SITE}/newsletter/">Monday brief</a> · <a href="{SITE}/sitemap.xml">Sitemap</a></p>
</footer>
</div>
<script>{JS}</script>
</body>
</html>
"""


def write(rel: str, html: str) -> None:
    path = ROOT / rel.lstrip("/")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def calc_block(salary=85000, hours=45, weeks=50, tax=25, commute=40, days=5, meetings=5) -> str:
    return f"""
<div class="card">
  <div class="grid grid-2">
    <div>
      <label for="salary">Annual salary</label>
      <input id="salary" inputmode="decimal" value="{salary}">
      <label for="hours">Real hours per week, including the ones that “don’t count”</label>
      <input id="hours" inputmode="decimal" value="{hours}">
      <label for="weeks">Weeks you actually work</label>
      <input id="weeks" inputmode="decimal" value="{weeks}">
      <label for="tax">Combined tax load, percent</label>
      <input id="tax" inputmode="decimal" value="{tax}">
      <label for="commute">Round-trip commute, minutes</label>
      <input id="commute" inputmode="decimal" value="{commute}">
      <label for="days">Commute days per week</label>
      <input id="days" inputmode="decimal" value="{days}">
      <label for="meetings">Meeting hours per week</label>
      <input id="meetings" inputmode="decimal" value="{meetings}">
    </div>
    <div>
      <div class="stat"><b id="out-net">—</b><span>Kept hour, after tax</span></div>
      <div class="stat"><b id="out-true">—</b><span>Kept hour after commute is counted as work</span></div>
      <div class="stat"><b id="out-gross">—</b><span>Gross hourly, before tax</span></div>
      <div class="stat"><b id="out-evening">—</b><span>Evening hours already sold (over 40 / week)</span></div>
      <div class="stat"><b id="out-commute">—</b><span>Commute, valued at your kept hour</span></div>
      <div class="stat"><b id="out-meetings">—</b><span>Meetings, valued at your kept hour, per year</span></div>
      <div class="stat"><b id="out-annual-net">—</b><span>Take-home, same tax load</span></div>
      <div class="share-row">
        <button type="button" id="copy-btn">Copy the number</button>
        <a class="btn moss" href="{SITE}/newsletter/">Get the Monday number</a>
      </div>
      <p class="note">Share link updates as you type: <code id="perm"></code></p>
      <textarea id="share-text" hidden></textarea>
    </div>
  </div>
</div>
"""


def home() -> None:
    title = "Kept Hour — what is an hour of your life worth after tax?"
    desc = "Turn a salary into a real hourly rate after tax, commute, and meetings. See the evenings you already sold. Free, no account."
    body = f"""
<main class="hero">
  <p class="kicker">A salary is a costume. The hour is the truth.</p>
  <h1>What is an hour of your life worth after tax?</h1>
  <p class="lede">Most “salary to hourly” tools divide by 2,080 and stop. That number flatters the job. Kept Hour uses the hours you actually give, then prices the commute and the meetings in the same unit: your evening.</p>
</main>
{calc_block()}
<section>
  <h2>Start from a number you already know</h2>
  <div class="grid grid-3">
    <a class="card" href="{SITE}/salary/"><h3>By salary</h3><p>120 pages. $35k to $250k, at 35 to 60 hours.</p></a>
    <a class="card" href="{SITE}/jobs/"><h3>By job</h3><p>50 roles with a typical salary and a typical real week.</p></a>
    <a class="card" href="{SITE}/cities/"><h3>By city</h3><p>Tax load and rent, so the hourly rate has a cost of living next to it.</p></a>
    <a class="card" href="{SITE}/compare/"><h3>Two offers</h3><p>The higher salary often loses on the hour. Compare them before you reply.</p></a>
  </div>
</section>
<section class="prose">
  <h2>How the kept hour is calculated</h2>
  <p>Gross hourly is salary divided by real weekly hours times weeks worked. The flattering version uses 40 hours and 52 weeks. If you work 47 hours for 50 weeks, you already donated 350 hours before anyone mentions “culture.”</p>
  <p>Kept hour is that gross rate times one minus your combined tax load. It is a planning rate, not a paycheck reconstruction. Payroll taxes, state tax, and retirement deferrals move it. The point is the shape: a raise that adds hours can lower the hour.</p>
  <p>Commute is not free because it is unpaid. A 40-minute round trip, 5 days, 50 weeks, is 167 hours. At a $30 kept hour that is $5,000 of life, spent in a seat.</p>
  <p>Meetings get the same treatment. Eight hours a week is 400 hours a year. If those hours produce no decision you can name, you can price them. That is the only argument that survives a calendar review.</p>
</section>
<section>
  <h2>Three ways this page gets used</h2>
  <div class="grid grid-3">
    <div class="card"><h3>The offer</h3><p>A new job pays more and asks for 10 more hours. Run both. Keep the one with the higher kept hour, not the higher salary.</p></div>
    <div class="card"><h3>The meeting</h3><p>Paste your rate into the meeting calculator. Decline, shorten, or bill the hour you can now name.</p></div>
    <div class="card"><h3>The commute</h3><p>Remote is not a perk if the kept hour does not move. Sometimes it does. Sometimes the city does.</p></div>
  </div>
  <div class="banner">
    <strong>Monday brief.</strong> One number, one sentence, no course. The list is the monetization lane: a paid annual brief once the free list is real. <a href="{SITE}/newsletter/">Join with an email you check.</a>
  </div>
</section>
"""
    extra = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebApplication","name":"Kept Hour","applicationCategory":"FinanceApplication","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"description":"Salary to real hourly calculator after tax, commute, and meetings."}</script>"""
    write("index.html", head(title, desc, "/", extra) + body + FOOT)


def salary_index() -> None:
    rows = []
    for s in SALARIES:
        g, n = s / (45 * 50), s / (45 * 50) * 0.75
        rows.append(f"<tr><td><a href='{SITE}/salary/{s}/'>{money(s)} salary</a></td><td>{rate(g)} gross</td><td>{rate(n)} kept</td><td>45 h × 50 wk, 25% tax</td></tr>")
    body = f"""
<main class="hero"><p class="kicker">Salary pages</p><h1>Every common salary, at the hours you actually work.</h1>
<p class="lede">These are not national medians. They are the arithmetic of a year, so a Reddit thread or a job offer can link a specific page instead of arguing in the abstract.</p></main>
<table><thead><tr><th>Salary</th><th>Gross hourly</th><th>Kept hour</th><th>Default week</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
"""
    write("salary/index.html", head("Salary to hourly — Kept Hour", "Salary to real hourly pages from $35,000 to $250,000, including evenings over 40 hours.", "/salary/") + body + FOOT)


def salary_page(salary: int) -> None:
    rows = []
    for h in HOUR_OPTS:
        gross = salary / (h * 50)
        net = gross * 0.75
        evenings = max(0, h - 40) * 50
        rows.append(
            f"<tr><td><a href='{SITE}/salary/{salary}/{h}/'>{h} h/week</a></td>"
            f"<td>{rate(gross)}</td><td>{rate(net)}</td><td>{evenings:.0f} h</td></tr>"
        )
    g40 = salary / 2080
    g45 = salary / (45 * 50)
    body = f"""
<main class="hero">
  <p class="kicker">Salary page</p>
  <h1>{money(salary)} a year is not {rate(g40)} an hour.</h1>
  <p class="lede">Dividing by 2,080 assumes a 40-hour week and a 52-week year. At 45 hours and 50 weeks, {money(salary)} is {rate(g45)} before tax. After a 25% planning load, the kept hour is {rate(g45*0.75)}. Change the assumptions. The page will not argue with you.</p>
</main>
{calc_block(salary=salary, hours=45, tax=25)}
<h2>Same salary, different weeks</h2>
<table><thead><tr><th>Week</th><th>Gross hourly</th><th>Kept hour at 25%</th><th>Evenings sold / year</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<section class="prose">
  <h2>What to do with {money(salary)}</h2>
  <p>If an offer matches this salary and adds hours, the kept hour is the comparison, not the title. A {money(salary)} job at 55 hours pays less per kept hour than a lower salary at 40, once tax is the same. Run both offers in the calculator and keep the higher hour.</p>
  <p>Evenings already sold are the hours above 40, times weeks worked. They are not a moral score. They are the number you can put next to a hobby, a child, or a second skill that might raise the next salary without raising the week.</p>
  <p>Related: <a href="{SITE}/salary/">all salaries</a>, <a href="{SITE}/meetings/8-hours/">what 8 meeting hours cost</a>, <a href="{SITE}/newsletter/">Monday brief</a>.</p>
</section>
"""
    write(
        f"salary/{salary}/index.html",
        head(
            f"{money(salary)} salary to hourly — Kept Hour",
            f"What {money(salary)} a year is per hour after tax, at 35 to 60 real hours a week. Not the 2,080-hour fairy tale.",
            f"/salary/{salary}/",
        )
        + body
        + FOOT,
    )


def salary_hour_page(salary: int, hours: int) -> None:
    gross = salary / (hours * 50)
    net = gross * 0.75
    evenings = max(0, hours - 40) * 50
    body = f"""
<main class="hero">
  <p class="kicker">{money(salary)} · {hours} hours</p>
  <h1>{money(salary)} at {hours} hours is a {rate(net)} kept hour.</h1>
  <p class="lede">Gross is {rate(gross)}. After a 25% planning tax load, you keep {rate(net)}. Evenings above a 40-hour week: {evenings:.0f} hours a year. Commute is not in that yet.</p>
</main>
{calc_block(salary=salary, hours=hours, tax=25)}
<section class="prose">
  <p>People share this page because the argument is already done. “I make {money(salary)}” and “I make {rate(net)} after tax for a {hours}-hour week” are different sentences. One gets respect in a meeting. The other tells you whether the meeting was worth opening the laptop.</p>
  <p><a href="{SITE}/salary/{salary}/">All weeks at {money(salary)}</a> · <a href="{SITE}/salary/">All salaries</a></p>
</section>
"""
    write(
        f"salary/{salary}/{hours}/index.html",
        head(
            f"{money(salary)} at {hours} hours a week — Kept Hour",
            f"{money(salary)} at {hours} hours is {rate(net)} after a 25% tax load, before commute.",
            f"/salary/{salary}/{hours}/",
        )
        + body
        + FOOT,
    )


def jobs_index() -> None:
    items = []
    for slug, name, sal, hrs in ROLES:
        net = (sal / (hrs * 50)) * 0.75
        items.append(f"<a href='{SITE}/jobs/{slug}/'><strong>{name}</strong> — typical {money(sal)}, kept hour about {rate(net)}</a>")
    body = f"""
<main class="hero"><p class="kicker">Jobs</p><h1>The kept hour of 50 jobs, before you negotiate the story.</h1>
<p class="lede">Each page starts from a typical US salary and a typical real week for that role. Both are defaults. Replace them. The job is the door; your week is the number.</p></main>
<div class="list">{''.join(items)}</div>
"""
    write("jobs/index.html", head("Kept hour by job — 50 roles", "Typical salary and real weekly hours for 50 jobs, converted to a kept hour after tax.", "/jobs/") + body + FOOT)


def job_page(slug: str, name: str, salary: int, hours: int) -> None:
    gross = salary / (hours * 50)
    net = gross * 0.75
    evenings = max(0, hours - 40) * 50
    # nearby roles by salary
    near = sorted(ROLES, key=lambda r: abs(r[2] - salary))[1:4]
    links = " · ".join(f"<a href='{SITE}/jobs/{s}/'>{n}</a>" for s, n, *_ in near)
    body = f"""
<main class="hero">
  <p class="kicker">Job page · defaults, not a survey</p>
  <h1>A {name.lower()} at {money(salary)} and {hours} hours keeps about {rate(net)} an hour.</h1>
  <p class="lede">That uses 50 working weeks and a 25% combined tax load. Gross hourly is {rate(gross)}. Hours above 40, if this week is typical, add up to {evenings:.0f} evenings-worth a year. If your offer is different, the calculator is the page.</p>
</main>
{calc_block(salary=salary, hours=hours, tax=25, meetings=6 if hours >= 45 else 3)}
<section class="prose">
  <h2>How to read a {name.lower()} offer</h2>
  <p>Title inflation is common and useless. Ask for the week: on-call, charting, prep, Slack after dinner, travel that is not on the clock. Put that number in hours, not the number on the poster.</p>
  <p>Then price one concession. A 30-minute daily standup, 5 days, 50 weeks, is 125 hours. At this kept hour that is about {money(125 * net)}. You do not have to say it that way in the room. You should know it before you say yes.</p>
  <p>Compare cities on the <a href="{SITE}/cities/">city pages</a>. A higher salary in a higher-tax, higher-rent city can lose to a quieter week somewhere cheaper. Rent on those pages is a planning range for a one-bedroom, not your lease.</p>
  <p>Nearby roles: {links}.</p>
  <p>Want this as a Monday number instead of a tab you forget? <a href="{SITE}/newsletter/">The brief is one email, one figure, no funnel theater.</a></p>
</section>
"""
    write(
        f"jobs/{slug}/index.html",
        head(
            f"{name} kept hour — {money(salary)} at {hours} hours",
            f"What a {name.lower()} keeps per hour after tax, starting from {money(salary)} and a {hours}-hour week.",
            f"/jobs/{slug}/",
        )
        + body
        + FOOT,
    )


def cities_index() -> None:
    items = []
    for slug, name, country, tax, rent in CITIES:
        items.append(
            f"<tr><td><a href='{SITE}/cities/{slug}/'>{name}</a></td><td>{country}</td><td>{tax:.0%}</td><td>{money(rent)}/mo</td></tr>"
        )
    body = f"""
<main class="hero"><p class="kicker">Cities</p><h1>The same salary is a different life once tax and rent sit beside it.</h1>
<p class="lede">Tax is a combined planning load, not your return. Rent is a one-bedroom asking-rent range for orientation. Both exist so the hourly page is not floating in a vacuum.</p></main>
<table><thead><tr><th>City</th><th>Country</th><th>Planning tax</th><th>1-bed rent range</th></tr></thead><tbody>{''.join(items)}</tbody></table>
<p class="note">Currency is shown in USD for comparison. London, Toronto, Vancouver, Sydney, and Melbourne figures are order-of-magnitude USD equivalents, not FX quotes.</p>
"""
    write("cities/index.html", head("Kept hour by city — tax load and rent", "City pages with a planning tax load and typical one-bedroom rent next to your kept hour.", "/cities/") + body + FOOT)


def city_page(slug, name, country, tax, rent) -> None:
    # illustrative 90k worker
    salary = 90000
    hours = 45
    gross = salary / (hours * 50)
    net = gross * (1 - tax)
    annual_net = salary * (1 - tax)
    rent_year = rent * 12
    rent_share = rent_year / annual_net if annual_net else 0
    hours_for_rent = rent_year / net if net else 0
    body = f"""
<main class="hero">
  <p class="kicker">{country} · planning defaults</p>
  <h1>In {name}, a {money(salary)} salary keeps about {rate(net)} an hour.</h1>
  <p class="lede">Planning tax load: {tax:.0%}. One-bedroom rent used here: {money(rent)} a month, {money(rent_year)} a year. That rent is about {rent_share:.0%} of take-home on this example, or {hours_for_rent:.0f} kept hours. Your lease and your bracket will differ. The ratio is the point.</p>
</main>
{calc_block(salary=salary, hours=hours, tax=int(tax*100), commute=35)}
<section class="prose">
  <h2>What the rent does to the hour</h2>
  <p>A raise that does not clear rent plus tax is a relocation costume. If you are choosing between {name} and a cheaper city, run the same salary in both calculators, then subtract a year of rent from take-home and divide by your real hours. The city with the higher leftover hour is the city that pays you.</p>
  <p>Remote workers: set commute to 0 and do not pretend the home office is free. A dedicated room has a rent. Put a fraction of rent into the commute field as “minutes” only if you want a nudge; better, subtract it mentally from take-home. The tool stays honest if you do.</p>
  <p><a href="{SITE}/cities/">All cities</a> · <a href="{SITE}/salary/90000/">$90,000 salary page</a></p>
</section>
"""
    write(
        f"cities/{slug}/index.html",
        head(
            f"Kept hour in {name}",
            f"Planning tax load and one-bedroom rent in {name}, next to a real hourly rate.",
            f"/cities/{slug}/",
        )
        + body
        + FOOT,
    )


def meetings_index() -> None:
    items = []
    for m in MEETINGS:
        items.append(f"<a href='{SITE}/meetings/{m}-hours/'><strong>{m} hours of meetings a week</strong> — {m*50:.0f} hours a year</a>")
    body = f"""
<main class="hero"><p class="kicker">Meetings</p><h1>A meeting is a purchase. Price it in kept hours.</h1>
<p class="lede">You would not approve an unbudgeted vendor. You approve unbudgeted hours every Tuesday. These pages turn a weekly meeting load into a year, then into dollars at your rate.</p></main>
<div class="list">{''.join(items)}</div>
"""
    write("meetings/index.html", head("What meetings cost in kept hours", "Price 3 to 20 meeting hours a week in annual hours and dollars.", "/meetings/") + body + FOOT)


def meeting_page(m: int) -> None:
    year = m * 50
    # at $40 kept hour example
    example = year * 40
    body = f"""
<main class="hero">
  <p class="kicker">Meeting load</p>
  <h1>{m} meeting hours a week is {year:.0f} hours a year.</h1>
  <p class="lede">At a $40 kept hour, that is {money(example)}. Your hour is probably not $40. Put the real salary in. Send the link to the person who owns the recurring invite, or just to yourself, before you accept next quarter’s series.</p>
</main>
{calc_block(meetings=m, hours=45)}
<section class="prose">
  <h2>A fair rule</h2>
  <p>Keep a meeting only if it names a decision, a draft, or a risk that moves this week. Status can be a paragraph. If the series cannot say which of the three it is, the year-cost above is the cost of politeness.</p>
  <p>Cutting {m} hours to half is {year/2:.0f} hours back. That is the cleanest raise available without a new job.</p>
</section>
"""
    write(
        f"meetings/{m}-hours/index.html",
        head(
            f"What {m} meeting hours a week cost",
            f"{m} meeting hours a week is {year:.0f} hours a year. Price them at your kept hour.",
            f"/meetings/{m}-hours/",
        )
        + body
        + FOOT,
    )


def compare() -> None:
    pairs = [(70000, 40, 90000, 55), (80000, 40, 100000, 50), (120000, 45, 150000, 60)]
    cards = []
    for a, ah, b, bh in pairs:
        an = (a / (ah * 50)) * 0.75
        bn = (b / (bh * 50)) * 0.75
        winner = "the lower salary" if an >= bn else "the higher salary"
        cards.append(
            f"<div class='card'><h3>{money(a)} at {ah}h vs {money(b)} at {bh}h</h3>"
            f"<p>Kept hours: {rate(an)} vs {rate(bn)}. On the hour, {winner} wins, before commute. "
            f"<a href='{SITE}/salary/{a}/{ah}/'>First offer</a> · <a href='{SITE}/salary/{b}/{bh}/'>Second offer</a></p></div>"
        )
    body = f"""
<main class="hero">
  <p class="kicker">Offers</p>
  <h1>The higher salary is not the higher hour.</h1>
  <p class="lede">People lose negotiations by comparing costumes. Compare kept hours. Tax load held at 25%, 50 weeks, no commute. Add the commute on each page before you decide.</p>
</main>
<div class="grid grid-3">{''.join(cards)}</div>
{calc_block(salary=90000, hours=50)}
<section class="prose">
  <p>Put offer A in the calculator. Copy the kept hour. Put offer B in. The larger kept hour is the better trade of life for money, unless one offer buys a skill that raises next year’s hour. That exception is real. It is also the excuse people use to ignore a bad week. Name the skill or do not take the cut.</p>
</section>
"""
    write("compare/index.html", head("Which offer pays more per hour — Kept Hour", "Compare two salaries by kept hour, not by the number on the offer letter.", "/compare/") + body + FOOT)


def newsletter() -> None:
    body = f"""
<main class="hero">
  <p class="kicker">The lane</p>
  <h1>Monday brief: one number about the hour you kept.</h1>
  <p class="lede">No course. No daily drip. One email a week: a worked example (a salary, a city, a meeting load) and one sentence on what to do with it. The list is free. The annual brief, when the list is real, is the paid lane — written for people who already know their number and want the year planned against it.</p>
</main>
<div class="card">
  <form action="https://formsubmit.co/kepthour.brief@gmail.com" method="POST">
    <label for="email">Email</label>
    <input id="email" type="email" name="email" required placeholder="you@domain.com" autocomplete="email">
    <input type="hidden" name="_subject" value="Kept Hour Monday brief">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="{SITE}/newsletter/thanks/">
    <input type="text" name="_honey" style="display:none">
    <p><button type="submit">Send me Monday</button></p>
    <p class="note">The form delivers to kepthour.brief@gmail.com through FormSubmit. The first submission from this site triggers a confirmation email in that inbox. Until that confirmation is clicked, new subscribers will not arrive. No tracker is loaded on this page. Do not put a confidential salary in the form. The calculator already has it.</p>
  </form>
  <p class="note">Prefer mail? <a href="mailto:kepthour.brief@gmail.com?subject=Monday%20brief">kepthour.brief@gmail.com</a></p>
</div>
<section class="prose">
  <h2>What you are buying later, not now</h2>
  <p>The paid product is an annual Kept Hour brief: your salary, your real week, your city, your meeting load, and a one-page plan for which hours to cut or sell. Price target is $39 once, not a subscription that punishes you for a number you already have. It does not ship until the free list has readers. Traffic first. Cash second. That order is the whole strategy.</p>
  <p>Affiliate notes, if any are added later, will be labeled on the page that carries them. This page has none.</p>
</section>
"""
    write("newsletter/index.html", head("Monday brief — Kept Hour", "One weekly number: what your hour was worth, and what to do with it.", "/newsletter/") + body + FOOT)


def about() -> None:
    body = f"""
<main class="hero">
  <p class="kicker">About</p>
  <h1>Kept Hour exists to make a salary legible.</h1>
</main>
<section class="prose">
  <p>A salary is an annual costume. Employers like it because it hides the week. Workers repeat it because it is the number they were given. The hour, after tax, after the commute, after the meetings, is the number that decides whether a job is a life or a lease on one.</p>
  <p>This site is a static calculator and a set of specific pages so people can share a result without making an account. It is operated as an independent project. It is not a bank, not a tax preparer, and not an employer.</p>
  <p>Corrections: if a default salary, tax load, or rent is wildly wrong for a role or a city, send the better public source. Defaults are planning anchors, updated when a better anchor is boring and checkable.</p>
  <p>Contact for the brief, corrections, and partnerships: <a href="mailto:kepthour.brief@gmail.com">kepthour.brief@gmail.com</a>. That inbox is the human step. The site does not need an account to be useful.</p>
  <h2>Method</h2>
  <p>Gross hourly = annual salary / (weekly hours × weeks worked). Kept hour = gross hourly × (1 − tax load). Commute hours = (round-trip minutes / 60) × commute days × weeks. Commute cost = commute hours × kept hour. Meeting cost = weekly meeting hours × weeks × kept hour. Evenings sold = max(0, weekly hours − 40) × weeks. None of these are tax advice. They are the same arithmetic a spreadsheet would do, written so a stranger can open a link.</p>
</section>
"""
    write("about/index.html", head("About Kept Hour", "Why Kept Hour exists, how the math works, and how to send a correction.", "/about/") + body + FOOT)


def privacy() -> None:
    body = """
<main class="hero"><p class="kicker">Privacy</p><h1>The calculator does not know you.</h1></main>
<section class="prose">
  <p>Numbers you type stay in the page. The share link puts those numbers in the URL so you can send them. If you send the link, you are publishing the numbers in it. Do not put a secret compensation figure in a URL you post to a company Slack if that figure is confidential.</p>
  <p>There is no analytics pixel and no advertising cookie. GitHub Pages may log ordinary server requests the way any host does. The Monday form sends your email to FormSubmit, which forwards it to kepthour.brief@gmail.com. That is the only personal data the form collects. We do not sell it.</p>
  <p>We do not sell personal information. We do not have any, unless you email us.</p>
</section>
"""
    write("privacy/index.html", head("Privacy — Kept Hour", "Kept Hour stores nothing you type. The Monday form sends an email address to FormSubmit and nowhere else.", "/privacy/") + body + FOOT)


def thanks() -> None:
    body = f"""
<main class="hero">
  <p class="kicker">Monday brief</p>
  <h1>You’re on the list if the inbox confirmed it.</h1>
  <p class="lede">If this was the first submission ever, it activated the form instead of subscribing you. Check kepthour.brief@gmail.com, confirm FormSubmit once, then submit again. After that, one email a week. No drip.</p>
  <p><a class="btn" href="{SITE}/">Back to the calculator</a></p>
</main>
"""
    write("newsletter/thanks/index.html", head("You’re in — Kept Hour", "Monday brief signup received.", "/newsletter/thanks/") + body + FOOT)


def robots_and_sitemap(urls: list[str]) -> None:
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    items = "\n".join(
        f"  <url><loc>{SITE}{u}</loc><lastmod>{UPDATED}</lastmod></url>" for u in urls
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
"""
    write("sitemap.xml", xml)
    key = "kept-hour-indexnow-" + "7f3c9a"
    write(f"{key}.txt", key)
    (ROOT / "INDEXNOW_KEY.txt").write_text(key + "\n")
    # Search Console HTML-file method. Exact bytes Google asked for.
    (ROOT / "googlec492d67015d750fe.html").write_text("google-site-verification: googlec492d67015d750fe.html\n")


def distribution() -> None:
    text = f"""# Kept Hour — 30-day distribution pack

Live: {SITE}/

## What this is
A free salary-to-real-hourly calculator. Share unit is a specific result URL, not the homepage.

## Post this (Reddit / forums) — do not spam, one honest comment where someone asked

Title: Dividing salary by 2,080 is how jobs hide the week

Body:
I got tired of “$90k is $43/hr” math that assumes 40 hours and 52 weeks. If you work 47 hours and take two weeks off, the hour is already different, and that is before tax and the commute.

I built a single-purpose page that does the ugly version: real hours, a tax load you can edit, commute priced at your after-tax hour, meetings priced the same way. No account.

{SITE}/

Example: $90k at 50 hours is not the LinkedIn number. The salary pages are here if you want a link that already has the figure:
{SITE}/salary/90000/

If your week is worse than the default, change the hours. The tool will not flatter you.

## Short posts

1. A salary is an annual costume. The kept hour is the truth. {SITE}/
2. 8 meetings a week is 400 hours a year. Price them before you accept the series. {SITE}/meetings/8-hours/
3. The commute is not free because it is unpaid. {SITE}/

## Communities where the question already exists
- r/personalfinance, r/salary, r/jobs, r/cscareerquestions, r/nursing, r/teachers — only when someone asks “is this offer worth it”
- Hacker News: Show HN only if a comment thread is already about compensation math. Do not spray.
- Indie Hackers / specific job Discords: one post, then leave

## Email the list
Inbox to claim: kepthour.brief@gmail.com
Form endpoint is a placeholder until Formspree (or Buttondown) is connected.

## Monetization lane (after traffic, not before)
1. Free Monday brief (one number).
2. $39 annual Kept Hour brief: their numbers, one page, which hours to cut or sell.
3. Optional labeled affiliate later for tax software or a calendar tool. Not on day one. Trust is the asset.

## Day 1 human blockers
- Claim kepthour.brief@gmail.com (or forward another inbox).
- Optional: connect a real Formspree/Buttondown form id in newsletter/index.html.
- Optional: custom domain. GitHub Pages URL works without it.
"""
    (ROOT / "DISTRIBUTION.md").write_text(text)


def main() -> None:
    urls = ["/", "/salary/", "/jobs/", "/cities/", "/meetings/", "/compare/", "/newsletter/", "/newsletter/thanks/", "/about/", "/privacy/"]
    home()
    salary_index()
    for s in SALARIES:
        salary_page(s)
        urls.append(f"/salary/{s}/")
        for h in HOUR_OPTS:
            salary_hour_page(s, h)
            urls.append(f"/salary/{s}/{h}/")
    jobs_index()
    for row in ROLES:
        job_page(*row)
        urls.append(f"/jobs/{row[0]}/")
    cities_index()
    for row in CITIES:
        city_page(*row)
        urls.append(f"/cities/{row[0]}/")
    compare()
    meetings_index()
    for m in MEETINGS:
        meeting_page(m)
        urls.append(f"/meetings/{m}-hours/")
    newsletter()
    thanks()
    about()
    privacy()
    robots_and_sitemap(urls)
    distribution()
    pages = list(ROOT.rglob("index.html"))
    print(f"pages={len(pages)} urls={len(urls)}")


if __name__ == "__main__":
    main()
