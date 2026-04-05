# 微信公众号文章排版

将文章排版为微信公众号可用的 HTML 格式。

## 设计特点

- 暖米色纸张背景 + 浅黄褐色外底
- 琥珀橙 (#d97706) 作为主色调，用于高亮、引用线、卡片标题等
- 清晰的信息层级：标题/正文/引用块/卡片/列表/分隔线
- 适配公众号编辑器限制：纯内联样式，宽度 670px
- 在公众号编辑器中使用时只复制内容部分

## 色板

- 外底：#e8e4dc (浅灰褐)
- 纸张：#fffef9 (暖白)
- 正文：#2d2d2d
- 标题：#1a1a1a
- 主色/高亮：#d97706 (琥珀橙)
- 高亮背景：#fef6f6 (浅暖粉)
- 次级文字：#5c2a2a
- 分隔线：#ddd

## HTML 模板

使用时按以下模板替换内容，所有样式使用内联 style：

```html
<div style="background:#e8e4dc; padding:40px 20px; font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;">
<div style="background:#fffef9; max-width:670px; margin:0 auto; box-shadow:0 2px 20px rgba(0,0,0,0.1); padding:40px 30px 50px;">

  <!-- 大标题 -->
  <div style="font-size:24px; line-height:1.5; color:#1a1a1a; font-weight:900; text-align:center; margin:20px 0 8px; letter-spacing:2px;">
    文章标题
  </div>
  <div style="font-size:12px; line-height:1.6; color:#aaa; margin:0 0 30px; text-align:center; letter-spacing:3px;">
    副标题/描述
  </div>

  <!-- 正文段落 -->
  <p style="font-size:16px; line-height:1.9; color:#2d2d2d; margin:16px 0; letter-spacing:0.2px; text-align:justify;">
    段落内容。<span style="color:#d97706; font-weight:bold;">橙色高亮文字</span>
  </p>

  <!-- 分隔线 -->
  <div style="text-align:center; font-size:14px; color:#ddd; letter-spacing:12px; margin:30px 0; user-select:none;">· · ·</div>

  <!-- 引用块 -->
  <div style="border-left:4px solid #d97706; padding:14px 18px; margin:24px 0; background:#fef6f6; border-radius:2px;">
    <p style="font-size:15px; color:#5c2a2a; line-height:1.85; margin:0; font-style:italic;">引用文字</p>
  </div>

  <!-- 小节标题 -->
  <div style="font-size:18px; line-height:1.5; color:#1a1a1a; font-weight:800; margin:28px 0 16px; text-align:center; letter-spacing:1px;">小节标题</div>

  <!-- 卡片容器 -->
  <div style="background:#fafaf9; border:1px solid #e7e5e4; border-radius:4px; padding:18px 20px; margin:24px 0;">
    
    <!-- 卡片标题 -->
    <div style="font-size:16px; color:#1a1a1a; font-weight:700; text-align:center; margin:0 0 14px; padding-bottom:10px; border-bottom:2px solid #d97706;">卡片标题</div>
    
    <!-- 案例标题 -->
    <div style="font-weight:700; color:#1a1a1a; font-size:16px; margin-bottom:10px;">案例：XXX</div>
    
    <!-- 编号行 -->
    <div style="display:flex; align-items:baseline; margin:12px 0; line-height:1.8; font-size:15px;">
      <span style="display:inline-block; width:20px; height:20px; line-height:20px; text-align:center; background:#d97706; color:#fff; font-size:12px; font-weight:700; border-radius:3px; margin-right:10px; flex-shrink:0;">1</span>
      <span>内容</span>
    </div>
  </div>

  <!-- 无序列表 -->
  <ul style="font-size:15px; line-height:2; color:#2d2d2d; padding-left:20px; margin:12px 0; list-style:disc;">
    <li><strong>加粗项</strong>：说明文字</li>
  </ul>

  <!-- 结尾 CTA -->
  <div style="text-align:center; margin:30px 0 10px; padding:22px 18px; border-top:2px solid #d97706; border-bottom:2px solid #d97706; background:#fef6f6;">
    <span style="font-size:12px; color:#ddd; letter-spacing:6px; margin-bottom:14px; display:block;">标 签</span>
    <p style="font-size:15px; color:#5c2a2a; margin:6px 0; text-align:center;">内容</p>
    <p style="font-size:18px; font-weight:800; color:#d97706; letter-spacing:2px; margin-top:10px;">金句</p>
  </div>

</div>
</div>
```

## 使用步骤

1. 根据上面的模板，把文章内容套用对应的 HTML 结构
2. 确保所有文字用 `style` 内联（公众号不支持外部 CSS 文件）
3. 在公众号编辑器中切换到"HTML 源码"模式
4. 将完整 HTML 粘贴进去
5. 切换回编辑模式即可看到效果

## 注意事项

- 公众号图片需用公众号自带图片上传功能，不能用外部链接
- 所有文字字号不要小于 14px，否则手机上阅读困难
- 段落之间保持 16px margin
- 高亮色统一使用 `#d97706`（琥珀橙）