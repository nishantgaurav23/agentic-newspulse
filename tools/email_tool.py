"""
Email dispatch tool for sending reports to users
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List

from config import settings
from models.schemas import NewsReport, Article


def format_report_html(report: NewsReport) -> str:
    """
    Format a NewsReport as HTML email

    Args:
        report: NewsReport object to format

    Returns:
        HTML string for email body
    """
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .summary {{
                background: #f8f9fa;
                padding: 20px;
                border-left: 4px solid #667eea;
                margin-bottom: 30px;
                border-radius: 5px;
            }}
            .article {{
                margin-bottom: 30px;
                padding: 20px;
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .article h2 {{
                color: #667eea;
                margin-top: 0;
            }}
            .priority {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .priority-critical {{
                background: #dc3545;
                color: white;
            }}
            .priority-high {{
                background: #fd7e14;
                color: white;
            }}
            .priority-medium {{
                background: #ffc107;
                color: #333;
            }}
            .priority-low {{
                background: #6c757d;
                color: white;
            }}
            .insights {{
                margin: 15px 0;
            }}
            .insights li {{
                margin: 8px 0;
            }}
            .citations {{
                margin-top: 15px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 5px;
                font-size: 14px;
            }}
            .citation {{
                margin: 10px 0;
                padding: 10px;
                background: white;
                border-left: 3px solid #667eea;
            }}
            .footer {{
                margin-top: 40px;
                padding: 20px;
                background: #f8f9fa;
                text-align: center;
                border-radius: 5px;
                color: #6c757d;
                font-size: 14px;
            }}
            a {{
                color: #667eea;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📰 NewsPulse AI Report</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">
                {report.report_date.strftime("%A, %B %d, %Y")}
            </p>
        </div>

        <div class="summary">
            <h2 style="margin-top: 0; color: #667eea;">Executive Summary</h2>
            <p>{report.executive_summary}</p>
            <p style="margin: 10px 0 0 0; font-size: 14px; color: #6c757d;">
                {report.total_articles} articles | Topics: {", ".join(report.topics_covered)}
            </p>
        </div>

        <div class="articles">
    """

    for article in report.articles:
        priority_class = f"priority-{article.priority.value}"

        html += f"""
        <div class="article">
            <span class="priority {priority_class}">{article.priority.value.upper()}</span>
            <h2>{article.title}</h2>
            <p><strong>Why this matters:</strong> {article.relevance_reason}</p>
            <p>{article.summary}</p>

            <div class="insights">
                <strong>Key Insights:</strong>
                <ul>
        """

        for insight in article.key_insights:
            html += f"<li>{insight}</li>"

        html += """
                </ul>
            </div>

            <div class="citations">
                <strong>Sources:</strong>
        """

        for i, citation in enumerate(article.citations, 1):
            html += f"""
                <div class="citation">
                    <strong>[{i}]</strong> {citation.claim}<br>
                    <em>"{citation.quote}"</em><br>
                    <a href="{citation.source_url}" target="_blank">{citation.source_title}</a>
                </div>
            """

        html += f"""
            </div>
            <p style="margin-top: 15px;">
                <a href="{article.url}" target="_blank">Read Full Article →</a>
            </p>
        </div>
        """

    html += f"""
        </div>

        <div class="footer">
            <p>
                <strong>Generated by NewsPulse AI</strong><br>
                Powered by Google ADK & Gemini 2.5 Flash<br>
                Report ID: {report.report_id}
            </p>
            <p style="margin-top: 15px;">
                <a href="#">Rate this report</a> | <a href="#">Update preferences</a>
            </p>
        </div>
    </body>
    </html>
    """

    return html


def send_email_report(
    report: NewsReport,
    recipient_email: str,
    cc_emails: Optional[List[str]] = None,
    bcc_emails: Optional[List[str]] = None,
    subject: Optional[str] = None,
) -> bool:
    """
    Send a news report via email with support for CC and BCC

    Args:
        report: NewsReport object to send
        recipient_email: Primary recipient email address
        cc_emails: Optional list of CC recipients
        bcc_emails: Optional list of BCC recipients
        subject: Optional custom subject line

    Returns:
        True if sent successfully, False otherwise
    """
    if subject is None:
        subject = f"📰 Your NewsPulse AI Report - {report.report_date.strftime('%B %d, %Y')}"

    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.smtp_username
    msg["To"] = recipient_email

    # Add CC recipients if provided
    if cc_emails and len(cc_emails) > 0:
        msg["Cc"] = ", ".join(cc_emails)

    # BCC is not added to headers (that's the point of BCC)
    # But we need to include them in the recipient list for SMTP

    # Generate HTML content
    html_content = format_report_html(report)

    # Attach HTML
    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    try:
        # Build complete recipient list (To + CC + BCC)
        all_recipients = [recipient_email]
        if cc_emails:
            all_recipients.extend(cc_emails)
        if bcc_emails:
            all_recipients.extend(bcc_emails)

        # Connect to SMTP server
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            # Send to all recipients (To, CC, and BCC)
            server.sendmail(
                from_addr=settings.smtp_username,
                to_addrs=all_recipients,
                msg=msg.as_string()
            )

        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
