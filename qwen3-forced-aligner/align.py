#!/usr/bin/env python3
"""
Qwen3 Forced Aligner 对齐脚本
用于在 Claude Code Skill 中调用
"""

import argparse
import json
import sys
import os


def align_audio_text(audio_path, text, language="Chinese", output_format="json"):
    """
    对音频和文本进行强制对齐

    Args:
        audio_path: 音频文件路径
        text: 要对齐的文本
        language: 语言名称（默认 Chinese）
        output_format: 输出格式（json, txt, srt）

    Returns:
        对齐结果
    """
    try:
        import torch
        from qwen_asr import Qwen3ForcedAligner
    except ImportError:
        print("错误: 未安装 qwen-asr 包", file=sys.stderr)
        print("请先运行: python install.py", file=sys.stderr)
        sys.exit(1)

    # 检查音频文件是否存在
    if not os.path.exists(audio_path):
        print(f"错误: 音频文件不存在: {audio_path}", file=sys.stderr)
        sys.exit(1)

    # 检查 CUDA 可用性
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        print("警告: CUDA 不可用，使用 CPU 推理（速度较慢）", file=sys.stderr)

    print(f"正在加载模型...", file=sys.stderr)

    # 加载模型
    try:
        model = Qwen3ForcedAligner.from_pretrained(
            "Qwen/Qwen3-ForcedAligner-0.6B",
            dtype=torch.bfloat16 if device.startswith("cuda") else torch.float32,
            device_map=device,
        )
        print(f"模型加载完成", file=sys.stderr)
    except Exception as e:
        print(f"模型加载失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 执行对齐
    print(f"正在对齐音频和文本...", file=sys.stderr)
    try:
        results = model.align(
            audio=audio_path,
            text=text,
            language=language,
        )
    except Exception as e:
        print(f"对齐失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 格式化输出
    if output_format == "json":
        return json.dumps(results, ensure_ascii=False, indent=2)
    elif output_format == "txt":
        lines = []
        for item in results:
            lines.append(f"[{item['start']:.2f} - {item['end']:.2f}] {item['text']}")
        return "\n".join(lines)
    elif output_format == "srt":
        lines = []
        for i, item in enumerate(results, 1):
            start = format_time(item['start'])
            end = format_time(item['end'])
            lines.append(f"{i}")
            lines.append(f"{start} --> {end}")
            lines.append(item['text'])
            lines.append("")
        return "\n".join(lines)
    else:
        return json.dumps(results, ensure_ascii=False, indent=2)


def format_time(seconds):
    """将秒数转换为 SRT 时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def main():
    parser = argparse.ArgumentParser(
        description="Qwen3 Forced Aligner - 语音文本强制对齐"
    )
    parser.add_argument(
        "audio",
        help="音频文件路径"
    )
    parser.add_argument(
        "--text", "-t",
        required=True,
        help="要对齐的文本"
    )
    parser.add_argument(
        "--language", "-l",
        default="Chinese",
        choices=[
            "Chinese", "English", "Cantonese", "French", "German",
            "Italian", "Japanese", "Korean", "Portuguese", "Russian", "Spanish"
        ],
        help="语言（默认: Chinese）"
    )
    parser.add_argument(
        "--output-format", "-f",
        default="json",
        choices=["json", "txt", "srt"],
        help="输出格式（默认: json）"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径（默认输出到 stdout）"
    )

    args = parser.parse_args()

    # 执行对齐
    result = align_audio_text(
        audio_path=args.audio,
        text=args.text,
        language=args.language,
        output_format=args.output_format
    )

    # 输出结果
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"结果已保存到: {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
