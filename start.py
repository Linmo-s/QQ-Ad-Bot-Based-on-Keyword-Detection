import subprocess
import sys
import time
from pathlib import Path

# ---------------- 基础路径 ----------------
BASE_DIR = Path(__file__).parent.resolve()

BACKEND_DIR = BASE_DIR / "QQBotConfig" / "backend"
FRONTEND_DIR = BASE_DIR / "QQBotConfig" / "frontend"
LLNONEBOT_EXE = BASE_DIR / "LLOneBot-win" / "llonebot.exe"
NONEBOT_DIR = BASE_DIR / "qqbot"

PYTHON_CMD = sys.executable
MAVEN_CMD = BASE_DIR / "maven396" / "bin" / "mvn.cmd"

# ---------------- 启动函数 ----------------
def run_process(cmd, cwd=None, name=""):
    """
    启动子进程并打印输出
    """
    print(f"========== 启动 {name} ==========")
    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )

    # 打印输出
    import threading
    def stream_output():
        try:
            for line in process.stdout:
                print(f"[{name}] {line.strip()}")
        except Exception as e:
            print(f"[{name}] 输出异常: {e}")

    t = threading.Thread(target=stream_output, daemon=True)
    t.start()
    return process

# ---------------- 主流程 ----------------
def main():
    processes = []

    try:
        # 1. 启动后端
        processes.append(run_process([str(MAVEN_CMD), "spring-boot:run"], BACKEND_DIR, "后端"))
        time.sleep(3)

        # 2. 启动前端
        processes.append(run_process(["npm.cmd", "run", "dev"], FRONTEND_DIR, "前端"))
        time.sleep(2)

        # 3. 启动 LLNoneBot.exe
        if LLNONEBOT_EXE.exists():
            processes.append(run_process([str(LLNONEBOT_EXE)], None, "LLNoneBot"))
            time.sleep(2)
        else:
            print(f"[LLNoneBot] 文件不存在: {LLNONEBOT_EXE}")

        # 4. 启动 NoneBot
        processes.append(run_process([PYTHON_CMD, "bot.py"], NONEBOT_DIR, "NoneBot"))

        print("\n所有程序已启动。按 Ctrl+C 停止并关闭所有子进程。\n")

        # 保持主线程
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C，正在终止所有子进程...")
        for p in processes:
            try:
                p.terminate()
            except Exception:
                pass
        print("已结束所有子进程。")

if __name__ == "__main__":
    main()
