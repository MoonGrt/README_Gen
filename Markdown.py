import os, shutil, sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon

# 完整 markdown 显示窗口
class Markdown(QWidget):
    def __init__(self):
        super().__init__()
        self.markdown = ''
        self.path = ''

        # 设置主窗口属性
        self.resize(1100, 800)
        self.setWindowTitle('Markdown Display')
        self.setWindowIcon(QIcon('images/icons/markdown.svg'))

        self.text_edit = QTextEdit()
        self.confirm_button = QPushButton("Confirm")
        # self.confirm_button.clicked.connect(self.save_markdown)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.confirm_button)

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
        self.text_edit.setHtml(self.markdown)
        # self.text_edit.setPlainText(self.markdown)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Markdown()
    window.show()
    sys.exit(app.exec_())
