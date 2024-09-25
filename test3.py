import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTextCursor, QTextBlockFormat, QImage

class TextEditWithDragDrop(QTextEdit):
    def __init__(self, parent=None):
        super(TextEditWithDragDrop, self).__init__(parent)
        self.setAcceptDrops(True)  # 允许接受拖放事件
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
            original_height = image.height()
            # 如果图片高度超过最大高度，进行缩放
            if original_height > self.max_height:
                scale_factor = self.max_height / original_height
                new_width = int(image.width() * scale_factor)
                image = image.scaled(new_width, self.max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)


            cursor = self.textCursor()

            # 设置块格式为居中
            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignCenter)
            # 插入图片
            cursor.insertBlock(block_format)  # 插入一个新块并应用居中格式
            cursor.insertImage(image, image_path)

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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.text_edit = TextEditWithDragDrop(self)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)
        self.setWindowTitle("QTextEdit 支持文件和图片拖放")
        self.resize(800, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
