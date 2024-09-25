import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem

class ContentTree(QTreeWidget):
    def __init__(self, name='Content'):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabels([name])
        self.root = self.invisibleRootItem()

    # 将内容项添加到内容树中，支持多级嵌套，新增展开参数
    def add_items(self, parent_text, children=None, default_checked=False, default_expanded=False, parent_item=None):
        # 如果 parent_item 是 None，说明是顶层节点，添加到根节点
        if parent_item is None:
            parent_item = QTreeWidgetItem(self.root, [parent_text])
        else:
            parent_item = QTreeWidgetItem(parent_item, [parent_text])
        # 设置复选框状态
        parent_item.setCheckState(0, 2 if default_checked else 0)
        # 控制该项是否展开
        if default_expanded:
            self.expandItem(parent_item)
        # 递归添加子节点
        if children:
            for child in children:
                # 如果子节点是字符串，直接添加
                if isinstance(child, str):
                    child_item = QTreeWidgetItem(parent_item, [child])
                    child_item.setCheckState(0, 0)
                # 如果子节点是元组或列表，则递归调用
                elif isinstance(child, (tuple, list)) and len(child) >= 2:
                    # child[0] 是子节点的文本，child[1] 是子节点的子项
                    child_text = child[0]
                    child_children = child[1] if len(child) > 1 else []
                    # 如果元组或列表有更多参数，分别获取default_checked和expanded的值
                    child_default_checked = child[2] if len(child) > 2 else False
                    child_default_expanded = child[3] if len(child) > 3 else False
                    # 递归调用，传递子节点的特有属性
                    self.add_items(child_text, child_children, default_checked=child_default_checked, default_expanded=child_default_expanded, parent_item=parent_item)

    # 获取内容树项目内容
    def get_items_state(self):
        result = {}
        for i in range(self.root.childCount()):
            child_item = self.root.child(i)
            self.get_items_recurse(child_item, result)
        return result

    # 递归获取内容树项目内容
    def get_items_recurse(self, item, result):
        item_text = item.text(0)
        item_state = item.checkState(0)
        result[item_text] = item_state

        for i in range(item.childCount()):
            child_item = item.child(i)
            self.get_items_recurse(child_item, result)

    # 处理选项状态改变时的逻辑
    def handle_contenttree_changed(self, item, column):
        if item.childCount() > 0:  # 只处理文件夹
            if item.checkState(0) == 0:
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    # child_item.setCheckState(0, 0)
                    child_item.setDisabled(True)  # 如果母选项未选中，则禁用子选项的选择功能
            elif item.checkState(0) == 2:
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    # child_item.setCheckState(0, 2)
                    child_item.setDisabled(False)  # 如果母选项选中，则开启子选项的选择功能

    # 递归获取所有项的名称、层级和选中状态
    def get_tree_content(self, item=None, level=0):
        if item is None:
            item = self.root
        content = []
        for i in range(item.childCount()):
            child = item.child(i)
            item_name = child.text(0)
            item_level = level
            is_checked = child.checkState(0) == 2  # 复选框状态为2表示选中
            content.append((item_name, item_level, is_checked))
            # 递归获取子项的内容
            content += self.get_tree_content(child, level + 1)
        return content

# Function to generate markdown from the section structure
def generate_readme(sections, level=1):
    markdown = ""
    for section in sections:
        for key, value in section.items():
            if value is True or (value is False and 'children' in section and section['children']):
                # Add the section title with corresponding heading level
                markdown += f"{'#' * level} {key}\n\n"
                if 'children' in section and section['children']:
                    # Recursively add the child sections
                    markdown += generate_readme(section['children'], level + 1)
    return markdown

def generate_markdown(content):
    markdown_text = ""
    for name, level, is_checked in content:
        if not level:  # 舍弃第一层
            continue
        if is_checked:
            # Add the section title with corresponding heading level
            markdown_text += f"<!-- {name.upper()} -->\n"
            # markdown_text += f"{'#' * level} {name}\n\n"
            markdown_text += f"{'#' * (level+1)} {name}\n\n"
    return markdown_text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()  # 创建主窗口
    layout = QVBoxLayout(window)  # 使用垂直布局

    # 创建 ContentTree 实例
    content_tree = ContentTree()

    # 添加一些示例项到内容树
    content_tree.add_items("README.md", [("Head", [], True),
                                         ("Contents", [], True),
                                         ("File Tree", [], True),
                                         ("About The Project", ["Built With"]),
                                         ("Getting Started", ["Prerequisites", "Installation"]),
                                         ("Usage", []),
                                         ("Roadmap", []),
                                         ("Version", []),
                                         ("Contributing", [], True),
                                         ("License", [], True),
                                         ("Contact", [], True),
                                         ("Acknowledgments", [], True)], True, True)  # parent child checked expanded
    content_tree.add_items("requirements.txt")
    content_tree.add_items("run.bat")
    content_tree.itemChanged.connect(content_tree.handle_contenttree_changed)

    # 将内容树添加到窗口布局中
    layout.addWidget(content_tree)

    window.setWindowTitle('Content Tree Viewer')
    window.resize(400, 300)
    window.show()  # 显示窗口

    content = content_tree.get_tree_content()
    print(content)
    print(generate_markdown(content))

    print(content_tree.get_items_state())

    sys.exit(app.exec_())  # 运行应用程序
