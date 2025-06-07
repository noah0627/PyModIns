# Python Module Installer

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![PyQt5 Version](https://img.shields.io/badge/PyQt5-5.15%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

一个功能强大的Python模块安装工具，支持多语言界面和多种安装方式。

## 功能特性

- 🚀 **多语言支持**：中文、英文、日文界面实时切换
- 📦 **多种安装方式**：
  - 单个模块安装
  - 从requirements.txt批量安装
  - Wheel文件安装
  - 模块升级和卸载
- 🌍 **镜像源选择**：支持PyPI官方源和国内镜像源
- 📊 **可视化界面**：直观的进度显示和安装日志
- ⚙️ **设置保存**：记住您的偏好设置

## 系统要求

- Python 3.6+
- PyQt5 5.15+
- pip 最新版本

## 安装方法

1. 克隆本仓库或下载源代码
```bash
git clone https://github.com/yourusername/python-module-installer.git
cd python-module-installer
```

2. 安装依赖
```bash
pip install PyQt5
```

3. 运行程序
```bash
python main.py
```

## 使用说明

### 主界面功能

1. **安装模块**：
   - 在输入框中输入模块名称（如numpy）
   - 点击"安装模块"按钮

2. **高级功能**：
   - 从requirements.txt安装
   - 安装Wheel文件
   - 升级模块
   - 卸载模块

3. **工具菜单**：
   - 查看安装日志
   - 导出已安装包列表
   - 列出已安装包
   - 程序设置

### 设置选项

- **界面语言**：中文/英文/日文
- **主题**：系统默认/浅色/深色
- **镜像源**：PyPI官方源/清华源/阿里云源等
- **代理设置**：支持HTTP代理配置

## 更新日志

### Release 2.0.2
- 新增实时语言切换功能
- 改进语言更改的重启提示
- 修复多个UI问题
- 增强稳定性

### Release 2.0.1
- 添加多语言支持
- 改进镜像源选择
- 修复若干小bug

## 常见问题

**Q: 更改语言后为什么需要重启？**
A: 部分界面元素需要重启才能完全应用语言更改，但您可以先预览效果。

**Q: 如何选择最快的镜像源？**
A: 根据您的网络环境，国内用户建议选择清华或阿里云镜像源。

**Q: 安装失败怎么办？**
A: 请查看安装日志获取详细错误信息，通常与网络连接或模块名称有关。

## 贡献指南

欢迎提交Issue或Pull Request！请确保您的代码符合PEP8规范。

## 许可证

本项目采用MIT许可证 - 详情请见LICENSE文件。
