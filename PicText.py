import sys, os, html2text, markdown, re
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QImage, QTextCursor, QTextBlockFormat
from PyQt5.QtCore import Qt, QUrl

class ImageTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 禁用拖放功能
        self.setAcceptDrops(False)
        # 启用拖放功能
        # self.setAcceptDrops(True)


    def dragEnterEvent(self, event):
        # 检查是否拖入的是文件，且文件为图片格式
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if all(url.isLocalFile() and os.path.splitext(url.toLocalFile())[1].lower() in ('.jpg', '.png', '.bmp') for url in urls):
                event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        # 当文件放下时，插入图片
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                image_path = url.toLocalFile()
                image = QImage(image_path)
                
                if image.isNull():
                    continue  # 无法加载图像时跳过

                # 获取光标并插入图片
                cursor = self.textCursor()
                # 设置段落居中
                block_format = QTextBlockFormat()
                block_format.setAlignment(Qt.AlignCenter)
                cursor.insertBlock(block_format)
                # 插入图片
                cursor.insertImage(image, image_path)
            
            event.acceptProposedAction()
        else:
            super().dropEvent(event)


class PicText(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 600)
        self.setWindowTitle('Piture Text Editor')
        self.setWindowIcon(QIcon('images/icons/markdown.svg'))

        # 创建菜单栏
        menubar = self.menuBar()
        # 创建文件菜单
        file_menu = menubar.addMenu('File')

        # 添加插入图片选项
        insert_image_action = QAction(QIcon(), 'Insert Image', self)
        insert_image_action.triggered.connect(self.insert_image)
        file_menu.addAction(insert_image_action)

        # 使用自定义的 ImageTextEdit 作为文本编辑器
        self.text_edit = ImageTextEdit(self)

        # 添加提交按钮
        self.gen_button = QPushButton("Gen", self)
        # self.gen_button.clicked.connect(self.test)

        # 添加按钮布局
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.gen_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def insert_image(self):
        # 打开文件对话框选择图片
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Image files (*.jpg *.png *.bmp)')
        if image_path:
            image = QImage(image_path)

            if image.isNull():
                return  # 如果无法加载图像，则返回
            else:
                # 获取当前光标并插入图片
                cursor = self.text_edit.textCursor()
                # 创建一个新的 QTextBlockFormat 对象
                block_format = QTextBlockFormat()
                # 设置段落居中对齐
                block_format.setAlignment(Qt.AlignCenter)
                # 应用居中对齐格式到当前段落
                cursor.insertBlock(block_format)
                # 插入图片
                cursor.insertImage(image, image_path)
                # 插入图片后，移动光标到下一行
                cursor.movePosition(QTextCursor.End)
                cursor.insertBlock()
                # 清除居中对齐，使新段落恢复默认的左对齐
                block_format.setAlignment(Qt.AlignLeft)
                cursor.setBlockFormat(block_format)
                # 更新文本编辑器的光标
                self.text_edit.setTextCursor(cursor)

    def get_text(self):
        html = self.text_edit.toHtml()
        markdown_content = html2text.html2text(html)
        return markdown_content

    def test(self):
        html = self.text_edit.toHtml()
        markdown_content = html2text.html2text(html)
        html_content = markdown.markdown(markdown_content)
        print(html)
        print('-----------------------------------------------------------------')
        print(markdown_content)
        # markdown_content = self.center_images_in_markdown(markdown_content)
        # print(markdown_content)
        print('-----------------------------------------------------------------')
        print(html_content)
        self.text_edit.setHtml(html_content)

    def center_images_in_markdown(self, markdown_text):
        # 定义正则表达式，匹配 Markdown 图片格式 ![alt text](image_url)
        img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        
        # 替换为居中的 HTML 格式
        def replace_with_centered_html(match):
            alt_text = match.group(1)
            img_url = match.group(2)
            # 用HTML div 和 img标签将图片居中
            return f'<div style="text-align:center;"><img src="{img_url}" alt="{alt_text}" /></div>'
        
        # 使用正则表达式进行替换
        centered_markdown = re.sub(img_pattern, replace_with_centered_html, markdown_text)
        
        return centered_markdown


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = PicText()
    editor.show()
    # editor.closeEvent = editor.get_text
    sys.exit(app.exec_())
