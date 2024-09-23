import re

html_text = '''
<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

<p align="right">(<a href="#top">back to top</a>)</p>
'''

# 使用正则表达式提取两个标记之间的内容
match = re.search(r'<!-- ABOUT THE PROJECT -->(.*?)<p align="right">', html_text, re.DOTALL)

if match:
    result = match.group(1).strip()
    print(result)
