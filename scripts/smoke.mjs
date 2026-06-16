// Headless smoke test — render every hash route and fail on console errors,
// page errors, HTTP >= 400, or suspiciously empty pages. Screenshots each route.
//
// Usage:
//   1) npm run build && npm run preview   (or: npm run dev) in another terminal
//   2) node scripts/smoke.mjs [baseURL]   (default http://localhost:4173)
//
// Uses puppeteer-core with the system Chrome/Edge (no Chromium download).
import { existsSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join } from "node:path";
import { launch } from "puppeteer-core";

const BASE = process.argv[2] || "http://localhost:4173";
const OUT = fileURLToPath(new URL("../.screenshots/", import.meta.url));

const routes = [
  ["skills", "/#/skills"],
  ["combos", "/#/combos"],
  ["practice", "/#/practice"],
  ["addons", "/#/addons"],
  ["tricks", "/#/tricks"],
  ["dps", "/#/dps"],
  ["reference", "/#/reference"],
  ["r1", "/#/r1"],
];

const CHROME_CANDIDATES = [
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
];

function findChrome() {
  for (const p of CHROME_CANDIDATES) if (existsSync(p)) return p;
  throw new Error("No Chrome/Edge found in: " + CHROME_CANDIDATES.join(", "));
}

mkdirSync(OUT, { recursive: true });

const browser = await launch({
  executablePath: findChrome(),
  headless: "new",
  args: ["--no-sandbox", "--disable-gpu"],
});

let failures = 0;
const page = await browser.newPage();
await page.setViewport({ width: 1400, height: 1000 });

for (const [name, route] of routes) {
  const errors = [];
  const onConsole = (msg) => { if (msg.type() === "error") errors.push("console: " + msg.text()); };
  const onPageError = (err) => errors.push("pageerror: " + err.message);
  const onResponse = (res) => { if (res.status() >= 400) errors.push(`http ${res.status()}: ${res.url()}`); };
  page.on("console", onConsole);
  page.on("pageerror", onPageError);
  page.on("response", onResponse);

  const url = BASE + route;
  await page.goto(url, { waitUntil: "networkidle2", timeout: 30000 });
  await new Promise((r) => setTimeout(r, 350)); // let the route settle
  const text = (await page.evaluate(() => document.body.innerText || "")).trim();
  await page.screenshot({ path: join(OUT, `${name}.png`) });

  page.off("console", onConsole);
  page.off("pageerror", onPageError);
  page.off("response", onResponse);

  // R1 is an intentionally near-empty reserved route — allow a lower bar.
  const minChars = name === "r1" ? 40 : 200;
  if (text.length < minChars) errors.push(`too little text (${text.length} chars)`);

  if (errors.length) {
    failures++;
    console.error(`FAIL ${name} (${route})`);
    for (const e of errors) console.error("   - " + e);
  } else {
    console.log(`ok   ${name} (${route}) — ${text.length} chars`);
  }
}

await browser.close();

if (failures) {
  console.error(`\n${failures} route(s) failed.`);
  process.exit(1);
}
console.log("\nAll routes rendered cleanly.");
