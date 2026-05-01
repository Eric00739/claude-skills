#!/usr/bin/env node

import { createRequire } from 'node:module';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';

const requireFromCwd = createRequire(path.join(process.cwd(), 'package.json'));

function parseArgs(argv) {
  const args = {
    count: 4,
    dryRun: false,
    minBytes: 80_000,
    names: [],
    images: [],
    project: process.cwd(),
    quality: 82,
    sinceMinutes: 240,
    sources: [],
    width: 1920,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const next = argv[index + 1];

    if (arg === '--dry-run') {
      args.dryRun = true;
      continue;
    }

    if (!arg.startsWith('--')) continue;
    if (!next || next.startsWith('--')) {
      throw new Error(`Missing value for ${arg}`);
    }

    index += 1;
    const key = arg.slice(2);
    if (['count', 'minBytes', 'quality', 'sinceMinutes', 'width'].includes(key)) {
      args[key] = Number(next);
    } else if (['images', 'names', 'sources'].includes(key)) {
      args[key] = next.split(',').map((item) => item.trim()).filter(Boolean);
    } else {
      args[key] = next;
    }
  }

  if (!args.slug) {
    throw new Error('Missing --slug <article-slug>');
  }

  return args;
}

function expandHome(inputPath) {
  if (!inputPath) return inputPath;
  if (inputPath === '~') return os.homedir();
  if (inputPath.startsWith('~/')) return path.join(os.homedir(), inputPath.slice(2));
  return inputPath;
}

async function pathExists(inputPath) {
  try {
    await fs.access(inputPath);
    return true;
  } catch {
    return false;
  }
}

async function collectFiles(root, options, depth = 0) {
  if (depth > options.maxDepth || !(await pathExists(root))) return [];

  const entries = await fs.readdir(root, { withFileTypes: true }).catch(() => []);
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(root, entry.name);
    if (entry.isDirectory()) {
      files.push(...await collectFiles(fullPath, options, depth + 1));
      continue;
    }

    if (!entry.isFile()) continue;
    if (!/\.(png|jpe?g|webp)$/i.test(entry.name)) continue;

    const stat = await fs.stat(fullPath).catch(() => null);
    if (!stat) continue;
    if (stat.size < options.minBytes) continue;
    if (stat.mtimeMs < options.sinceMs) continue;

    files.push({ path: fullPath, size: stat.size, mtimeMs: stat.mtimeMs });
  }

  return files;
}

function defaultSourceRoots() {
  const home = os.homedir();
  return [
    path.join(home, 'Downloads'),
    path.join(home, 'Desktop'),
    path.join(home, 'Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files'),
  ];
}

function scoreCandidate(candidate) {
  const normalized = candidate.path.toLowerCase();
  let score = candidate.mtimeMs;

  if (normalized.includes('/temp/inputtemp/')) score += 10_000_000;
  if (normalized.includes('/temp/rwtemp/')) score += 8_000_000;
  if (normalized.includes('/downloads/')) score += 2_000_000;
  if (normalized.includes('/thumb/')) score -= 20_000_000;
  if (normalized.includes('/cache/')) score -= 5_000_000;

  return score;
}

async function findCandidates(args) {
  const sinceMs = Date.now() - args.sinceMinutes * 60 * 1000;
  const explicit = [];

  for (const imagePath of args.images.map(expandHome)) {
    const stat = await fs.stat(imagePath).catch(() => null);
    if (stat?.isFile()) {
      explicit.push({ path: imagePath, size: stat.size, mtimeMs: stat.mtimeMs });
    }
  }

  const sourceRoots = (args.sources.length > 0 ? args.sources : defaultSourceRoots()).map(expandHome);
  const scannedGroups = await Promise.all(sourceRoots.map((root) => collectFiles(root, {
    maxDepth: root.includes('xwechat_files') ? 9 : 2,
    minBytes: args.minBytes,
    sinceMs,
  })));

  const seen = new Set();
  return [...explicit, ...scannedGroups.flat()]
    .filter((candidate) => {
      if (seen.has(candidate.path)) return false;
      seen.add(candidate.path);
      return true;
    })
    .sort((left, right) => scoreCandidate(right) - scoreCandidate(left))
    .slice(0, args.count);
}

async function loadSharp() {
  try {
    const sharpPath = requireFromCwd.resolve('sharp');
    const sharpModule = await import(sharpPath);
    return sharpModule.default || sharpModule;
  } catch {
    throw new Error('The image collector needs sharp. Run it from the website repo after dependencies are installed.');
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const projectRoot = path.resolve(expandHome(args.project));
  const outputDir = path.join(projectRoot, 'public/images/blog', args.slug);
  const candidates = await findCandidates(args);

  if (candidates.length === 0) {
    throw new Error('No recent source images found. Check image files were saved locally, or pass --images path1,path2.');
  }

  console.log(`Found ${candidates.length} image candidate(s):`);
  for (const candidate of candidates) {
    console.log(`- ${candidate.path}`);
  }

  if (args.dryRun) return;

  const sharp = await loadSharp();
  await fs.mkdir(outputDir, { recursive: true });

  for (let index = 0; index < candidates.length; index += 1) {
    const candidate = candidates[index];
    const baseName = args.names[index] || `article-image-${index + 1}`;
    const safeName = baseName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || `article-image-${index + 1}`;
    const outputPath = path.join(outputDir, `${safeName}.webp`);

    await sharp(candidate.path)
      .rotate()
      .resize({ width: args.width, withoutEnlargement: true })
      .webp({ quality: args.quality })
      .toFile(outputPath);

    console.log(`Wrote /images/blog/${args.slug}/${safeName}.webp`);
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
