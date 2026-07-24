import os
from dotenv import load_dotenv
from google import genai

from kpi_generator import kpis


# Load API Key

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

business_context = """
Business Context

The company is a multi-store retail chain selling products across multiple categories.

The objective of management is to:

• Increase Revenue
• Improve Profitability
• Optimize Discount Strategy
• Reduce Product Returns
• Improve Store Performance
• Increase Customer Lifetime Value

The KPIs have already been calculated using SQL and Python.
Your responsibility is to interpret them like a Senior Business Consultant.
Focus on business decisions rather than simply repeating KPI values.
"""

# prompt for generating the executive report 

prompt = f"""
You are a Senior Business Analyst working at ZS Associates.

Your task is to prepare an executive business report for the CEO based ONLY on the business KPIs below.

==========================================================
BUSINESS KPIs
==========================================================

{kpis}

==========================================================

Write a professional executive report.

The report must contain the following sections exactly in this order.

EXECUTIVE SUMMARY

Write 4-5 concise bullet points summarizing the company's overall performance.

----------------------------------------------------------

REVENUE & PROFITABILITY

Analyse

• Revenue performance
• Profit performance
• Profit margin
• Average Order Value

Explain what these indicate about the business.

----------------------------------------------------------

PRODUCT PERFORMANCE

Analyse

• Top revenue products
• Top revenue category
• Highest margin category

Mention whether revenue appears concentrated in a few products or well distributed.

Recommend inventory or merchandising actions wherever appropriate.

----------------------------------------------------------

CUSTOMER INSIGHTS

Analyse

• Top customers
• Average Order Value

Explain customer behaviour.

Suggest retention or loyalty strategies.

----------------------------------------------------------

STORE & REGIONAL PERFORMANCE

Analyse

• Top revenue stores
• Highest profit city
• Highest profit region

Identify which stores are outperforming.

Suggest how management can replicate successful practices across lower-performing stores.

----------------------------------------------------------

RETURN ANALYSIS

Analyse

• Return rate
• Return reason breakdown

Explain operational implications.

Suggest actions to reduce returns.

----------------------------------------------------------

DISCOUNT EFFECTIVENESS

Analyse the least profitable discount level.

Explain whether discounts appear to improve revenue at the expense of profitability.

Suggest pricing recommendations.

----------------------------------------------------------

STRATEGIC RECOMMENDATIONS

Provide EXACTLY FIVE recommendations.

Each recommendation should contain

Recommendation:
Business Impact:

----------------------------------------------------------

OVERALL ASSESSMENT

Write one concluding paragraph summarizing the company's business health.

==========================================================

Rules

1. Never invent numbers.
2. Use ONLY the supplied KPIs.
3. Explain WHY every KPI matters.
4. Do not simply repeat KPI values.
5. Write like a management consultant at McKinsey, BCG, Bain, Deloitte or ZS.
6. Use professional business language.
7. Do not use Markdown symbols (#, ##, **).
8. Keep the report around 600 words.
"""

# ==========================================
# Generate Report
# ==========================================

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=business_context + "\n\n" + prompt
)

report = response.text

print("\n")
print("=" * 70)
print("EXECUTIVE SALES REPORT")
print("=" * 70)
print(report)

# ==========================================
# Save as PDF
# ==========================================

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

pdf = SimpleDocTemplate("Executive_Report.pdf")

styles = getSampleStyleSheet()

story = []

story.append(Paragraph("<b><font size=18>Executive Sales Report</font></b>", styles["Title"]))
story.append(Paragraph("<br/><br/>", styles["Normal"]))

for line in report.split("\n"):
    if line.strip():
        story.append(Paragraph(line.replace("\n", "<br/>"), styles["BodyText"]))

pdf.build(story)

print("\n✅ Executive_Report.pdf generated successfully!")