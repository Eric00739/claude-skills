# 微信公众号文章排版

将文章排版为微信公众号可用的 HTML 格式。

## 设计特点

- 暖米色纸张背景 (#fffef8) + 浅褐外底 (#f5f0e8)
- 琥珀橙 (#d97706) 作为主色调，金色 (#fcd34d) 作为点缀
- 衬线字体 (Georgia/Songti) 增加质感
- 小节编号 + 渐变分隔线
- 微信兼容：不用 flexbox、border-radius
- 宽度 680px

## 色板

| 元素 | 颜色 |
|------|------|
| 外底 | #f5f0e8 |
| 纸张 | #fffef8 |
| 正文 | #333333 |
| 标题 | #1a1a1a |
| 主色 | #d97706 |
| 金色 | #fcd34d |
| 引用背景 | #fff7ed |
| 卡片背景 | #faf8f5 |

---

## 必用元素

### 顶部装饰条

```html
<div style="height:4px; background:linear-gradient(to right, #d97706, #f59e0b, #d97706);"></div>
```

### 大标题

```html
<div style="font-size:26px; line-height:1.45; color:#1a1a1a; font-weight:700; text-align:center; margin:24px 0 12px; letter-spacing:0.5px;">
  文章标题
</div>
```

### 副标题标签

```html
<div style="text-align:center; margin:0 0 8px;">
  <span style="display:inline-block; font-size:11px; color:#d97706; letter-spacing:3px; padding:4px 16px; border:1px solid #d97706;">分类标签</span>
</div>
<div style="font-size:13px; color:#999; margin:0 0 36px; text-align:center; font-style:italic;">
  描述/导语
</div>
```

### 正文段落

```html
<p style="font-size:16px; line-height:2; color:#333; margin:18px 0; text-align:justify;">
  段落内容。<span style="color:#d97706; font-weight:600;">高亮文字</span>
</p>
```

### 分隔线（三点渐变）

```html
<div style="text-align:center; margin:44px 0;">
  <span style="display:inline-block; width:8px; height:8px; background:#d97706; margin:0 6px;"></span>
  <span style="display:inline-block; width:8px; height:8px; background:#d97706; opacity:0.5; margin:0 6px;"></span>
  <span style="display:inline-block; width:8px; height:8px; background:#d97706; opacity:0.25; margin:0 6px;"></span>
</div>
```

### 小节标题（带编号）

```html
<div style="margin:36px 0 20px;">
  <div style="font-size:14px; color:#d97706; letter-spacing:2px; margin-bottom:8px;">01</div>
  <div style="font-size:19px; color:#1a1a1a; font-weight:700; line-height:1.4;">
    小节标题
  </div>
</div>
```

---

## 可选元素

### 引用块（带引号装饰）

```html
<div style="margin:28px 0; padding:24px 28px; background:linear-gradient(135deg, #fff7ed 0%, #fffbf5 100%); position:relative;">
  <div style="position:absolute; top:12px; left:20px; font-size:48px; color:#d97706; opacity:0.2; font-family:Georgia,serif; line-height:1;">"</div>
  <p style="font-size:17px; color:#78350f; line-height:1.9; margin:0; padding-left:24px; font-style:italic;">
    引用文字
  </p>
</div>
```

### 金句块（深色反白）

```html
<div style="margin:28px 0; padding:20px 24px; background:#1a1a1a; text-align:center;">
  <p style="font-size:16px; color:#fcd34d; line-height:1.8; margin:0; font-style:italic;">
    金句内容
  </p>
</div>
```

### 信息卡片

```html
<div style="background:#faf8f5; padding:20px 24px; margin-bottom:12px; border-left:3px solid #d97706;">
  <div style="font-size:14px; color:#d97706; font-weight:600; margin-bottom:6px;">卡片标题</div>
  <div style="font-size:14px; color:#555; line-height:1.7;">卡片内容</div>
</div>
```

### 故事块（案例展示）

```html
<div style="margin:32px 0; padding:0; position:relative;">
  <div style="position:absolute; left:0; top:0; bottom:0; width:3px; background:linear-gradient(to bottom, #d97706, #fcd34d);"></div>
  <div style="padding:24px 24px 24px 28px; background:#fefce8;">
    <p style="font-size:13px; color:#92400e; margin:0 0 12px; font-weight:600; letter-spacing:1px;">真实案例</p>
    <p style="font-size:15px; line-height:1.9; color:#444; margin:0 0 12px;">故事内容</p>
    <p style="font-size:12px; color:#d97706; margin:16px 0 0; text-align:right;">—— 来源</p>
  </div>
</div>
```

### 解决方案卡片

```html
<div style="margin-bottom:16px; padding:20px 24px; background:#faf8f5;">
  <div style="margin-bottom:10px;">
    <span style="display:inline-block; width:24px; height:24px; line-height:24px; text-align:center; background:#d97706; color:#fff; font-size:13px; font-weight:700; margin-right:10px; vertical-align:middle;">1</span>
    <strong style="font-size:16px; color:#1a1a1a;">标题</strong>
  </div>
  <p style="font-size:14px; line-height:1.8; color:#555; margin:0; padding-left:34px;">
    说明内容
  </p>
</div>
```

### 代码块

```html
<div style="margin:12px 0; padding:12px 16px; background:#292524; color:#fcd34d; font-family:Consolas,Monaco,monospace; font-size:14px;">
  /context list
</div>
```

### 行内代码

```html
<span style="padding:2px 6px; background:#f5f0e6; color:#d97706; font-family:Consolas,Monaco,monospace; font-size:14px;">/context list</span>
```

### 结尾标记

```html
<div style="text-align:center; margin:48px 0 0; padding-top:32px; border-top:1px solid #e8e0d4;">
  <div style="font-size:14px; color:#999; letter-spacing:6px;">— 完 —</div>
</div>
```

### 底部装饰条

```html
<div style="height:4px; background:linear-gradient(to right, #d97706, #f59e0b, #d97706);"></div>
```

---

## 微信兼容要点

| 问题 | 解决方案 |
|------|----------|
| 不支持 flexbox | 用 inline-block + vertical-align |
| 不支持 border-radius | 不用圆角 |
| 渐变背景 | 用 linear-gradient 可以 |
| 分隔点 | 用 span + inline-block 实现 |
| 字体 | Georgia/Songti SC 衬线字体 |

---

## 使用步骤

1. 用顶部装饰条开始
2. 标题 + 副标题标签
3. 正文段落（行高 2.0）
4. 小节用编号标题 + 分隔线
5. 引用/卡片/故事块按需使用
6. 结尾标记 + 底部装饰条
7. 在公众号编辑器切换 HTML 源码模式粘贴