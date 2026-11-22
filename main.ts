// gta6-meme-x-01 — entry bot.
// Copies POST.json (the X post URL for this meme entry) from the repo
// root into the harness output directory.
//
// The harness runs this file with Node 22 from the repo root (the bot
// directory). It only reads POST.json and writes one file; no network,
// no other input. If POST.json is missing or the output directory cannot
// be created, the entry is invalid, so we fail loudly instead of
// writing a partial output.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

try {
  mkdirSync(outDir, { recursive: true });
  copyFileSync(join(botDir, "POST.json"), join(outDir, "POST.json"));
  console.log("POST.json copied to", join(outDir, "POST.json"));
} catch (err) {
  // Surface the exact cause: a missing POST.json means the X post was
  // never linked, and an unwritable output dir means the harness cannot
  // grade this entry at all. Either way the entry must not pass silently.
  console.error(
    "failed to copy POST.json from bot dir",
    JSON.stringify(botDir),
    "to output dir",
    JSON.stringify(outDir),
    "-",
    err instanceof Error ? err.message : String(err),
  );
  process.exit(1);
}
