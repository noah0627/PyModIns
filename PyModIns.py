import os
import sys
import threading
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QWidget, QProgressBar, QMessageBox, QTextEdit,
                             QDialog, QHBoxLayout, QComboBox, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QUrl
from PyQt5.QtGui import QDesktopServices
from subprocess import Popen, PIPE
import traceback
import json
import platform
from datetime import datetime


# ==================== 多语言支持 ====================
class Translator:
    def __init__(self):
        self.languages = {
            "en": self._english(),
            "zh": self._chinese(),
            "ja": self._japanese()
        }
        self.current_lang = "zh"  # 默认中文

    def set_language(self, lang):
        if lang in self.languages:
            self.current_lang = lang
        return self.languages[self.current_lang]

    def text(self, key):
        return self.languages[self.current_lang].get(key, key)

    def _english(self):
        return {
            "app_title": "Python Module Installer - Release 2.0.2",
            "menu_file": "File",
            "menu_tools": "Tools",
            "menu_help": "Help",
            "view_log": "View Log",
            "export_packages": "Export Packages",
            "exit": "Exit",
            "settings": "Settings",
            "list_packages": "List Packages",
            "about": "About",
            "documentation": "Documentation",
            "check_updates": "Check Updates",
            "update_log": "Update Log",
            "install_module": "Install Module",
            "module_name_placeholder": "Enter module name (e.g. numpy)",
            "install_from_req": "Install from requirements.txt",
            "install_wheel": "Install Wheel File",
            "upgrade_module": "Upgrade Module",
            "uninstall_module": "Uninstall Module",
            "log_window_title": "Install Log",
            "save_log": "Save Log",
            "clear_log": "Clear Log",
            "close": "Close",
            "about_title": "Version Information",
            "version": "Version: Release 2.0.2",
            "build_date": "Build Date: 2025.6.7",
            "copyright": "©2025 Noah1001. All rights reserved",
            "update_log_title": "Update Log",
            "update_content": """Version Release 2.0.2 Update Log:

1. Added real-time language switching
2. Improved restart prompt for language changes
3. Fixed several UI issues
4. Enhanced stability

New Features:
- Instant language preview
- Smoother restart process
- Better error handling""",
            "settings_title": "Settings",
            "theme": "Theme:",
            "theme_options": ["System Default", "Light", "Dark"],
            "mirror": "Mirror Source:",
            "mirror_options": [
                "Default (PyPI)",
                "Tsinghua (https://pypi.tuna.tsinghua.edu.cn/simple)",
                "Aliyun (https://mirrors.aliyun.com/pypi/simple)",
                "Douban (https://pypi.douban.com/simple)",
                "USTC (https://pypi.mirrors.ustc.edu.cn/simple)"
            ],
            "proxy": "Proxy Settings:",
            "proxy_placeholder": "http://proxy.example.com:8080",
            "save_settings": "Save Settings",
            "req_window_title": "Install from Requirements",
            "req_placeholder": "Path to requirements.txt",
            "browse": "Browse",
            "install_req": "Install Requirements",
            "wheel_window_title": "Install Wheel File",
            "wheel_placeholder": "Path to .whl file",
            "install_wheel": "Install Wheel",
            "success": "Success",
            "error": "Error",
            "module_empty": "Module name cannot be empty",
            "file_not_found": "File not found!",
            "no_requirements": "No requirements found in file!",
            "installing_packages": "Installing {count} packages...",
            "invalid_wheel": "Please select a valid .whl file!",
            "confirm_uninstall": "Confirm Uninstall",
            "uninstall_confirm": "Are you sure you want to uninstall {module}?",
            "latest_version": "You are using the latest Release 2.0.2 version",
            "settings_saved": "Settings have been saved successfully",
            "save_error": "Failed to save settings: {error}",
            "fatal_error": "Fatal Error",
            "crash_message": "The application encountered a fatal error:\n{error}\n\nVersion: Release 2.0.2\nSystem: {system}",
            "restart_required": "Restart required",
            "restart_message": "Language change requires restart. Restart now?",
            "yes": "Yes",
            "no": "No",
            "language": "Language:",
            "language_options": ["Chinese", "English", "Japanese"]
        }

    def _chinese(self):
        return {
            "app_title": "Python模块安装器 - Release 2.0.2",
            "menu_file": "文件",
            "menu_tools": "工具",
            "menu_help": "帮助",
            "view_log": "查看日志",
            "export_packages": "导出已安装包",
            "exit": "退出",
            "settings": "设置",
            "list_packages": "列出已安装包",
            "about": "关于",
            "documentation": "文档",
            "check_updates": "检查更新",
            "update_log": "更新日志",
            "install_module": "安装模块",
            "module_name_placeholder": "输入模块名 (例如 numpy)",
            "install_from_req": "从requirements.txt安装",
            "install_wheel": "安装Wheel文件",
            "upgrade_module": "升级模块",
            "uninstall_module": "卸载模块",
            "log_window_title": "安装日志",
            "save_log": "保存日志",
            "clear_log": "清空日志",
            "close": "关闭",
            "about_title": "版本信息",
            "version": "版本: Release 2.0.2",
            "build_date": "构建时间: 2025.6.7",
            "copyright": "©2025 Noah1001. 保留所有权利",
            "update_log_title": "更新日志",
            "update_content": """版本 Release 2.0.2 更新日志:

1. 添加实时语言切换功能
2. 改进语言更改的重启提示
3. 修复多个UI问题
4. 增强稳定性

新特性:
- 即时语言预览
- 更流畅的重启过程
- 更好的错误处理""",
            "settings_title": "设置",
            "theme": "主题:",
            "theme_options": ["系统默认", "浅色", "深色"],
            "mirror": "镜像源:",
            "mirror_options": [
                "默认(PyPI)",
                "清华(https://pypi.tuna.tsinghua.edu.cn/simple)",
                "阿里云(https://mirrors.aliyun.com/pypi/simple)",
                "豆瓣(https://pypi.douban.com/simple)",
                "中科大(https://pypi.mirrors.ustc.edu.cn/simple)"
            ],
            "proxy": "代理设置:",
            "proxy_placeholder": "http://代理地址:端口",
            "save_settings": "保存设置",
            "req_window_title": "从requirements.txt安装",
            "req_placeholder": "requirements.txt文件路径",
            "browse": "浏览",
            "install_req": "安装requirements",
            "wheel_window_title": "安装Wheel文件",
            "wheel_placeholder": ".whl文件路径",
            "install_wheel": "安装Wheel",
            "success": "成功",
            "error": "错误",
            "module_empty": "模块名不能为空",
            "file_not_found": "文件未找到!",
            "no_requirements": "文件中没有找到requirements!",
            "installing_packages": "正在安装 {count} 个包...",
            "invalid_wheel": "请选择有效的.whl文件!",
            "confirm_uninstall": "确认卸载",
            "uninstall_confirm": "确定要卸载 {module} 吗?",
            "latest_version": "您正在使用最新的 Release 2.0.2 版本",
            "settings_saved": "设置已成功保存",
            "save_error": "保存设置失败: {error}",
            "fatal_error": "致命错误",
            "crash_message": "应用程序遇到致命错误:\n{error}\n\n版本: Release 2.0.2\n系统: {system}",
            "restart_required": "需要重启",
            "restart_message": "语言更改需要重启应用。立即重启吗?",
            "yes": "是",
            "no": "否",
            "language": "语言:",
            "language_options": ["中文", "English", "日本語"]
        }

    def _japanese(self):
        return {
            "app_title": "Pythonモジュールインストーラー - Release 2.0.2",
            "menu_file": "ファイル",
            "menu_tools": "ツール",
            "menu_help": "ヘルプ",
            "view_log": "ログを表示",
            "export_packages": "パッケージをエクスポート",
            "exit": "終了",
            "settings": "設定",
            "list_packages": "インストール済みパッケージ一覧",
            "about": "バージョン情報",
            "documentation": "ドキュメント",
            "check_updates": "更新を確認",
            "update_log": "更新ログ",
            "install_module": "モジュールをインストール",
            "module_name_placeholder": "モジュール名を入力 (例: numpy)",
            "install_from_req": "requirements.txtからインストール",
            "install_wheel": "Wheelファイルをインストール",
            "upgrade_module": "モジュールをアップグレード",
            "uninstall_module": "モジュールをアンインストール",
            "log_window_title": "インストールログ",
            "save_log": "ログを保存",
            "clear_log": "ログをクリア",
            "close": "閉じる",
            "about_title": "バージョン情報",
            "version": "バージョン: Release 2.0.2",
            "build_date": "ビルド日: 2025.6.7",
            "copyright": "©2025 Noah1001. 全著作権所有",
            "update_log_title": "更新ログ",
            "update_content": """バージョン Release 2.0.2 更新内容:

1. リアルタイム言語切替機能を追加
2. 言語変更時の再起動プロンプトを改善
3. 複数のUI問題を修正
4. 安定性を向上

新機能:
- インスタント言語プレビュー
- スムーズな再起動プロセス
- より良いエラー処理""",
            "settings_title": "設定",
            "theme": "テーマ:",
            "theme_options": ["システムデフォルト", "ライト", "ダーク"],
            "mirror": "ミラーソース:",
            "mirror_options": [
                "デフォルト (PyPI)",
                "清華大学(https://pypi.tuna.tsinghua.edu.cn/simple)",
                "阿里雲(https://mirrors.aliyun.com/pypi/simple)",
                "豆瓣(https://pypi.douban.com/simple)",
                "中国科学技術大学(https://pypi.mirrors.ustc.edu.cn/simple)"
            ],
            "proxy": "プロキシ設定:",
            "proxy_placeholder": "http://proxy.example.com:8080",
            "save_settings": "設定を保存",
            "req_window_title": "requirements.txtからインストール",
            "req_placeholder": "requirements.txtファイルのパス",
            "browse": "参照",
            "install_req": "requirementsをインストール",
            "wheel_window_title": "Wheelファイルをインストール",
            "wheel_placeholder": ".whlファイルのパス",
            "install_wheel": "Wheelをインストール",
            "success": "成功",
            "error": "エラー",
            "module_empty": "モジュール名を入力してください",
            "file_not_found": "ファイルが見つかりません!",
            "no_requirements": "requirementsが見つかりません!",
            "installing_packages": "{count} 個のパッケージをインストール中...",
            "invalid_wheel": "有効な.whlファイルを選択してください!",
            "confirm_uninstall": "アンインストールの確認",
            "uninstall_confirm": "{module} をアンインストールしますか?",
            "latest_version": "最新の Release 2.0.2 バージョンを使用しています",
            "settings_saved": "設定が正常に保存されました",
            "save_error": "設定の保存に失敗しました: {error}",
            "fatal_error": "致命的なエラー",
            "crash_message": "アプリケーションで致命的なエラーが発生しました:\n{error}\n\nバージョン: Release 2.0.2\nシステム: {system}",
            "restart_required": "再起動が必要です",
            "restart_message": "言語変更には再起動が必要です。今すぐ再起動しますか?",
            "yes": "はい",
            "no": "いいえ",
            "language": "言語:",
            "language_options": ["中文", "English", "日本語"]
        }


translator = Translator()


# ==================== 信号发射器 ====================
class SignalEmitter(QObject):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    install_complete = pyqtSignal(bool, str)
    requirement_loaded = pyqtSignal(list)


# ==================== 日志窗口 ====================
class LogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translator.text("log_window_title"))
        self.setGeometry(100, 100, 1000, 800)

        layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("font-size: 14px; font-family: 'Consolas';")
        layout.addWidget(self.log_text)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton(translator.text("save_log"))
        self.save_btn.clicked.connect(self.save_log)
        self.clear_btn = QPushButton(translator.text("clear_log"))
        self.clear_btn.clicked.connect(self.clear_log)
        self.close_btn = QPushButton(translator.text("close"))
        self.close_btn.clicked.connect(self.close)

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def append_log(self, text):
        self.log_text.append(text)
        self.log_text.ensureCursorVisible()

    def save_log(self):
        file_path, _ = QFileDialog.getSaveFileName(self, translator.text("save_log"), "",
                                                   "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.log_text.toPlainText())

    def clear_log(self):
        self.log_text.clear()


# ==================== 更新日志窗口 ====================
class UpdateLogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translator.text("update_log_title"))
        self.setFixedSize(700, 600)

        layout = QVBoxLayout()

        version_label = QLabel("Release 2.0.2")
        version_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(version_label)

        date_label = QLabel(translator.text("build_date"))
        layout.addWidget(date_label)

        log_text = QTextEdit()
        log_text.setReadOnly(True)
        log_text.setPlainText(translator.text("update_content"))
        layout.addWidget(log_text)

        close_button = QPushButton(translator.text("close"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)


# ==================== 关于窗口 ====================
class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translator.text("about_title"))
        self.setFixedSize(600, 500)

        layout = QVBoxLayout()
        title_label = QLabel("Python Module Installer")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel(translator.text("version"))
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        build_label = QLabel(translator.text("build_date"))
        build_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(build_label)

        copyright_label = QLabel(translator.text("copyright"))
        copyright_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(copyright_label)

        system_info = QLabel(
            f"System: {platform.system()} {platform.release()}\n"
            f"Architecture: {platform.machine()}\n"
            f"Python: {platform.python_version()}\n"
            f"PyQt5: {self.get_pyqt_version()}"
        )
        system_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(system_info)

        # 添加链接
        link_layout = QHBoxLayout()

        github_btn = QPushButton("GitHub")
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com")))

        docs_btn = QPushButton(translator.text("documentation"))
        docs_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://docs.python.org")))

        update_log_btn = QPushButton(translator.text("update_log"))
        update_log_btn.clicked.connect(self.show_update_log)

        link_layout.addWidget(github_btn)
        link_layout.addWidget(docs_btn)
        link_layout.addWidget(update_log_btn)
        layout.addLayout(link_layout)

        close_button = QPushButton(translator.text("close"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)

    def get_pyqt_version(self):
        try:
            from PyQt5.Qt import PYQT_VERSION_STR
            return PYQT_VERSION_STR
        except:
            return translator.text("error")

    def show_update_log(self):
        update_log = UpdateLogWindow(self)
        update_log.exec_()


# ==================== 设置窗口 ====================
class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle(translator.text("settings_title"))
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        # 主题设置
        theme_label = QLabel(translator.text("theme"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(translator.text("theme_options"))
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_combo)

        # 语言设置
        lang_label = QLabel(translator.text("language"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(translator.text("language_options"))

        # 设置当前语言选项
        current_lang = translator.current_lang
        if current_lang == "zh":
            self.lang_combo.setCurrentIndex(0)
        elif current_lang == "en":
            self.lang_combo.setCurrentIndex(1)
        elif current_lang == "ja":
            self.lang_combo.setCurrentIndex(2)

        self.lang_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(lang_label)
        layout.addWidget(self.lang_combo)

        # 镜像源设置
        mirror_label = QLabel(translator.text("mirror"))
        self.mirror_combo = QComboBox()
        self.mirror_combo.addItems(translator.text("mirror_options"))
        layout.addWidget(mirror_label)
        layout.addWidget(self.mirror_combo)

        # 代理设置
        proxy_label = QLabel(translator.text("proxy"))
        self.proxy_edit = QLineEdit()
        self.proxy_edit.setPlaceholderText(translator.text("proxy_placeholder"))
        layout.addWidget(proxy_label)
        layout.addWidget(self.proxy_edit)

        # 保存按钮
        save_btn = QPushButton(translator.text("save_settings"))
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        self.setLayout(layout)

        # 加载设置
        self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding='utf-8') as f:
                    settings = json.load(f)
                    if "theme" in settings:
                        index = self.theme_combo.findText(settings["theme"])
                        if index >= 0:
                            self.theme_combo.setCurrentIndex(index)
                    if "mirror" in settings:
                        index = self.mirror_combo.findText(settings["mirror"])
                        if index >= 0:
                            self.mirror_combo.setCurrentIndex(index)
                    if "proxy" in settings:
                        self.proxy_edit.setText(settings["proxy"])
                    if "language" in settings:
                        index = self.lang_combo.findText(settings["language"])
                        if index >= 0:
                            self.lang_combo.setCurrentIndex(index)
        except Exception as e:
            print(f"加载设置失败: {str(e)}")

    def change_language(self, index):
        """更改语言并提示重启"""
        lang_map = {0: "zh", 1: "en", 2: "ja"}
        new_lang = lang_map[index]

        if new_lang != translator.current_lang:
            # 更新翻译器语言
            translator.set_language(new_lang)

            # 更新当前窗口文本
            self.retranslate_ui()

            # 更新父窗口文本
            if self.parent_window:
                self.parent_window.retranslate_ui()

            # 提示用户重启
            reply = QMessageBox.question(
                self,
                translator.text("restart_required"),
                translator.text("restart_message"),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # 保存设置
                self.save_settings()
                # 重启应用
                QApplication.exit(100)  # 使用特殊退出码表示需要重启

    def retranslate_ui(self):
        """重新翻译UI文本"""
        self.setWindowTitle(translator.text("settings_title"))
        self.layout().itemAt(0).widget().setText(translator.text("theme"))
        self.layout().itemAt(2).widget().setText(translator.text("language"))
        self.layout().itemAt(4).widget().setText(translator.text("mirror"))
        self.layout().itemAt(6).widget().setText(translator.text("proxy"))
        self.proxy_edit.setPlaceholderText(translator.text("proxy_placeholder"))
        self.layout().itemAt(8).widget().setText(translator.text("save_settings"))

        # 更新下拉框选项
        self.theme_combo.clear()
        self.theme_combo.addItems(translator.text("theme_options"))

        self.lang_combo.clear()
        self.lang_combo.addItems(translator.text("language_options"))
        current_lang = translator.current_lang
        if current_lang == "zh":
            self.lang_combo.setCurrentIndex(0)
        elif current_lang == "en":
            self.lang_combo.setCurrentIndex(1)
        elif current_lang == "ja":
            self.lang_combo.setCurrentIndex(2)

        self.mirror_combo.clear()
        self.mirror_combo.addItems(translator.text("mirror_options"))

    def save_settings(self):
        """保存设置"""
        try:
            settings = {
                "theme": self.theme_combo.currentText(),
                "language": self.lang_combo.currentText(),
                "mirror": self.mirror_combo.currentText(),
                "proxy": self.proxy_edit.text(),
                "version": "Release 2.0.2"
            }
            with open("settings.json", "w", encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, translator.text("success"),
                                    translator.text("settings_saved"))
        except Exception as e:
            QMessageBox.critical(self, translator.text("error"),
                                 translator.text("save_error").format(error=str(e)))


# ==================== 需求文件窗口 ====================
class RequirementWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translator.text("req_window_title"))
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText(translator.text("req_placeholder"))
        layout.addWidget(self.file_path_edit)

        browse_btn = QPushButton(translator.text("browse"))
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)

        self.install_btn = QPushButton(translator.text("install_req"))
        self.install_btn.clicked.connect(self.install_requirements)
        layout.addWidget(self.install_btn)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, translator.text("req_window_title"), "",
                                                   "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.file_path_edit.setText(file_path)

    def install_requirements(self):
        file_path = self.file_path_edit.text()
        if not os.path.exists(file_path):
            self.status_label.setText(translator.text("file_not_found"))
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            if not requirements:
                self.status_label.setText(translator.text("no_requirements"))
                return

            self.parent().install_multiple_modules(requirements)
            self.status_label.setText(translator.text("installing_packages").format(count=len(requirements)))

        except Exception as e:
            self.status_label.setText(f"{translator.text('error')}: {str(e)}")


# ==================== Wheel安装窗口 ====================
class WheelInstallWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translator.text("wheel_window_title"))
        self.setFixedSize(500, 300)

        layout = QVBoxLayout()

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText(translator.text("wheel_placeholder"))
        layout.addWidget(self.file_path_edit)

        browse_btn = QPushButton(translator.text("browse"))
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)

        install_btn = QPushButton(translator.text("install_wheel"))
        install_btn.clicked.connect(self.install_wheel)
        layout.addWidget(install_btn)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, translator.text("wheel_window_title"), "",
                                                   "Wheel Files (*.whl);;All Files (*)")
        if file_path:
            self.file_path_edit.setText(file_path)

    def install_wheel(self):
        wheel_path = self.file_path_edit.text()
        if not os.path.exists(wheel_path):
            self.status_label.setText(translator.text("file_not_found"))
            return

        if not wheel_path.endswith('.whl'):
            self.status_label.setText(translator.text("invalid_wheel"))
            return

        try:
            self.parent().install_wheel_file(wheel_path)
            self.status_label.setText(
                f"{translator.text('installing_packages').format(count=1)}: {os.path.basename(wheel_path)}")
        except Exception as e:
            self.status_label.setText(f"{translator.text('error')}: {str(e)}")


# ==================== 主窗口 ====================
class ModuleInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.log_window = None
        self.signal_emitter = SignalEmitter()
        self.signal_emitter.log_signal.connect(self.handle_log)
        self.signal_emitter.progress_signal.connect(self.update_progress)
        self.signal_emitter.install_complete.connect(self.handle_install_complete)
        self.signal_emitter.requirement_loaded.connect(self.handle_requirement_loaded)
        self.initUI()
        self.load_settings()

    def initUI(self):
        """初始化用户界面"""
        self.setWindowTitle(translator.text("app_title"))
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 主安装区域
        main_group = QWidget()
        main_layout = QVBoxLayout(main_group)

        self.entry = QLineEdit()
        self.entry.setPlaceholderText(translator.text("module_name_placeholder"))
        main_layout.addWidget(self.entry)

        install_btn = QPushButton(translator.text("install_module"))
        install_btn.clicked.connect(self.start_install)
        main_layout.addWidget(install_btn)

        # 高级选项
        advanced_group = QWidget()
        advanced_layout = QVBoxLayout(advanced_group)

        requirements_btn = QPushButton(translator.text("install_from_req"))
        requirements_btn.clicked.connect(self.show_requirements_window)
        advanced_layout.addWidget(requirements_btn)

        wheel_btn = QPushButton(translator.text("install_wheel"))
        wheel_btn.clicked.connect(self.show_wheel_install_window)
        advanced_layout.addWidget(wheel_btn)

        upgrade_btn = QPushButton(translator.text("upgrade_module"))
        upgrade_btn.clicked.connect(self.upgrade_module)
        advanced_layout.addWidget(upgrade_btn)

        uninstall_btn = QPushButton(translator.text("uninstall_module"))
        uninstall_btn.clicked.connect(self.uninstall_module)
        advanced_layout.addWidget(uninstall_btn)

        # 添加到主布局
        layout.addWidget(main_group)
        layout.addWidget(advanced_group)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # 菜单栏
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu(translator.text("menu_file"))
        log_action = file_menu.addAction(translator.text("view_log"))
        log_action.triggered.connect(self.show_log)
        export_action = file_menu.addAction(translator.text("export_packages"))
        export_action.triggered.connect(self.export_packages)
        exit_action = file_menu.addAction(translator.text("exit"))
        exit_action.triggered.connect(self.close)

        # 工具菜单
        tools_menu = menubar.addMenu(translator.text("menu_tools"))
        settings_action = tools_menu.addAction(translator.text("settings"))
        settings_action.triggered.connect(self.show_settings)
        list_action = tools_menu.addAction(translator.text("list_packages"))
        list_action.triggered.connect(self.list_installed_packages)

        # 帮助菜单
        help_menu = menubar.addMenu(translator.text("menu_help"))
        about_action = help_menu.addAction(translator.text("about"))
        about_action.triggered.connect(self.show_about)
        docs_action = help_menu.addAction(translator.text("documentation"))
        docs_action.triggered.connect(self.open_documentation)
        check_update_action = help_menu.addAction(translator.text("check_updates"))
        check_update_action.triggered.connect(self.check_for_updates)
        update_log_action = help_menu.addAction(translator.text("update_log"))
        update_log_action.triggered.connect(self.show_update_log)

    def retranslate_ui(self):
        """重新翻译所有UI文本"""
        self.setWindowTitle(translator.text("app_title"))

        # 更新菜单栏
        self.menuBar().actions()[0].setText(translator.text("menu_file"))
        self.menuBar().actions()[1].setText(translator.text("menu_tools"))
        self.menuBar().actions()[2].setText(translator.text("menu_help"))

        # 更新文件菜单
        file_menu = self.menuBar().actions()[0].menu()
        file_menu.actions()[0].setText(translator.text("view_log"))
        file_menu.actions()[1].setText(translator.text("export_packages"))
        file_menu.actions()[2].setText(translator.text("exit"))

        # 更新工具菜单
        tools_menu = self.menuBar().actions()[1].menu()
        tools_menu.actions()[0].setText(translator.text("settings"))
        tools_menu.actions()[1].setText(translator.text("list_packages"))

        # 更新帮助菜单
        help_menu = self.menuBar().actions()[2].menu()
        help_menu.actions()[0].setText(translator.text("about"))
        help_menu.actions()[1].setText(translator.text("documentation"))
        help_menu.actions()[2].setText(translator.text("check_updates"))
        help_menu.actions()[3].setText(translator.text("update_log"))

        # 更新主界面按钮
        central_widget = self.centralWidget()
        main_group = central_widget.layout().itemAt(0).widget()
        main_group.layout().itemAt(1).widget().setText(translator.text("install_module"))

        advanced_group = central_widget.layout().itemAt(1).widget()
        advanced_group.layout().itemAt(0).widget().setText(translator.text("install_from_req"))
        advanced_group.layout().itemAt(1).widget().setText(translator.text("install_wheel"))
        advanced_group.layout().itemAt(2).widget().setText(translator.text("upgrade_module"))
        advanced_group.layout().itemAt(3).widget().setText(translator.text("uninstall_module"))

        # 更新输入框提示
        main_group.layout().itemAt(0).widget().setPlaceholderText(translator.text("module_name_placeholder"))

    def load_settings(self):
        """加载设置"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding='utf-8') as f:
                    settings = json.load(f)
                    if "language" in settings:
                        lang_map = {"中文": "zh", "English": "en", "日本語": "ja"}
                        translator.set_language(lang_map.get(settings["language"], "zh"))
                        self.retranslate_ui()
                    return settings
            return {}
        except Exception as e:
            print(f"加载设置失败: {str(e)}")
            return {}

    def save_settings(self):
        """保存设置"""
        pass

    def safe_install(self, module_name=None, upgrade=False, uninstall=False):
        """安全安装模块"""
        try:
            module = module_name or self.entry.text().strip()
            if not module:
                self.signal_emitter.install_complete.emit(False, translator.text("module_empty"))
                return

            # 从设置获取镜像源
            mirror_url = ""
            settings = self.load_settings()
            if "mirror" in settings:
                if "清华" in settings["mirror"] or "Tsinghua" in settings["mirror"]:
                    mirror_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
                elif "阿里云" in settings["mirror"] or "Aliyun" in settings["mirror"]:
                    mirror_url = "https://mirrors.aliyun.com/pypi/simple"
                elif "豆瓣" in settings["mirror"] or "Douban" in settings["mirror"]:
                    mirror_url = "https://pypi.douban.com/simple"
                elif "中科大" in settings["mirror"] or "USTC" in settings["mirror"]:
                    mirror_url = "https://pypi.mirrors.ustc.edu.cn/simple"

            self.signal_emitter.progress_signal.emit(10)

            if uninstall:
                command = ['pip', 'uninstall', '-y', module]
            elif upgrade:
                command = ['pip', 'install', '--upgrade', module]
            else:
                command = ['pip', 'install', module]

            if mirror_url:
                command.extend(['-i', mirror_url, '--trusted-host', mirror_url.split('/')[2]])

            with Popen(command,
                       stdout=PIPE,
                       stderr=PIPE,
                       text=True,
                       bufsize=1,
                       universal_newlines=True) as process:

                for line in process.stdout:
                    self.signal_emitter.log_signal.emit(line)

                for line in process.stderr:
                    self.signal_emitter.log_signal.emit(f"{translator.text('error')}: {line}")

                process.wait()
                self.signal_emitter.progress_signal.emit(100)

                if process.returncode == 0:
                    action = translator.text("uninstall_module") if uninstall else translator.text(
                        "upgrade_module") if upgrade else translator.text("install_module")
                    self.signal_emitter.install_complete.emit(True,
                                                              f"{action.replace('模块', '')} {module} {translator.text('success').lower()}")
                else:
                    action = translator.text("uninstall_module") if uninstall else translator.text(
                        "upgrade_module") if upgrade else translator.text("install_module")
                    self.signal_emitter.install_complete.emit(False,
                                                              f"{action.replace('模块', '')} {module} {translator.text('error').lower()}")

        except Exception as e:
            error_msg = f"{translator.text('fatal_error')}: {str(e)}\n{traceback.format_exc()}"
            self.signal_emitter.log_signal.emit(error_msg)
            self.signal_emitter.install_complete.emit(False, error_msg)

    def install_wheel_file(self, wheel_path):
        """安装Wheel文件"""
        try:
            if not os.path.exists(wheel_path):
                self.signal_emitter.install_complete.emit(False, translator.text("file_not_found"))
                return

            self.signal_emitter.progress_signal.emit(10)

            command = ['pip', 'install', wheel_path]

            with Popen(command,
                       stdout=PIPE,
                       stderr=PIPE,
                       text=True,
                       bufsize=1,
                       universal_newlines=True) as process:

                for line in process.stdout:
                    self.signal_emitter.log_signal.emit(line)

                for line in process.stderr:
                    self.signal_emitter.log_signal.emit(f"{translator.text('error')}: {line}")

                process.wait()
                self.signal_emitter.progress_signal.emit(100)

                if process.returncode == 0:
                    wheel_name = os.path.basename(wheel_path)
                    self.signal_emitter.install_complete.emit(True,
                                                              f"{translator.text('install_wheel')} {wheel_name} {translator.text('success').lower()}")
                else:
                    self.signal_emitter.install_complete.emit(False,
                                                              f"{translator.text('install_wheel')} {translator.text('error').lower()}")

        except Exception as e:
            error_msg = f"{translator.text('fatal_error')} {translator.text('install_wheel').lower()}: {str(e)}\n{traceback.format_exc()}"
            self.signal_emitter.log_signal.emit(error_msg)
            self.signal_emitter.install_complete.emit(False, error_msg)

    def install_multiple_modules(self, modules):
        """安装多个模块"""

        def worker():
            total = len(modules)
            for i, module in enumerate(modules, 1):
                self.signal_emitter.log_signal.emit(f"\n=== {translator.text('install_module')} {module} ===\n")
                self.safe_install(module_name=module)
                self.signal_emitter.progress_signal.emit(int((i / total) * 100))

            self.signal_emitter.install_complete.emit(True,
                                                      f"{translator.text('install_module')} {total} {translator.text('success').lower()}")

        threading.Thread(target=worker, daemon=True).start()

    def start_install(self):
        """开始安装"""
        threading.Thread(target=self.safe_install, daemon=True).start()

    def upgrade_module(self):
        """升级模块"""
        module = self.entry.text().strip()
        if not module:
            QMessageBox.warning(self, translator.text("error"), translator.text("module_empty"))
            return
        threading.Thread(target=lambda: self.safe_install(module_name=module, upgrade=True), daemon=True).start()

    def uninstall_module(self):
        """卸载模块"""
        module = self.entry.text().strip()
        if not module:
            QMessageBox.warning(self, translator.text("error"), translator.text("module_empty"))
            return

        reply = QMessageBox.question(self, translator.text("confirm_uninstall"),
                                     translator.text("uninstall_confirm").format(module=module),
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            threading.Thread(target=lambda: self.safe_install(module_name=module, uninstall=True), daemon=True).start()

    def list_installed_packages(self):
        """列出已安装包"""
        try:
            with Popen(['pip', 'list', '--format=json'],
                       stdout=PIPE,
                       stderr=PIPE,
                       text=True,
                       universal_newlines=True) as process:

                output, error = process.communicate()

                if process.returncode == 0:
                    packages = json.loads(output)
                    package_list = "\n".join([f"{p['name']}=={p['version']}" for p in packages])
                    self.show_log_window(f"{translator.text('list_packages')}:\n{package_list}")
                else:
                    self.signal_emitter.log_signal.emit(
                        f"{translator.text('error')} {translator.text('list_packages').lower()}: {error}")

        except Exception as e:
            self.signal_emitter.log_signal.emit(
                f"{translator.text('error')} {translator.text('list_packages').lower()}: {str(e)}")

    def export_packages(self):
        """导出包列表"""
        file_path, _ = QFileDialog.getSaveFileName(self, translator.text("export_packages"), "requirements.txt",
                                                   "Text Files (*.txt)")
        if file_path:
            try:
                with Popen(['pip', 'freeze'],
                           stdout=PIPE,
                           stderr=PIPE,
                           text=True,
                           universal_newlines=True) as process:

                    output, error = process.communicate()

                    if process.returncode == 0:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(output)
                        QMessageBox.information(self, translator.text("success"),
                                                f"{translator.text('export_packages')} {file_path} {translator.text('success').lower()}")
                    else:
                        QMessageBox.critical(self, translator.text("error"),
                                             f"{translator.text('export_packages')} {translator.text('error').lower()}: {error}")

            except Exception as e:
                QMessageBox.critical(self, translator.text("error"),
                                     f"{translator.text('export_packages')} {translator.text('error').lower()}: {str(e)}")

    def handle_log(self, message):
        """处理日志"""
        if self.log_window is None:
            self.log_window = LogWindow(self)
            self.log_window.show()
        self.log_window.append_log(message)

    def show_log_window(self, message):
        """显示日志窗口"""
        if self.log_window is None:
            self.log_window = LogWindow(self)
            self.log_window.show()
        self.log_window.append_log(message)

    def update_progress(self, value):
        """更新进度"""
        self.progress_bar.setValue(value)

    def handle_install_complete(self, success, message):
        """处理安装完成"""
        if success:
            QMessageBox.information(self, translator.text("success"), message)
        else:
            QMessageBox.critical(self, translator.text("error"), message)

    def handle_requirement_loaded(self, requirements):
        """处理需求文件加载"""
        self.install_multiple_modules(requirements)

    def show_log(self):
        """显示日志"""
        if self.log_window is None:
            self.log_window = LogWindow(self)
        self.log_window.show()

    def show_about(self):
        """显示关于窗口"""
        about_window = AboutWindow(self)
        about_window.exec_()

    def show_update_log(self):
        """显示更新日志"""
        update_log = UpdateLogWindow(self)
        update_log.exec_()

    def show_settings(self):
        """显示设置窗口"""
        settings_window = SettingsWindow(self)
        settings_window.exec_()

    def show_requirements_window(self):
        """显示需求文件窗口"""
        requirements_window = RequirementWindow(self)
        requirements_window.exec_()

    def show_wheel_install_window(self):
        """显示Wheel安装窗口"""
        wheel_window = WheelInstallWindow(self)
        wheel_window.exec_()

    def open_documentation(self):
        """打开文档"""
        QDesktopServices.openUrl(QUrl("https://pip.pypa.io/en/stable/"))

    def check_for_updates(self):
        """检查更新"""
        QMessageBox.information(self, translator.text("check_updates"),
                                translator.text("latest_version"))

    def closeEvent(self, event):
        """关闭事件"""
        self.save_settings()
        event.accept()


# ==================== 主程序入口 ====================
if __name__ == "__main__":
    while True:
        app = QApplication(sys.argv)
        window = ModuleInstaller()
        window.show()

        exit_code = app.exec_()

        # 检查是否需要重启
        if exit_code != 100:
            break

        # 重启应用
        python = sys.executable
        os.execl(python, python, *sys.argv)
