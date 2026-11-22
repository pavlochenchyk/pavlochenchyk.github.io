#!/usr/bin/env python3
"""Build the Product Manager version of the site: pm/index.html.

The design version (index.html) is the single source. This script copies it,
swaps the PM-specific parts and rewrites asset paths for the /pm/ folder.
Every swap must match exactly once, otherwise the build fails, so a change
in index.html that breaks a swap is caught instead of silently skipped.

Run from the repo root after any change to index.html:
    python3 tools/build_pm.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "pm" / "index.html"
CV_PM = "assets/Pavlo_Chenchyk_CV_Product_Manager.pdf"
CV_DESIGN = "assets/Pavlo_Chenchyk_CV_Head_of_Design.pdf"
PARTS = ROOT / "tools" / "pm_parts"  # PM-only blocks (Readberry case); the design version never sees them


def swap(html, pattern, repl, name, count=1, regex=False):
    if regex:
        found = len(re.findall(pattern, html, flags=re.S))
    else:
        found = html.count(pattern)
    if found != count:
        sys.exit(f"build_pm: '{name}' matched {found} times, expected {count}")
    if regex:
        return re.sub(pattern, lambda m: repl, html, flags=re.S)
    return html.replace(pattern, repl)


def drop_card(html, href, name):
    pattern = r'<article class="project">(?:(?!</article>).)*?href="' + re.escape(href) + r'"(?:(?!</article>).)*?</article>\n?'
    return swap(html, pattern, "", f"card {name}", regex=True)


def company(html, marker, new_block, name):
    pattern = r'<div class="company"><p class="company__name"><strong>' + re.escape(marker) + r'.*?</div></div>(?=\n)'
    return swap(html, pattern, new_block, f"company {name}", regex=True)


ROLE = "Product Manager &middot; Growth &amp; Monetization"

SUMMARY = (
    "Product manager with 10+ years building web and mobile products, focused on growth and monetization across subscription, marketplace and e-commerce models. Most recently I led a subscription iOS app at NODERA Group, a venture builder: launched the MVP in 2 months, cut blended CAC by 74% with audience and creative testing, and grew AOV 1.8&#215; with intro offers and longer plans. Before that, as Head of Product &amp; Design at Develux, a multi-product EdTech company, I sat on the C-level team, co-owned product discovery and delivery for 3+ products and cut hypothesis-to-release time by 43%. Earlier I founded and ran an e-commerce business. A UX and research background keeps my discovery grounded in customer evidence, and I work AI-first: prototyping, analysis of aggregated data and creative production."
)

SKILLS = {
    "designer": ("Product", "Product skills", [
        "Product strategy and roadmap", "Discovery and customer research",
        "Hypothesis prioritization", "A/B testing", "Product analytics",
        "Retention and engagement"]),
    "founder": ("Growth &amp; business", "Growth and business skills", [
        "Web-to-app funnels", "Onboarding and paywall optimization", "Pricing experiments",
        "Subscription and hybrid monetization", "Paid acquisition, ASO and creative testing",
        "P&amp;L and financial forecasting", "Unit economics"]),
    "manager": ("Leadership", "Leadership skills", [
        "Cross-functional teams and external partners", "OKRs and goal setting",
        "Hiring and team growth", "Work with C-level stakeholders"]),
    "ai": ("AI &amp; tools", "AI and tools", [
        "Claude Code", "AI-assisted data analysis", "Mixpanel", "Google Analytics 4", "Adapty", "AppsFlyer",
        "FunnelFox", "Meta Ads Manager", "Google Ads", "Figma"]),
}


def skills_markup():
    tabs = '<button type="button" class="skills__tab" data-f="all" aria-pressed="true">All</button>'
    rows = ""
    for key, (label, aria, items) in SKILLS.items():
        tabs += f'<button type="button" class="skills__tab" data-f="{key}" aria-pressed="false">{label}</button>'
        lis = "".join(f'<li data-g="{key}">{i}</li>' for i in items)
        rows += f'<ul class="skills__list" data-g="{key}" aria-label="{aria}">{lis}</ul>'
    return tabs, rows


def job(title, dates, bullets, note=None):
    n = f'<p class="job__note">{note}</p>' if note else ""
    ul = "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>" if bullets else ""
    return (f'<div class="job"><p class="job__head"><span class="job__title">{title}</span>'
            f'<span class="job__dates">{dates}</span></p>{n}{ul}</div>')


def company_block(name, kind, jobs, tail=""):
    return (f'<div class="company"><p class="company__name"><strong>{name}</strong> <span>{kind}</span></p>'
            + "".join(jobs) + tail + "</div>")


READBERRY = company_block("&#8220;NODERA-Group&#8221;", "Venture builder", [job(
    'Venture Lead &amp; Product Manager',
    "Mar 2026 &ndash; Nov 2026", [
        "Took a subscription iOS app from discovery to App Store launch in 2 months and ran it as a unit economics test.",
        "Owned strategy, roadmap and P&amp;L; steered ad spend by forecasts vs actuals.",
        "Cut blended CAC by 74% ($263 &#8594; $68): found a high-intent audience and scaled creative production 10&#215; across Meta, ASA and ASO.",
        "Built and iterated a web-to-app funnel (web quiz &#8594; paywall &#8594; app) to 2.3% landing-to-paid on a hard paywall.",
        "Grew AOV 1.8&#215; with intro offers and longer plans and lifted LTV/CAC from 0.4&#215; to 1.3&#215;; held a 53% monthly rebill rate on web with renewal priced 67% above the intro.",
        "Raised activation from 36% to 55% and doubled week-3 retention with a new player, an original-text mode and quizzes.",
        "Designed the metric set and a CRM dashboard with automated feeds from Mixpanel and Adapty; ran funnel, cohort, creative and failed-payment reviews to decide what to scale or cut.",
        "Built the scale-up P&amp;L and payback model behind the decision not to fund the next stage.",
    ])])

DEVELUX = company_block("&#8220;DEVELUX&#8221;", "Multiproduct EdTech company", [job(
    'Head of Product &amp; Design <span class="job__off">&middot; official title: Chief Design Officer</span>', "Jan 2024 &ndash; Mar 2026", [
        'Part of the C-level team reporting to the CEO; co-set product strategy and priorities for 3+ products, including <a href="https://studyagent.com/" target="_blank" rel="noopener">StudyAgent</a>. Led a product design and research team of up to 17 people.',
        "Co-owned product discovery and delivery for 3+ products: feature roadmap, hypothesis backlog and success metrics.",
        'Cut median time from hypothesis to release from 3.5 to 2&nbsp;weeks and raised the share of initiatives hitting their success metric from 9% to 14% (<a href="#develux">case study</a>).',
        "Set up UX Research and UX Writing and a shared insight hub that feeds product discovery.",
        "Cascaded company OKRs every quarter to department leads and individual team members.",
        "Grew the team from 2 to 17 people within the planned headcount and budget.",
    ], note="Promoted from Lead Product Designer (Mar 2023 &ndash; Jan 2024)")])

ROCKEN = company_block("&#8220;ROCKEN&#8221;", "HR tech", [job(
    "Product Designer", "May 2022 &ndash; Mar 2023", [
        "Worked across a job board, CRM, candidate service and internal dashboard on web, desktop and mobile.",
        "Combined quantitative data and user research to find problem areas, turned findings into hypotheses with success metrics, and validated changes through A/B tests.",
        'Raised visitor-to-application conversion by 14% year over year and cut searches with no results by 26% (<a href="#rocken">case study</a>).',
    ])])

PUSHOK = company_block("&#8220;PUSH-OK&#8221;", "Pet supplies e-commerce", [job(
    "Founder", "Sep 2019 &ndash; Feb 2022", [
        "Founded and ran an online store: business strategy, marketing and customer acquisition.",
        "Oversaw the store&#8217;s technical development and supporting business systems; managed finances and accounting.",
    ], note="Alongside the role at Promodo")])

PROMODO = company_block("&#8220;PROMODO&#8221;", "Digital marketing agency", [
    job("Team Lead UX/UI Designer", "Feb 2022 &ndash; May 2022", []),
    job("UX/UI Designer", "Nov 2018 &ndash; Feb 2022", []),
], tail="<ul>"
    "<li>Built the agency&#8217;s Conversion Rate Optimization service: audit framework and hypothesis backlog for client e-commerce sites.</li>"
    "<li>Led a team of 5 designers.</li></ul>")


def build():
    h = SRC.read_text(encoding="utf-8")

    h = swap(h, "<title>Pavlo Chenchyk — Head of Design · Design Lead</title>",
             "<title>Pavlo Chenchyk — Product Manager · Growth &amp; Monetization</title>", "title")

    desc_design = ("Pavlo Chenchyk — Head of Design and Design Lead with 10+ years in product design. "
                   "Former Chief Design Officer who grew a design and research team from 2 to 17 people.")
    desc_pm = ("Pavlo Chenchyk — Product Manager with 10+ years in B2C and SaaS products. Led a subscription "
               "iOS app venture: web-to-app funnel, monetization, retention and P&amp;L. Former Chief Design Officer.")
    h = swap(h, f'content="{desc_design}"', f'content="{desc_pm}"', "meta descriptions", count=2)
    h = swap(h, '<meta property="og:title" content="Pavlo Chenchyk — Head of Design · Design Lead">',
             '<meta property="og:title" content="Pavlo Chenchyk — Product Manager · Growth &amp; Monetization">', "og title")
    h = swap(h, '<meta property="og:url" content="https://pavlochenchyk.github.io/">',
             '<meta property="og:url" content="https://pavlochenchyk.github.io/pm/">', "og url")

    # Home: roles ring, product first (same length, so the ring keeps its spacing).

    # Develux case: product framing (Head of Product & Design, official title CDO).
    h = swap(h, "Building a design &amp; research function", "Rebuilding product discovery and delivery", "develux title", count=2)
    h = swap(h, "<dd>Lead Product Designer &#8594; Chief Design Officer</dd>",
             '<dd>Head of Product &amp; Design</dd>', "develux role")
    h = swap(h, "Two designers drew what product managers asked for, and only 9% of initiatives hit their success metric. Over three years I built a 17-person design and research function that works in every stage of the product process. The success rate grew to 14%, and hypotheses now reach release in 2&nbsp;weeks instead of 3.5.",
             "Only 9% of product initiatives hit their success metric, and a hypothesis took 3.5&nbsp;weeks to reach release. Over three years I co-owned product discovery and delivery across 3+ products and built a 17-person product design and research team that works in every stage of the process. The success rate grew to 14%, and hypotheses now reach release in 2&nbsp;weeks.", "develux in short")
    h = swap(h, "The product process we built: design became a partner in every stage",
             "The product process we built: product, design and research own it together", "develux after sub")
    h = swap(h, '<p class="dx-qd__t">Goals &amp; vision</p><p class="dx-qd__d">Company OKRs turned into quarterly goals each person could act on. Our vision',
             '<p class="dx-qd__t">Strategy &amp; goals</p><p class="dx-qd__d">Co-set product strategy and priorities for 3+ products, and turned company OKRs into quarterly goals each person could act on. Our vision', "develux goals")
    h = swap(h, "Design&#8217;s inputs, outputs and checkpoints, agreed with every team it touches.", "Inputs, outputs and checkpoints for every stage of the product process, agreed with every team involved.", "develux delivery card")
    h = swap(h, '<p class="project__role">Chief Design Officer</p>', '<p class="project__role">Head of Product &amp; Design</p>', "develux card role")
    h = swap(h, '<img src="assets/cover-develux.jpg?v=3" width="580" height="355" alt="Develux — building a design and research function, leadership case"',
             '<img src="assets/cover-develux-pm.jpg" width="580" height="355" alt="Develux — product processes across product management, design and research"', "develux cover")
    # Rocken case: product work only, no pure UI/design parts (CRM, Dashboard, UI block).
    h = swap(h, r'<article class="product">\s*<img src="assets/r-crm\.jpg".*?</article>\s*', "", "rocken crm card", regex=True)
    h = swap(h, r'<article class="product">\s*<img src="assets/r-dash\.jpg".*?</article>\s*', "", "rocken dash card", regex=True)
    h = swap(h, "<br>Refresh the UI.", "", "rocken refresh ui")
    h = swap(h, r'<li><a href="#jobs-ui">.*?</a></li>', "", "rocken ui subnav", regex=True)
    h = swap(h, r'\s*<div class="block" id="jobs-ui">.*?(?=\n    </div>\n  </div>\n\n  <!-- =+ CRM)', "", "rocken ui block", regex=True)
    h = swap(h, r'  <!-- =+ CRM =+ -->.*?(?=  <!-- =+ TALENT)', "", "rocken crm section", regex=True)
    h = swap(h, r'\n  <!-- =+ DASHBOARD =+ -->.*?(?=\n</div>\n<a class="totop" href="#rocken-top")', "", "rocken dashboard section", regex=True)
    h = swap(h, "which gave us a chance to do a full redesign.<br><br>2. Design and propose a monetisation model",
             "which gave us a chance to rethink what motivates candidates to come back.<br><br>2. Propose a monetisation model", "rocken talent challenge")
    # Projects: PM-relevant cases only.
    h = drop_card(h, "https://www.behance.net/gallery/134924403/UIUX-Epul-Payment-system", "epul")
    h = drop_card(h, "https://asalart.ua/", "asalart")
    # Marketplace card: lead with the result.
    h = swap(h, '<p class="project__domain">Freelance marketplace for student writing</p>',
             '<p class="project__domain">Fixing the biggest funnel drop-off: +6% first orders</p>', "writers card")
    # Marketplace case header: lead with the problem solved.
    h = swap(h, '<p class="wr-head__name">Freelance marketplace for student writing</p>',
             '<p class="wr-head__name">Three winning experiments that grew first and repeat orders</p>', "writers header")
    # Order: Readberry, marketplace, Develux, Rocken, Tabletki.
    card = re.search(r'<article class="project">(?:(?!</article>).)*?href="#writers"(?:(?!</article>).)*?</article>\n?', h, flags=re.S)
    if not card:
        sys.exit("build_pm: writers card not found")
    h = h.replace(card.group(0), "", 1)
    rb_card = (PARTS / "readberry_card.html").read_text(encoding="utf-8")
    h = swap(h, '<div class="projects">\n<article class="project">',
             '<div class="projects">\n' + rb_card + card.group(0) + '<article class="project">', "projects start")
    if not (h.find('href="#readberry" aria-label') < h.find('href="#writers" aria-label') < h.find('href="#develux" aria-label')):
        sys.exit("build_pm: cards are not in the order readberry, writers, develux")
    # Next-case chain in the same order: readberry -> writers -> develux -> rocken -> tabletki -> readberry.
    nxt = 'class="back back--next" href="#'
    h = swap(h, nxt + 'develux"', nxt + '@readberry"', "next after tabletki")
    h = swap(h, nxt + 'rocken"', nxt + '@develux"', "next after writers")
    h = swap(h, nxt + 'writers"', nxt + '@rocken"', "next after develux")
    h = h.replace(nxt + '@', nxt)

    # Readberry case (PM only): view, styles, router, show-reel modal.
    view = (PARTS / "readberry_view.html").read_text(encoding="utf-8")
    h = swap(h, '</section><section class="view" id="view-writers" hidden>',
             '</section>' + view + '<section class="view" id="view-writers" hidden>', "readberry view")
    css = (PARTS / "readberry.css").read_text(encoding="utf-8")
    # Before the main stylesheet, so the dark-theme --bg rules that follow win over the beige canvas.
    h = swap(h, "<style>:root{color-scheme:light;box-sizing:border-box}",
             "<style>" + css + "</style><style>:root{color-scheme:light;box-sizing:border-box}", "readberry css")
    h = swap(h, "develux:'view-develux'};", "develux:'view-develux',readberry:'view-readberry'};", "router views")
    h = swap(h, "if(/^dx-/.test(h)) return {view:'develux',anchor:h};",
             "if(/^dx-/.test(h)) return {view:'develux',anchor:h};\n    if(/^rb-/.test(h)) return {view:'readberry',anchor:h};", "router rb anchors")
    h = swap(h, "all.forEach(function(v){v.hidden=v.id!==views[r.view];});",
             "all.forEach(function(v){v.hidden=v.id!==views[r.view];});document.documentElement.setAttribute('data-view',r.view);", "router data-view")
    js = (PARTS / "readberry.js.html").read_text(encoding="utf-8")
    h = swap(h, "</body>", js + "</body>", "readberry js")

    # About.
    h = swap(h, '<p class="about__role">Head of Design &middot; Design Lead &middot; Wroclaw, Poland</p>',
             f'<p class="about__role">{ROLE} &middot; Wroclaw, Poland</p>', "about role")
    h = swap(h, f'href="{CV_DESIGN}"', f'href="{CV_PM}"', "cv links", count=2)
    h = re_sub_once(h, r'(<h2 class="about__h">Summary</h2><p>).*?(</p>)', r"\g<1>" + SUMMARY + r"\g<2>", "summary")

    tabs, rows = skills_markup()
    h = re_sub_once(h, r'(<div class="skills__tabs" role="group" aria-label="Filter skills">).*?(</div>)',
                    r"\g<1>" + tabs + r"\g<2>", "skill tabs")
    h = re_sub_once(h, r'(<div class="skills__rows" id="skills-rows">).*?(</div>)',
                    r"\g<1>" + rows + r"\g<2>", "skill rows")

    h = company(h, "&#8220;NODERA-Group&#8221;", READBERRY, "readberry")
    h = company(h, "&#8220;DEVELUX&#8221;", DEVELUX, "develux")
    h = company(h, "&#8220;ROCKEN&#8221;", ROCKEN, "rocken")
    h = company(h, "&#8220;PROMODO&#8221;", PUSHOK + "\n        " + PROMODO, "promodo")

    # Paths: pm/ sits one level down.
    h, n = re.subn(r'(?<![\w./-])assets/', "../assets/", h)
    if n < 50:
        sys.exit(f"build_pm: only {n} asset paths rewritten, expected many more")

    banner = "<!-- Generated by tools/build_pm.py from ../index.html. Do not edit by hand. -->\n"
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(banner + h, encoding="utf-8")
    print(f"build_pm: wrote {OUT.relative_to(ROOT)} ({len(h):,} chars, {n} asset paths)")


def re_sub_once(h, pattern, repl, name):
    found = len(re.findall(pattern, h, flags=re.S))
    if found != 1:
        sys.exit(f"build_pm: '{name}' matched {found} times, expected 1")
    return re.sub(pattern, lambda m: m.expand(repl), h, count=1, flags=re.S)


if __name__ == "__main__":
    build()
