#!/usr/bin/env python3
"""
TTS 生成脚本

功能：
- 从 CSV 文件或分镜 Markdown 的"音频生成清单"读取对白列表
- 使用 Edge TTS 生成音频，默认 xiaoxiao 女声、-8% 慢速讲解
- 输出到指定目录
- 生成 audio_info.json 供验证脚本使用

CSV 格式：
    filename,text
    audio_001_开场.wav,"我们先看看题目里告诉了什么。"
    audio_002_介绍.wav,"你发现了吗？图里这个量发生了变化。"

使用：
    python generate_tts.py audio_list.csv ./audio
    python generate_tts.py 分镜.md ./audio
    python generate_tts.py 分镜.md ./audio --voice xiaoxiao --rate -8%

支持的声音：
    xiaoxiao (晓晓，女声，默认，适合亲和老师语气)
    xiaoyi (晓伊，女声)
    yunyang (云扬，男声)
    yunjian (云健，男声)
"""

import sys
import os
import csv
import json
import asyncio
import argparse
from pathlib import Path

# 声音映射表
VOICE_MAP = {
    'xiaoxiao': 'zh-CN-XiaoxiaoNeural',      # 晓晓，女声，默认
    'xiaoyi': 'zh-CN-XiaoyiNeural',          # 晓伊，女声
    'yunyang': 'zh-CN-YunyangNeural',        # 云扬，男声
    'yunjian': 'zh-CN-YunjianNeural',        # 云健，男声
    'xiaoxiao-dialect': 'zh-CN-XiaoxiaoNeural',  # 晓晓方言
    'xiaoxiao-multilingual': 'zh-CN-XiaoxiaoMultilingualNeural',
}

DEFAULT_VOICE = "xiaoxiao"
DEFAULT_RATE = "-8%"
DEFAULT_VOLUME = "+0%"
DEFAULT_PITCH = "+0Hz"


def format_default_for_help(value):
    """argparse 使用 % 格式化 help 文本，默认值里的百分号需要转义。"""
    return value.replace("%", "%%")


def normalize_cli_tts_options(argv):
    """
    支持 `--rate -8%` 这种自然写法。

    argparse 会把 -8% 误判为新选项，所以在解析前转成 `--rate=-8%`。
    """
    options_allowing_dash_values = {"--rate", "--volume", "--pitch"}
    normalized = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in options_allowing_dash_values and i + 1 < len(argv):
            value = argv[i + 1]
            if value.startswith("-") and not value.startswith("--"):
                normalized.append(f"{arg}={value}")
                i += 2
                continue
        normalized.append(arg)
        i += 1
    return normalized


def parse_cli_args(argv):
    """解析命令行参数，默认使用适合小学生教学视频的亲和女声慢速配置。"""
    argv = normalize_cli_tts_options(list(argv))
    parser = argparse.ArgumentParser(
        description="从 CSV 或分镜 Markdown 生成 Edge TTS 配音音频",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("input_file", help="CSV 文件路径，或包含音频生成清单的分镜 Markdown")
    parser.add_argument("output_dir", nargs="?", default="./audio", help="输出目录（默认：./audio）")
    parser.add_argument("--voice", default=DEFAULT_VOICE, choices=sorted(VOICE_MAP.keys()),
                        help=f"声音选择（默认：{DEFAULT_VOICE}，亲和女声）")
    parser.add_argument("--rate", default=DEFAULT_RATE,
                        help=f"语速调整（默认：{format_default_for_help(DEFAULT_RATE)}，更适合小学生听清）")
    parser.add_argument("--volume", default=DEFAULT_VOLUME,
                        help=f"音量调整（默认：{format_default_for_help(DEFAULT_VOLUME)}）")
    parser.add_argument("--pitch", default=DEFAULT_PITCH,
                        help=f"音高调整（默认：{DEFAULT_PITCH}）")
    return parser.parse_args(argv)


async def generate_audio(text, output_path, voice=DEFAULT_VOICE, rate=DEFAULT_RATE,
                         volume=DEFAULT_VOLUME, pitch=DEFAULT_PITCH):
    """
    生成单条音频

    参数:
        text: 文本内容
        output_path: 输出文件路径
        voice: 声音名称
        rate: 语速，例如 -8%
        volume: 音量，例如 +0%
        pitch: 音高，例如 +0Hz

    返回:
        (success, duration)
    """
    voice_id = VOICE_MAP.get(voice, VOICE_MAP[DEFAULT_VOICE])

    try:
        try:
            import edge_tts
        except ImportError:
            print("Error: edge-tts 未安装")
            print("请运行: uv pip install edge-tts")
            return False, 0

        communicate = edge_tts.Communicate(text, voice_id, rate=rate, volume=volume, pitch=pitch)
        await communicate.save(output_path)

        # 获取时长
        duration = await get_audio_duration(output_path)
        return True, duration
    except Exception as e:
        print(f"  Error generating {output_path}: {e}")
        return False, 0


async def get_audio_duration(audio_path):
    """获取音频时长"""
    try:
        from mutagen.mp3 import MP3
        audio = MP3(audio_path)
        return audio.info.length
    except:
        pass

    try:
        import wave
        with wave.open(audio_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)
    except:
        pass

    return 0


def parse_csv(csv_path):
    """
    解析 CSV 文件

    支持格式：
    - 标准 CSV: filename,text
    - 带 BOM 的 UTF-8
    - 不同分隔符（优先逗号，支持分号）
    """
    entries = []

    # 尝试不同编码
    encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb2312']

    for encoding in encodings:
        try:
            with open(csv_path, 'r', encoding=encoding) as f:
                # 尝试检测分隔符
                sample = f.read(2048)
                f.seek(0)

                delimiter = ','
                if ';' in sample and sample.count(';') > sample.count(','):
                    delimiter = ';'

                reader = csv.DictReader(f, delimiter=delimiter)

                for row in reader:
                    # 支持不同的列名
                    filename = row.get('filename') or row.get('文件名') or row.get('file')
                    text = row.get('text') or row.get('对白') or row.get('content') or row.get('读白')

                    if filename and text:
                        entries.append({
                            'filename': filename,
                            'text': text.strip()
                        })

            print(f"✓ 解析 CSV 成功 ({encoding}), 共 {len(entries)} 条")
            return entries

        except Exception as e:
            continue

    # 如果都失败，尝试简单解析
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:  # 跳过标题行
                parts = line.strip().split(',', 1)
                if len(parts) == 2:
                    entries.append({
                        'filename': parts[0].strip(),
                        'text': parts[1].strip().strip('"')
                    })
        if entries:
            print(f"✓ 简单解析 CSV 成功, 共 {len(entries)} 条")
            return entries
    except:
        pass

    print("Error: 无法解析 CSV 文件")
    return []


def clean_table_cell(value):
    """清理 Markdown 表格单元格中的包装引号和空白。"""
    value = (value or "").strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    return value


def parse_storyboard_markdown(storyboard_path):
    """
    从分镜 Markdown 的"音频生成清单"表格提取 TTS 条目。

    需要的表头包含：幕号、文件名、读白文本。其他列会被忽略。
    返回格式与 parse_csv 一致：[{filename, text}, ...]
    """
    content = Path(storyboard_path).read_text(encoding="utf-8")

    import re

    match = re.search(r"##\s*音频生成清单.*?(?=\n##\s+|\Z)", content, re.DOTALL)
    if not match:
        print("Error: 分镜中未找到 '音频生成清单' 部分")
        return []

    entries = []
    for raw_line in match.group(0).splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if "---" in line:
            continue

        cells = [clean_table_cell(cell) for cell in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0] == "幕号" or not cells[0].isdigit():
            continue

        filename = cells[1]
        text = cells[2]
        if filename and text:
            entries.append({"filename": filename, "text": text})

    print(f"✓ 解析分镜成功，共 {len(entries)} 条")
    return entries


def parse_input_file(input_path):
    """根据文件扩展名自动解析 CSV 或分镜 Markdown。"""
    input_path = Path(input_path)
    if input_path.suffix.lower() in {".md", ".markdown"}:
        return parse_storyboard_markdown(input_path)
    return parse_csv(input_path)


async def generate_all(input_path, output_dir, voice=DEFAULT_VOICE, rate=DEFAULT_RATE,
                       volume=DEFAULT_VOLUME, pitch=DEFAULT_PITCH):
    """批量生成音频"""
    # 解析 CSV 或分镜 Markdown
    entries = parse_input_file(input_path)
    if not entries:
        return False

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 生成音频
    results = []
    total = len(entries)

    print(f"\n开始生成音频 (声音: {voice}, 语速: {rate}, 音量: {volume}, 音高: {pitch})...")
    print("="*50)

    for i, entry in enumerate(entries, 1):
        filename = entry['filename']
        text = entry['text']

        # 确保文件扩展名正确
        if not filename.endswith(('.wav', '.mp3')):
            filename += '.wav'

        output_path = os.path.join(output_dir, filename)

        print(f"[{i}/{total}] {filename}")
        print(f"    文本: {text[:50]}{'...' if len(text) > 50 else ''}")

        success, duration = await generate_audio(text, output_path, voice, rate, volume, pitch)

        if success:
            # 从文件名提取幕号
            scene_num = extract_scene_number(filename)
            results.append({
                'scene': scene_num,
                'file': filename,
                'text': text,
                'duration': round(duration, 2)
            })
            print(f"    ✓ 时长: {duration:.2f}s")
        else:
            print(f"    ✗ 失败")

        print()

    # 生成 audio_info.json
    if results:
        info = {
            'files': results,
            'total_duration': sum(r['duration'] for r in results),
            'count': len(results),
            'voice': voice,
            'rate': rate,
            'volume': volume,
            'pitch': pitch
        }

        info_path = os.path.join(output_dir, 'audio_info.json')
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)

        print(f"已生成: {info_path}")

    return len(results) == len(entries)


def extract_scene_number(filename):
    """从文件名提取幕号"""
    # 支持格式: audio_001_xxx.wav, scene_01_xxx.wav, 001_xxx.wav
    import re
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return 0


def main():
    args = parse_cli_args(sys.argv[1:])
    input_path = args.input_file
    output_dir = args.output_dir

    # 检查文件
    if not os.path.exists(input_path):
        print(f"Error: 输入文件不存在: {input_path}")
        sys.exit(1)

    print(f"输入文件: {input_path}")
    print(f"输出目录: {output_dir}")
    print(f"使用声音: {args.voice}")
    print(f"语速/音量/音高: {args.rate} / {args.volume} / {args.pitch}")
    print("")

    # 运行
    success = asyncio.run(generate_all(input_path, output_dir, args.voice, args.rate, args.volume, args.pitch))

    if success:
        print("\n✅ 全部生成成功！")
        sys.exit(0)
    else:
        print("\n⚠️ 部分生成失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
