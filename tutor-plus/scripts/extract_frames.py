#!/usr/bin/env python3
"""
Extract review frames from a rendered video with ffmpeg.

Usage:
    python scripts/extract_frames.py media/videos/script/1080p60/MathScene.mp4 --interval 5
"""

import argparse
import subprocess
import sys
from pathlib import Path


def extract_frames(video_path: Path, output_dir: Path, interval: int) -> bool:
    if not video_path.exists():
        print(f"Error: 视频文件不存在: {video_path}")
        return False

    output_dir.mkdir(parents=True, exist_ok=True)
    output_pattern = output_dir / "frame_%04d.png"
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vf",
        f"fps=1/{interval}",
        str(output_pattern),
    ]

    print("执行命令:", " ".join(cmd))
    try:
        result = subprocess.run(cmd, check=False)
    except FileNotFoundError:
        print("Error: 未找到 ffmpeg，请先安装 ffmpeg")
        return False

    if result.returncode != 0:
        print("Error: 关键帧提取失败")
        return False

    print(f"关键帧已输出到: {output_dir}")
    return True


def main():
    parser = argparse.ArgumentParser(description="从 Manim 视频中按固定间隔提取关键帧")
    parser.add_argument("video", help="视频文件路径")
    parser.add_argument("--interval", type=int, default=5, help="提取间隔秒数，默认 5")
    parser.add_argument("--output", default="frames", help="输出目录，默认 frames")
    args = parser.parse_args()

    if args.interval <= 0:
        print("Error: --interval 必须大于 0")
        sys.exit(1)

    ok = extract_frames(Path(args.video), Path(args.output), args.interval)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
