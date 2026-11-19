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
    "Product leader with 10+ years building B2C and SaaS products for web and mobile. "
    "I founded and ran Readberry, a subscription iOS app, owning product strategy, roadmap and P&amp;L, "
    "the web-to-app funnel, pricing and monetization experiments. Before that, as Chief Design Officer "
    "at Develux, a multi-product EdTech company, I was part of the C-level team and worked with product "
    "teams on discovery and delivery: together we cut hypothesis-to-release time by more than 40% and "
    "lifted initiative success rate by 56%. Earlier I founded and ran PUSH-OK, a pet supplies e-commerce "
    "business. I work AI-first and prototype and build front end with Claude Code."
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
        "Claude Code", "Mixpanel", "Google Analytics 4", "Adapty", "AppsFlyer",
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
    'Founder &amp; Product Lead &mdash; <a href="https://apps.apple.com/ua/app/readberry-pdf-voice-reader/id6761894830" target="_blank" rel="noopener">Readberry</a>',
    "Mar 2026 &ndash; Nov 2026", [
        "Took a subscription iOS app from market research and customer discovery to App Store launch, with the MVP built in two months, then ran it as a business.",
        "Owned product strategy, roadmap and P&amp;L; updated forecasts against actual performance to steer spending and growth priorities.",
        "Built and optimised a web-to-app funnel: Meta traffic to a web quiz, then into the app via deep link. Iterated on quiz and onboarding steps, paywalls and pricing.",
        "Tested monetization beyond subscriptions, including a hybrid model with in-app purchases of extra usage limits.",
        "Improved retention through its leading indicators, frequency and depth of use, with habit mechanics: streaks, quizzes and flashcards.",
        "Set up video creative production for Meta and tracked key metrics for each creative concept; organised acquisition through Meta, ASO and Apple Search Ads.",
        "Led a cross-functional team and external partners across development and marketing; built parts of the front end myself with Claude Code.",
    ])])

DEVELUX = company_block("&#8220;DEVELUX&#8221;", "Multiproduct EdTech company", [job(
    "Chief Design Officer", "Jan 2024 &ndash; Mar 2026", [
        'Part of the C-level team reporting to the CEO. Led the design and research function of up to 17 people across 3+ products, including <a href="https://studyagent.com/" target="_blank" rel="noopener">StudyAgent</a>.',
        'Worked with product teams on discovery and delivery: cut median time from hypothesis to release from 3.5 to 2&nbsp;weeks and raised the share of initiatives hitting their success metric from 9% to 14% (<a href="#develux">case study</a>).',
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
    "<li>Built the agency&#8217;s Conversion Rate Optimization service from scratch: audit framework, hypothesis backlog and A/B testing process for client e-commerce sites.</li>"
    "<li>Led a team of 5 designers.</li></ul>")


def build():
    h = SRC.read_text(encoding="utf-8")

    h = swap(h, "<title>Pavlo Chenchyk — Head of Design · Design Lead</title>",
             "<title>Pavlo Chenchyk — Product Manager · Growth &amp; Monetization</title>", "title")

    desc_design = ("Pavlo Chenchyk — Head of Design and Design Lead with 10+ years in product design. "
                   "Former Chief Design Officer who grew a design and research team from 2 to 17 people.")
    desc_pm = ("Pavlo Chenchyk — Product Manager with 10+ years in B2C and SaaS products. Founded and ran "
               "a subscription iOS app: web-to-app funnel, monetization, retention and P&amp;L. Former Chief Design Officer.")
    h = swap(h, f'content="{desc_design}"', f'content="{desc_pm}"', "meta descriptions", count=2)
    h = swap(h, '<meta property="og:title" content="Pavlo Chenchyk — Head of Design · Design Lead">',
             '<meta property="og:title" content="Pavlo Chenchyk — Product Manager · Growth &amp; Monetization">', "og title")
    h = swap(h, '<meta property="og:url" content="https://pavlochenchyk.github.io/">',
             '<meta property="og:url" content="https://pavlochenchyk.github.io/pm/">', "og url")

    # Home: roles ring, product first (same length, so the ring keeps its spacing).
    h = swap(h, 'aria-label="Designer, manager, founder"', 'aria-label="Product, founder, designer"', "ring label")
    h = swap(h, ">DESIGNER&#160;&#8226;&#160;MANAGER&#160;&#8226;&#160;FOUNDER&#160;&#8226;&#160;<",
             ">PRODUCT&#160;&#8226;&#160;FOUNDER&#160;&#8226;&#160;DESIGNER&#160;&#8226;&#160;<", "ring text")

    # Projects: PM-relevant cases only.
    h = drop_card(h, "#tabletki", "tabletki")
    h = drop_card(h, "https://www.behance.net/gallery/134924403/UIUX-Epul-Payment-system", "epul")
    h = drop_card(h, "https://asalart.ua/", "asalart")
    # Marketplace card: lead with the result.
    h = swap(h, '<p class="project__domain">Freelance marketplace for student writing</p>',
             '<p class="project__domain">Fixing the biggest funnel drop-off: +6% first orders</p>', "writers card")
    # Marketplace case header: lead with the problem solved.
    h = swap(h, '<p class="wr-head__name">Freelance marketplace for student writing</p>',
             '<p class="wr-head__name">Three winning experiments that grew first and repeat orders</p>', "writers header")
    # Order: Readberry, marketplace, Develux, Rocken.
    card = re.search(r'<article class="project">(?:(?!</article>).)*?href="#writers"(?:(?!</article>).)*?</article>\n?', h, flags=re.S)
    if not card:
        sys.exit("build_pm: writers card not found")
    h = h.replace(card.group(0), "", 1)
    rb_card = (PARTS / "readberry_card.html").read_text(encoding="utf-8")
    h = swap(h, '<div class="projects">\n<article class="project">',
             '<div class="projects">\n' + rb_card + card.group(0) + '<article class="project">', "projects start")
    if not (h.find('href="#readberry" aria-label') < h.find('href="#writers" aria-label') < h.find('href="#develux" aria-label')):
        sys.exit("build_pm: cards are not in the order readberry, writers, develux")
    # Next-case chain in the same order: readberry -> writers -> develux -> rocken -> readberry.
    nxt = 'class="back back--next" href="#'
    h = swap(h, nxt + 'tabletki"', nxt + '@readberry"', "next after rocken")
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
