import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem

class FileTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabels(["File Tree"])
        self.root = self.invisibleRootItem()

    # 添加文件、文件夹到文件树中
    def add_items(self, parent_item, path, parent_is_root=True):
        # 存储文件夹和文件
        folders = []
        files = []

        for item_name in os.listdir(path):
            item_path = os.path.join(path, item_name)
            if os.path.isdir(item_path):
                folders.append(item_name)
            else:
                files.append(item_name)

        # 首先添加文件夹，然后添加文件
        for item_name in folders + files:
            item_path = os.path.join(path, item_name)
            item = QTreeWidgetItem(parent_item, [item_name])

            if parent_is_root:  # 如果是第一层，设置默认勾选
                if item_name != '.git':
                    item.setCheckState(0, 2)
                else:
                    item.setCheckState(0, 0)
            else:
                item.setCheckState(0, 0)

            if os.path.isdir(item_path):
                self.add_items(item, item_path, False)

            # # 发射 itemChanged 信号，模拟用户手动更改选项的操作
            # self.itemChanged.emit(item, 0)

    # 获取用户选择的文件、文件夹生成的markdown文件树
    def get_markdown_tree(self):
        return "└─ Project\n" + self.get_markdown_tree_recurse(self.root)

    # 递归生成markdown文件树
    def get_markdown_tree_recurse(self, item, indent='', last=False):
        content = ""
        if item.childCount() == 0:
            return content

        # pattern 1
        # indent += '  '
        # for i in range(item.childCount()):
        #     child_item = item.child(i)
        #     item_name = child_item.text(0)

        #     if child_item.checkState(0) == 2:
        #         if child_item.childCount() > 0:
        #             content += f"{indent}- /{item_name}/\n"
        #         else:
        #             content += f"{indent}- {item_name}\n"
        #         content += self.get_markdown_tree_recurse(child_item, indent, True)


        # # pattern 2
        # indent += '   ' if last or item == self.root else '│  '
        # for i in range(item.childCount()):
        #     child_item = item.child(i)
        #     item_name = child_item.text(0)
        #     is_last = i==item.childCount()-1

        #     if child_item.checkState(0) == 2:
        #         if child_item.childCount() > 0:
        #             content += indent + ('└─ ' if is_last else '├─ ') + '/' + item_name + '/\n'
        #             content += self.get_markdown_tree_recurse(child_item, indent, is_last)
        #         else:
        #             content += indent + ('└─ ' if is_last else '├─ ') + item_name + '\n'


        # pattern 3
        indent += '  ' if last or item == self.root else '│ '

        # 统计文件和文件夹数
        file_cnt = 0
        folder_cnt = 0
        for i in range(item.childCount()):
            child_item = item.child(i)
            if child_item.checkState(0) == 2 and child_item.childCount() == 0:
                file_cnt += 1
            elif child_item.checkState(0) == 2 and child_item.childCount() > 0:
                folder_cnt += 1

        # 处理文件类型的子项
        if file_cnt:
            index = 0
            for i in range(item.childCount()):
                child_item = item.child(i)
                item_name = child_item.text(0)
                is_last = index == file_cnt - 1

                if child_item.checkState(0) == 2 and child_item.childCount() == 0:
                    index += 1
                    content += indent + ('└─ ' if not folder_cnt and is_last else '├─ ') + item_name + '\n'

        # 处理文件夹类型的子项
        if folder_cnt:
            index = 0
            for i in range(item.childCount()):
                child_item = item.child(i)
                item_name = child_item.text(0)
                is_last = index == folder_cnt - 1
                # last = i == folder_cnt

                if child_item.checkState(0) == 2 and child_item.childCount() > 0:
                    index += 1
                    content += indent + ('└─ ' if is_last else '├─ ') + '/' + item_name + '/\n'
                    content += self.get_markdown_tree_recurse(child_item, indent, is_last)

        return content

    def handle_filetree_changed(self, item, column):
        # 处理选项状态改变时的逻辑
        if item.childCount() > 0:  # 只处理文件夹
            if item.checkState(0) == 0:
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    child_item.setCheckState(0, 0)
                    child_item.setDisabled(True)  # 如果母选项未选中，则禁用子选项的选择功能
            elif item.checkState(0) == 2:
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    child_item.setDisabled(False)  # 如果母选项选中，则开启子选项的选择功能
                    # if child_item.text(0) != '.git':
                    #     child_item.setCheckState(0, 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()  # 创建主窗口
    layout = QVBoxLayout(window)  # 使用垂直布局

    # 创建 FileTree 实例
    file_tree = FileTree()
    file_tree.itemChanged.connect(file_tree.handle_filetree_changed)
    file_tree.add_items(file_tree.root, '.')  # 替换为你的目录路径

    # 将文件树添加到窗口布局中
    layout.addWidget(file_tree)

    window.setWindowTitle('File Tree Viewer')
    window.resize(600, 400)
    window.show()  # 显示窗口

    sys.exit(app.exec_())  # 运行应用程序
