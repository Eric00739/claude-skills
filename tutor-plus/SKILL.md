---
name: tutor-plus
description: |
  数学一对一辅导与视频制作技能。用于解答数学题、生成 HTML/SVG 讲解资料、规划分镜、生成亲和自然的 TTS 配音，并把分镜实现为带音频的 Manim 教学视频。适用于学生粘贴数学题图片/文字、需要小学生也能听懂的可视化讲解、需要带配音教学视频的任务。
---

# tutor-plus

## 目标

把数学题处理成可讲、可看、可验证的视频制作项目：

1. 先完成数学分析，明确已知条件、推导事实、证明目标和作图方法。
2. 用 HTML + SVG 做静态可视化讲义，确认图形和解题路径。
3. 写分镜脚本，拆成若干幕，每幕包含画面、字幕、读白、动画和目的；读白要像亲和女老师给小学生讲题。
4. 从分镜或 CSV 生成 TTS 音频，并记录每幕真实时长；默认使用慢速女声，方便孩子听清。
5. 根据分镜和音频时长实现 Manim 动画，确保画面等待音频。
6. 运行结构检查、渲染视频、抽取关键帧复查。

## 快速流程

新建项目：

```bash
python init.py my_lesson
cd my_lesson
uv venv .venv
uv pip install -r requirements.txt
```

生成音频，二选一：

```bash
python scripts/generate_tts.py audio_list.csv ./audio
python scripts/generate_tts.py 分镜.md ./audio
```

默认语音为 `xiaoxiao`，语速 `-8%`。如需调整，可显式传入 `--voice`、`--rate`、`--volume`、`--pitch`。

验证音频并回填时长：

```bash
python scripts/validate_audio.py 分镜.md ./audio
```

检查和渲染：

```bash
python scripts/check.py script.py
python scripts/render.py -f script.py -s MathScene -q h --no-preview
python scripts/extract_frames.py media/videos/script/1080p60/MathScene.mp4 --interval 5
```

## 分镜格式

分镜必须包含"音频生成清单"，这样 `generate_tts.py` 和 `validate_audio.py` 能直接读取：

```markdown
## 音频生成清单

| 幕号 | 文件名 | 读白文本 | 时长 | 说话人 | 情感 |
|------|--------|----------|------|--------|------|
| 1 | audio_001_开场.wav | "我们先看看题目里告诉了什么。" | | xiaoxiao | 亲切、慢速 |
| 2 | audio_002_关键一步.wav | "别急着算，先想想水为什么会上升。" | | xiaoxiao | 鼓励、引导 |
```

规则：

- 幕号从 1 开始连续编号。
- 文件名格式用 `audio_001_幕名.wav` 或 `.mp3`，与实际生成文件保持一致。
- 时长列先留空，由 `validate_audio.py` 回填。
- 字幕保持短句，读白要自然口语化。写读白前先阅读 `references/narration_style.md`。
- 每幕只讲一个核心点，读白优先使用"我们先看..."、"你发现了吗？"、"别急，先想一想"这类亲切引导。
- 在"动画"字段写清退场时间，避免文字残留，例如 `3.0s: → 字幕退场`。

## Manim 实现规则

- 从 `templates/script_scaffold.py` 生成 `script.py`，不要从空白文件手写。
- 每幕开头调用 `self.add_scene_audio(scene_num)`，确保视频包含声音。
- 动画总时长必须大于等于该幕音频时长；如果动画太短，用 `self.wait()` 补齐。
- 配音提到什么，画面就高亮什么。提到边长就高亮边，提到点就高亮点，提到结论就强调结论。
- 使用 `create_subtitle()`、`show_subtitle_timed()`、`show_subtitle_with_audio()` 管理字幕，幕结束前清掉文字。
- 所有几何计算放在 `calculate_geometry()`，所有关键条件和画布范围检查放在 `assert_geometry()`。
- 用 2D 坐标组织几何数据，传给 Manim 时再转成 `(x, y, 0)`。

## 数学讲解原则

- 面向小学生时，按"生活/实物现象 → 数量关系 → 图形模型 → 算式 → 回答问题"推进。
- 先让孩子看懂题意，再写公式；先问"为什么这样算"，再给计算过程。
- 一屏只解决一个认知目标。不要把已知条件、图形、公式和结论都挤在同一处。
- 读白要像老师在旁边轻声带着想，不要像教材定义或论文证明。
- 解题说明优先使用定义、定理、相似、等积、旋转、对称、勾股等几何推理。
- 坐标可以服务于动画定位，但不要把坐标法写成主要证明思路，除非用户明确要求。
- 证明题中要先列出"已知条件、要证结论、可用事实、证明路线"。
- 如果题目图片信息不足，先指出缺失条件，再给出可继续推进的假设。

## 质量检查

渲染前必须运行：

```bash
python scripts/check.py script.py
```

检查重点：

- 存在 `calculate_geometry()`、`assert_geometry()`、`define_elements()`。
- 存在继承 `Scene` 的场景类。
- 存在 `add_sound()` 调用路径。
- 保留脚手架里的音频和字幕辅助方法。

渲染后复查：

- 音频是否逐幕出现，没有静音幕。
- 画面是否等待音频，没有截断。
- 字幕是否清晰，且没有残留到下一幕。
- 读白是否自然、不生硬，是否符合亲和女老师讲给小学生听的语气。
- 几何图形是否在画布内，关键点线是否与讲解同步高亮。

## 参考资源

- `templates/script_scaffold.py`：推荐脚手架。
- `templates/script_example.py`：完整示例。
- `references/narration_style.md`：小学生数学视频的读白、语气和配音规范。
- `references/storyboard_sample.md`：分镜样例。
- `sample/geometry_proof/`：旧版完整项目，可参考风格，不要照抄路径约定。
