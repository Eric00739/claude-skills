# Tutor_Plus - 数学教学视频制作

Tutor_Plus 用于把数学题处理成 HTML/SVG 讲解资料、分镜脚本、TTS 配音和 Manim 教学视频。

## 主要改进

- `generate_tts.py` 同时支持 `audio_list.csv` 和分镜 Markdown 的"音频生成清单"。
- `init.py` 会把 `scripts/`、`requirements.txt` 和脚手架一起复制到新项目，初始化后可直接运行。
- `check.py` 与 `script_scaffold.py` 保持一致，不再要求不存在的 `Subtitle` / `TitleSubtitle` 类。
- 脚手架默认通过 `add_scene_audio()` 添加音频，避免无声视频。
- 新增 `scripts/extract_frames.py` 用于渲染后抽取关键帧复查。

## 使用方式

```bash
# 初始化一个课程视频项目
python init.py my_lesson
cd my_lesson

# 安装依赖
uv venv .venv
uv pip install -r requirements.txt

# 生成配音，支持 CSV 或分镜 Markdown
python scripts/generate_tts.py audio_list.csv ./audio
python scripts/generate_tts.py 分镜.md ./audio --voice xiaoxiao

# 验证音频并回填分镜时长
python scripts/validate_audio.py 分镜.md ./audio

# 检查并渲染
python scripts/check.py script.py
python scripts/render.py -f script.py -s MathScene -q h --no-preview
```

## 目录说明

- `SKILL.md` - Tutor_Plus 工作流和使用规则
- `init.py` - 新项目初始化脚本
- `scripts/` - TTS、音频验证、代码检查、渲染和关键帧抽取脚本
- `templates/` - Manim 脚手架和示例
- `references/` - 分镜参考
- `sample/` - 旧版完整示例，仅作参考
