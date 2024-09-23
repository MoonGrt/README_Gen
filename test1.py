import markdown

# Define your markdown text
md_text = """
<!-- FILE TREE -->
## File Tree

```
└─ Project
  ├─ LICENSE
  ├─ README.md
  ├─ README_Gen.py
  ├─ requirements.txt
  ├─ run.bat
  ├─ temple_blank_cn.md
  ├─ temple_blank_en.md
  ├─ temple_cn.md
  ├─ temple_en.md
  ├─ /icons/
  └─ /images/

```
"""

# Convert Markdown to HTML
html_output = markdown.markdown(md_text)

# Display the HTML
print(html_output)
