import sys, re, markdown
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon

# 完整 markdown 显示窗口
class Markdown(QWidget):
    def __init__(self, mode='plaintext'):
        super().__init__()
        self.mode = mode
        self.markdown = ''
        self.path = ''

        # 设置主窗口属性
        self.resize(1100, 800)
        self.setWindowTitle('Markdown Display')
        self.setWindowIcon(QIcon('images/icons/markdown.svg'))

        self.text_edit = QTextEdit()

        self.mode_button = QPushButton('Mode', self)
        self.mode_button.clicked.connect(self.mode_switch)
        self.confirm_button = QPushButton("Confirm")
        # self.confirm_button.clicked.connect(self.save_markdown)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.mode_button)
        bottom_layout.addWidget(self.confirm_button)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addLayout(bottom_layout)

        # self.markdown_showfile('README.md')  # test
        self.setLayout(layout)


    # 显示 markdown
    def markdown_show(self, markdown, path):
        self.markdown = markdown
        self.path = path
        self.text_edit.setPlainText(self.markdown)
        self.show()

    def markdown_showfile(self, file):
        # 读取文件内容
        with open(file, 'r', encoding='utf-8') as f:
            self.markdown = f.read()
        # 将内容设置到文本编辑器中
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(self.markdown)

    def mode_switch(self):
        if self.mode == 'plaintext':
            self.mode = 'html'
            # html = markdown.markdown(self.markdown)
            html = self.markdown_to_html(self.markdown)
            self.text_edit.setHtml(html)

        elif self.mode == 'html':
            self.mode = 'plaintext'
            self.text_edit.setPlainText(self.markdown)

    def markdown_to_html(self, md_text):
        html_lines = []
        # 正则表达式用于检测简单的 HTML 标签
        html_tag_pattern = re.compile(r'<[^>]+>')
        # 处理每一行
        for line in md_text.splitlines():
            # 如果检测到 HTML 标签，直接保留
            if html_tag_pattern.search(line):
                html_lines.append(line)
                continue
            # 标题
            if line.startswith('#'):
                header_level = line.count('#', 0, line.find(' '))
                line_content = line.strip('# ').strip()
                html_lines.append(f"<h{header_level}>{line_content}</h{header_level}>")
            # # 处理代码块
            # if line.startswith('```'):
            #     if html_lines and html_lines[-1].startswith('<pre><code>'):
            #         # 结束代码块
            #         html_lines.append('</code></pre>')
            #     else:
            #         # 开始代码块
            #         html_lines.append('<pre><code>')
            #     continue
            # 无序列表
            elif line.startswith('- '):
                html_lines.append(f"<ul><li>{line[2:].strip()}</li></ul>")
            # 加粗 **text**
            elif '**' in line:
                line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                html_lines.append(f"<p>{line}</p>")
            # 斜体 *text*
            elif '*' in line:
                line = line.replace('*', '<em>', 1).replace('*', '</em>', 1)
                html_lines.append(f"<p>{line}</p>")
            # 链接 [text](url)
            elif '[' in line and ']' in line and '(' in line and ')' in line:
                start_text = line.find('[')
                end_text = line.find(']', start_text)
                start_url = line.find('(', end_text)
                end_url = line.find(')', start_url)
                text = line[start_text+1:end_text]
                url = line[start_url+1:end_url]
                html_lines.append(f'<a href="{url}">{text}</a>')
            # 普通段落
            else:
                if line.strip():
                    html_lines.append(f"<p>{line.strip()}</p>")

        # 将 HTML 行组合
        return "\n".join(html_lines)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Markdown()
    window.show()
    sys.exit(app.exec_())
