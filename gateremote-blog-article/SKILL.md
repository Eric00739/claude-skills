---
name: gateremote-blog-article
description: Standardize GateRemoteSource blog article publishing. Use when the assistant is asked to turn Eric Huang's draft, pasted article text, loose notes, or image set into a publish-ready GateRemote blog post with the site's fixed article structure, compressed WebP images, author bio, comments box, responsive reading-map sidebar, and GitHub-ready implementation.
---

# GateRemote Blog Article

## Overview

Use this skill to convert rough or polished RF remote-control article drafts into the fixed GateRemoteSource blog format. Keep Eric Huang's practical, experience-based voice while making the article readable, credible, responsive, and consistent with the existing site.

For the detailed house format, read `references/blog-format.md` before editing an article.

## Workflow

1. Read the repo first. Confirm current blog data shape in `src/data/blog.ts`, article page template in `src/app/[locale]/blog/[slug]/page.tsx`, and shared components such as `AuthorBio` and `BlogCommentBox`.
2. Preserve the user's article meaning. Edit structure, headings, rhythm, and image placement, but do not invent technical claims, test results, certifications, customer stories, or product specs.
3. Create or update one article entry in `src/data/blog.ts`. Use a clean SEO slug, real date, category, excerpt, read time, hero image, author, and structured `content` blocks.
4. Place article images under `public/images/blog/<slug>/`. Do this automatically; do not ask the user where images should go.
5. Run the bundled image collector when image files are not already in the article folder. From the website repo root:
   `node ~/.codex/skills/gateremote-blog-article/scripts/collect-blog-images.mjs --slug <slug> --count <n> --names hero,section-one,section-two`
6. Convert originals to compressed WebP, preserve aspect ratio, and reference the final WebP paths from content blocks.
7. Keep the article page template fixed: compact hero, readable article column, responsive reading map, comments box after the article body, author bio after comments, and final CTA.
8. Verify with `npm run lint` and `npm run build`. For visual changes, inspect desktop and mobile widths in the browser and check for horizontal overflow.
9. Stage only relevant article/code/image files. Do not include previews, raw source images, screenshots, or unrelated untracked assets unless the user explicitly asks.

## Image Intake Automation

- Always create `public/images/blog/<slug>/` first.
- If the user provides explicit image paths, pass them to the collector with `--images path1,path2`.
- If images were pasted, downloaded, or sent through WeChat without clean paths, run the collector before asking for help. It scans recent files from Downloads, Desktop, and WeChat temp folders, prioritizing `InputTemp` and `RWTemp`.
- Use semantic output names that match the article structure, such as `shared-rf-channel`, `collision-scenarios`, `anti-collision-techniques`, and `rf-system-evolution`.
- If the collector finds more candidates than needed, use the most recent relevant files and verify dimensions/content with `view_image` when necessary.
- Ask for image paths only after the automated scan finds no usable local images or finds unrelated files only.

## Fixed Page Rules

- Desktop: show the sticky reading map in the right rail with numbered sections, section count, read time, and comments shortcut.
- Mobile/tablet: show a compact collapsible reading map near the top of the article.
- Heading anchors must be unique. If two headings share the same text, suffix later anchor IDs instead of duplicating IDs.
- Avoid duplicate comment shortcuts in the same right rail. Keep the primary comments shortcut inside the reading map.
- Comments: label as `Comments`, keep the form visible and responsive, and route submissions through the existing email-draft behavior unless the user asks for a real backend.
- Author: always include Eric Huang's avatar and bio, but keep the card compact so it supports trust without interrupting reading.
- Hero: keep it concise. Do not make the article header feel like a landing-page hero.
- Images: use 16:9 article visuals where possible, compressed WebP, descriptive alt text, and captions only when they add context.

## Quality Bar

- Make the article feel like an expert note from a factory/export practitioner, not a generic SEO post.
- Prefer short paragraphs and meaningful headings.
- Keep all UI responsive at common widths: 390px, 768px, and 1440px.
- Avoid fake filler articles, fake testimonials, fake stats, or decorative UI that does not improve reading.
- When unsure where to place an image, place it after the section that first introduces that concept.
