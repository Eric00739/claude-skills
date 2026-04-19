#!/usr/bin/env python3
"""
Qwen3 Forced Aligner 安装脚本
自动安装模型和依赖
"""

import subprocess
import sys
import os


def run_command(cmd, check=True):
    """运行 shell 命令"""
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result


def check_conda():
    """检查是否安装了 conda"""
    try:
        subprocess.run(["conda", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_environment():
    """创建 conda 环境"""
    print("=" * 60)
    print("步骤 1: 创建 Python 3.12 环境")
    print("=" * 60)

    env_name = "qwen3-asr"

    # 检查环境是否已存在
    result = subprocess.run(
        ["conda", "env", "list"],
        capture_output=True,
        text=True
    )

    if env_name in result.stdout:
        print(f"环境 '{env_name}' 已存在")
        choice = input("是否重新创建? [y/N]: ").strip().lower()
        if choice == 'y':
            run_command(["conda", "remove", "-n", env_name, "--all", "-y"])
            run_command(["conda", "create", "-n", env_name, "python=3.12", "-y"])
    else:
        run_command(["conda", "create", "-n", env_name, "python=3.12", "-y"])

    print(f"\n环境 '{env_name}' 创建完成")
    return env_name


def install_package(env_name):
    """安装 qwen-asr 包"""
    print("\n" + "=" * 60)
    print("步骤 2: 安装 qwen-asr 包")
    print("=" * 60)

    # 使用 conda run 在环境中执行 pip
    run_command([
        "conda", "run", "-n", env_name, "pip", "install", "-U", "qwen-asr"
    ])

    print("\nqwen-asr 安装完成")


def install_flash_attention(env_name):
    """安装 Flash Attention 2"""
    print("\n" + "=" * 60)
    print("步骤 3: 安装 Flash Attention 2（可选，推荐）")
    print("=" * 60)

    print("Flash Attention 2 可以减少 GPU 显存使用并加速推理")
    choice = input("是否安装 Flash Attention 2? [Y/n]: ").strip().lower()

    if choice in ('', 'y', 'yes'):
        print("正在安装 Flash Attention 2，这可能需要几分钟...")
        print("如果内存不足，请设置 MAX_JOBS=4")

        result = run_command([
            "conda", "run", "-n", env_name,
            "pip", "install", "-U", "flash-attn", "--no-build-isolation"
        ], check=False)

        if result.returncode == 0:
            print("Flash Attention 2 安装成功")
        else:
            print("Flash Attention 2 安装失败，模型仍可运行但速度较慢")
    else:
        print("跳过 Flash Attention 2 安装")


def verify_installation(env_name):
    """验证安装"""
    print("\n" + "=" * 60)
    print("步骤 4: 验证安装")
    print("=" * 60)

    test_code = """
import torch
from qwen_asr import Qwen3ForcedAligner

print("Python 包导入成功!")
print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA 设备: {torch.cuda.get_device_name(0)}")
    print(f"CUDA 显存: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

print("\\n安装验证通过！")
"""

    result = run_command(
        ["conda", "run", "-n", env_name, "python", "-c", test_code],
        check=False
    )

    return result.returncode == 0


def print_usage(env_name):
    """打印使用说明"""
    print("\n" + "=" * 60)
    print("安装完成！")
    print("=" * 60)

    print(f"""
使用方法:

1. 激活环境:
   conda activate {env_name}

2. Python API 示例:
   from qwen_asr import Qwen3ForcedAligner
   import torch

   model = Qwen3ForcedAligner.from_pretrained(
       "Qwen/Qwen3-ForcedAligner-0.6B",
       dtype=torch.bfloat16,
       device_map="cuda:0",
   )

   results = model.align(
       audio="audio.wav",
       text="甚至出现交易几乎停滞的情况。",
       language="Chinese",
   )

   for item in results:
       print(f"{{item['text']}}: {{item['start']:.2f}}s - {{item['end']:.2f}}s")

3. 支持的 11 种语言:
   - Chinese（中文）
   - English（英语）
   - Cantonese（粤语）
   - French（法语）
   - German（德语）
   - Italian（意大利语）
   - Japanese（日语）
   - Korean（韩语）
   - Portuguese（葡萄牙语）
   - Russian（俄语）
   - Spanish（西班牙语）

4. 首次运行时会自动下载模型（约 1.2GB）

更多帮助: 在 Claude Code 中询问关于 Qwen3 Forced Aligner 的使用
""")


def main():
    """主函数"""
    print("=" * 60)
    print("Qwen3 Forced Aligner 安装脚本")
    print("=" * 60)
    print()

    # 检查 conda
    if not check_conda():
        print("错误: 未检测到 conda")
        print("请先安装 Anaconda 或 Miniconda:")
        print("https://docs.conda.io/en/latest/miniconda.html")
        sys.exit(1)

    print("检测到 conda")
    print()

    # 创建环境
    env_name = create_environment()

    # 安装包
    install_package(env_name)

    # 安装 Flash Attention
    install_flash_attention(env_name)

    # 验证安装
    if verify_installation(env_name):
        print_usage(env_name)
    else:
        print("\n警告: 安装验证未通过，请检查错误信息")
        sys.exit(1)


if __name__ == "__main__":
    main()
