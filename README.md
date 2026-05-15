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

### gateremote-blog-article

GateRemoteSource 博客文章发布 Skill。用于把 Eric Huang 的 RF remote controls 文章草稿、图片和松散笔记整理成固定的网站 blog 格式，包含文章结构、WebP 图片规范、作者简介、评论区、阅读目录和发布检查流程。

**使用方法：**
```bash
# Claude Code
mkdir -p ~/.claude/skills/gateremote-blog-article
cp -R gateremote-blog-article/* ~/.claude/skills/gateremote-blog-article/

# Codex
mkdir -p ~/.codex/skills/gateremote-blog-article
cp -R gateremote-blog-article/* ~/.codex/skills/gateremote-blog-article/
```

然后输入 `用 gateremote-blog-article 处理这篇文章` 即可触发。

### de-AI-writing

中文写作、改写、润色、翻译和审阅的去 AI 味技能。在 good-writing 作者文风底座上做保真修补，清除路标词、二分对照壳、讲义腔、AI 隐喻、伪口语化和模板结构。

**支持任务类型：** 从零写、改写、翻译（保结构）、审稿、润色

**使用方法：**
```bash
mkdir -p ~/.claude/skills/de-AI-writing
cp -R de-AI-writing/* ~/.claude/skills/de-AI-writing/
```

然后在 Claude Code 中输入 `/de-AI-writing` 即可触发。

### good-writing

作者文风复现引擎。从真实作者文章中提取写作 DNA，提供半文半白、长短句节奏、类比先行等风格约束。

**使用方法：**
```bash
mkdir -p ~/.claude/skills/good-writing
cp -R good-writing/* ~/.claude/skills/good-writing/
```

然后在 Claude Code 中输入 `/good-writing` 即可触发。
