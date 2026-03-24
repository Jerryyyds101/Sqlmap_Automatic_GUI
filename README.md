# SQLMap 自动注入工具

一个基于SQLMap的图形化SQL注入工具，支持GET和POST请求，自动检测参数，方便CTF比赛中快速获取flag。

## 功能特点

- **图形化界面**：直观的用户界面，无需记忆命令行参数
- **支持GET和POST请求**：可测试不同类型的注入点
- **自动参数检测**：自动爬取网站并检测潜在的注入参数
- **实时输出**：实时显示SQLMap的执行过程和结果
- **自动注入**：一键启动注入，自动回答所有问题

## 安装与使用

### 环境要求

- Python 2.7 或 Python 3.x
- Windows 操作系统

### 安装步骤

1. 克隆或下载本项目到本地
2. 确保项目目录结构完整，包含以下文件：
   - `sqlmap_gui.py` - 图形化界面主文件
   - `启动SQLMap图形界面.bat` - Windows批处理启动脚本
   - `启动SQLMap图形界面.ps1` - PowerShell启动脚本
   - `sqlmapproject-sqlmap-8f75402` - SQLMap核心目录

### 使用方法

1. 双击运行 `启动SQLMap图形界面.bat` 或 `启动SQLMap图形界面.ps1`
2. 在弹出的图形界面中：
   - **GET注入**：直接在URL输入框中输入包含参数的URL（如 `http://example.com/vulnerable.php?id=1`）
   - **POST注入**：选择POST请求类型，输入目标URL和POST数据（如 `username=admin&password=123`）
3. 点击"开始注入"按钮
4. 等待注入完成，查看结果区域获取flag

## 技术细节

- **多线程处理**：使用线程执行注入，避免界面卡顿
- **自动参数检测**：使用 `--forms` 和 `--crawl=2` 参数自动检测表单和爬取网站
- **高级检测**：使用 `--level=5` 和 `--risk=3` 参数提高检测能力
- **自动转储**：使用 `--dump` 参数尝试自动获取数据库内容

## 注意事项

- 仅用于合法的渗透测试和CTF比赛，请勿用于非法用途
- 测试过程可能会产生大量网络请求，请确保目标允许测试
- 部分网站可能有WAF防护，SQLMap会尝试自动绕过

## 许可证

本项目基于SQLMap，遵循SQLMap的许可证（GPL v2）。

## 致谢

- [SQLMap](https://sqlmap.org/) - 强大的SQL注入工具
- 所有为SQLMap做出贡献的开发者
