from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR


OUT = "deliverables/GEO_Product_Strategy.pptx"
W, H = Inches(13.333), Inches(7.5)
NAVY = RGBColor(16, 33, 65)
TEAL = RGBColor(20, 184, 166)
CORAL = RGBColor(255, 112, 67)
INK = RGBColor(30, 41, 59)
MUTED = RGBColor(100, 116, 139)
LIGHT = RGBColor(244, 247, 250)
WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(34, 197, 94)
AMBER = RGBColor(245, 158, 11)


prs = Presentation()
prs.slide_width = W
prs.slide_height = H
blank = prs.slide_layouts[6]


def rect(slide, x, y, w, h, fill=LIGHT, radius=False, line=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line or fill
    return shape


def text(slide, x, y, w, h, value, size=18, bold=False, color=INK,
         align=PP_ALIGN.LEFT, font="Aptos"):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.margin_left = frame.margin_right = Inches(0.04)
    frame.margin_top = frame.margin_bottom = Inches(0.02)
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = frame.paragraphs[0]
    p.text = value
    p.alignment = align
    p.font.name = font
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    return box


def title(slide, heading, kicker=None):
    if kicker:
        text(slide, 0.55, 0.28, 12.2, 0.28, kicker.upper(), 10, True, TEAL)
    text(slide, 0.55, 0.58, 12.2, 0.55, heading, 28, True, NAVY)
    rect(slide, 0.55, 1.18, 12.2, 0.03, TEAL)


def footer(slide, num, source=None):
    if source:
        text(slide, 0.55, 7.12, 11.7, 0.22, source, 7, False, MUTED)
    text(slide, 12.35, 7.08, 0.42, 0.22, str(num), 8, True, MUTED, PP_ALIGN.RIGHT)


def notes(slide, value):
    slide.notes_slide.notes_text_frame.text = value


def base_slide(kicker, heading, num, source=None):
    slide = prs.slides.add_slide(blank)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WHITE
    title(slide, heading, kicker)
    footer(slide, num, source)
    return slide


# 1
slide = prs.slides.add_slide(blank)
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = NAVY
rect(slide, 0, 0, 13.333, 0.12, TEAL)
text(slide, 0.75, 1.05, 11.8, 0.35, "GEO / PRODUCT STRATEGY", 12, True, TEAL)
text(slide, 0.75, 1.55, 10.9, 1.25, "From AI visibility\nto measurable action", 34, True, WHITE)
text(slide, 0.75, 3.15, 9.8, 0.55, "AI Visibility Action Engine", 20, False, RGBColor(207, 250, 254))
rect(slide, 9.85, 1.35, 2.55, 3.55, RGBColor(28, 51, 92), True)
for i, (name, value, col) in enumerate([("TRACK", "4 engines", TEAL), ("ACT", "3 fixes", CORAL), ("GROW", "1 loop", AMBER)]):
    y = 1.85 + i * 1.05
    text(slide, 10.15, y, 1.95, 0.24, name, 9, True, col)
    text(slide, 10.15, y + 0.28, 1.95, 0.42, value, 16, True, WHITE)
text(slide, 0.75, 6.75, 7, 0.28, "Product Strategy & 12-month Monetization Roadmap", 11, False, RGBColor(203,213,225))
footer(slide, 1)
notes(slide, "Open with the strategic shift: GEO is moving brands from SEO reporting to answer-level execution. Position the feature as a closed loop, not another dashboard.")

# 2
slide = base_slide("State of AI search", "The search journey is becoming an answer journey", 2,
                   "Source: Pew Research Center, July 22, 2025, Google AI Overviews click study")
text(slide, 0.65, 1.5, 3.2, 0.75, "Traditional search", 14, True, NAVY)
rect(slide, 0.65, 2.35, 2.7, 1.05, LIGHT, True)
text(slide, 0.85, 2.58, 2.3, 0.5, "Query → 10 links", 18, True, INK)
text(slide, 4.15, 1.5, 3.2, 0.75, "AI-generated answer", 14, True, NAVY)
rect(slide, 4.15, 2.35, 2.7, 1.05, RGBColor(224, 242, 241), True)
text(slide, 4.35, 2.58, 2.3, 0.5, "Question → answer", 18, True, INK)
text(slide, 7.7, 1.5, 4.6, 0.75, "The brand blind spot", 14, True, NAVY)
rect(slide, 7.7, 2.35, 4.7, 2.15, RGBColor(255, 247, 237), True)
text(slide, 8.0, 2.65, 4.1, 0.38, "Which prompts trigger you?", 16, True, INK)
text(slide, 8.0, 3.12, 4.1, 0.38, "What sources shape the answer?", 16, True, INK)
text(slide, 8.0, 3.59, 4.1, 0.38, "Which competitor gets cited?", 16, True, INK)
text(slide, 0.65, 4.95, 12.0, 0.55, "8%  traditional result clicks with AI summary", 20, True, CORAL)
text(slide, 0.65, 5.45, 12.0, 0.45, "vs 15% when no AI summary appeared", 16, False, MUTED)
text(slide, 0.65, 6.05, 12.0, 0.45, "1% clicked an in-summary source  |  26% abandoned browsing", 14, True, INK)
notes(slide, "Use one statistic block only. Pew observed 900 US adults in March 2025. Traditional result CTR was 8% on AI-summary visits vs 15% without one; in-summary source clicks were 1%. This supports urgency, not universal market size.")

# 3
slide = base_slide("Users", "Three buyers, one shared failure: no answer-level insight", 3)
personas = [
    ("CMO", "Owns category perception", ["Explain share of voice", "Defend brand narrative", "Tie visibility to pipeline"]),
    ("SEO lead", "Owns discoverability", ["Find citation gaps", "Repair technical blockers", "Win answer inclusion"]),
    ("Brand manager", "Owns reputation", ["Catch sentiment shifts", "Protect factual claims", "Activate PR priorities"]),
]
for i, (role, sub, pains) in enumerate(personas):
    x = 0.65 + i * 4.15
    rect(slide, x, 1.55, 3.75, 4.65, LIGHT, True)
    rect(slide, x, 1.55, 3.75, 0.12, [TEAL, CORAL, AMBER][i])
    text(slide, x + 0.25, 1.95, 3.25, 0.42, role, 22, True, NAVY)
    text(slide, x + 0.25, 2.38, 3.25, 0.38, sub, 12, False, MUTED)
    for j, pain in enumerate(pains):
        rect(slide, x + 0.25, 3.05 + j * 0.82, 0.42, 0.42, [TEAL, CORAL, AMBER][i], True)
        text(slide, x + 0.82, 3.04 + j * 0.82, 2.55, 0.44, pain, 13, True, INK)
notes(slide, "The CMO buys business interpretation, the SEO lead buys implementation, and the brand manager buys narrative control. Our interface must serve all three with the same evidence graph.")

# 4
slide = base_slide("Feature", "AI Visibility Action Engine: measure → diagnose → fix", 4)
steps = [
    ("1", "Prompt-level tracking", "Share of voice\nMention rate\nSentiment\nRank position"),
    ("2", "Citation Gap Analyzer", "Cited domains\nCompetitor-only sources\nAnswer-level evidence"),
    ("3", "Prioritised action queue", "Create / update\nPR targets\nSchema fixes"),
]
for i, (n, head, body) in enumerate(steps):
    x = 0.65 + i * 4.15
    rect(slide, x, 1.55, 3.75, 3.85, LIGHT, True)
    rect(slide, x, 1.55, 0.62, 0.62, [TEAL, CORAL, AMBER][i], True)
    text(slide, x, 1.64, 0.62, 0.38, n, 16, True, WHITE, PP_ALIGN.CENTER)
    text(slide, x + 0.82, 1.7, 2.7, 0.38, head, 16, True, NAVY)
    text(slide, x + 0.25, 2.55, 3.25, 1.8, body, 15, False, INK)
    rect(slide, x + 0.25, 4.72, 3.25, 0.42, [RGBColor(204,251,241), RGBColor(255,237,213), RGBColor(254,243,199)][i], True)
    text(slide, x + 0.25, 4.72, 3.25, 0.42, ["Every prompt", "Every answer", "Impact × effort"][i], 11, True, INK, PP_ALIGN.CENTER)
rect(slide, 0.65, 5.72, 12.05, 0.55, NAVY, True)
text(slide, 0.65, 5.72, 12.05, 0.55, "Re-measure after action to close the loop", 16, True, WHITE, PP_ALIGN.CENTER)
notes(slide, "This is the product thesis: tracking alone produces another report. The engine converts answer-level evidence into a ranked implementation queue, then measures the change.")

# 5
slide = base_slide("User flow", "One dashboard turns monitoring into a next action", 5)
text(slide, 0.65, 1.38, 12, 0.34, "Prompt set: “best CRM for enterprise”  •  Market: US  •  Engines: 4", 12, True, MUTED)
rect(slide, 0.65, 1.85, 12.05, 4.65, NAVY, True)
rect(slide, 0.9, 2.1, 2.05, 4.15, RGBColor(28,51,92), True)
text(slide, 1.12, 2.34, 1.6, 0.32, "OVERVIEW", 10, True, TEAL)
for i, lab in enumerate(["Visibility", "Prompts", "Citations", "Actions"]):
    text(slide, 1.12, 2.82 + i*0.65, 1.6, 0.32, lab, 12, True, WHITE if i == 0 else RGBColor(203,213,225))
rect(slide, 3.15, 2.1, 3.0, 1.55, WHITE, True)
text(slide, 3.38, 2.32, 2.55, 0.3, "SHARE OF VOICE", 9, True, MUTED)
text(slide, 3.38, 2.72, 2.55, 0.56, "18%", 26, True, CORAL)
text(slide, 5.85, 2.1, 3.0, 1.55, "", 1)
rect(slide, 6.35, 2.1, 3.0, 1.55, WHITE, True)
text(slide, 6.58, 2.32, 2.55, 0.3, "MENTION RATE", 9, True, MUTED)
text(slide, 6.58, 2.72, 2.55, 0.56, "43%", 26, True, TEAL)
rect(slide, 9.55, 2.1, 2.85, 1.55, WHITE, True)
text(slide, 9.78, 2.32, 2.38, 0.3, "SENTIMENT", 9, True, MUTED)
text(slide, 9.78, 2.72, 2.38, 0.56, "+8 pts", 26, True, GREEN)
rect(slide, 3.15, 3.85, 9.25, 2.4, WHITE, True)
text(slide, 3.38, 4.05, 3.2, 0.32, "TOP ACTIONS", 9, True, MUTED)
actions = [("1", "Create: comparison guide", "Impact 9  Effort 4"), ("2", "Target: G2 + Gartner", "Impact 8  Effort 6"), ("3", "Add FAQ schema", "Impact 6  Effort 2")]
for i, (n, a, m) in enumerate(actions):
    y = 4.5 + i*0.52
    rect(slide, 3.38, y, 0.38, 0.38, [CORAL, AMBER, TEAL][i], True)
    text(slide, 3.38, y, 0.38, 0.38, n, 10, True, WHITE, PP_ALIGN.CENTER)
    text(slide, 3.95, y-0.02, 4.6, 0.38, a, 12, True, INK)
    text(slide, 9.25, y-0.02, 2.65, 0.38, m, 11, True, MUTED, PP_ALIGN.RIGHT)
notes(slide, "Walk through the wireframe: select prompts and market, view answer-level metrics, inspect citation gaps, then execute the highest-impact action. Key metrics are share of voice, mention rate, sentiment, rank, and source gap.")

# 6
slide = base_slide("Requirements", "Ship a narrow MVP, isolate the volatility", 6)
cols = [("MVP", TEAL), ("Later", AMBER)]
for i, (head, col) in enumerate(cols):
    x = 0.65 + i*4.55
    rect(slide, x, 1.55, 4.15, 3.2, LIGHT, True)
    rect(slide, x, 1.55, 4.15, 0.12, col)
    text(slide, x+0.25, 1.92, 3.65, 0.38, head, 18, True, NAVY)
    items = (
        ["US / EN", "4 engines", "Prompt tracking", "Citation gap", "Ranked fixes", "CSV export"]
        if i == 0 else
        ["20+ markets", "All languages", "Agent/API", "Auto publishing", "SSO / governance", "Custom models"]
    )
    for j, item in enumerate(items):
        text(slide, x+0.25, 2.55+j*0.35, 3.65, 0.28, "• " + item, 12, False, INK)
rect(slide, 9.75, 1.55, 2.95, 3.2, RGBColor(255,247,237), True)
text(slide, 10.0, 1.92, 2.45, 0.38, "Sampling policy", 18, True, NAVY)
text(slide, 10.0, 2.55, 2.45, 1.75, "• Repeat 3× per prompt\n• 24h confidence band\n• Geo + locale locked\n• Versioned query batches", 12, False, INK)
rect(slide, 0.65, 5.05, 12.05, 1.08, NAVY, True)
text(slide, 0.9, 5.28, 11.55, 0.42, "Edge cases: answer variance · geo/language drift · API outages · source disagreement", 14, True, WHITE, PP_ALIGN.CENTER)
notes(slide, "The MVP proves the loop in English and one market. Sampling repeats answers to separate real movement from model variance. Store locale, engine, timestamp, prompt version, and source set for every observation.")

# 7 competitor comparison
slide = base_slide("Market", "The category is converging on tracking; action is fragmented", 7,
                   "Sources: vendor sites/product pages; pricing/features marked (verify) where unconfirmed")
headers = ["Tool", "LLM coverage", "Prompt", "Citations", "Actions", "Pricing / segment"]
rows = [
    ["Profound", "Broad", "Yes", "Yes", "Limited", "Enterprise (verify)"],
    ["Peec AI", "Broad", "Yes", "Yes", "Recommendations", "From $95/mo; SMB–mid-market"],
    ["Otterly.AI", "Major engines", "Yes", "Yes", "Limited", "Subscription (verify)"],
    ["AthenaHQ", "Very broad", "Yes", "Yes", "Content agent", "Free + from $295/mo"],
    ["Semrush AI Toolkit", "Major engines", "Yes", "Yes", "AI recommendations", "Semrush tiers"],
    ["Ahrefs Brand Radar", "AI search", "Yes", "Yes", "SEO-led", "Ahrefs segments (verify)"],
    ["Rankscale", "Major engines", "Yes", "Yes", "Limited", "Free trial + paid (verify)"],
]
table = slide.shapes.add_table(len(rows)+1, len(headers), Inches(0.55), Inches(1.55),
                               Inches(12.15), Inches(4.95)).table
table.columns[0].width = Inches(1.65)
for j, h in enumerate(headers):
    cell = table.cell(0,j); cell.text=h
    cell.fill.solid(); cell.fill.fore_color.rgb=NAVY
for i,row in enumerate(rows, start=1):
    for j,val in enumerate(row):
        cell=table.cell(i,j); cell.text=val
        cell.fill.solid(); cell.fill.fore_color.rgb=WHITE if i%2 else LIGHT
for row in table.rows:
    for cell in row.cells:
        cell.margin_left=Inches(0.06); cell.margin_right=Inches(0.06)
        for p in cell.text_frame.paragraphs:
            p.font.name="Aptos"; p.font.size=Pt(9)
            p.font.color.rgb=INK
            p.alignment=PP_ALIGN.LEFT
text(slide, 0.55, 6.62, 12.0, 0.28, "Pattern: strong tracking; uneven closed-loop execution and transparent pricing.", 12, True, CORAL)
notes(slide, "Comparison is a directional market scan, not a procurement-grade audit. Vendor capabilities and pricing change quickly. Verify before a customer-facing claim. Included at least Profound, Peec AI, Otterly.AI, AthenaHQ, Semrush AI Toolkit, Ahrefs Brand Radar, and Rankscale.")

# 8
slide = base_slide("Positioning", "Win on the closed loop—not more charts", 8)
nodes = [("MEASURE", TEAL), ("DIAGNOSE", CORAL), ("ACT", AMBER), ("RE-MEASURE", GREEN)]
for i,(lab,col) in enumerate(nodes):
    x=0.8+i*3.12
    rect(slide,x,2.15,2.25,1.25,col,True)
    text(slide,x,2.15,2.25,1.25,lab,16,True,WHITE,PP_ALIGN.CENTER)
    if i<3:
        text(slide,x+2.35,2.55,0.65,0.38,"→",22,True,MUTED,PP_ALIGN.CENTER)
text(slide, 1.05, 4.05, 11.1, 0.52, "Citation-gap evidence  ×  impact/effort prioritisation  ×  before/after proof", 18, True, NAVY, PP_ALIGN.CENTER)
rect(slide, 2.55, 5.05, 8.2, 0.75, RGBColor(224,242,241), True)
text(slide, 2.55, 5.05, 8.2, 0.75, "Differentiation: source-to-action-to-source", 18, True,NAVY,PP_ALIGN.CENTER)
notes(slide, "Position against measurement-first tools. GEO should not merely tell a brand that visibility moved. It should show which cited competitors caused the gap, recommend the smallest effective fix, and re-run the same prompt set.")

# 9
slide = base_slide("Success", "North Star: attributable answer visibility lifted", 9)
rect(slide,0.65,1.55,3.25,4.65,NAVY,True)
text(slide,0.95,1.95,2.65,0.38,"NORTH STAR",10,True,TEAL)
text(slide,0.95,2.55,2.65,1.15,"Lift in\nShare of Voice",26,True,WHITE)
text(slide,0.95,4.15,2.65,0.44,"on actioned prompts",12,False,RGBColor(203,213,225))
for i,(h,b) in enumerate([("Input","Prompt coverage · engine uptime"),("Quality","Source confirmation · sample confidence"),("Action","Fixes shipped · time to first fix"),("Outcome","SOV lift · positive sentiment · pipeline")]):
    x=4.25+(i%2)*4.15; y=1.55+(i//2)*2.18
    rect(slide,x,y,3.75,1.78,LIGHT,True)
    text(slide,x+0.25,y+0.25,3.25,0.32,h.upper(),9,True,[TEAL,CORAL,AMBER,GREEN][i])
    text(slide,x+0.25,y+0.72,3.25,0.62,b,13,True,INK)
notes(slide,"Measure activation from prompt coverage, answer confidence, and action completion. Use holdout prompts and stable prompts for causal evidence. Outcome is share-of-voice lift plus positive-sentiment and commercial proxy metrics.")

# 10
slide = base_slide("Roadmap — 3 months", "One motion per month: prove, package, monetize", 10)
months=[
("MONTH 1","Validate","Top 100 prompts\n4 engines\nBaseline + proof"),
("MONTH 2","Activate","Citation gaps\nRanked fixes\nPilot 10 brands"),
("MONTH 3","Monetize","Starter/Growth pilot\nFree audit funnel\nUsage reporting"),
]
for i,(m,h,b) in enumerate(months):
    x=0.65+i*4.15
    rect(slide,x,1.65,3.75,3.95,LIGHT,True)
    rect(slide,x,1.65,3.75,0.62,[TEAL,CORAL,AMBER][i])
    text(slide,x,1.65,3.75,0.62,m,11,True,WHITE,PP_ALIGN.CENTER)
    text(slide,x+0.25,2.55,3.25,0.42,h,20,True,NAVY)
    text(slide,x+0.25,3.25,3.25,1.45,b,14,False,INK)
rect(slide,0.65,5.95,12.05,0.48,NAVY,True)
text(slide,0.65,5.95,12.05,0.48,"Monetization experiments: free audit → claimable report → paid 30-day pilot",13,True,WHITE,PP_ALIGN.CENTER)
notes(slide,"Month 1 establishes a credible measurement baseline. Month 2 proves action utility through one pilot cohort. Month 3 runs a pricing experiment and uses the free audit as lead generation.")

# 11
slide = base_slide("Roadmap — 12 months", "Expand the loop beyond a dashboard", 11)
quarters=[
("Q1","Core","4 engines\nCitations\nAction queue"),
("Q2","Coverage","Multi-market\nLanguages\nIntegrations"),
("Q3","Agent/API","Brief-to-fix\nCMS + PR\nWebhook/API"),
("Q4","Enterprise","SSO/RBAC\nAudit trails\nSLA / support"),
]
for i,(q,h,b) in enumerate(quarters):
    x=0.65+i*3.05
    rect(slide,x,1.65,2.75,4.15,LIGHT,True)
    text(slide,x+0.25,1.95,2.25,0.32,q,11,True,[TEAL,CORAL,AMBER,GREEN][i])
    text(slide,x+0.25,2.55,2.25,0.42,h,18,True,NAVY)
    text(slide,x+0.25,3.25,2.25,1.45,b,13,False,INK)
text(slide,0.65,6.25,12.05,0.32,"Platform expansion: engines + channels + markets → governed action + measurable outcomes",13,True,CORAL)
notes(slide,"Sequence platform breadth behind one reliable action loop. Q1 proves the core. Q2 adds regional and multilingual coverage. Q3 enables execution through APIs and agents. Q4 supports enterprise governance.")

# 12
slide = base_slide("Monetization", "Price on value units, meter carefully", 12)
tiers=[
("Starter","50 prompts","2 engines","1 seat","$290/mo"),
("Growth","250 prompts","6 engines","5 seats","$890/mo"),
("Enterprise","Custom","Custom markets","SSO / SLA","Custom"),
]
for i,(name,prompts,eng,seats,price) in enumerate(tiers):
    x=0.65+i*4.15
    rect(slide,x,1.55,3.75,3.55,[RGBColor(240,253,250),LIGHT,RGBColor(255,247,237)][i],True)
    text(slide,x+0.25,1.82,3.25,0.38,name,18,True,NAVY)
    text(slide,x+0.25,2.45,3.25,1.15,prompts+"\n"+eng+"\n"+seats,13,True,INK)
    text(slide,x+0.25,4.25,3.25,0.42,price,18,True,[TEAL,CORAL,AMBER][i])
rect(slide,0.65,5.38,12.05,0.78,NAVY,True)
text(slide,0.85,5.38,11.65,0.78,"Add-ons: extra markets · branded reports · API runs · done-for-you optimization",13,True,WHITE,PP_ALIGN.CENTER)
text(slide,0.65,6.43,12.05,0.35,"Unit logic: (answer calls + retries × API cost) + margin guardrail → prompt/engine packs",11,True,MUTED)
notes(slide,"Starter validates the category. Growth is the expansion tier. Enterprise is driven by governance, global markets, API usage, and SLA. Keep a gross-margin guardrail and meter repeated answers rather than one-shot query volume.")

# 13
slide = base_slide("Risks & ask", "Move fast where we control the loop", 13)
risks=[
("API cost","Cache + sample + rerun only on change","Cost / prompt"),
("Platform volatility","Engine adapters + answer provenance","Data freshness"),
("Data access","Export + API + human-confirmed sources","Coverage"),
]
for i,(risk,mit,metric) in enumerate(risks):
    y=1.55+i*1.05
    rect(slide,0.65,y,12.05,0.82,LIGHT,True)
    text(slide,0.9,y,2.2,0.82,risk,14,True,[CORAL,AMBER,TEAL][i])
    text(slide,3.15,y,6.35,0.82,mit,13,False,INK)
    text(slide,9.75,y,2.65,0.82,metric,11,True,MUTED,PP_ALIGN.RIGHT)
rect(slide,0.65,5.05,12.05,1.08,NAVY,True)
text(slide,0.65,5.05,12.05,0.52,"ASK",10,True,TEAL,PP_ALIGN.CENTER)
text(slide,0.65,5.45,12.05,0.48,"Approve 10-brand pilot + 3-month build",20,True,WHITE,PP_ALIGN.CENTER)
notes(slide,"Close with the ask: approve a ten-brand, one-market pilot. Gate expansion on action completion and share-of-voice lift. Keep API cost and sampling metrics visible from day one.")

prs.save(OUT)
print(OUT)
