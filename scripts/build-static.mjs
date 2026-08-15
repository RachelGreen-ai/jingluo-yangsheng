import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { basename, join } from "node:path";

const root = process.cwd();
const outDir = join(root, "public");
const excludedNames = new Set([
  ".git",
  ".vercel",
  "node_modules",
  "public",
]);

rmSync(outDir, { force: true, recursive: true });
mkdirSync(outDir, { recursive: true });

for (const entry of [
  ".gitignore",
  "assets",
  "build",
  "face_landmarker.task",
  "index.html",
  "任脉.html",
  "手厥阴心包经.html",
  "手太阳小肠经.html",
  "手太阴肺经.html",
  "手少阳三焦经.html",
  "手少阴心经.html",
  "手阳明大肠经.html",
  "督脉.html",
  "穴位核对清单.md",
  "足厥阴肝经.html",
  "足太阳膀胱经.html",
  "足太阴脾经.html",
  "足少阳胆经.html",
  "足少阴肾经.html",
  "足阳明胃经.html",
]) {
  if (entry.startsWith(".env") || excludedNames.has(basename(entry))) {
    continue;
  }

  const source = join(root, entry);
  if (existsSync(source)) {
    cpSync(source, join(outDir, entry), { recursive: true });
  }
}
