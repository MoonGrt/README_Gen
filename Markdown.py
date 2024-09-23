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
        self.setGeometry(420, 220, 1100, 800)   # 设置窗口左上角位置为 (x, y)，宽度为 w，高度为 h
        self.setWindowTitle('Markdown display')
        self.setWindowIcon(QIcon('images/icons/markdown.svg'))

        self.text_edit = QTextEdit()
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.save_markdown)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)
        
        self.markdown_showfile('README.md')



    # 显示 markdown
    def markdown_show(self, markdown, MIT_license, path, contents):
        self.markdown = markdown
        self.path = path
        self.contents = contents
        self.MIT_license = MIT_license
        self.text_edit.setPlainText(self.markdown)

    def markdown_showfile(self, file):
        # 读取文件内容
        with open(file, 'r', encoding='utf-8') as f:
            self.markdown = f.read()
        # 将内容设置到文本编辑器中
        self.text_edit.setReadOnly(True)
        self.text_edit.setHtml(self.markdown)
        # self.text_edit.setPlainText(self.markdown)

    # 保存 markdown 到文件
    def save_markdown(self):
        if self.path:
            # 将 License 内容保存到文件中
            readme_path = self.path+'/LICENSE'
            with open(readme_path, 'w', encoding='utf-8') as readme_file:
                readme_file.write(self.MIT_license)
            print(f"LICENSE generated successfully at {readme_path}")

            # 将readme_content内容保存到文件中
            readme_path = self.path+'/README.md'
            with open(readme_path, 'w', encoding='utf-8') as readme_file:
                readme_file.write(self.markdown)
            print(f"README.md generated successfully at {readme_path}")

            self.copy_images_folder()
        else:
            QMessageBox.information(self, "Message", "Please select a folder")
        self.close()

    def copy_images_folder(self):
        # 获取当前目录下的 'images' 文件夹路径
        source_folder = os.path.join(os.getcwd(), 'images')

        # 检查 'images' 文件夹是否存在
        if not os.path.exists(source_folder):
            print("错误：当前目录下找不到 'images' 文件夹。")
            return

        # 检查目标文件夹是否存在，如果不存在则创建
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print(f"已创建目标文件夹：{self.path}")

        # 构建目标文件夹中 'images' 文件夹的路径
        destination_path = os.path.join(self.path, 'images')

        try:
            # 使用 shutil.copytree 复制 'images' 文件夹到目标文件夹
            shutil.copytree(source_folder, destination_path)
            print(f"成功将 'images' 文件夹复制到 {self.path}")
        except shutil.Error as e:
            print(f"复制 'images' 文件夹时发生错误：{e}")
        except Exception as e:
            print(f"{e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Markdown()
    window.show()
    sys.exit(app.exec_())
