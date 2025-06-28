from weasyprint import HTML

def to_pdf(html_string: str) -> bytes:
    """Convert raw HTML string to PDF bytes."""
    return HTML(string=html_string).write_pdf()
