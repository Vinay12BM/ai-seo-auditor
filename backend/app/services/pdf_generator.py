# backend/app/services/pdf_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

def generate_seo_pdf(report_data: dict) -> bytes:
    """
    Generates a professional PDF report from the Gemini SEO analysis JSON.
    Returns the PDF content as bytes.
    """
    # Use BytesIO to create an in-memory file for the PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                            leftMargin=72, rightMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    Story = []

    # --- Custom Styles ---
    styles.add(ParagraphStyle(name='TitleStyle', fontSize=24, spaceAfter=20, alignment=1, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='Heading2', fontSize=16, spaceBefore=12, spaceAfter=6, fontName='Helvetica-Bold', leftIndent=0))
    styles.add(ParagraphStyle(name='Normal', fontSize=10, spaceAfter=6))
    
    # --- 1. Report Header ---
    Story.append(Paragraph("AI-Powered SEO Audit Report", styles['TitleStyle']))
    Story.append(Paragraph(f"<b>Overall SEO Score: {report_data.get('overall_seo_score')}/100</b>", styles['Heading2']))
    
    score = report_data.get('overall_seo_score', 0)
    score_color = colors.green if score >= 70 else (colors.orange if score >= 50 else colors.red)
    Story.append(Paragraph(f"<b>Summary:</b> {report_data.get('summary')}", styles['Normal']))
    Story.append(Spacer(0, 12))

    # --- 2. Issues Found Table ---
    Story.append(Paragraph("🎯 High-Priority Issues & Recommended Actions", styles['Heading2']))
    
    # Define table structure (Header row + data)
    table_data = [['Category', 'Issue', 'Priority', 'Recommended Action']]
    
    for issue in report_data.get('issues_found', []):
        row_color = colors.lightcoral if issue['priority'] == 'High' else (colors.yellow if issue['priority'] == 'Medium' else colors.lightgreen)
        table_data.append([
            issue['category'], 
            issue['issue'], 
            Paragraph(f"<b>{issue['priority']}</b>", styles['Normal']), 
            issue['recommended_action']
        ])

    # Create the Table object
    col_widths = [70, 120, 50, 200]
    issue_table = Table(table_data, colWidths=col_widths)
    
    # Apply Table Style
    issue_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue), # Header Background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), # Header Text
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        # Color the priority column based on data (requires separate logic if done fully dynamically)
        # For simplicity, we bolded the text above.
    ]))
    
    Story.append(issue_table)
    Story.append(Spacer(0, 20))

    # --- 3. Technical Evaluation & Forecast ---
    Story.append(Paragraph("⚙️ Technical SEO Evaluation", styles['Heading2']))
    tech_eval = report_data.get('technical_seo_evaluation', {})
    
    tech_data = [
        ['Metric', 'Evaluation'],
        ['Site Speed', tech_eval.get('site_speed', 'N/A')],
        ['Mobile Usability', tech_eval.get('mobile_usability', 'N/A')],
        ['Structured Data', tech_eval.get('structured_data', 'N/A')]
    ]
    
    tech_table = Table(tech_data, colWidths=[120, 320])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    Story.append(tech_table)
    Story.append(Spacer(0, 12))
    
    Story.append(Paragraph("📈 Ranking Forecast", styles['Heading2']))
    Story.append(Paragraph(report_data.get('ranking_forecast', 'N/A'), styles['Normal']))
    Story.append(Spacer(0, 12))
    
    Story.append(Paragraph("💡 Keyword Strategy Suggestions", styles['Heading2']))
    keywords = ", ".join(report_data.get('keyword_strategy_suggestions', []))
    Story.append(Paragraph(keywords, styles['Normal']))

    # --- Build the PDF document ---
    doc.build(Story)
    
    # Get the value of the BytesIO buffer (the PDF content)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes