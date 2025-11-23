#  QQ-Ad-Bot-Based-on-Keyword-Detection
本项目基于 LLOneBot 与 NoneBot 开发，旨在为二次元摄影师及毛娘提供高效的接单条发送工具。机器人有关键词检测、延时发送、模拟打字延迟等功能，尽可能的模拟真人发送接单条；支持目标群管理，可开启或关闭特定群的消息推送；提供文字与图片消息灵活设置，满足个性化需求。同时，项目配备 WebUI 控制界面，实现对配置文件的可视化管理，操作直观便捷，极大提升接单条发送效率与管理体验。

##  项目结构

QQ-Ad-Bot-Based-on-Keyword-Detection/

├── LLOneBot/                 # LLOneBot 相关文件

│   └── llonebot.exe          # llonebot 启动器

├── maven396/                 # 依赖：Maven 3.9.6

├── qqbot/                    # NoneBot 本体

│   ├── plugins/keywords_sender/  # 核心插件，实现功能

│   └── bot.py                # NoneBot 启动脚本

├── QQBotConfig/              # 前端和后端配置

│   ├── backend/              # 后端

│   └── frontend/             # 前端

├── start.bat                 # 一键启动（建议管理员模式运行）

├── start.py                  # Python 一键启动脚本

├── requirements.txt          # Python 依赖列表

└── README.md                 # 项目说明文件

## ⚙️ 环境配置

1. 克隆项目

    git clone https://github.com/Linmo-s/QQ-Ad-Bot-Based-on-Keyword-Detection.git

2. 安装依赖

    pip install -r requirements.txt # 这里只安装了最小依赖环境，还有一些像前端启动npm的依赖没有写出

3. 启动

    右键start.bat以管理员模式启动（不以管理员模式启动容易出现llonebot无法启动的问题）

## 🧑‍💻 作者信息

作者: <br>
LinMo[访问我的主页](https://github.com/Linmo-s)<br>

"# QQ-Ad-Bot-Based-on-Keyword-Detection" 
"# QQ-Ad-Bot-Based-on-Keyword-Detection" 
"# QQ-Ad-Bot-Based-on-Keyword-Detection" 
