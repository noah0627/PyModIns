import os
import sys
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QWidget, QProgressBar, QMessageBox, QTextEdit,
                             QDialog, QHBoxLayout, QComboBox, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QUrl
from PyQt5.QtGui import QDesktopServices
from subprocess import Popen, PIPE
import traceback
import json
import platform


# ==================== 多语言支持 ====================
class Translator:
    def __init__(self):
        self.languages = {
            "en": self._english(),
            "zh": self._chinese(),
            "ja": self._japanese()
        }
        self.current_lang = "zh"

    def set_language(self, lang):
        if lang in self.languages:
            self.current_lang = lang
        return self.languages[self.current_lang]

    def text(self, key):
        return self.languages[self.current_lang].get(key, key)

    def _english(self):
        return {
            "app_title": "Python Module Installer - Release 2.0.3",
            "menu_file": "File",
            "menu_tools": "Tools",
            "menu_help": "Help",
            "view_log": "View Log",
            "export_packages": "Export Packages",
            "exit": "Exit",
            "settings": "Settings",
            "list_packages": "List Packages",
            "about": "About",
            "update_log": "Update Log",
            "install_module": "Install Module",
            "module_name_placeholder": "Enter module name (e.g. numpy)",
            "install_from_req": "Install from requirements.txt",
            "install_wheel": "Install Wheel File",
            "upgrade_module": "Upgrade Module",
            "uninstall_module": "Uninstall Module",
            "update_pip": "Update pip",  # 新增
            "log_window_title": "Install Log",
            "save_log": "Save Log",
            "clear_log": "Clear Log",
            "close": "Close",
            "about_title": "Version Information",
            "version": "Version: Release 2.0.3",
            "build_date": "Build Date: 2026.11.17",
            "copyright": "Made by Noah1001",
            "update_log_title": "Update Log",
            "update_content": """Version Release 2.0.3 Update Log:

1. Fixed a critical bug that caused the application to crash on changing the language
2. Removed the update check feature
3. Removed the "latest version" message from the update check
4. Removed the theme selection feature
5. Added a button to update pip

New Features:
- Update pip button""",
            "settings_title": "Settings",
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
            "settings_saved": "Settings have been saved successfully",
            "save_error": "Failed to save settings: {error}",
            "fatal_error": "Fatal Error",
            "crash_message": "The application encountered a fatal error:\n{error}\n\nVersion: Release 2.0.3\nSystem: {system}",
            "restart_required": "Restart required",
            "restart_message": "Language change requires restart. Restart now?",
            "yes": "Yes",
            "no": "No",
            "language": "Language:",
            "language_options": ["Chinese", "English", "Japanese"]
        }

    def _chinese(self):
        return {
            "app_title": "Python模块安装器 - Release 2.0.3",
            "menu_file": "文件",
            "menu_tools": "工具",
            "menu_help": "帮助",
            "view_log": "查看日志",
            "export_packages": "导出已安装包",
            "exit": "退出",
            "settings": "设置",
            "list_packages": "列出已安装包",
            "about": "关于",
            "update_log": "更新日志",
            "install_module": "安装模块",
            "module_name_placeholder": "输入模块名 (例如 numpy)",
            "install_from_req": "从requirements.txt安装",
            "install_wheel": "安装Wheel文件",
            "upgrade_module": "升级模块",
            "uninstall_module": "卸载模块",
            "update_pip": "更新 pip",  # 新增
            "log_window_title": "安装日志",
            "save_log": "保存日志",
            "clear_log": "清空日志",
            "close": "关闭",
            "about_title": "版本信息",
            "version": "版本: Release 2.0.3",
            "build_date": "构建时间: 2026.11.17",
            "copyright": "Created by Noah1001",
            "update_log_title": "更新日志",
            "update_content": """版本 Release 2.0.3 更新日志:

1. 修复了语言更改时导致应用程序崩溃的严重错误
2. 移除了更新检查功能
3. 移除了更新检查中的“已是最新版本”提示
4. 移除了主题选择功能
5. 增加了更新 pip 的按钮

新特性:
- 更新 pip 按钮""",
            "settings_title": "设置",
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
            "settings_saved": "设置已成功保存",
            "save_error": "保存设置失败: {error}",
            "fatal_error": "致命错误",
            "crash_message": "应用程序遇到致命错误:\n{error}\n\n版本: Release 2.0.3\n系统: {system}",
            "restart_required": "需要重启",
            "restart_message": "语言更改需要重启应用。立即重启吗?",
            "yes": "是",
            "no": "否",
            "language": "语言:",
            "language_options": ["中文", "English", "日本語"]
        }

    def _japanese(self):
        return {
            "app_title": "Pythonモジュールインストーラー - Release 2.0.3",
            "menu_file": "ファイル",
            "menu_tools": "ツール",
            "menu_help": "ヘルプ",
            "view_log": "ログを表示",
            "export_packages": "パッケージをエクスポート",
            "exit": "終了",
            "settings": "設定",
            "list_packages": "インストール済みパッケージ一覧",
            "about": "バージョン情報",
            "update_log": "更新ログ",
            "install_module": "モジュールをインストール",
            "module_name_placeholder": "モジュール名を入力 (例: numpy)",
            "install_from_req": "requirements.txtからインストール",
            "install_wheel": "Wheelファイルをインストール",
            "upgrade_module": "モジュールをアップグレード",
            "uninstall_module": "モジュールをアンインストール",
            "update_pip": "pipを更新",  # 新增
            "log_window_title": "インストールログ",
            "save_log": "ログを保存",
            "clear_log": "ログをクリア",
            "close": "閉じる",
            "about_title": "バージョン情報",
            "version": "バージョン: Release 2.0.3",
            "build_date": "ビルド日: 2026.11.17",
            "copyright": "Created by Noah1001",
            "update_log_title": "更新ログ",
            "update_content": """バージョン Release 2.0.3 更新内容:

1. 言語変更時にアプリケーションがクラッシュする重大なバグを修正
2. 更新チェック機能を削除
3. 更新チェックの「最新バージョンです」メッセージを削除
4. テーマ選択機能を削除
5. pipを更新するボタンを追加

新機能:
- pipを更新するボタン""",
            "settings_title": "設定",
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
            "settings_saved": "設定が正常に保存されました",
            "save_error": "設定の保存に失敗しました: {error}",
            "fatal_error": "致命的なエラー",
            "crash_message": "アプリケーションで致命的なエラーが発生しました:\n{error}\n\nバージョン: Release 2.0.3\nシステム: {system}",
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

        version_label = QLabel("Release 2.0.3")
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

        link_layout = QHBoxLayout()

        github_btn = QPushButton("GitHub")
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/noah0627/PyModIns")))

        update_log_btn = QPushButton(translator.text("update_log"))
        update_log_btn.clicked.connect(self.show_update_log)

        link_layout.addWidget(github_btn)
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

        # 语言设置
        self.lang_label = QLabel(translator.text("language"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(translator.text("language_options"))

        current_lang = translator.current_lang
        if current_lang == "zh":
            self.lang_combo.setCurrentIndex(0)
        elif current_lang == "en":
            self.lang_combo.setCurrentIndex(1)
        elif current_lang == "ja":
            self.lang_combo.setCurrentIndex(2)

        self.lang_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.lang_label)
        layout.addWidget(self.lang_combo)

        # 镜像源设置
        self.mirror_label = QLabel(translator.text("mirror"))
        self.mirror_combo = QComboBox()
        self.mirror_combo.addItems(translator.text("mirror_options"))
        layout.addWidget(self.mirror_label)
        layout.addWidget(self.mirror_combo)

        # 代理设置
        self.proxy_label = QLabel(translator.text("proxy"))
        self.proxy_edit = QLineEdit()
        self.proxy_edit.setPlaceholderText(translator.text("proxy_placeholder"))
        layout.addWidget(self.proxy_label)
        layout.addWidget(self.proxy_edit)

        # 保存按钮
        self.save_btn = QPushButton(translator.text("save_settings"))
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        # 加载设置
        self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding='utf-8') as f:
                    settings = json.load(f)
                    if "mirror" in settings:
                        index = self.mirror_combo.findText(settings["mirror"])
                        if index >= 0:
                            self.mirror_combo.setCurrentIndex(index)
                    if "proxy" in settings:
                        self.proxy_edit.setText(settings["proxy"])
                    if "language" in settings:
                        # 关键：屏蔽信号，防止读取设置时触发 change_language
                        self.lang_combo.blockSignals(True)
                        index = self.lang_combo.findText(settings["language"])
                        if index >= 0:
                            self.lang_combo.setCurrentIndex(index)
                        self.lang_combo.blockSignals(False)
        except Exception as e:
            print(f"加载设置失败: {str(e)}")

    def change_language(self, index):
        """更改语言并提示重启"""
        if index < 0:
            return

        lang_map = {0: "zh", 1: "en", 2: "ja"}
        new_lang = lang_map[index]

        if new_lang != translator.current_lang:
            # 先弹窗，如果确定要改，再改语言
            reply = QMessageBox.question(
                self,
                translator.text("restart_required"),
                translator.text("restart_message"),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                translator.set_language(new_lang)
                self.save_settings()
                QApplication.exit(100)  # 触发重启
            else:
                # 用户点否，UI回滚到当前语言
                self.lang_combo.blockSignals(True)
                old_lang_map = {"zh": 0, "en": 1, "ja": 2}
                self.lang_combo.setCurrentIndex(old_lang_map[translator.current_lang])
                self.lang_combo.blockSignals(False)

    def retranslate_ui(self):
        """重新翻译UI文本 (仅在需要时调用，目前由重启逻辑代替)"""
        self.setWindowTitle(translator.text("settings_title"))
        self.lang_label.setText(translator.text("language"))
        self.mirror_label.setText(translator.text("mirror"))
        self.proxy_label.setText(translator.text("proxy"))
        self.proxy_edit.setPlaceholderText(translator.text("proxy_placeholder"))
        self.save_btn.setText(translator.text("save_settings"))

        self.lang_combo.blockSignals(True)
        self.lang_combo.clear()
        self.lang_combo.addItems(translator.text("language_options"))
        
        current_lang = translator.current_lang
        if current_lang == "zh":
            self.lang_combo.setCurrentIndex(0)
        elif current_lang == "en":
            self.lang_combo.setCurrentIndex(1)
        elif current_lang == "ja":
            self.lang_combo.setCurrentIndex(2)
            
        self.lang_combo.blockSignals(False) 
        self.mirror_combo.clear()
        self.mirror_combo.addItems(translator.text("mirror_options"))

    def save_settings(self):
        """保存设置"""
        try:
            settings = {
                "language": self.lang_combo.currentText(),
                "mirror": self.mirror_combo.currentText(),
                "proxy": self.proxy_edit.text(),
                "version": "Release 2.0.3"
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
        self.load_settings()
        self.initUI() 
        
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

        self.install_btn = QPushButton(translator.text("install_module"))
        self.install_btn.clicked.connect(self.start_install)
        main_layout.addWidget(self.install_btn)

        # 高级选项
        advanced_group = QWidget()
        advanced_layout = QVBoxLayout(advanced_group)

        self.requirements_btn = QPushButton(translator.text("install_from_req"))
        self.requirements_btn.clicked.connect(self.show_requirements_window)
        advanced_layout.addWidget(self.requirements_btn)

        self.wheel_btn = QPushButton(translator.text("install_wheel"))
        self.wheel_btn.clicked.connect(self.show_wheel_install_window)
        advanced_layout.addWidget(self.wheel_btn)

        self.upgrade_btn = QPushButton(translator.text("upgrade_module"))
        self.upgrade_btn.clicked.connect(self.upgrade_module)
        advanced_layout.addWidget(self.upgrade_btn)

        self.uninstall_btn = QPushButton(translator.text("uninstall_module"))
        self.uninstall_btn.clicked.connect(self.uninstall_module)
        advanced_layout.addWidget(self.uninstall_btn)

        # 新增：更新 pip 按钮
        self.update_pip_btn = QPushButton(translator.text("update_pip"))
        self.update_pip_btn.clicked.connect(self.update_pip)
        advanced_layout.addWidget(self.update_pip_btn)

        layout.addWidget(main_group)
        layout.addWidget(advanced_group)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # 菜单栏
        menubar = self.menuBar()

        # 文件菜单
        self.file_menu = menubar.addMenu(translator.text("menu_file"))
        self.log_action = self.file_menu.addAction(translator.text("view_log"))
        self.log_action.triggered.connect(self.show_log)
        self.export_action = self.file_menu.addAction(translator.text("export_packages"))
        self.export_action.triggered.connect(self.export_packages)
        self.exit_action = self.file_menu.addAction(translator.text("exit"))
        self.exit_action.triggered.connect(self.close)

        # 工具菜单
        self.tools_menu = menubar.addMenu(translator.text("menu_tools"))
        self.settings_action = self.tools_menu.addAction(translator.text("settings"))
        self.settings_action.triggered.connect(self.show_settings)
        self.list_action = self.tools_menu.addAction(translator.text("list_packages"))
        self.list_action.triggered.connect(self.list_installed_packages)

        # 帮助菜单
        self.help_menu = menubar.addMenu(translator.text("menu_help"))
        self.about_action = self.help_menu.addAction(translator.text("about"))
        self.about_action.triggered.connect(self.show_about)
        self.update_log_action = self.help_menu.addAction(translator.text("update_log"))
        self.update_log_action.triggered.connect(self.show_update_log)

    def retranslate_ui(self):
        """重新翻译所有UI文本 (实名制调用)"""
        self.setWindowTitle(translator.text("app_title"))

        # 菜单栏
        self.file_menu.setTitle(translator.text("menu_file"))
        self.tools_menu.setTitle(translator.text("menu_tools"))
        self.help_menu.setTitle(translator.text("menu_help"))

        # 菜单项
        self.log_action.setText(translator.text("view_log"))
        self.export_action.setText(translator.text("export_packages"))
        self.exit_action.setText(translator.text("exit"))
        self.settings_action.setText(translator.text("settings"))
        self.list_action.setText(translator.text("list_packages"))
        self.about_action.setText(translator.text("about"))
        self.update_log_action.setText(translator.text("update_log"))

        # 按钮和输入框
        self.install_btn.setText(translator.text("install_module"))
        self.entry.setPlaceholderText(translator.text("module_name_placeholder"))
        self.requirements_btn.setText(translator.text("install_from_req"))
        self.wheel_btn.setText(translator.text("install_wheel"))
        self.upgrade_btn.setText(translator.text("upgrade_module"))
        self.uninstall_btn.setText(translator.text("uninstall_module"))
        self.update_pip_btn.setText(translator.text("update_pip")) # 新增

    def load_settings(self):
        """加载设置"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding='utf-8') as f:
                    settings = json.load(f)
                    if "language" in settings:
                        lang_map = {"中文": "zh", "English": "en", "日本語": "ja"}
                        translator.set_language(lang_map.get(settings["language"], "zh"))
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

            # 核心优化：使用 sys.executable -m pip 保证环境正确
            if uninstall:
                command = [sys.executable, '-m', 'pip', 'uninstall', '-y', module]
            elif upgrade:
                command = [sys.executable, '-m', 'pip', 'install', '--upgrade', module]
            else:
                command = [sys.executable, '-m', 'pip', 'install', module]

            if mirror_url:
                command.extend(['-i', mirror_url, '--trusted-host', mirror_url.split('/')[2]])

            with Popen(command, stdout=PIPE, stderr=PIPE, text=True, bufsize=1, universal_newlines=True) as process:
                for line in process.stdout:
                    self.signal_emitter.log_signal.emit(line)
                for line in process.stderr:
                    self.signal_emitter.log_signal.emit(f"{translator.text('error')}: {line}")

                process.wait()
                self.signal_emitter.progress_signal.emit(100)

                if process.returncode == 0:
                    action = translator.text("uninstall_module") if uninstall else translator.text("upgrade_module") if upgrade else translator.text("install_module")
                    self.signal_emitter.install_complete.emit(True, f"{action.replace('模块', '')} {module} {translator.text('success').lower()}")
                else:
                    action = translator.text("uninstall_module") if uninstall else translator.text("upgrade_module") if upgrade else translator.text("install_module")
                    self.signal_emitter.install_complete.emit(False, f"{action.replace('模块', '')} {module} {translator.text('error').lower()}")

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

            command = [sys.executable, '-m', 'pip', 'install', wheel_path]

            with Popen(command, stdout=PIPE, stderr=PIPE, text=True, bufsize=1, universal_newlines=True) as process:
                for line in process.stdout:
                    self.signal_emitter.log_signal.emit(line)
                for line in process.stderr:
                    self.signal_emitter.log_signal.emit(f"{translator.text('error')}: {line}")

                process.wait()
                self.signal_emitter.progress_signal.emit(100)

                if process.returncode == 0:
                    wheel_name = os.path.basename(wheel_path)
                    self.signal_emitter.install_complete.emit(True, f"{translator.text('install_wheel')} {wheel_name} {translator.text('success').lower()}")
                else:
                    self.signal_emitter.install_complete.emit(False, f"{translator.text('install_wheel')} {translator.text('error').lower()}")

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

            self.signal_emitter.install_complete.emit(True, f"{translator.text('install_module')} {total} {translator.text('success').lower()}")

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
            
    def update_pip(self):
        """更新 pip 到最新版本"""
        threading.Thread(target=lambda: self.safe_install(module_name="pip", upgrade=True), daemon=True).start()

    def list_installed_packages(self):
        """列出已安装包"""
        try:
            with Popen([sys.executable, '-m', 'pip', 'list', '--format=json'], stdout=PIPE, stderr=PIPE, text=True, universal_newlines=True) as process:
                output, error = process.communicate()

                if process.returncode == 0:
                    packages = json.loads(output)
                    package_list = "\n".join([f"{p['name']}=={p['version']}" for p in packages])
                    self.show_log_window(f"{translator.text('list_packages')}:\n{package_list}")
                else:
                    self.signal_emitter.log_signal.emit(f"{translator.text('error')} {translator.text('list_packages').lower()}: {error}")

        except Exception as e:
            self.signal_emitter.log_signal.emit(f"{translator.text('error')} {translator.text('list_packages').lower()}: {str(e)}")

    def export_packages(self):
        """导出包列表"""
        file_path, _ = QFileDialog.getSaveFileName(self, translator.text("export_packages"), "requirements.txt", "Text Files (*.txt)")
        if file_path:
            try:
                with Popen([sys.executable, '-m', 'pip', 'freeze'], stdout=PIPE, stderr=PIPE, text=True, universal_newlines=True) as process:
                    output, error = process.communicate()

                    if process.returncode == 0:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(output)
                        QMessageBox.information(self, translator.text("success"), f"{translator.text('export_packages')} {file_path} {translator.text('success').lower()}")
                    else:
                        QMessageBox.critical(self, translator.text("error"), f"{translator.text('export_packages')} {translator.text('error').lower()}: {error}")

            except Exception as e:
                QMessageBox.critical(self, translator.text("error"), f"{translator.text('export_packages')} {translator.text('error').lower()}: {str(e)}")

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