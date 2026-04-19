#!/usr/bin/env python3
"""
使用示例：批量对齐多个音频文件
"""

from qwen_asr import Qwen3ForcedAligner
import torch
import json


def batch_align(audio_text_pairs, language="Chinese"):
    """
    批量对齐多个音频-文本对

    Args:
        audio_text_pairs: 列表，每个元素是 (audio_path, text) 元组
        language: 语言

    Returns:
        结果列表
    """
    # 加载模型（只需加载一次）
    model = Qwen3ForcedAligner.from_pretrained(
        "Qwen/Qwen3-ForcedAligner-0.6B",
        dtype=torch.bfloat16,
        device_map="cuda:0",
    )

    results = []
    for audio_path, text in audio_text_pairs:
        print(f"处理: {audio_path}")
        result = model.align(
            audio=audio_path,
            text=text,
            language=language,
        )
        results.append({
            "audio": audio_path,
            "text": text,
            "alignment": result
        })

    return results


def save_to_srt(results, output_path):
    """保存对齐结果为 SRT 字幕格式"""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, item in enumerate(results["alignment"], 1):
            start = item["start"]
            end = item["end"]
            text = item["text"]

            # 转换为 SRT 时间格式
            def to_srt_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                millis = int((seconds % 1) * 1000)
                return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

            f.write(f"{i}\n")
            f.write(f"{to_srt_time(start)} --> {to_srt_time(end)}\n")
            f.write(f"{text}\n\n")


if __name__ == "__main__":
    # 示例：对齐单个文件
    model = Qwen3ForcedAligner.from_pretrained(
        "Qwen/Qwen3-ForcedAligner-0.6B",
        dtype=torch.bfloat16,
        device_map="cuda:0",
    )

    result = model.align(
        audio="example.wav",
        text="这是一个示例文本，用于演示强制对齐功能。",
        language="Chinese",
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 示例：批量对齐
    # pairs = [
    #     ("audio1.wav", "第一段文本"),
    #     ("audio2.wav", "第二段文本"),
    # ]
    # results = batch_align(pairs)
    # for r in results:
    #     print(f"{r['audio']}: {len(r['alignment'])} 个对齐项")
