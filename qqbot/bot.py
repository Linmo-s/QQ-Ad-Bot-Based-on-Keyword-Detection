import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from pathlib import Path

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)

# 加载插件
# 当前文件所在目录
BASE_DIR = Path(__file__).parent
PLUGIN_DIR = BASE_DIR / "plugins"  # 指向 qqbot/plugins 文件夹
nonebot.load_plugins(str(PLUGIN_DIR))

if __name__ == "__main__":
    nonebot.run()
