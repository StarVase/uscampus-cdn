import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget, QMessageBox,
    QGroupBox, QGridLayout, QComboBox
)
from PyQt5.QtCore import Qt

def generate_version_code():
    """生成版本代码，格式为年月日01"""
    today = datetime.now().strftime("%y%m%d")
    version_dir = "version-control"
    
    # 确保版本控制目录存在
    if not os.path.exists(version_dir):
        os.makedirs(version_dir)
    
    # 格式为年月日01
    version_code = int(today + "01")
    
    return version_code

def create_version(version_name, logs, download, page, version_code=None):
    """创建新版本"""
    if version_code is None:
        version_code = generate_version_code()
    
    version_data = {
        "version_name": version_name,
        "version_code": version_code,
        "logs": logs,
        "download": download,
        "page": page
    }
    
    return version_data

def write_version(version_data):
    """将版本数据写入文件"""
    version_code = version_data["version_code"]
    version_file = f"version-control/{version_code}.json"
    
    with open(version_file, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=2, ensure_ascii=False)
    
    return version_file

def read_version(version_code):
    """读取指定版本的信息"""
    version_file = f"version-control/{version_code}.json"
    
    if not os.path.exists(version_file):
        return None
    
    with open(version_file, 'r', encoding='utf-8') as f:
        version_data = json.load(f)
    
    return version_data

def publish_version(version_data):
    """发布版本（同步到latest.json）"""
    with open("latest.json", 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=2, ensure_ascii=False)
    
    return True

def list_versions():
    """列出所有版本"""
    version_dir = "version-control"
    
    if not os.path.exists(version_dir):
        return []
    
    files = os.listdir(version_dir)
    versions = []
    
    for file in files:
        if file.endswith('.json'):
            version_code = file.split('.')[0]
            try:
                version_data = read_version(version_code)
                if version_data:
                    versions.append(version_data)
            except Exception as e:
                print(f"读取版本文件 {file} 时出错: {e}")
    
    # 按版本代码排序
    versions.sort(key=lambda x: x["version_code"], reverse=True)
    
    return versions

class VersionManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("版本管理工具")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 创建标签页
        self.create_tab = QWidget()
        self.read_tab = QWidget()
        self.publish_tab = QWidget()
        self.list_tab = QWidget()
        
        self.tab_widget.addTab(self.create_tab, "创建新版本")
        self.tab_widget.addTab(self.read_tab, "读取版本")
        self.tab_widget.addTab(self.publish_tab, "发布版本")
        self.tab_widget.addTab(self.list_tab, "列出所有版本")
        
        # 初始化各个标签页
        self.init_create_tab()
        self.init_read_tab()
        self.init_publish_tab()
        self.init_list_tab()
    
    def init_create_tab(self):
        """初始化创建新版本标签页"""
        layout = QVBoxLayout(self.create_tab)
        
        # 创建版本信息组
        group_box = QGroupBox("版本信息")
        layout.addWidget(group_box)
        
        grid_layout = QGridLayout(group_box)
        
        # 版本名称
        grid_layout.addWidget(QLabel("版本名称:"), 0, 0)
        self.version_name_entry = QLineEdit()
        self.version_name_entry.setFixedWidth(400)
        grid_layout.addWidget(self.version_name_entry, 0, 1)
        
        release_button = QPushButton("自动填入release")
        release_button.clicked.connect(self.fill_release)
        grid_layout.addWidget(release_button, 0, 2)
        
        # 版本代号
        grid_layout.addWidget(QLabel("版本代号:"), 1, 0)
        self.version_code_entry = QLineEdit()
        self.version_code_entry.setFixedWidth(200)
        grid_layout.addWidget(self.version_code_entry, 1, 1)
        
        generate_button = QPushButton("自动生成")
        generate_button.clicked.connect(self.generate_code)
        grid_layout.addWidget(generate_button, 1, 2)
        
        # 更新日志
        grid_layout.addWidget(QLabel("更新日志:"), 2, 0, Qt.AlignmentFlag.AlignTop)
        self.logs_text = QTextEdit()
        self.logs_text.setFixedHeight(150)
        grid_layout.addWidget(self.logs_text, 2, 1, 1, 2)
        
        # 下载链接
        grid_layout.addWidget(QLabel("下载链接:"), 3, 0)
        self.download_entry = QLineEdit()
        self.download_entry.setFixedWidth(500)
        grid_layout.addWidget(self.download_entry, 3, 1)
        
        gitee_download_button = QPushButton("自动生成gitee链接")
        gitee_download_button.clicked.connect(self.generate_gitee_download)
        grid_layout.addWidget(gitee_download_button, 3, 2)
        
        # 发布页面链接
        grid_layout.addWidget(QLabel("发布页面链接:"), 4, 0)
        self.page_entry = QLineEdit()
        self.page_entry.setFixedWidth(500)
        grid_layout.addWidget(self.page_entry, 4, 1)
        
        gitee_page_button = QPushButton("自动填写gitee发布页")
        gitee_page_button.clicked.connect(self.fill_gitee_page)
        grid_layout.addWidget(gitee_page_button, 4, 2)
        
        # 按钮
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        create_button = QPushButton("创建版本")
        create_button.clicked.connect(self.create_version)
        button_layout.addWidget(create_button)
        
        create_publish_button = QPushButton("创建并发布")
        create_publish_button.clicked.connect(self.create_and_publish)
        button_layout.addWidget(create_publish_button)
        
        clear_button = QPushButton("清空")
        clear_button.clicked.connect(self.clear_create_form)
        button_layout.addWidget(clear_button)
    
    def init_read_tab(self):
        """初始化读取版本标签页"""
        layout = QVBoxLayout(self.read_tab)
        
        # 创建读取版本组
        group_box = QGroupBox("读取版本")
        layout.addWidget(group_box)
        
        grid_layout = QGridLayout(group_box)
        
        # 版本选择
        grid_layout.addWidget(QLabel("选择版本:"), 0, 0)
        self.read_version_combo = QComboBox()
        self.read_version_combo.setFixedWidth(400)
        grid_layout.addWidget(self.read_version_combo, 0, 1)
        
        refresh_button = QPushButton("刷新版本列表")
        refresh_button.clicked.connect(self.refresh_read_version_list)
        grid_layout.addWidget(refresh_button, 0, 2)
        
        read_button = QPushButton("读取")
        read_button.clicked.connect(self.read_version)
        grid_layout.addWidget(read_button, 1, 0, 1, 3)
        
        # 版本信息显示
        self.version_info_group = QGroupBox("版本信息")
        self.version_info_layout = QVBoxLayout(self.version_info_group)
        grid_layout.addWidget(self.version_info_group, 2, 0, 1, 3)
        
        # 初始为空
        self.version_info_layout.addWidget(QLabel("请选择一个版本并点击读取按钮"))
        
        # 初始加载版本列表
        self.refresh_read_version_list()
    
    def init_publish_tab(self):
        """初始化发布版本标签页"""
        layout = QVBoxLayout(self.publish_tab)
        
        # 创建发布版本组
        group_box = QGroupBox("发布版本")
        layout.addWidget(group_box)
        
        grid_layout = QGridLayout(group_box)
        
        # 版本选择
        grid_layout.addWidget(QLabel("选择版本:"), 0, 0)
        self.publish_version_combo = QComboBox()
        self.publish_version_combo.setFixedWidth(400)
        grid_layout.addWidget(self.publish_version_combo, 0, 1)
        
        refresh_button = QPushButton("刷新版本列表")
        refresh_button.clicked.connect(self.refresh_publish_version_list)
        grid_layout.addWidget(refresh_button, 0, 2)
        
        publish_button = QPushButton("发布")
        publish_button.clicked.connect(self.publish_version)
        grid_layout.addWidget(publish_button, 1, 0, 1, 3)
        
        # 发布结果
        grid_layout.addWidget(QLabel("发布结果:"), 2, 0, Qt.AlignmentFlag.AlignTop)
        self.publish_result_text = QTextEdit()
        self.publish_result_text.setReadOnly(True)
        self.publish_result_text.setFixedHeight(150)
        grid_layout.addWidget(self.publish_result_text, 2, 1, 1, 2)
        
        # 初始加载版本列表
        self.refresh_publish_version_list()
    
    def init_list_tab(self):
        """初始化列出所有版本标签页"""
        layout = QVBoxLayout(self.list_tab)
        
        # 创建所有版本组
        group_box = QGroupBox("所有版本")
        layout.addWidget(group_box)
        
        list_layout = QVBoxLayout(group_box)
        
        # 列表框
        self.versions_listbox = QListWidget()
        list_layout.addWidget(self.versions_listbox)
        
        # 按钮
        refresh_button = QPushButton("刷新列表")
        refresh_button.clicked.connect(self.refresh_versions_list)
        list_layout.addWidget(refresh_button)
        
        # 初始加载列表
        self.refresh_versions_list()
    
    def generate_code(self):
        """生成版本代号"""
        code = generate_version_code()
        self.version_code_entry.setText(str(code))
    
    def fill_release(self):
        """自动填入release"""
        current_text = self.version_name_entry.text().strip()
        if current_text:
            if not current_text.endswith(" Release"):
                self.version_name_entry.setText(current_text + " Release")
        else:
            self.version_name_entry.setText("Release")
    
    def generate_gitee_download(self):
        """自动生成gitee release链接"""
        version_code = self.version_code_entry.text().strip()
        version_name = self.version_name_entry.text().strip()
        
        if not version_code:
            QMessageBox.critical(self, "错误", "请先生成或输入版本代号")
            return
        
        # 提取版本号（去除Release后缀）
        if version_name.endswith(" Release"):
            version = version_name[:-8].strip()
        else:
            version = version_name.strip()
        
        # 生成gitee release链接
        gitee_link = f"https://gitee.com/StarVase/uscampus-infomation-release/releases/download/{version_code}/uscampus-{version}-release.apk"
        self.download_entry.setText(gitee_link)
    
    def fill_gitee_page(self):
        """自动填写gitee发布页"""
        gitee_page = "https://gitee.com/StarVase/uscampus-infomation-release/releases/"
        self.page_entry.setText(gitee_page)
    
    def refresh_read_version_list(self):
        """刷新读取版本的下拉列表"""
        self.read_version_combo.clear()
        versions = list_versions()
        
        if not versions:
            self.read_version_combo.addItem("没有找到版本文件")
        else:
            for version in versions:
                item_text = f"{version['version_code']} - {version['version_name']}"
                self.read_version_combo.addItem(item_text, version['version_code'])
    
    def refresh_publish_version_list(self):
        """刷新发布版本的下拉列表"""
        self.publish_version_combo.clear()
        versions = list_versions()
        
        if not versions:
            self.publish_version_combo.addItem("没有找到版本文件")
        else:
            for version in versions:
                item_text = f"{version['version_code']} - {version['version_name']}"
                self.publish_version_combo.addItem(item_text, version['version_code'])
    
    def create_version(self):
        """创建版本"""
        version_name = self.version_name_entry.text().strip()
        version_code_str = self.version_code_entry.text().strip()
        logs = self.logs_text.toPlainText().strip()
        download = self.download_entry.text().strip()
        page = self.page_entry.text().strip()
        
        if not version_name:
            QMessageBox.critical(self, "错误", "版本名称不能为空")
            return
        
        if not logs:
            QMessageBox.critical(self, "错误", "更新日志不能为空")
            return
        
        if not download:
            QMessageBox.critical(self, "错误", "下载链接不能为空")
            return
        
        if not page:
            QMessageBox.critical(self, "错误", "发布页面链接不能为空")
            return
        
        version_code = None
        if version_code_str:
            try:
                version_code = int(version_code_str)
            except ValueError:
                QMessageBox.critical(self, "错误", "版本代号必须是数字")
                return
        
        version_data = create_version(version_name, logs, download, page, version_code)
        try:
            file_path = write_version(version_data)
            QMessageBox.information(self, "成功", f"版本文件已创建: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建版本失败: {str(e)}")
    
    def create_and_publish(self):
        """创建并发布版本"""
        version_name = self.version_name_entry.text().strip()
        version_code_str = self.version_code_entry.text().strip()
        logs = self.logs_text.toPlainText().strip()
        download = self.download_entry.text().strip()
        page = self.page_entry.text().strip()
        
        if not version_name:
            QMessageBox.critical(self, "错误", "版本名称不能为空")
            return
        
        if not logs:
            QMessageBox.critical(self, "错误", "更新日志不能为空")
            return
        
        if not download:
            QMessageBox.critical(self, "错误", "下载链接不能为空")
            return
        
        if not page:
            QMessageBox.critical(self, "错误", "发布页面链接不能为空")
            return
        
        version_code = None
        if version_code_str:
            try:
                version_code = int(version_code_str)
            except ValueError:
                QMessageBox.critical(self, "错误", "版本代号必须是数字")
                return
        
        version_data = create_version(version_name, logs, download, page, version_code)
        try:
            file_path = write_version(version_data)
            publish_version(version_data)
            QMessageBox.information(self, "成功", f"版本文件已创建: {file_path}\n并已发布到latest.json")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建并发布版本失败: {str(e)}")
    
    def clear_create_form(self):
        """清空创建表单"""
        self.version_name_entry.clear()
        self.version_code_entry.clear()
        self.logs_text.clear()
        self.download_entry.clear()
        self.page_entry.clear()
    
    def read_version(self):
        """读取版本"""
        current_index = self.read_version_combo.currentIndex()
        if current_index < 0:
            QMessageBox.critical(self, "错误", "请选择一个版本")
            return
        
        version_code = self.read_version_combo.currentData()
        if version_code is None:
            QMessageBox.critical(self, "错误", "没有找到版本信息")
            return
        
        version_data = read_version(version_code)
        if version_data:
            # 清空版本信息组
            for i in reversed(range(self.version_info_layout.count())):
                widget = self.version_info_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            # 版本名称
            name_layout = QHBoxLayout()
            name_layout.addWidget(QLabel("版本名称:"), 0)
            name_edit = QLineEdit(version_data['version_name'])
            name_edit.setReadOnly(True)
            name_edit.setFixedWidth(400)
            name_layout.addWidget(name_edit, 1)
            self.version_info_layout.addLayout(name_layout)
            
            # 版本代号
            code_layout = QHBoxLayout()
            code_layout.addWidget(QLabel("版本代号:"), 0)
            code_edit = QLineEdit(str(version_data['version_code']))
            code_edit.setReadOnly(True)
            code_edit.setFixedWidth(200)
            code_layout.addWidget(code_edit, 1)
            self.version_info_layout.addLayout(code_layout)
            
            # 更新日志
            logs_layout = QVBoxLayout()
            logs_layout.addWidget(QLabel("更新日志:"))
            # 直接使用版本数据中的日志，因为它已经包含了正确的换行符
            logs_edit = QTextEdit(version_data['logs'])
            logs_edit.setReadOnly(True)
            logs_edit.setFixedHeight(150)
            logs_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
            # 设置文本格式，确保换行符被正确处理
            logs_edit.setPlainText(version_data['logs'])
            logs_layout.addWidget(logs_edit)
            self.version_info_layout.addLayout(logs_layout)
            
            # 下载链接
            download_layout = QHBoxLayout()
            download_layout.addWidget(QLabel("下载链接:"), 0)
            download_edit = QLineEdit(version_data['download'])
            download_edit.setReadOnly(True)
            download_edit.setFixedWidth(500)
            download_layout.addWidget(download_edit, 1)
            self.version_info_layout.addLayout(download_layout)
            
            # 发布页面
            page_layout = QHBoxLayout()
            page_layout.addWidget(QLabel("发布页面:"), 0)
            page_edit = QLineEdit(version_data['page'])
            page_edit.setReadOnly(True)
            page_edit.setFixedWidth(500)
            page_layout.addWidget(page_edit, 1)
            self.version_info_layout.addLayout(page_layout)
        else:
            QMessageBox.critical(self, "错误", f"版本文件不存在: version-control/{version_code}.json")
    
    def publish_version(self):
        """发布版本"""
        current_index = self.publish_version_combo.currentIndex()
        if current_index < 0:
            QMessageBox.critical(self, "错误", "请选择一个版本")
            return
        
        version_code = self.publish_version_combo.currentData()
        if version_code is None:
            QMessageBox.critical(self, "错误", "没有找到版本信息")
            return
        
        version_data = read_version(version_code)
        if version_data:
            try:
                publish_version(version_data)
                info = json.dumps(version_data, indent=2, ensure_ascii=False)
                self.publish_result_text.setText(f"版本已发布到latest.json\n\n{info}")
                QMessageBox.information(self, "成功", "版本已发布到latest.json")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"发布版本失败: {str(e)}")
        else:
            QMessageBox.critical(self, "错误", f"版本文件不存在: version-control/{version_code}.json")
    
    def refresh_versions_list(self):
        """刷新版本列表"""
        self.versions_listbox.clear()
        versions = list_versions()
        
        if not versions:
            self.versions_listbox.addItem("没有找到版本文件")
        else:
            for version in versions:
                line = f"版本代码: {version['version_code']} | 版本名称: {version['version_name']} | 下载链接: {version['download']}"
                self.versions_listbox.addItem(line)

if __name__ == "__main__":
    app = QApplication([])
    window = VersionManagerGUI()
    window.show()
    app.exec()
