from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf_report(filename, score, matched, missing, recommendations):
    os.makedirs("generated_reports", exist_ok=True)

    path = f"generated_reports/{filename}.pdf"

    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("ResumeIQ Analysis Report", styles["Title"]))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"Resume Score: {score}%", styles["Heading2"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Matched Skills:", styles["Heading3"]))
    for item in matched:
        content.append(Paragraph(f"- {item}", styles["BodyText"]))

    content.append(Spacer(1, 12))

    content.append(Paragraph("Missing Skills:", styles["Heading3"]))
    for item in missing:
        content.append(Paragraph(f"- {item}", styles["BodyText"]))

    content.append(Spacer(1, 12))

    content.append(Paragraph("Recommendations:", styles["Heading3"]))
    for item in recommendations:
        content.append(Paragraph(f"- {item}", styles["BodyText"]))

    doc.build(content)

    return path