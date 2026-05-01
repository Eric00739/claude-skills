# GateRemoteSource Blog Format

## Content Model

Use `src/data/blog.ts` as the source of truth. Each real article should include:

- `slug`: lowercase, hyphenated, stable SEO slug.
- `title`: specific, experience-led title.
- `excerpt`: one sentence explaining the practical problem.
- `category`: usually `rf-engineering` for RF design articles.
- `publishedAt`: ISO date string.
- `readTime`: realistic estimate.
- `author`: `Eric Huang`.
- `image`: hero image path.
- `content`: structured blocks only.

Supported content block types:

- `paragraph`: normal article prose.
- `heading`: becomes an `h2` and appears in the reading map.
- `list`: use for concrete checks, symptoms, causes, or sourcing criteria.
- `callout`: use sparingly for a key engineering or sourcing principle.
- `quote`: use for one strong thesis sentence.
- `image`: include `src`, `alt`, and optional `caption`.

## Article Structure

Recommended sequence:

1. Opening problem: start with the real business or engineering pain.
2. First image: hero or conceptual visual after the opening setup.
3. Technical sections: each major concept gets one clear `heading`.
4. Practical sourcing or manufacturing implication: connect circuit details to buyer risk.
5. Closing argument: reliability, repeatability, margin, or trust.
6. Comments box: invite RF questions and real project problems.
7. Author bio: compact trust block with Eric's avatar and experience.
8. Final CTA: existing help/contact block.

## Reading Map

The article template should keep the fixed reading-map behavior:

- Desktop right rail: `Reading map`, `Article sections`, numbered links, section count, read time, comments shortcut.
- Mobile/tablet: collapsible `Reading map` before the main body.
- Keep link text from actual article headings.
- Keep generated heading IDs unique even when headings repeat.
- Show no more than 9 desktop links and no more than 12 mobile links unless the design is intentionally revised.
- If the article has more links than the visible limit, show a small overflow note instead of making the sidebar too tall.

## Image Rules

- Store article assets in `public/images/blog/<slug>/`.
- Create that folder automatically for every new article. The user should not need to decide the destination.
- Before asking for image paths, run `scripts/collect-blog-images.mjs` from the skill to scan recent Downloads, Desktop, and WeChat temp images, then convert the selected images into the article folder.
- Convert user-provided PNG/JPG to WebP before publishing.
- Prefer 16:9 images for article visuals.
- Keep original aspect ratio; do not crop in a way that distorts labels, instruments, boards, or remote controls.
- Use descriptive alt text such as `433 MHz transmitter module with crystal oscillator and matching circuit`.
- Do not upload raw preview images unless explicitly requested.

## Image Collector

Use this pattern from the website repo root:

```bash
node ~/.codex/skills/gateremote-blog-article/scripts/collect-blog-images.mjs \
  --slug rf-remote-control-concurrency-anti-collision \
  --count 4 \
  --names shared-rf-channel,collision-scenarios,anti-collision-techniques,rf-system-evolution
```

Useful options:

- `--images path1,path2`: use explicit source files first.
- `--sources dir1,dir2`: scan specific directories.
- `--sinceMinutes 240`: adjust the recent-file search window.
- `--dry-run`: list candidates without writing files.

After conversion, use `view_image` or a browser check to confirm the selected WebP files match the intended article sections.

## Verification

Run:

```bash
npm run lint
npm run build
```

For visual changes, inspect at:

- 390px mobile
- 768px tablet
- 1440px desktop

Check that:

- There is no horizontal overflow.
- Article images are not distorted.
- Comments and author bio are visible.
- The reading map exists on desktop and has a mobile fallback.
