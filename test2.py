import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget

class HtmlViewer(QWidget):
    def __init__(self):
        super().__init__()

        # 创建QTextEdit控件
        self.text_edit = QTextEdit()

        # 禁用编辑功能，让它仅用于展示HTML
        self.text_edit.setReadOnly(True)

        # 设置HTML内容
        html_content = """
<h2>File Tree</h2>
<p>```
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
  └─ /images/</p>
<p>```</p>
        """

        # 加载HTML到QTextEdit
        self.text_edit.setHtml(html_content)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        # 设置窗口标题
        self.setWindowTitle("HTML Viewer")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    viewer = HtmlViewer()
    viewer.resize(400, 300)
    viewer.show()

    sys.exit(app.exec_())
