import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QImage, QTextCursor, QTextBlockFormat
from PyQt5.QtCore import Qt

class PicText(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 禁用拖放功能
        # self.setAcceptDrops(False)
        # 启用拖放功能
        self.setAcceptDrops(True)
        self.max_height = 400  # 设置图片最大高度

    # 重写 dragEnterEvent 方法，检查是否是文件或文本拖入
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.acceptProposedAction()  # 接受拖动事件
        else:
            event.ignore()

    # 重写 dropEvent 方法，处理拖放的文件或文本
    def dropEvent(self, event):
        self.setReadOnly(True)  # 防止 调用父类的 dropEvent 方法 时，写入内容
        super().dropEvent(event)  # 调用父类的 dropEvent 方法，以确保光标能够正确更新
        self.setReadOnly(False)

        if event.mimeData().hasUrls():  # 如果拖入的是文件
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()  # 获取本地文件路径
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    # 如果是图片文件
                    self.insert_image(file_path)
                else:
                    # 如果是文本文件
                    try:
                        with open(file_path, 'r') as file:
                            content = file.read()  # 读取文件内容
                            self.append(content)  # 插入到 QTextEdit
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
            event.acceptProposedAction()
        elif event.mimeData().hasText():  # 如果拖入的是纯文本
            text = event.mimeData().text()
            self.append(text)  # 插入到 QTextEdit
            event.acceptProposedAction()
        else:
            event.ignore()

    # 插入居中图片到 QTextEdit 中
    def insert_image(self, image_path):
        image = QImage(image_path)
        if not image.isNull():
            image_height = image.height()
            if image_height > self.max_height:
                html = f'<img src="{image_path}" height="{self.max_height}" style="max-width: 100%;"/>'
            else:
                html = f'<img src="{image_path}" />'

            cursor = self.textCursor()

            # 设置块格式为居中
            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignCenter)
            # 插入图片
            cursor.insertBlock(block_format)  # 插入一个新块并应用居中格式
            # cursor.insertImage(image, image_path)
            cursor.insertHtml(html)

            # 移动光标到插入块的后面
            cursor.insertBlock()  # 插入一个新块以结束当前块
            cursor.movePosition(QTextCursor.StartOfBlock)  # 将光标移动到新块的开始
            # 清除居中对齐，使新段落恢复默认的左对齐
            block_format.setAlignment(Qt.AlignLeft)
            cursor.setBlockFormat(block_format)
            # 更新文本编辑器的光标
            self.setTextCursor(cursor)
                
        else:
            print(f"Failed to load image {image_path}")

    def set_content(self, content):
        self.setHtml(content)


class MainWindow(QMainWindow):
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
        insert_image_action = QAction(QIcon(), 'Insert', self)
        insert_image_action.triggered.connect(self.insert_image)
        file_menu.addAction(insert_image_action)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(insert_image_action)

        # 使用自定义的 PicText 作为文本编辑器
        self.text_edit = PicText(self)

        # 添加提交按钮
        self.gen_button = QPushButton("Gen", self)

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

    def test(self):
        html = self.text_edit.toHtml()
        html = html.replace("F:/Project/Python/Project/README_Gen/", '')
        html = html.splitlines()  # 将字符串按行分割成列表
        html = '\n'.join(html[4:])  # 跳过前四行
        print('-----------------------------------------------------------------')
        print(html)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = MainWindow()
    editor.show()
    editor.gen_button.clicked.connect(editor.test)
    sys.exit(app.exec_())
