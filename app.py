from __future__ import annotations

import html
import base64
import textwrap
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).parent

st.set_page_config(
    page_title="YMBC Smart Information Kiosk",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


PAGES = {
    "Home": {
        "icon": "⌂",
        "title": "Welcome to Yeldo Mar Baselios College",
        "eyebrow": "Excellence in education",
        "description": "Discover opportunities, explore knowledge and build your future with us.",
    },
    "College Information": {
        "icon": "▥",
        "title": "College Information",
        "eyebrow": "About YMBC",
        "description": "Learn about our history, vision, mission, departments and achievements.",
    },
    "Admission": {
        "icon": "▣",
        "title": "Admission",
        "eyebrow": "Your next chapter starts here",
        "description": "Apply for undergraduate and postgraduate programmes at YMBC.",
    },
    "Courses & Departments": {
        "icon": "▱",
        "title": "Courses & Departments",
        "eyebrow": "Find your direction",
        "description": "Explore the wide range of undergraduate and postgraduate programmes offered at YMBC.",
    },
    "Campus Facilities": {
        "icon": "▤",
        "title": "Campus Facilities",
        "eyebrow": "A campus built for momentum",
        "description": "Explore world-class infrastructure and student amenities at Yeldo Mar Baselios College.",
    },
    "Visitor Information": {
        "icon": "⌖",
        "title": "Visitor Information",
        "eyebrow": "Plan your visit",
        "description": "Find location, directions, visiting details and important guidelines.",
    },
    "Contact Us": {
        "icon": "◌",
        "title": "Contact Us",
        "eyebrow": "We are here to help",
        "description": "Get in touch with Yeldo Mar Baselios College for any enquiries.",
    },
}

NAV_ITEMS = [
    "Home",
    "Ask AI",
    "College Information",
    "Admission",
    "Courses & Departments",
    "Campus Facilities",
    "Visitor Information",
    "Contact Us",
]

COURSES = [
    {"name": "BCA", "title": "Bachelor of Computer Applications", "level": "UG", "duration": "3 years", "department": "Computer Science", "tone": "rose", "icon": "⌘"},
    {"name": "B.Sc.", "title": "Bachelor of Science", "level": "UG", "duration": "3 years", "department": "Science", "tone": "blue", "icon": "⚗"},
    {"name": "B.A.", "title": "Bachelor of Arts", "level": "UG", "duration": "3 years", "department": "Arts", "tone": "lilac", "icon": "▤"},
    {"name": "B.Com.", "title": "Bachelor of Commerce", "level": "UG", "duration": "3 years", "department": "Commerce", "tone": "sand", "icon": "▥"},
    {"name": "MCA", "title": "Master of Computer Applications", "level": "PG", "duration": "2 years", "department": "Computer Science", "tone": "lilac", "icon": "</>"},
    {"name": "M.Sc.", "title": "Master of Science", "level": "PG", "duration": "2 years", "department": "Science", "tone": "mint", "icon": "▰"},
]

FACILITIES = [
    {"name": "Library", "description": "A well-equipped library with a vast collection of books, journals and e-resources.", "icon": "▤", "tone": "rose", "image": "library.png", "detail": "Quiet reading zones, reference help and digital resources support focused study."},
    {"name": "Computer Laboratories", "description": "Modern computer labs with high-speed internet and updated software.", "icon": "▣", "tone": "blue", "image": "computer-lab-facility.png", "detail": "Dedicated labs support programming, design, analytics and practical coursework."},
    {"name": "Science Laboratories", "description": "Well-equipped laboratories for hands-on learning and research.", "icon": "⚗", "tone": "mint", "image": "science-lab.png", "detail": "Safe, supervised lab spaces support practical discovery across the sciences."},
    {"name": "Classrooms", "description": "Spacious, smart and student-friendly classrooms for effective learning.", "icon": "▦", "tone": "sand", "image": "classrooms.png", "detail": "Bright, flexible learning rooms with presentation-ready teaching tools."},
    {"name": "Auditorium", "description": "A modern auditorium for seminars, conferences and cultural events.", "icon": "◉", "tone": "rose", "image": "auditorium.png", "detail": "A high-capacity venue for talks, performances, ceremonies and community events."},
    {"name": "Sports Facilities", "description": "Facilities for indoor and outdoor sports to promote a healthy lifestyle.", "icon": "✧", "tone": "blue", "image": "sports.png", "detail": "Make time for movement with spaces for recreation, practice and campus events."},
    {"name": "Campus & Environment", "description": "A green, clean and peaceful campus that fosters learning and creativity.", "icon": "◌", "tone": "mint", "image": "campus-environment.png", "detail": "Thoughtful landscaping creates a calm, walkable setting for campus life."},
    {"name": "Cafeteria", "description": "A hygienic and spacious cafeteria offering a variety of food options.", "icon": "▰", "tone": "sand", "image": "cafeteria.png", "detail": "A welcoming break point with convenient food and beverage options."},
]

GALLERY_ITEMS = [
    ("Morning on campus", "Sunlit paths and a slower start to the day.", "blue", "campus-environment.png"),
    ("Learning spaces", "Bright rooms designed for focus and collaboration.", "sand", "classrooms.png"),
    ("Library moments", "Quiet corners for research, reading and reflection.", "rose", "library.png"),
    ("Beyond the classroom", "A campus that gives space to community and play.", "mint", "sports.png"),
]

FAQS = [
    ("How can I apply for admission?", "Start with the Admission Overview, review eligibility and required documents, then send us an enquiry for the current application window."),
    ("What are the eligibility criteria?", "Eligibility varies by programme. The admissions team can confirm the latest requirements for the course you are considering."),
    ("Which courses are available at YMBC?", "YMBC offers undergraduate and postgraduate programmes in Computer Science, Science, Arts, Commerce and allied areas."),
    ("What documents are required?", "Typically, applicants need certificates, transfer records, conduct certificate, photograph and a valid identity document."),
    ("When will the admission process start?", "Dates are published by the college each cycle. Use the Contact Us form to request the latest schedule."),
]


ICON_PATHS = {
    "search": '<circle cx="11" cy="11" r="7.5"/><path d="m16.5 16.5 5 5"/>',
    "bell": '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9Z"/><path d="M10 21h4"/>',
    "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    "chevron": '<path d="m9 18 6-6-6-6"/>',
    "check": '<path d="m5 12 4 4L19 6"/>',
    "home": '<path d="m3 11 9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/>',
    "pin": '<path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a14 14 0 0 0 5 5L15 13l5 2v4c0 1-1 2-2 2C10 21 3 14 3 6c0-1 1-2 2-2Z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "building": '<path d="M4 21V5l8-3 8 3v16M2 21h20M8 21v-5h8v5M8 8h1M15 8h1M8 11h1M15 11h1"/>',
    "layers": '<path d="m12 2 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5"/><path d="m3 17 9 5 9-5"/>',
    "book": '<path d="M4 5a3 3 0 0 1 3-3h12v17H7a3 3 0 0 0-3 3V5Z"/><path d="M4 19a3 3 0 0 1 3-3h12"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/>',
    "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "spark": '<path d="m12 3 1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3ZM19 17l.7 2.3L22 20l-2.3.7L19 23l-.7-2.3L16 20l2.3-.7L19 17Z"/>',
}


def icon(name: str, size: int = 20, stroke: float = 1.8) -> str:
    path = ICON_PATHS.get(name, ICON_PATHS["spark"])
    return f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'


def esc(value: object) -> str:
    return html.escape(str(value))


@lru_cache(maxsize=None)
def asset_src(filename: str) -> str:
    asset_path = BASE_DIR / "assets" / "images" / filename
    if not asset_path.exists():
        return ""
    encoded = base64.b64encode(asset_path.read_bytes()).decode("ascii")
    return f"data:image/{asset_path.suffix.lstrip('.').lower()};base64,{encoded}"


def load_css() -> None:
    css_path = BASE_DIR / "styles" / "style.css"
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def set_page(page: str) -> None:
    st.session_state.page = page
    st.session_state.active_nav = page
    st.session_state.active_tab = ""


def sidebar() -> None:
    current = st.session_state.get("page", "Home")
    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <div class="seal-mark" aria-label="Yeldo Mar Baselios College seal"><img src="{asset_src('logo-seal.png')}" alt="Yeldo Mar Baselios College seal" /></div>
                <div class="sidebar-college">Yeldo Mar<br/>Baselios College</div>
                <div class="sidebar-location">Kothamangalam, Kerala, India</div>
                <div class="kiosk-label">Smart Information Kiosk</div>
                <div class="sidebar-tagline">Learn <span>•</span> Explore <span>•</span> Grow</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for item in NAV_ITEMS:
            if item == "Ask AI":
                target = "Ask AI"
            else:
                target = item
            selected = current == target or (item == "Ask AI" and current == "Ask AI")
            label = f"{'●' if selected else '○'}  {item}"
            if st.button(label, key=f"nav_{item}", use_container_width=True):
                set_page(target)
                st.rerun()
        st.markdown(
            """
            <div class="sidebar-footer-art" aria-hidden="true">
                <div class="cap-line"></div>
                <div class="cap-shape">⌒</div>
                <div class="footer-glow"></div>
                <strong>Your Future<br/>Starts Here...</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )


def topbar() -> None:
    st.markdown('<div class="topbar-rule"></div>', unsafe_allow_html=True)
    cols = st.columns([1.5, 2.2, 0.5, 1.15], vertical_alignment="center")
    with cols[0]:
        st.markdown(
            f'<div class="brand-lockup"><span class="brand-monogram">YMBC</span><span class="brand-divider"></span><span><strong>Yeldo Mar Baselios College</strong><small>Kothamangalam, Kerala, India</small></span></div>',
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.text_input("Search the campus", placeholder="Search for information…", key="global_search", label_visibility="collapsed")
    with cols[2]:
        if st.button("◔", key="notification", help="Notifications"):
            st.session_state.toast = "You are all caught up."
    with cols[3]:
        now = datetime.now()
        st.markdown(
            f'<div class="weather-pill"><span class="sun-symbol">☼</span><span><strong>{now.strftime("%I:%M %p")}</strong><small>{now.strftime("%a, %b %d, %Y")}</small></span><b>28° C</b></div>',
            unsafe_allow_html=True,
        )
    query = st.session_state.get("global_search", "").strip()
    if query:
        matches = [name for name in list(PAGES) + ["Ask AI"] if query.lower() in name.lower()]
        if matches:
            st.markdown(f'<div class="search-hint">{icon("search", 16)} Showing quick links for <strong>{esc(query)}</strong>: ' + " · ".join(esc(m) for m in matches) + "</div>", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="search-hint">{icon("info", 16)} No exact page match yet — try “admission”, “courses”, “library”, or “contact”.</div>', unsafe_allow_html=True)


def campus_art() -> str:
    return f'<img class="campus-photo" src="{asset_src("campus-hero.png")}" alt="Yeldo Mar Baselios College campus building" />'


def hero(page: str, home: bool = False) -> None:
    data = PAGES[page]
    heading = data["title"] if not home else "Welcome to <span>Yeldo Mar Baselios College</span>"
    crumb = "Home" if home else f'Home <span class="crumb-sep">›</span> {esc(page)}'
    hero_markup = f"""<section class="hero-panel {'hero-home' if home else ''}">
{campus_art()}
<div class="hero-overlay"></div>
<div class="hero-content">
<div class="breadcrumbs">{icon('home', 15)} {crumb}</div>
<div class="hero-eyebrow">{icon('spark', 15)} {esc(data['eyebrow'])}</div>
<h1>{heading}</h1>
<p>{esc(data['description'])}</p>
<div class="hero-actions">
<span class="hero-chip">{icon('check', 15)} Student-first campus</span>
<span class="hero-chip soft">{icon('spark', 15)} Designed for your next step</span>
</div>
</div>
<div class="hero-wave"></div>
</section>"""
    st.markdown(textwrap.dedent(hero_markup), unsafe_allow_html=True)


def page_tabs(items: list[str], active: str | None = None) -> str:
    active_label = active or items[0]
    cols = st.columns(len(items))
    for idx, item in enumerate(items):
        with cols[idx]:
            if st.button(item, key=f"tab_{item}", use_container_width=True):
                st.session_state.active_tab = item
                st.rerun()
    return st.session_state.get("active_tab", active_label)


def section_heading(title: str, subtitle: str | None = None, icon_name: str = "spark") -> None:
    sub = f'<p>{esc(subtitle)}</p>' if subtitle else ""
    st.markdown(f'<div class="section-heading"><div class="heading-icon">{icon(icon_name, 20)}</div><div><h2>{esc(title)}</h2>{sub}</div></div>', unsafe_allow_html=True)


def metric_strip() -> None:
    metrics = [("30+", "Programmes", "layers"), ("10+", "Departments", "building"), ("3000+", "Students", "users"), ("28", "Years of excellence", "target")]
    markup = '<div class="metric-strip">'
    for value, label, icon_name in metrics:
        markup += f'<div class="metric"><div class="metric-icon">{icon(icon_name, 22)}</div><div><strong>{value}</strong><span>{label}</span></div></div>'
    markup += '</div>'
    st.markdown(markup, unsafe_allow_html=True)


def assistant_panel(compact: bool = False) -> None:
    st.markdown(
        f"""
        <div class="assistant-panel {'compact' if compact else ''}">
            <div class="assistant-header"><div class="assistant-avatar">✦</div><div><strong>YMBC Assistant</strong><span>Your college information guide</span></div><span class="assistant-live">● live</span></div>
            <div class="assistant-body"><div class="assistant-bubble"><strong>👋 Welcome to YMBC!</strong><br/>Ask me about courses, admission, departments, facilities and more.</div>
            <div class="try-label">Try asking:</div>
            <div class="prompt-list"><span>What courses are available?</span><span>How can I apply?</span><span>Where is the library?</span></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    prompts = ["What courses are available?", "How can I apply?", "Where is the library?"]
    cols = st.columns(3)
    for i, prompt in enumerate(prompts):
        with cols[i]:
            if st.button(prompt, key=f"prompt_{'compact' if compact else 'home'}_{i}", use_container_width=True):
                st.session_state.assistant_answer = {
                    prompts[0]: "YMBC offers UG and PG programmes across Computer Science, Science, Arts and Commerce.",
                    prompts[1]: "Visit the Admission page to review eligibility and documents, then send an enquiry to the college team.",
                    prompts[2]: "The library is located in the academic block. The Campus Facilities page has more details.",
                }[prompt]
    answer = st.session_state.get("assistant_answer")
    if answer:
        st.info(answer, icon="✦")
    st.text_input("Ask the YMBC Assistant", placeholder="Type your question here…", key="assistant_input", label_visibility="collapsed")
    if st.button("Ask Assistant", key=f"ask_submit_{'compact' if compact else 'home'}", type="primary", use_container_width=True):
        query = st.session_state.get("assistant_input", "").strip()
        if query:
            st.session_state.assistant_answer = f"I’ll help with “{query}”. Start with the page navigation above, or send an enquiry for a direct answer."
        else:
            st.session_state.assistant_answer = "Type a question and I’ll point you in the right direction."
        st.rerun()


def home_page() -> None:
    hero("Home", home=True)
    st.markdown('<div class="quick-actions"><span>Explore the campus</span><span>Get answers in seconds</span><span>Plan your next step</span></div>', unsafe_allow_html=True)
    cards = [
        ("College Information", "Learn about our story, vision, mission and achievements.", "building", "rose"),
        ("Ask AI", "Get instant, intelligent answers to college-related questions.", "spark", "blue"),
        ("Admission", "Eligibility, application details and important dates in one place.", "book", "sand"),
        ("Courses", "Explore programmes and academic information across departments.", "layers", "blue"),
        ("Campus Facilities", "Discover the library, labs, classrooms and student spaces.", "building", "mint"),
        ("Visitor Information", "Location, directions, visiting hours and helpful guidelines.", "pin", "lilac"),
    ]
    st.markdown('<div class="card-grid home-cards">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, (title, description, icon_name, tone) in enumerate(cards):
        with cols[idx % 3]:
            st.markdown(f'<div class="info-card tone-{tone}"><div class="card-top"><div class="card-icon">{icon(icon_name, 26)}</div><span class="round-arrow">{icon("arrow", 18)}</span></div><h3>{esc(title)}</h3><p>{esc(description)}</p></div>', unsafe_allow_html=True)
            if st.button(f"Open {title}", key=f"home_card_{idx}", use_container_width=True):
                set_page(title if title in PAGES else "Ask AI")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    metric_strip()
    st.markdown('<div class="home-bottom-grid">', unsafe_allow_html=True)
    left, right = st.columns([1.22, 0.78])
    with left:
        section_heading("A calmer way to find your next step", "Everything you need to explore YMBC, gathered into a single smart kiosk.", "target")
        st.markdown('<div class="spotlight-card"><div class="spotlight-mark">✦</div><div><strong>Built around clarity</strong><p>Move from curiosity to confidence with clear information, useful prompts and friendly signposting.</p></div><span class="spotlight-line"></span></div>', unsafe_allow_html=True)
    with right:
        assistant_panel(compact=True)
    st.markdown('</div>', unsafe_allow_html=True)


def college_info_page() -> None:
    hero("College Information")
    active = page_tabs(["About YMBC", "History", "Vision & Mission", "Principal’s Message", "Departments", "Achievements"])
    st.markdown(f'<div class="tab-status">{icon("check", 15)} Viewing <strong>{esc(active)}</strong></div>', unsafe_allow_html=True)
    if active == "History":
        section_heading("A story of steady progress", "A college that has grown by staying close to its students and its community.", "calendar")
        st.markdown('<div class="timeline"><div><span>01</span><strong>Foundation</strong><p>YMBC began with a commitment to accessible, value-based higher education.</p></div><div><span>02</span><strong>Expansion</strong><p>New departments and programmes broadened opportunities for the region.</p></div><div><span>03</span><strong>Today</strong><p>A connected campus where learning, purpose and community meet.</p></div></div>', unsafe_allow_html=True)
    elif active == "Vision & Mission":
        section_heading("Vision & Mission", "The principles that guide the learning experience.", "target")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="quote-card blue"><h3>Vision</h3><p>To be a centre of excellence in higher education, fostering knowledge, values and social commitment.</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="quote-card rose"><h3>Mission</h3><p>To impart quality education, promote research and innovation, and nurture responsible citizens for a better world.</p></div>', unsafe_allow_html=True)
    else:
        left, right = st.columns([1.3, 0.7])
        with left:
            section_heading("About YMBC", "A closer look at the college and the people who make it feel like home.", "building")
            st.markdown('<div class="content-card"><p>Yeldo Mar Baselios College (YMBC), Kothamangalam, is a higher education institution in Kerala committed to academic excellence, value-based education and the holistic development of students.</p><p>Our campus brings together strong teaching, practical learning and a supportive student experience — helping every learner turn potential into progress.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="principal-card"><div class="portrait">PM</div><div><span class="eyebrow-small">Principal’s message</span><h3>“Learning becomes meaningful when it opens a door for someone else.”</h3><p>We strive to provide a vibrant academic environment that nurtures knowledge, values and leadership for a better society.</p><strong>— Principal, Yeldo Mar Baselios College</strong></div></div>', unsafe_allow_html=True)
        with right:
            st.markdown('<div class="quick-info-card"><h3>Quick information</h3><div><b>Location</b><span>Kothamangalam, Kerala, India</span></div><div><b>Affiliation</b><span>Mahatma Gandhi University, Kottayam</span></div><div><b>Type</b><span>Aided College</span></div><div><b>Programmes</b><span>UG & PG programmes</span></div></div>', unsafe_allow_html=True)
    metric_strip()


def admission_page() -> None:
    hero("Admission")
    active = page_tabs(["Admission Overview", "Available Courses", "Eligibility Criteria", "Application Procedure", "Required Documents", "Important Dates", "FAQs"])
    if active == "FAQs":
        section_heading("Frequently Asked Questions", "A quick guide to the most common admission questions.", "info")
        for question, answer in FAQS:
            with st.expander(question):
                st.write(answer)
        return
    if active == "Eligibility Criteria":
        section_heading("Eligibility criteria", "Know what you need before you begin your application.", "check")
        st.markdown('<div class="eligibility-grid"><div class="content-card"><h3>Undergraduate programmes</h3><p>Completion of higher secondary education or an equivalent qualification. Programme-specific requirements may apply.</p></div><div class="content-card"><h3>Postgraduate programmes</h3><p>A recognised undergraduate degree in the relevant stream. Speak with the admission desk for programme-level details.</p></div></div>', unsafe_allow_html=True)
        return
    if active == "Application Procedure":
        section_heading("Application procedure", "Four simple steps from first question to confirmed place.", "arrow")
        st.markdown('<div class="process-steps"><div><span>01</span><strong>Check eligibility</strong><p>Review the programme and its requirements.</p></div><div><span>02</span><strong>Apply online / offline</strong><p>Submit your application with accurate details.</p></div><div><span>03</span><strong>Submit documents</strong><p>Keep certificates and identity proof ready.</p></div><div><span>04</span><strong>Confirmation</strong><p>Our team will guide you through the next step.</p></div></div>', unsafe_allow_html=True)
        return
    if active == "Required Documents":
        section_heading("Required documents", "Keep these essentials ready for a smoother application.", "book")
        document_names = ["Application form (online/offline)", "Educational certificates", "Transfer certificate (TC)", "Conduct certificate", "Passport-size photograph", "Identity proof (Aadhaar / other)"]
        cols = st.columns(2)
        for idx, name in enumerate(document_names):
            with cols[idx % 2]:
                st.markdown(f'<div class="check-row">{icon("check", 16)} {esc(name)}</div>', unsafe_allow_html=True)
        return
    if active == "Important Dates":
        section_heading("Important dates", "Use this as a starting point and confirm the latest schedule with the college.", "calendar")
        st.markdown('<div class="date-grid"><div><span>01</span><strong>Enquiry window</strong><p>Open now — connect with the admission team.</p></div><div><span>02</span><strong>Application review</strong><p>Documents are checked after submission.</p></div><div><span>03</span><strong>Confirmation</strong><p>Selected applicants receive next-step guidance.</p></div></div>', unsafe_allow_html=True)
        return
    if active == "Available Courses":
        section_heading("Available courses", "Explore programmes before you apply.", "layers")
        render_course_cards(show_filter=False)
        return
    left, right = st.columns([1.22, 0.78])
    with left:
        section_heading("Admission overview", "A clear path into a campus that keeps your goals in view.", "book")
        st.markdown('<div class="content-card"><p>Yeldo Mar Baselios College offers a wide range of undergraduate and postgraduate programmes across Arts, Science, Commerce and Computer Applications, with a strong focus on academic excellence and holistic development.</p><p>Tell us what you want to study and our team will help you understand eligibility, documents and the best next step.</p></div>', unsafe_allow_html=True)
        if st.button("Enquire about admission →", key="admission_enquiry", type="primary"):
            st.session_state.page = "Contact Us"
            st.session_state.toast = "Your enquiry form is ready."
            st.rerun()
    with right:
        st.markdown(f'<div class="admission-photo"><img src="{asset_src("admission-books.png")}" alt="Graduation cap and books" /><span>Make your next move</span></div><div class="admission-stats"><div><strong>30+</strong><span>Programmes</span></div><div><strong>10+</strong><span>Departments</span></div><div><strong>UG & PG</strong><span>Study levels</span></div><div><strong>3000+</strong><span>Students</span></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="lower-grid"><div class="content-card"><h3>Admission process</h3><div class="mini-process"><span>01<br/><b>Eligibility</b></span><i></i><span>02<br/><b>Apply</b></span><i></i><span>03<br/><b>Documents</b></span><i></i><span>04<br/><b>Confirm</b></span></div></div><div class="content-card"><h3>Need help?</h3><p>Ask a question and we’ll help you find the right starting point.</p><button class="fake-link">Talk to the admission team →</button></div></div>', unsafe_allow_html=True)


def render_course_cards(show_filter: bool = True) -> None:
    if show_filter:
        filter_cols = st.columns([1, 1, 2])
        with filter_cols[0]:
            level = st.selectbox("Programme level", ["All programmes", "Undergraduate (UG)", "Postgraduate (PG)"], label_visibility="visible")
        with filter_cols[1]:
            dept = st.selectbox("Department", ["All departments", "Computer Science", "Science", "Arts", "Commerce"], label_visibility="visible")
        with filter_cols[2]:
            course_query = st.text_input("Search courses", placeholder="Search by programme or department…", label_visibility="visible")
    else:
        level, dept, course_query = "All programmes", "All departments", ""
    filtered = []
    for course in COURSES:
        level_ok = level == "All programmes" or (level.startswith("Undergraduate") and course["level"] == "UG") or (level.startswith("Postgraduate") and course["level"] == "PG")
        dept_ok = dept == "All departments" or course["department"] == dept
        query_ok = not course_query or course_query.lower() in (course["name"] + course["title"] + course["department"]).lower()
        if level_ok and dept_ok and query_ok:
            filtered.append(course)
    if not filtered:
        st.warning("No programmes match those filters. Try widening your search.")
        return
    cols = st.columns(3)
    for idx, course in enumerate(filtered):
        with cols[idx % 3]:
            st.markdown(f'<div class="course-card tone-{course["tone"]}"><div class="course-top"><span class="course-icon">{course["icon"]}</span><b>{course["level"]}</b></div><h3>{esc(course["name"])}</h3><p>{esc(course["title"])}</p><div class="course-meta"><span>{icon("calendar", 14)} {esc(course["duration"])}</span><span>{icon("building", 14)} {esc(course["department"])}</span></div></div>', unsafe_allow_html=True)
            if st.button(f"View {course['name']} details →", key=f"course_{course['name']}", use_container_width=True):
                st.session_state.selected_course = course["name"]
    selected = st.session_state.get("selected_course")
    if selected:
        course = next((c for c in COURSES if c["name"] == selected), None)
        if course:
            st.markdown(f'<div class="selected-course"><div><span class="eyebrow-small">Selected programme</span><h3>{esc(course["name"])} — {esc(course["title"])}</h3><p>A focused {course["duration"]} pathway within the {esc(course["department"])} department.</p></div><div class="selected-badge">{esc(course["level"])}</div></div>', unsafe_allow_html=True)


def courses_page() -> None:
    hero("Courses & Departments")
    active = page_tabs(["All Programmes", "Undergraduate (UG)", "Postgraduate (PG)", "Departments", "Programme Details", "Career Opportunities"])
    if active == "Departments":
        section_heading("Departments at YMBC", "Find the academic home that matches your curiosity.", "building")
        dept_cols = st.columns(4)
        for idx, dept in enumerate(["Computer Science", "Science", "Arts", "Commerce", "Management", "Languages", "Mathematics", "Social Work"]):
            with dept_cols[idx % 4]:
                st.markdown(f'<div class="dept-card"><div>{icon("building", 22)}</div><strong>{esc(dept)}</strong><span>Explore department →</span></div>', unsafe_allow_html=True)
        return
    if active == "Programme Details":
        section_heading("Programme details", "Select a course below to see the shape of the journey.", "info")
        render_course_cards(show_filter=False)
        return
    if active == "Career Opportunities":
        section_heading("Career opportunities", "Strong foundations for a changing world of work.", "target")
        st.markdown('<div class="opportunity-grid"><div class="content-card"><h3>Build capability</h3><p>Learn through a blend of concepts, practical work and peer collaboration.</p></div><div class="content-card"><h3>Find your direction</h3><p>Explore pathways across technology, science, commerce, arts and beyond.</p></div><div class="content-card"><h3>Stay connected</h3><p>Grow with a campus community that values curiosity, confidence and responsibility.</p></div></div>', unsafe_allow_html=True)
        return
    section_heading("Available programmes", "Use filters to narrow down your next move.", "layers")
    render_course_cards(show_filter=True)
    st.markdown(f'<div class="programme-highlight"><img src="{asset_src("computer-lab.png")}" alt="Computer laboratory" /><div><span class="eyebrow-small">Programme highlight</span><h3>Learn where ideas become capability</h3><p>Our programmes connect strong foundations with practical learning, collaborative work and the confidence to build what comes next.</p></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="departments-strip"><strong>{icon}</strong><h3>Departments at YMBC</h3><span>Computer Science</span><span>Science</span><span>Arts</span><span>Commerce</span><span>Management</span></div>'.format(icon=icon("building", 20)), unsafe_allow_html=True)


def facilities_page() -> None:
    hero("Campus Facilities")
    active = page_tabs(["All Facilities", "Academic", "Learning", "Technology", "Sports & Recreation", "Student Amenities", "Infrastructure", "Campus Gallery"])
    if active == "Campus Gallery":
        section_heading("Campus gallery", "A visual tour of the places that shape the YMBC experience.", "spark")
        gallery_index = st.session_state.get("gallery_index", 0)
        gallery_cols = st.columns(4)
        for idx, (name, caption, tone, image_name) in enumerate(GALLERY_ITEMS):
            with gallery_cols[idx]:
                st.markdown(f'<div class="gallery-tile tone-{tone}"><div class="gallery-scene"><img class="gallery-image" src="{asset_src(image_name)}" alt="{esc(name)}" /><span>{idx + 1:02d}</span></div><div><strong>{esc(name)}</strong><p>{esc(caption)}</p></div></div>', unsafe_allow_html=True)
                if st.button(f"View {idx + 1:02d}", key=f"gallery_{idx}", use_container_width=True):
                    st.session_state.gallery_index = idx
                    st.rerun()
        selected_gallery = GALLERY_ITEMS[gallery_index]
        st.markdown(f'<div class="selected-course"><div><span class="eyebrow-small">Gallery view {gallery_index + 1:02d}</span><h3>{esc(selected_gallery[0])}</h3><p>{esc(selected_gallery[1])}</p></div><div class="selected-badge">Campus life</div></div>', unsafe_allow_html=True)
        return
    section_heading(active, "Spaces that make daily learning feel more capable and more comfortable.", "building")
    cols = st.columns(4)
    for idx, facility in enumerate(FACILITIES):
        with cols[idx % 4]:
            st.markdown(f'<div class="facility-card"><div class="facility-art tone-{facility["tone"]}"><img class="facility-photo" src="{asset_src(facility["image"])}" alt="{esc(facility["name"])}" /><span class="facility-icon">{facility["icon"]}</span></div><div class="facility-copy"><div class="card-top"><h3>{esc(facility["name"])}</h3><span class="round-arrow">{icon("arrow", 16)}</span></div><p>{esc(facility["description"])}</p></div></div>', unsafe_allow_html=True)
            if st.button(f"Explore {facility['name']}", key=f"facility_{idx}", use_container_width=True):
                st.session_state.selected_facility = facility["name"]
    selected = st.session_state.get("selected_facility")
    if selected:
        facility = next((f for f in FACILITIES if f["name"] == selected), None)
        if facility:
            st.markdown(f'<div class="selected-course"><div><span class="eyebrow-small">Facility spotlight</span><h3>{esc(facility["name"])}</h3><p>{esc(facility["detail"])}</p></div><div class="selected-badge">Open</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="facility-strip"><strong>Campus at a glance</strong><span>Library</span><span>Computer labs</span><span>Science labs</span><span>Auditorium</span><span>Sports</span><span>Cafeteria</span></div>', unsafe_allow_html=True)


def visitor_page() -> None:
    hero("Visitor Information")
    active = page_tabs(["Overview", "Location & Directions", "Visiting Hours", "Visitor Guidelines", "Nearby Facilities", "Campus Map"])
    if active == "Visiting Hours":
        section_heading("Visiting hours", "Plan a comfortable, well-timed campus visit.", "calendar")
        st.markdown('<div class="hours-card"><div><span>Monday – Friday</span><strong>09:30 AM – 04:30 PM</strong></div><div><span>Saturday</span><strong>09:30 AM – 01:00 PM</strong></div><div><span>Sunday</span><strong>Closed</strong></div></div>', unsafe_allow_html=True)
        return
    if active == "Visitor Guidelines":
        section_heading("Visitor guidelines", "A few simple reminders help everyone have a smooth visit.", "check")
        for text in ["Visit during the specified office hours.", "Report at the college reception on arrival.", "Carry a valid government ID for verification.", "Follow campus rules and maintain decorum.", "Prior appointment is recommended for official meetings."]:
            st.markdown(f'<div class="check-row">{icon("check", 16)} {esc(text)}</div>', unsafe_allow_html=True)
        return
    if active == "Location & Directions":
        section_heading("How to reach YMBC", "The campus is easy to find from Kothamangalam and nearby hubs.", "pin")
        st.markdown('<div class="route-grid"><div><strong>By road</strong><p>Well connected by state and national highways to Kothamangalam.</p></div><div><strong>By bus</strong><p>Kothamangalam Bus Stand — approximately 2 km from the college.</p></div><div><strong>By air</strong><p>Cochin International Airport (COK) — approximately 45 km.</p></div></div>', unsafe_allow_html=True)
        return
    if active == "Nearby Facilities":
        section_heading("Nearby facilities", "Useful stops within easy reach of campus.", "pin")
        st.markdown('<div class="nearby-grid"><div><strong>Restaurants</strong><span>Within 1 km</span></div><div><strong>Stay options</strong><span>Hotels & lodges nearby</span></div><div><strong>Hospitals</strong><span>Within 3 km</span></div><div><strong>ATM & shops</strong><span>Conveniently nearby</span></div></div>', unsafe_allow_html=True)
        return
    left, right = st.columns([1.05, 0.95])
    with left:
        section_heading("Plan your visit", "Welcome to Yeldo Mar Baselios College.", "pin")
        st.markdown('<div class="content-card"><p>Here you can find the essential information to plan a smooth and productive campus visit. If you are unsure where to start, reach out to the college office and we will point you in the right direction.</p></div>', unsafe_allow_html=True)
        if st.button("Get directions →", key="get_directions", type="primary"):
            st.session_state.active_tab = "Location & Directions"
            st.rerun()
    with right:
        st.markdown(f'<div class="map-card"><img class="map-photo" src="{asset_src("campus-map.png")}" alt="Map showing Yeldo Mar Baselios College in Kothamangalam" /><div class="map-pin">⌖</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="route-grid"><div><strong>Location</strong><p>Kothamangalam,<br/>Kerala, India</p></div><div><strong>Visiting hours</strong><p>Monday – Friday<br/>09:30 AM – 04:30 PM</p></div><div><strong>Contact</strong><p>+91 484 282xxxx<br/>(College Office)</p></div></div>', unsafe_allow_html=True)


def contact_page() -> None:
    hero("Contact Us")
    active = page_tabs(["Get in Touch", "Location & Map", "Office Timings", "Enquiry Form", "Quick Enquiries"])
    if active == "Office Timings":
        section_heading("Office timings", "Reach us during the following hours.", "calendar")
        st.markdown('<div class="hours-card"><div><span>Monday – Friday</span><strong>09:30 AM – 04:30 PM</strong></div><div><span>Saturday</span><strong>09:30 AM – 01:00 PM</strong></div></div>', unsafe_allow_html=True)
        return
    if active == "Location & Map":
        section_heading("Our location", "Find us in Kothamangalam, Kerala.", "pin")
        st.markdown(f'<div class="map-card map-large"><img class="map-photo" src="{asset_src("campus-map.png")}" alt="Map showing Yeldo Mar Baselios College in Kothamangalam" /><div class="map-pin">⌖</div></div>', unsafe_allow_html=True)
        return
    if active == "Quick Enquiries":
        section_heading("Quick enquiries", "Choose a topic and the team will help you find the right answer.", "spark")
        for label in ["Admission enquiry", "Course information", "General enquiry"]:
            if st.button(f"{label}  →", key=f"quick_{label}", use_container_width=True):
                st.session_state.contact_topic = label
                st.session_state.active_tab = "Enquiry Form"
                st.rerun()
        return
    left, center, right = st.columns([0.82, 1.2, 0.98])
    with left:
        section_heading("Contact information", "We are one message away.", "phone")
        st.markdown('<div class="contact-list"><div><b>College address</b><span>Yeldo Mar Baselios College<br/>Kothamangalam, Kerala, India</span></div><div><b>Phone</b><span>+91 484 282xxxx (Office)</span></div><div><b>Email</b><span>info@ymbc.ac.in</span></div><div><b>Website</b><span>www.ymbc.ac.in</span></div></div>', unsafe_allow_html=True)
    with center:
        section_heading("Send us a message", "Have a question, suggestion or enquiry?", "mail")
        with st.form("contact_form", clear_on_submit=False):
            name = st.text_input("Your name *", placeholder="Your name")
            phone = st.text_input("Phone number *", placeholder="+91 …")
            email = st.text_input("Email address", placeholder="you@example.com")
            topic = st.selectbox("Enquiry type *", ["Select an enquiry type", "Admission enquiry", "Course information", "Campus visit", "General enquiry"])
            message = st.text_area("Your message *", placeholder="How can we help?", height=120)
            submitted = st.form_submit_button("Send message →", use_container_width=True, type="primary")
        if submitted:
            errors = []
            if not name.strip(): errors.append("Please add your name.")
            if not phone.strip(): errors.append("Please add a phone number.")
            if topic == "Select an enquiry type": errors.append("Please choose an enquiry type.")
            if not message.strip(): errors.append("Please add a short message.")
            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.session_state.form_sent = True
                st.success("Thanks — your enquiry is ready for the YMBC team.")
    with right:
        st.markdown('<div class="social-card"><h3>Connect with us</h3><p>Follow campus life and updates.</p><div class="social-row"><span>yt</span><span>ig</span><span>f</span><span>in</span><span>𝕏</span></div></div><div class="quick-info-card mini"><h3>Quick help</h3><div><b>Office hours</b><span>Mon–Fri · 09:30–04:30</span></div><div><b>Response time</b><span>Usually within 2 working days</span></div></div>', unsafe_allow_html=True)


def ask_ai_page() -> None:
    hero("Home")
    section_heading("Ask AI", "A friendly guide to the information you need most.", "spark")
    left, right = st.columns([1.18, 0.82])
    with left:
        assistant_panel()
        st.markdown('<div class="content-card"><h3>Suggested topics</h3><p>Ask about admission, programmes, departments, facilities, directions or contact details.</p><div class="topic-grid"><span>Admission</span><span>Courses</span><span>Facilities</span><span>Visitor info</span></div></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="assistant-side-card"><h3>How I can help</h3><div><span>01</span><p>Point you to the right page.</p></div><div><span>02</span><p>Summarise key college information.</p></div><div><span>03</span><p>Help you prepare an enquiry.</p></div></div>', unsafe_allow_html=True)


def main() -> None:
    load_css()
    for key, default in {"page": "Home", "active_tab": "", "toast": "", "assistant_answer": "", "selected_course": "", "selected_facility": ""}.items():
        st.session_state.setdefault(key, default)
    sidebar()
    topbar()
    page = st.session_state.get("page", "Home")
    if st.session_state.get("toast"):
        st.toast(st.session_state.toast)
        st.session_state.toast = ""
    if page == "Home":
        home_page()
    elif page == "Ask AI":
        ask_ai_page()
    elif page == "College Information":
        college_info_page()
    elif page == "Admission":
        admission_page()
    elif page == "Courses & Departments":
        courses_page()
    elif page == "Campus Facilities":
        facilities_page()
    elif page == "Visitor Information":
        visitor_page()
    elif page == "Contact Us":
        contact_page()
    else:
        home_page()


if __name__ == "__main__":
    main()
