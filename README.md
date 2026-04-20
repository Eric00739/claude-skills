# Claude Code Skills Collection

这个仓库存放我创建的 Claude Code Skills。

## Skills 列表

### khazix-writer

数字生命卡兹克开源的公众号长文写作 Skill，包含完整的写作风格规则、四层自检体系、内容方法论和风格示例库。

**使用方法：**
```bash
# 安装到本地
mkdir -p ~/.claude/skills/khazix-writer
cp khazix-writer/SKILL.md ~/.claude/skills/khazix-writer/
```

然后在 Claude Code 中输入 `/khazix-writer` 即可触发。

### wechat-article-formatter

将文章排版为微信公众号可用的 HTML 格式。

**设计特点：**
- 暖米色纸张背景 + 浅黄褐色外底
- 琥珀橙 (#d97706) 作为主色调
- 内联样式适配公众号编辑器限制
- 宽度 670px

**使用方法：**
```bash
# 安装到本地
mkdir -p ~/.claude/skills/wechat-article-formatter
cp wechat-article-formatter/SKILL.md ~/.claude/skills/wechat-article-formatter/
```

然后在 Claude Code 中输入 `/wechat-article-formatter` 即可触发。

### math-video-generator

自动生成数学教学视频的完整 Skill，包含8步工作流：数学分析→HTML可视化→分镜设计→TTS配音→验证→Manim脚手架→动画代码→视频渲染。

**功能特点：**
- ✅ 8步完整工作流自动化
- ✅ 支持自然语音（Edge-TTS 和 Qwen-TTS）
- ✅ 音画自动同步
- ✅ 1080p60高清输出

**使用方法：**
```bash
# 安装到本地
mkdir -p ~/.claude/skills/math-video-generator
cp -r math-video-generator/* ~/.claude/skills/math-video-generator/
```

然后直接向 Claude 提供数学题目即可自动触发，或使用 `/math-video-generator` 命令。

**触发条件：**
- 用户粘贴数学题图片
- 用户提供数学题文本
- 用户提到"数学视频"、"教学动画"、"数学讲解"
