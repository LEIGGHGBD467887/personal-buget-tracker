#!/usr/bin/env python3
"""
Convert Markdown thesis to PDF
"""
import markdown2
import os
from pathlib import Path

def convert_markdown_to_pdf():
    """Convert COMPLETE_THESIS_REPORT.md to PDF"""
    
    # Read the markdown file
    md_file = Path("COMPLETE_THESIS_REPORT.md")
    
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return False
    
    try:
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks', 'toc'])
        
        # Create a complete HTML document with styling
        full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Budget Tracker - Thesis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 28px;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 25px;
            margin-bottom: 12px;
            font-size: 22px;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }}
        
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 18px;
        }}
        
        h4, h5, h6 {{
            color: #95a5a6;
            margin-top: 15px;
            margin-bottom: 8px;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        ul, ol {{
            margin-left: 30px;
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }}
        
        table th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        
        table td {{
            border: 1px solid #ddd;
            padding: 10px;
        }}
        
        table tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        table tr:hover {{
            background-color: #f0f0f0;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}
        
        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            color: #ecf0f1;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-left: 0;
            margin-bottom: 15px;
            color: #7f8c8d;
            font-style: italic;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        
        strong {{
            color: #2c3e50;
            font-weight: bold;
        }}
        
        em {{
            font-style: italic;
            color: #34495e;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        .page-break {{
            page-break-after: always;
        }}
        
        @media print {{
            body {{
                background-color: white;
                padding: 0;
            }}
            
            .container {{
                max-width: 100%;
                box-shadow: none;
                padding: 0;
            }}
            
            h1 {{
                page-break-before: always;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>
"""
        
        # Save HTML file
        html_file = Path("COMPLETE_THESIS_REPORT.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"[OK] HTML file created: {html_file}")
        
        # Try to convert HTML to PDF using pdfkit
        try:
            import pdfkit
            pdf_file = Path("COMPLETE_THESIS_REPORT.pdf")
            
            # Check if wkhtmltopdf is installed
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None,
            }
            
            pdfkit.from_file(str(html_file), str(pdf_file), options=options)
            print(f"[OK] PDF file created: {pdf_file}")
            return True
            
        except Exception as e:
            print(f"[NOTE] pdfkit requires wkhtmltopdf. {str(e)}")
            print(f"[OK] HTML file is ready: {html_file}")
            print("  You can open this HTML file in a browser and print to PDF")
            return True
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = convert_markdown_to_pdf()
    if success:
        print("\n[SUCCESS] Conversion completed successfully!")
    else:
        print("\n[FAILED] Conversion failed!")
