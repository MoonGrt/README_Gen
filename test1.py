import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout, QPushButton
import requests

def get_repoinfo(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repositories = response.json()
        return repositories
    else:
        print(f"Error: Unable to fetch repositories. Status code: {response.status_code}")
        return None

class RepoSelectorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # 创建标签
        label = QLabel("选择要使用的仓库:")

        # 获取用户仓库列表
        repositories = get_repoinfo("MoonGrt")

        # 创建仓库选择框并填充内容
        self.repo_combobox = QComboBox(self)
        if repositories:
            for repo in repositories:
                self.repo_combobox.addItem(repo["name"])

        # 创建确认按钮
        confirm_button = QPushButton("确认", self)
        confirm_button.clicked.connect(self.confirm_selection)

        # 创建垂直布局
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.repo_combobox)
        layout.addWidget(confirm_button)

        # 设置主窗口布局
        self.setLayout(layout)

        # 设置窗口标题和大小
        self.setWindowTitle('仓库选择器')
        self.setGeometry(300, 300, 300, 150)

    def confirm_selection(self):
        # 获取用户选择的仓库
        selected_repo = self.repo_combobox.currentText()
        print(f"用户选择了仓库: {selected_repo}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    selector_app = RepoSelectorApp()
    selector_app.show()
    sys.exit(app.exec_())
