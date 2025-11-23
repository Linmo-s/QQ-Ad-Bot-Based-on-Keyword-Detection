import random
import asyncio
import json
from pathlib import Path
from datetime import datetime, timedelta

import nonebot
from nonebot.plugin import PluginMetadata, on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.typing import T_State
from nonebot_plugin_apscheduler import scheduler
from nonebot.log import logger

__plugin_meta__ = PluginMetadata(
    name="关键词计数图文延迟发送",
    description="每群收到指定数量关键词消息后，随机延迟发送图文，并模拟打字",
    usage="无需命令，自动计数延迟发送",
)

# ----------------- 配置文件路径 -----------------
CURRENT_FILE = Path(__file__).resolve()
CONFIG_FILE = CURRENT_FILE.parent.parent.parent.parent / "QQBotConfig" / "backend" / "src" / "main" / "java" / "com" / "qqbot" / "resources" / "config.json"

# ----------------- 配置文件操作 -----------------
def load_config():
    """读取配置文件"""
    if not CONFIG_FILE.exists():
        logger.warning(f"配置文件不存在: {CONFIG_FILE}, 创建空配置")
        return {"target_groups": [], "global_config": {}}
    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg: dict):
    """保存配置文件"""
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)

# ----------------- 计数器初始化 -----------------
group_message_counter = {}

# ----------------- 延迟发送 -----------------
async def delayed_send(bot: Bot, group_id: int, text_message: str, image_path: str):
    """延迟发送消息，模拟打字"""
    try:
        typing_duration = random.randint(3, 6)
        await asyncio.sleep(typing_duration)

        path = Path(image_path)
        if path.exists():
            message = MessageSegment.text(text_message) + MessageSegment.image(str(path))
            logger.info(f"图片存在，发送图文消息: {path}")
        else:
            message = MessageSegment.text(text_message)
            logger.warning(f"图片文件不存在，仅发送文本消息: {path}")

        await bot.send_group_msg(group_id=group_id, message=message)
        logger.success(f"延迟发送成功，群 {group_id} (模拟打字: {typing_duration}s)")
    except Exception as e:
        logger.error(f"延迟发送失败，群 {group_id}：{str(e)}")

# ----------------- 消息监听 -----------------
message_listener = on_message()

@message_listener.handle()
async def handle_group_message(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id

    # 每次处理消息时动态读取配置
    cfg = load_config()
    global_cfg = cfg.get("global_config", {})
    target_groups_cfg = cfg.get("target_groups", [])

    # 获取启用的群列表
    enabled_groups = [g["id"] for g in target_groups_cfg if g.get("enabled", True)]

    # 如果群未启用或不在配置中，直接返回
    if group_id not in enabled_groups:
        logger.debug(f"群 {group_id} 未启用，跳过")
        return

    # 当前群配置
    group_cfg = next((g for g in target_groups_cfg if g["id"] == group_id), None)
    if not group_cfg:
        logger.debug(f"群 {group_id} 配置不存在，跳过")
        return

    # 获取关键词、触发次数、文本和图片路径
    keywords = global_cfg.get("keywords", "").split()
    message_limit = global_cfg.get("triggerCount", 0)
    text_message = global_cfg.get("textMessage", "")
    image_path = global_cfg.get("imagePath", "")

    message_text = event.get_plaintext()
    if not any(keyword in message_text for keyword in keywords):
        return

    # 初始化计数器
    if group_id not in group_message_counter:
        group_message_counter[group_id] = 0
    group_message_counter[group_id] += 1
    logger.debug(f"群 {group_id} 关键词计数: {group_message_counter[group_id]}/{message_limit}")

    # 达到触发条件
    if group_message_counter[group_id] >= message_limit:
        group_message_counter[group_id] = 0

        delay_seconds = random.randint(30, 90)
        run_time = datetime.now() + timedelta(seconds=delay_seconds)

        scheduler.add_job(
            delayed_send,
            "date",
            run_date=run_time,
            args=[bot, group_id, text_message, image_path],
            id=f"delayed_send_{group_id}_{run_time.timestamp()}",
            replace_existing=True,
            misfire_grace_time=120
        )
        logger.info(f"群 {group_id} 达到触发条件，将在 {delay_seconds} 秒后发送")
