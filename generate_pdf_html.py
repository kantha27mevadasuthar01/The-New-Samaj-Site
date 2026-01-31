import markdown
import re

# Read the Markdown file
with open('Project Documentation.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Convert Mermaid blocks to <div class="mermaid"> for the JS library to find
# Regex looks for ```mermaid ... ``` blocks
pattern = r'```mermaid\n(.*?)```'
text = re.sub(pattern, r'<div class="mermaid">\1</div>', text, flags=re.DOTALL)

# Convert the rest of Markdown to HTML
html_content = markdown.markdown(text, extensions=['tables', 'fenced_code'])

# Create the final HTML with valid structure, CSS, and Mermaid JS
final_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Documentation</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css">
    <style>
        body {{
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }}
        @media (max-width: 767px) {{
            body {{
                padding: 15px;
            }}
        }}
        .markdown-body {{
            background-color: white; /* Ensure white bg for printing */
        }}
        /* Print optimizations */
        @media print {{
            body {{
                max-width: 100%;
                padding: 0;
            }}
        }}
    </style>
</head>
<body class="markdown-body">
    {html_content}

    <!-- Mermaid JS -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</body>
</html>
"""

# Write to output file
with open('documentation_printable.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Successfully created documentation_printable.html")
