---
name: qwen3-forced-aligner
description: 使用 Qwen3 Forced Aligner 模型进行语音-文本强制对齐，生成精确的时间戳
version: 1.0.0
author: Eric
---

# Qwen3 Forced Aligner

Qwen3-ForcedAligner-0.6B 是一个非自回归语音强制对齐模型，支持 11 种语言的文本-语音对齐，可返回词/字符级时间戳。

## 功能

- 语音与文本的强制对齐
- 生成词级和字符级时间戳
- 支持 11 种语言：中文、英语、粤语、法语、德语、意大利语、日语、韩语、葡萄牙语、俄语、西班牙语
- 支持本地音频文件、URL、base64 数据
- 支持批量处理

## 前置要求

- Python 3.12+
- CUDA 支持（推荐）
- 约 2GB GPU 显存

## 安装

### 方法 1：使用 Skill 安装脚本（推荐）

```bash
# 进入 skill 目录
cd ~/.claude/skills/qwen3-forced-aligner

# 运行安装脚本
python install.py
```

### 方法 2：手动安装

```bash
# 创建虚拟环境
conda create -n qwen3-asr python=3.12 -y
conda activate qwen3-asr

# 安装 qwen-asr 包
pip install -U qwen-asr

# 可选：安装 FlashAttention 2 加速（推荐）
pip install -U flash-attn --no-build-isolation
```

## 使用方式

### 方式 1：作为 Claude Code Skill

在 Claude Code 对话中直接调用：

```
对齐这个音频文件: /path/to/audio.wav
文本: 甚至出现交易几乎停滞的情况。
语言: 中文
```

### 方式 2：Python API

```python
from qwen_asr import Qwen3ForcedAligner
import torch

# 加载模型
model = Qwen3ForcedAligner.from_pretrained(
    "Qwen/Qwen3-ForcedAligner-0.6B",
    dtype=torch.bfloat16,
    device_map="cuda:0",
)

# 执行对齐
results = model.align(
    audio="audio.wav",
    text="甚至出现交易几乎停滞的情况。",
    language="Chinese",
)

# 结果包含时间戳信息
for item in results:
    print(f"{item['text']}: {item['start']} - {item['end']}")
```

### 方式 3：命令行

```bash
# 激活环境
conda activate qwen3-asr

# 运行对齐脚本
python -c "
from qwen_asr import Qwen3ForcedAligner
import torch

model = Qwen3ForcedAligner.from_pretrained(
    'Qwen/Qwen3-ForcedAligner-0.6B',
    dtype=torch.bfloat16,
    device_map='cuda:0',
)

results = model.align(
    audio='audio.wav',
    text='甚至出现交易几乎停滞的情况。',
    language='Chinese',
)

print(results)
"
```

## 输入格式

- **音频**: 本地路径、URL、base64 编码数据、`(numpy.ndarray, sample_rate)` 元组
- **文本**: 纯文本字符串
- **语言**: 语言名称（如 "Chinese", "English" 等）

## 输出格式

返回包含以下字段的列表：

```python
[
    {
        "text": "词或字符",
        "start": 0.0,    # 开始时间（秒）
        "end": 1.23,     # 结束时间（秒）
    },
    ...
]
```

## 支持的模型

| 模型 | 大小 | 用途 |
|------|------|------|
| Qwen/Qwen3-ForcedAligner-0.6B | 0.6B | 强制对齐专用模型 |

## 相关资源

- [Qwen3-ASR GitHub](https://github.com/QwenLM/Qwen3-ASR)
- [Hugging Face 模型](https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B)
- [ModelScope 模型](https://modelscope.cn/models/Qwen/Qwen3-ForcedAligner-0.6B)
