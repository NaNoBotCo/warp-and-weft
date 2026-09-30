/* weave.js — everything that moves on Warp and Weft. Plain canvas, no libraries.
   Hero loom · draft (threading × tie-up × treadling) · ikat tie-and-dye · shawl redrawn ·
   seven friezes · satin steps · math cloth · cocoon · Silk Road map. */
(function () {
"use strict";
const LANG = document.documentElement.lang, TH = LANG === "th", KM = LANG === "km";
const T = (en, th, km) => (TH ? th : KM ? (km || en) : en);
const Q = new URLSearchParams(location.search);
const STILL = matchMedia("(prefers-reduced-motion: reduce)").matches;

// the shawl's palette: 0 ground, 1 gold, 2 orange, 3 rust, 4 teal, 5 pink, 6 white, 7 warp black
const HEX = ["#2e1c14", "#e9a53c", "#d8701e", "#9c3a1c", "#17897f", "#df5f9c", "#ece5d6", "#1a100b"];
const RGB = HEX.map(h => [1, 3, 5].map(i => parseInt(h.substr(i, 2), 16)));
const GOLD = 1, OR = 2, RUST = 3, TEAL = 4, PINK = 5, WH = 6, BK = 7;
const KHMER = '"Noto Sans Khmer","Khmer Sangam MN","Khmer MN","Khmer UI",sans-serif';
const THAI = '"Noto Sans Thai","Thonburi","Leelawadee UI",Tahoma,sans-serif';
const UI = KM ? KHMER : TH ? THAI : "system-ui,sans-serif";

const $ = s => document.querySelector(s);
function hash(a, b) {
  let h = (Math.imul(a | 0, 374761393) + Math.imul(b | 0, 668265263)) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}
function noise1(x, s) {
  const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f);
  return hash(i, s) * (1 - u) + hash(i + 1, s) * u;
}
const mod = (a, n) => ((a % n) + n) % n;
function fit(cv, h) {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const w = cv.clientWidth || cv.parentNode.clientWidth;
  cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); cv.style.height = h + "px";
  const x = cv.getContext("2d"); x.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { x, w, h, dpr };
}
function live(el, on) {
  if (!("IntersectionObserver" in window)) { on(true); return; }
  new IntersectionObserver(es => es.forEach(e => on(e.isIntersecting)), { rootMargin: "80px" }).observe(el);
}
function loop(el, frame) { // runs frame(dt) while el is on screen
  let on = false, last = 0, id = 0;
  function tick(t) { const dt = Math.min(0.05, (t - (last || t)) / 1000); last = t; frame(dt); if (on) id = requestAnimationFrame(tick); }
  live(el, v => { if (v && !on) { on = true; last = 0; id = requestAnimationFrame(tick); } else if (!v) { on = false; cancelAnimationFrame(id); } });
}
function nearest(r, g, b) {
  let best = 1, bd = 1e9;
  for (let k = 1; k < 7; k++) { const c = RGB[k], d = (r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2; if (d < bd) { bd = d; best = k; } }
  return best;
}
// draw with canvas paths at 4× then read one colour per cell: a picture becomes a plan for threads
function raster(W, H, draw) {
  const S = 4, c = document.createElement("canvas"); c.width = W * S; c.height = H * S;
  const x = c.getContext("2d"); x.scale(S, S); draw(x);
  const d = x.getImageData(0, 0, W * S, H * S).data, out = new Uint8Array(W * H);
  for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
    const p = ((j * S + 2) * W * S + i * S + 2) * 4;
    out[j * W + i] = d[p + 3] < 110 ? 0 : nearest(d[p], d[p + 1], d[p + 2]);
  }
  return { W, H, d: out };
}

// ---------- motifs, after the shawl ----------
function star(x, cx, cy, r, col) {
  x.strokeStyle = HEX[col || TEAL]; x.lineWidth = 1.15; x.lineCap = "round"; x.beginPath();
  for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4, rr = k % 2 ? r * 0.62 : r; x.moveTo(cx, cy); x.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr); }
  x.stroke();
}
function flower(x, cx, cy, r) {
  x.fillStyle = HEX[PINK];
  for (let k = 0; k < 4; k++) { const a = k * Math.PI / 2; x.beginPath(); x.arc(cx + Math.cos(a) * r * 0.55, cy + Math.sin(a) * r * 0.55, r * 0.47, 0, 7); x.fill(); }
  x.fillStyle = HEX[TEAL]; x.beginPath(); x.arc(cx, cy, r * 0.3, 0, 7); x.fill();
}
function bloom(x, cx, cy, r, col) {
  x.fillStyle = HEX[col || OR]; x.beginPath(); x.arc(cx, cy, r * 0.62, 0, 7); x.fill();
  for (let k = 0; k < 6; k++) { const a = k * Math.PI / 3; x.beginPath(); x.arc(cx + Math.cos(a) * r, cy + Math.sin(a) * r, r * 0.3, 0, 7); x.fill(); }
  x.fillStyle = HEX[RUST]; x.beginPath(); x.arc(cx, cy, r * 0.28, 0, 7); x.fill();
}
function sprig(x, cx, cy, r) {
  x.strokeStyle = HEX[WH]; x.lineWidth = 1; x.lineCap = "round"; x.beginPath();
  x.moveTo(cx, cy - r); x.lineTo(cx, cy + r);
  for (let k = -1; k <= 1; k++) { const y = cy + k * r * 0.6; x.moveTo(cx, y); x.lineTo(cx - r * 0.6, y - r * 0.35); x.moveTo(cx, y); x.lineTo(cx + r * 0.6, y - r * 0.35); }
  x.stroke();
}
// a standing humped cow (zebu) facing left, in a 100 × 70 box, after the shawl
function cow(x, ox, oy, s) {
  x.save(); x.translate(ox, oy); x.scale(s, s);
  x.fillStyle = HEX[GOLD]; x.strokeStyle = HEX[GOLD]; x.beginPath();
  x.moveTo(24, 20); x.bezierCurveTo(27, 5, 41, 5, 44, 18); x.lineTo(84, 20); x.bezierCurveTo(91, 22, 92, 35, 86, 43);
  x.lineTo(86, 68); x.lineTo(80, 68); x.lineTo(79, 49); x.lineTo(75, 49); x.lineTo(74, 68); x.lineTo(68, 68); x.lineTo(68, 47);
  x.bezierCurveTo(58, 51, 45, 51, 37, 47); x.lineTo(37, 68); x.lineTo(31, 68); x.lineTo(30, 50); x.lineTo(28, 50); x.lineTo(27, 68); x.lineTo(21, 68); x.lineTo(21, 44);
  x.bezierCurveTo(16, 45, 12, 41, 10, 36); x.lineTo(4, 38); x.lineTo(1, 34); x.lineTo(2, 26); x.lineTo(8, 18);
  x.lineTo(5, 9); x.lineTo(10, 12); x.lineTo(13, 17); x.lineTo(19, 15); x.bezierCurveTo(21, 18, 22, 20, 24, 20);
  x.closePath(); x.fill();
  x.lineWidth = 2.6; x.lineCap = "round"; x.beginPath(); x.moveTo(88, 24); x.quadraticCurveTo(96, 34, 93, 58); x.stroke();
  x.beginPath(); x.arc(93, 60, 3.2, 0, 7); x.fill();
  x.strokeStyle = HEX[RUST]; x.lineWidth = 3; x.beginPath();
  x.moveTo(28, 12); x.quadraticCurveTo(34, 8, 40, 13); // hump
  x.moveTo(42, 46); x.lineTo(64, 46); x.moveTo(21, 57); x.lineTo(37, 57); x.moveTo(68, 57); x.lineTo(86, 57);
  x.stroke(); x.restore();
}
function word(x, text, cx, cy, size, col, font) {
  x.fillStyle = HEX[col]; x.font = `700 ${size}px ${font || KHMER}`; x.textAlign = "center"; x.textBaseline = "middle";
  x.fillText(text, cx, cy);
}
const KOU = "គោ";
function sprinkle(x, y, flip) {
  const row = flip ? [[4, bloom], [14, star], [25, sprig], [36, flower], [47, sprig], [58, star], [67, bloom]]
                   : [[4, sprig], [13, bloom], [23, star], [35, flower], [47, star], [57, bloom], [66, sprig]];
  for (const [cx, f] of row) f === flower ? flower(x, cx, y, 5) : f === star ? star(x, cx, y, 4.2) : f === bloom ? bloom(x, cx, y, 2.4) : sprig(x, cx, y, 3.4);
}
function shawlDesign() {
  return raster(72, 104, x => {
    for (let i = 0; i < 8; i++) bloom(x, 4.5 + i * 9, 3, 1.8, i % 2 ? PINK : OR);
    word(x, KOU, 17, 14, 13, TEAL); word(x, KOU, 46, 14, 13, GOLD); bloom(x, 64, 14, 2.6);
    sprinkle(x, 28, false);
    cow(x, 7, 34, 0.56); flower(x, 37, 66, 4); bloom(x, 67, 50, 2.2); star(x, 67, 64, 3.6);
    sprinkle(x, 80, true);
    word(x, KOU, 17, 93, 13, GOLD); word(x, KOU, 46, 93, 13, TEAL); flower(x, 65, 93, 4);
  });
}

// ---------- the renderer: weft-faced cloth, one cell per crossing ----------
// weave(c, q) true = warp on top at that crossing. Hol cloth is a 1/2 twill: warp shows one in three.
const HOL = (c, q) => mod(c + q, 3) === 0;
function weaveImage(D, cols, rows, cell, o) {
  const img = new ImageData(cols * cell, rows * cell), px = img.data, W = D.W, H = D.H;
  const bleed = o.bleed || 0, seed = o.seed || 7, weave = o.weave || HOL, warp = RGB[o.warp == null ? BK : o.warp];
  for (let r = 0; r < rows; r++) {
    const q = o.pick ? o.pick(r) : r, qq = o.flip ? H - 1 - mod(q, H) : mod(q, H);
    const sh = bleed ? Math.round((noise1(qq * 0.5, seed) - 0.5) * 2.2 * bleed) : 0;
    for (let c = 0; c < cols; c++) {
      let jit = 0;
      if (bleed) { const h = hash(c >> 1, qq * 7 + seed); jit = h < 0.12 * bleed ? -1 : h > 1 - 0.12 * bleed ? 1 : 0; }
      const k = D.d[qq * W + mod(c + sh + jit, W)], wf = RGB[k], up = weave(c, q);
      for (let j = 0; j < cell; j++) {
        const vy = 1.12 - 0.34 * Math.abs((j + 0.5) / cell - 0.5) * 2;
        for (let i = 0; i < cell; i++) {
          const o4 = ((r * cell + j) * cols * cell + c * cell + i) * 4;
          if (up) {
            const vx = 1.25 - 0.45 * Math.abs((i + 0.5) / cell - 0.5) * 2;
            px[o4] = warp[0] * vx + wf[0] * 0.14; px[o4 + 1] = warp[1] * vx + wf[1] * 0.14; px[o4 + 2] = warp[2] * vx + wf[2] * 0.14;
          } else { px[o4] = wf[0] * vy; px[o4 + 1] = wf[1] * vy; px[o4 + 2] = wf[2] * vy; }
          px[o4 + 3] = 255;
        }
      }
    }
  }
  return img;
}
function toCanvas(img) { const c = document.createElement("canvas"); c.width = img.width; c.height = img.height; c.getContext("2d").putImageData(img, 0, 0); return c; }

// ---------- hero: a loom weaving the shawl ----------
function hero(D) {
  const cv = $("#loom"); if (!cv) return;
  const card = Q.has("card");
  let st, cell, cols, cloth, fellY, pick, prog = 0, dir = 1, beat = 0, woven = 0;
  const H = D.H, T3 = 3 * H, speed = 3.2;
  function setup() {
    const h = card ? 630 : Math.round(Math.max(460, Math.min(innerHeight * 0.8, 760)));
    st = fit(cv, h); cell = st.w < 640 ? 3 : 4; cols = Math.ceil(st.w / cell) + 1;
    fellY = Math.round(h * (card ? 0.5 : 0.46));
    cloth = toCanvas(weaveImage(D, cols, T3, cell, { bleed: 1.6, seed: 11, pick: r => T3 - 1 - r, flip: true }));
    if (pick == null) pick = H + (card ? 84 : 70);
    draw();
  }
  function draw() {
    const x = st.x, w = st.w, h = st.h, pp = 2 * H + mod(pick, H), iCur = T3 - 1 - pp;
    x.imageSmoothingEnabled = false;
    // warp: dark threads coming down to the fell; the lifted ones catch the light
    const g = x.createLinearGradient(0, 0, 0, fellY); g.addColorStop(0, "#0d0705"); g.addColorStop(1, "#24160f");
    x.fillStyle = g; x.fillRect(0, 0, w, fellY + cell);
    for (let c = 0; c < cols; c++) {
      const up = HOL(c, pp), X = c * cell + cell / 2;
      x.strokeStyle = up ? "rgba(214,176,120,.55)" : "rgba(120,86,60,.35)"; x.lineWidth = Math.max(1, cell * 0.55);
      x.beginPath(); x.moveTo(X, 0); x.lineTo(X, fellY); x.stroke();
    }
    // heddles and reed
    const hy = fellY * 0.55;
    x.fillStyle = "rgba(20,11,7,.8)"; x.fillRect(0, hy - 3, w, 6); x.fillRect(0, hy + 22, w, 6);
    x.strokeStyle = "rgba(233,165,60,.35)"; x.lineWidth = 1; x.beginPath();
    for (let c = 0; c < cols; c += 3) { const X = c * cell + cell / 2; x.moveTo(X, hy); x.lineTo(X, hy + 22); } x.stroke();
    const ry = fellY - 16 + Math.sin(Math.min(1, beat) * Math.PI) * 12;
    x.fillStyle = "#6b4a2e"; x.fillRect(0, ry - 5, w, 9); x.fillStyle = "rgba(255,220,170,.25)"; x.fillRect(0, ry - 5, w, 2);
    // cloth already woven, newest at the fell
    const vis = Math.ceil((h - fellY) / cell);
    x.drawImage(cloth, 0, (iCur + 1) * cell, cols * cell, vis * cell, 0, fellY + cell, cols * cell, vis * cell);
    // the pick being laid
    x.fillStyle = "#1a100b"; x.fillRect(0, fellY, w, cell);
    const sx = dir > 0 ? 0 : (1 - prog) * w, sw = prog * w;
    if (sw > 0) x.drawImage(cloth, sx, iCur * cell, sw, cell, sx, fellY, sw, cell);
    // shuttle
    const shx = dir > 0 ? prog * w : (1 - prog) * w, shy = fellY + cell / 2 - 1;
    if (beat === 0 && prog < 1) {
      x.save(); x.translate(shx, shy); x.scale(dir, 1);
      const sg = x.createLinearGradient(0, -8, 0, 8); sg.addColorStop(0, "#c7925a"); sg.addColorStop(1, "#6b4020");
      x.fillStyle = sg; x.beginPath(); x.moveTo(34, 0); x.quadraticCurveTo(10, -9, -34, 0); x.quadraticCurveTo(10, 9, 34, 0); x.fill();
      x.fillStyle = HEX[(mod(pick, 5) + 1) % 6 || GOLD]; x.fillRect(-12, -3, 22, 6);
      x.restore();
    }
    if (!card) {
      x.fillStyle = "rgba(236,229,214,.55)"; x.font = `12px ${UI}`; x.textAlign = "right"; x.textBaseline = "bottom";
      x.fillText(T(`${woven.toLocaleString()} picks woven while you watched`, `ทอไป ${woven.toLocaleString()} เส้นพุ่ง ระหว่างที่คุณดูอยู่`, `ត្បាញបាន ${woven.toLocaleString()} ជួរ ខណៈពេលដែលអ្នកមើល`), w - 14, h - 10);
    }
  }
  setup();
  let rw = 0; addEventListener("resize", () => { if (Math.abs(cv.clientWidth - rw) > 2) { rw = cv.clientWidth; setup(); } });
  rw = cv.clientWidth;
  if (STILL || card) return;
  loop(cv, dt => {
    if (beat > 0) { beat += dt * 7; if (beat >= 1) { beat = 0; prog = 0; dir = -dir; pick++; woven++; } }
    else { prog += dt * speed * (st.w < 640 ? 1.25 : 1); if (prog >= 1) { prog = 1; beat = 0.001; } }
    draw();
  });
}

// ---------- the draft: cloth as a matrix product ----------
function draft() {
  const cv = $("#draft"), cl = $("#draft-cloth"); if (!cv) return;
  const S = 4, TR = 4, E = 24, P = 20;
  let th = [], tu = [], tr = [], warpC = TEAL, weftC = GOLD;
  const PRE = {
    plain: ["0123", [[0, 2], [1, 3], [0, 2], [1, 3]], "01"],
    basket: ["0011", [[0], [1], [0], [1]], "0011"],
    hol: ["012", [[0], [1], [2], [3]], "012"],
    twill: ["0123", [[0, 1], [1, 2], [2, 3], [3, 0]], "0123"],
    twill31: ["0123", [[0, 1, 2], [1, 2, 3], [2, 3, 0], [3, 0, 1]], "0123"],
    diamond: ["012321", [[0, 1], [1, 2], [2, 3], [3, 0]], "012321"],
  };
  function load(k) {
    const p = PRE[k];
    th = Array.from({ length: E }, (_, e) => +p[0][e % p[0].length]);
    tu = Array.from({ length: S * TR }, () => false); p[1].forEach((ss, t) => ss.forEach(s => (tu[s * TR + t] = true)));
    tr = Array.from({ length: P }, (_, q) => +p[2][q % p[2].length]);
    draw();
  }
  const up = (e, q) => tu[th[mod(e, E)] * TR + tr[mod(q, P)]];
  let st, cs;
  function draw() {
    const w = cv.clientWidth; cs = Math.max(8, Math.min(20, Math.floor(w / (E + 1 + TR))));
    st = fit(cv, (S + 1 + P) * cs + 2); const x = st.x; x.clearRect(0, 0, st.w, st.h);
    const ink = getComputedStyle(document.body).getPropertyValue("--ink").trim() || "#2a1a12";
    function grid(ox, oy, nx, ny, fill) {
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        const f = fill(i, j); x.fillStyle = f || "rgba(128,110,90,.12)"; x.fillRect(ox + i * cs + 1, oy + j * cs + 1, cs - 2, cs - 2);
      }
    }
    const tx = (E + 1) * cs, dy = (S + 1) * cs;
    grid(0, 0, E, S, (i, j) => (th[i] === S - 1 - j ? ink : 0));
    grid(tx, 0, TR, S, (i, j) => (tu[(S - 1 - j) * TR + i] ? ink : 0));
    grid(tx, dy, TR, P, (i, j) => (tr[j] === i ? ink : 0));
    grid(0, dy, E, P, (i, j) => HEX[up(i, j) ? warpC : weftC]);
    // the cloth itself, with thread shading
    const cc = st.w < 500 ? 5 : 7, cols = Math.ceil(cl.clientWidth / cc), rows = Math.ceil(150 / cc);
    const plain = { W: 1, H: 1, d: new Uint8Array([weftC]) };
    const cst = fit(cl, rows * cc); cst.x.imageSmoothingEnabled = false;
    const img = toCanvas(weaveImage(plain, cols, rows, cc, { weave: (c, q) => up(c, q), warp: warpC }));
    cst.x.drawImage(img, 0, 0, cols * cc, rows * cc, 0, 0, cols * cc, rows * cc);
  }
  cv.addEventListener("click", ev => {
    const r = cv.getBoundingClientRect(), i = Math.floor((ev.clientX - r.left) / cs), j = Math.floor((ev.clientY - r.top) / cs);
    const ti = i - (E + 1), pj = j - (S + 1);
    if (j < S && i < E) th[i] = S - 1 - j;
    else if (j < S && ti >= 0 && ti < TR) tu[(S - 1 - j) * TR + ti] = !tu[(S - 1 - j) * TR + ti];
    else if (pj >= 0 && pj < P && ti >= 0 && ti < TR) tr[pj] = ti;
    else return;
    draw();
  });
  document.querySelectorAll("[data-draft]").forEach(b => b.addEventListener("click", () => {
    const k = b.dataset.draft;
    if (k === "colour") { const pairs = [[TEAL, GOLD], [BK, PINK], [RUST, WH], [GOLD, TEAL], [BK, GOLD]]; const n = pairs.findIndex(p => p[0] === warpC && p[1] === weftC); [warpC, weftC] = pairs[(n + 1) % pairs.length]; draw(); }
    else if (k === "random") { th = th.map(() => Math.floor(Math.random() * S)); tu = tu.map(() => Math.random() < 0.5); tr = tr.map(() => Math.floor(Math.random() * TR)); draw(); }
    else load(k);
  }));
  load("diamond");
  addEventListener("resize", draw);
}

// ---------- ikat: tie, dye, untie, weave ----------
function ikat() {
  const cv = $("#ikat-cv"); if (!cv) return;
  const W = 40, H = 28;
  const MOTIF = {
    cow: x => { cow(x, 3, 2, 0.34); flower(x, 36, 6, 3.4); star(x, 36, 22, 3); },
    stars: x => { star(x, 8, 7, 5); flower(x, 24, 7, 6); star(x, 36, 20, 5); flower(x, 14, 21, 6); star(x, 30, 7, 3); },
    kou: x => { word(x, KOU, 20, 14, 18, TEAL); flower(x, 4, 5, 3); flower(x, 36, 23, 3); },
  };
  let key = "cow", D, fold = false, bleed = 1.5, stage = 0, a = 0, playing = !STILL;
  const CAP = [
    [T("Draw the picture on squared paper. Each row is one weft thread.", "วาดลายบนกระดาษตาราง แต่ละแถวคือเส้นพุ่งหนึ่งเส้น", "គូរក្បាច់លើក្រដាសការ៉ូ។ ជួរនីមួយៗ គឺអំបោះទទឹងមួយសរសៃ។")],
    [T("Stretch the weft threads on a frame and tie tight bindings over every square that should stay light.", "ขึงเส้นพุ่งบนโฮง แล้วมัดเชือกให้แน่นทุกช่องที่ต้องการให้สีอ่อน", "សន្ធឹងអំបោះទទឹងលើស៊ុម ហើយចងឱ្យណែនលើគ្រប់ក្រឡាដែលត្រូវរក្សាពណ៌ស្រាល។")],
    [T("Dip the whole bundle. Dye soaks everything the bindings leave open: the ground colour.", "จุ่มทั้งปอยลงหม้อย้อม สีซึมทุกส่วนที่ไม่ได้มัด กลายเป็นสีพื้น", "ជ្រលក់បាច់អំបោះទាំងមូល។ ពណ៌ជ្រាបចូលកន្លែងដែលមិនបានចង ក្លាយជាពណ៌ផ្ទៃ។")],
    [T("Cut the bindings on the teal squares and dye again.", "แก้เชือกตรงช่องสีเขียวหัวเป็ด แล้วย้อมอีกรอบ", "កាត់ចំណងលើក្រឡាពណ៌បៃតងខៀវ ហើយជ្រលក់ម្តងទៀត។")],
    [T("Tie the teal back up, cut the rest, dye the gold.", "มัดช่องเขียวกลับคืน แก้ที่เหลือ แล้วย้อมสีทอง", "ចងក្រឡាពណ៌បៃតងខៀវវិញ កាត់ចំណងដែលនៅសល់ ហើយជ្រលក់ពណ៌មាស។")],
    [T("Untie everything. The picture is in the thread before any weaving.", "แก้มัดทั้งหมด ลายอยู่ในเส้นด้ายแล้ว ทั้งที่ยังไม่ได้ทอ", "ស្រាយចំណងទាំងអស់។ ក្បាច់នៅក្នុងអំបោះរួចហើយ មុនពេលត្បាញ។")],
    [T("Weave the threads in order. Each one drifts a little: that feathered edge is the mark of ikat.", "ทอเส้นพุ่งทีละเส้นตามลำดับ แต่ละเส้นเหลื่อมกันนิดหน่อย ขอบฟุ้งนี้คือเอกลักษณ์ของผ้ามัดย้อมเส้นด้าย", "ត្បាញអំបោះតាមលំដាប់។ សរសៃនីមួយៗរំកិលបន្តិច៖ គែមព្រាលៗនោះ ជាស្នាមនៃការចងជ្រលក់អំបោះ។")],
  ];
  function build() {
    D = raster(W, H, MOTIF[key]);
    for (let i = 0; i < D.d.length; i++) { const k = D.d[i]; D.d[i] = k === 0 ? 0 : (k === TEAL ? TEAL : k === PINK ? PINK : GOLD); }
    if (fold) for (let j = 0; j < H; j++) for (let i = W / 2; i < W; i++) D.d[j * W + i] = D.d[j * W + (W - 1 - i)];
  }
  let st;
  function draw() {
    const narrow = cv.clientWidth < 620, pw = narrow ? cv.clientWidth : (cv.clientWidth - 24) / 2;
    const cs = Math.floor(pw / W), ph = cs * H;
    st = fit(cv, narrow ? ph * 2 + 24 : ph); const x = st.x; x.clearRect(0, 0, st.w, st.h);
    const second = D.d.some(k => k === TEAL) && D.d.some(k => k !== TEAL && k > 0);
    // skein
    const lvl = a;
    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
      const k = D.d[j * W + i], X = i * cs, Y = j * cs;
      const dyeHere = (H - j) / H <= lvl * 1.05;
      let col = "#efe7d8";
      if (stage >= 2) col = k === 0 ? (stage > 2 || dyeHere ? HEX[0] : col) : col;
      if (stage >= 3 && k === TEAL) col = stage > 3 || dyeHere ? HEX[TEAL] : col;
      if (stage >= 4 && k > 0 && k !== TEAL) col = stage > 4 || dyeHere ? HEX[k] : col;
      if (stage === 3 && !second && k > 0) col = dyeHere ? HEX[k] : col;
      x.fillStyle = col; x.fillRect(X, Y + cs * 0.18, cs, cs * 0.64);
      const tied = (stage === 1 || stage === 2) ? k > 0 : stage === 3 ? k > 0 && k !== TEAL : stage === 4 ? k === TEAL : false;
      if (stage === 0 && k > 0) { x.fillStyle = "rgba(60,40,30,.35)"; x.fillRect(X + 1, Y + 1, cs - 2, cs - 2); }
      if (tied && j % 2 === 0) {
        x.fillStyle = "#d8cdb6"; x.fillRect(X, Y, cs, cs * 2);
        x.strokeStyle = "rgba(156,58,28,.55)"; x.lineWidth = 1; x.beginPath();
        for (let s = 0; s < 3; s++) { x.moveTo(X, Y + s * cs * 0.7); x.lineTo(X + cs, Y + s * cs * 0.7 + cs * 0.5); } x.stroke();
      }
    }
    x.fillStyle = "rgba(90,60,40,.8)"; x.fillRect(0, 0, 3, ph); x.fillRect(pw - 3, 0, 3, ph);
    // cloth
    const ox = narrow ? 0 : pw + 24, oy = narrow ? ph + 24 : 0;
    if (stage >= 6) {
      const rows = Math.min(H, Math.ceil(a * H)), cc = Math.max(3, Math.floor(cs / 2)), cols = Math.floor(pw / cc);
      const Dd = { W, H, d: D.d };
      const img = toCanvas(weaveImage(Dd, cols, H * 2, cc, { bleed, seed: 5, pick: r => r, weave: HOL }));
      x.imageSmoothingEnabled = false;
      const shown = Math.min(H * 2, Math.ceil(a * H * 2));
      x.drawImage(img, 0, 0, cols * cc, shown * cc, ox, oy, cols * cc, shown * cc);
      x.fillStyle = "rgba(26,16,11,.9)"; x.fillRect(ox, oy + shown * cc, cols * cc, ph - shown * cc > 0 ? Math.min(ph, H * 2 * cc) - shown * cc : 0);
    } else {
      x.fillStyle = "rgba(26,16,11,.9)"; x.fillRect(ox, oy, pw, ph);
      x.strokeStyle = "rgba(214,176,120,.25)"; x.beginPath();
      for (let i = 0; i < pw; i += 4) { x.moveTo(ox + i + 1, oy); x.lineTo(ox + i + 1, oy + ph); } x.stroke();
    }
    $("#ikat-cap").textContent = `${stage + 1} / 7 · ${CAP[stage][0]}`;
  }
  function next(n) { stage = mod(stage + n, 7); a = STILL ? 1 : 0; draw(); }
  build(); draw();
  document.querySelectorAll("[data-ikat]").forEach(b => b.addEventListener("click", () => {
    const k = b.dataset.ikat;
    if (k === "next") { playing = false; next(1); } else if (k === "prev") { playing = false; next(-1); }
    else if (k === "play") { playing = !playing; } else { key = k; build(); stage = 0; a = 0; draw(); }
  }));
  const fb = $("#ikat-fold"); if (fb) fb.addEventListener("change", () => { fold = fb.checked; build(); draw(); });
  const bl = $("#ikat-bleed"); if (bl) bl.addEventListener("input", () => { bleed = +bl.value; draw(); });
  addEventListener("resize", draw);
  let hold = 0;
  loop(cv, dt => {
    if (!playing) { if (a < 1) { a = Math.min(1, a + dt * 0.8); draw(); } return; }
    if (a < 1) { a = Math.min(1, a + dt * (stage === 6 ? 0.35 : 0.7)); draw(); }
    else if ((hold += dt) > (stage === 6 ? 3 : 1.4)) { hold = 0; next(1); }
  });
}

// ---------- the shawl, redrawn ----------
function shawl(D) {
  const cv = $("#shawl-draw"); if (!cv) return;
  const bl = $("#shawl-bleed"), zm = $("#shawl-zoom");
  function draw() {
    const cell = +zm.value, h = Math.min(560, Math.round(cv.clientWidth * 1.2)), st = fit(cv, h);
    const cols = Math.ceil(st.w / cell), rows = Math.ceil(h / cell);
    st.x.imageSmoothingEnabled = false;
    st.x.drawImage(toCanvas(weaveImage(D, cols, rows, cell, { bleed: +bl.value, seed: 3, pick: r => r + 2 })), 0, 0);
  }
  bl.addEventListener("input", draw); zm.addEventListener("input", draw); addEventListener("resize", draw); draw();
}

// ---------- seven friezes from one motif ----------
function frieze() {
  const ed = $("#motif"), cv = $("#friezes"); if (!ed) return;
  const N = 7;
  let m = ("0000000" + "0111110" + "0100010" + "0101010" + "0101110" + "0100000" + "0000000").split("").map(Number);
  const G = [
    ["p1", "hop", "กระโดดไปข้างหน้า", "m,m,m,m", "លោតទៅមុខ"], ["p11g", "step", "ก้าวเดิน", "m,v,m,v", "ដើរជំហាន"], ["p1m1", "sidle", "ก้าวข้าง", "m,u,m,u", "ដើរចំហៀង"],
    ["p2", "spinning hop", "กระโดดหมุน", "m,r,m,r", "លោតបង្វិល"], ["p2mg", "spinning sidle", "ก้าวข้างหมุน", "m,u,v,r", "ដើរចំហៀងបង្វិល"],
    ["p11m", "jump", "กระโดดสองเท้า", "mv,mv,mv,mv", "លោតជើងពីរ"], ["p2mm", "spinning jump", "กระโดดสองเท้าหมุน", "mv,ur,mv,ur", "លោតជើងពីរបង្វិល"],
  ];
  const COLS = [GOLD, TEAL, PINK, OR, WH, GOLD, TEAL];
  let es;
  function drawEd() {
    es = fit(ed, Math.min(168, ed.clientWidth)); const c = es.w / N, x = es.x;
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) { x.fillStyle = m[j * N + i] ? HEX[GOLD] : "#3a261b"; x.fillRect(i * c + 1, j * c + 1, c - 2, c - 2); }
  }
  function drawF() {
    const w = cv.clientWidth, px = w < 520 ? 3 : 4, unit = (N + 1) * px, stripH = (2 * N + 2) * px, gap = 30;
    const st = fit(cv, G.length * (stripH + gap)), x = st.x; x.clearRect(0, 0, st.w, st.h);
    G.forEach((g, gi) => {
      const oy = gi * (stripH + gap) + 18, mid = oy + (N + 1) * px, ops = g[3].split(",");
      x.fillStyle = "#2e1c14"; x.fillRect(0, oy, st.w, stripH);
      x.fillStyle = getComputedStyle(document.body).getPropertyValue("--ink").trim() || "#2a1a12";
      x.font = `600 13px ${UI}`; x.textBaseline = "bottom"; x.textAlign = "left";
      x.fillText(`${T(g[1], g[2], g[4])} · ${g[0]}`, 0, oy - 3);
      x.fillStyle = HEX[COLS[gi]];
      for (let s = 0; s * unit < st.w; s++) {
        const op = ops[s % 4], ox = s * unit + px / 2;
        for (const o of op === "mv" ? ["m", "v"] : op === "ur" ? ["u", "r"] : [op])
          for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
            if (!m[j * N + i]) continue;
            const ii = (o === "u" || o === "r") ? N - 1 - i : i, below = o === "v" || o === "r";
            x.fillRect(ox + ii * px, below ? mid + (N - 1 - j) * px : mid - (N - j) * px, px, px);
          }
      }
    });
  }
  ed.addEventListener("click", ev => {
    const r = ed.getBoundingClientRect(), c = r.width / N, i = Math.floor((ev.clientX - r.left) / c), j = Math.floor((ev.clientY - r.top) / c);
    if (i >= 0 && i < N && j >= 0 && j < N) { m[j * N + i] ^= 1; drawEd(); drawF(); }
  });
  document.querySelectorAll("[data-motif]").forEach(b => b.addEventListener("click", () => {
    const k = b.dataset.motif;
    m = k === "clear" ? m.map(() => 0) : k === "random" ? m.map(() => (Math.random() < 0.4 ? 1 : 0))
      : ("0000000" + "0111110" + "0100010" + "0101010" + "0101110" + "0100000" + "0000000").split("").map(Number);
    drawEd(); drawF();
  }));
  drawEd(); drawF(); addEventListener("resize", () => { drawEd(); drawF(); });
}

// ---------- satin: which steps tie every thread down ----------
function satin() {
  const cv = $("#satin"); if (!cv) return;
  const nI = $("#satin-n"), kI = $("#satin-k"), out = $("#satin-out");
  const gcd = (a, b) => (b ? gcd(b, a % b) : a);
  let t = 0;
  function draw() {
    const n = +nI.value; kI.max = n - 1; let k = Math.min(+kI.value, n - 1);
    $("#satin-nv").textContent = n; $("#satin-kv").textContent = k;
    const reps = cv.clientWidth < 520 ? 2 : 3, cells = n * reps, cs = Math.floor(Math.min(cv.clientWidth, 520) / cells);
    const st = fit(cv, cells * cs), x = st.x; x.clearRect(0, 0, st.w, st.h);
    const tied = new Set(); for (let r = 0; r < n; r++) tied.add((r * k) % n);
    for (let r = 0; r < cells; r++) {
      // weft float: one long bar, broken where it dips under
      x.fillStyle = HEX[GOLD]; x.fillRect(0, r * cs + cs * 0.12, cells * cs, cs * 0.76);
      const sheen = 0.5 + 0.5 * Math.sin(t * 1.4 - r * 0.35);
      x.fillStyle = `rgba(255,245,220,${0.1 + 0.18 * sheen})`; x.fillRect(0, r * cs + cs * 0.18, cells * cs, cs * 0.18);
      for (let c = 0; c < cells; c++) if (mod(c, n) === (r % n * k) % n) {
        x.fillStyle = HEX[BK]; x.fillRect(c * cs + cs * 0.15, r * cs, cs * 0.7, cs);
        x.fillStyle = HEX[TEAL]; x.beginPath(); x.arc(c * cs + cs / 2, r * cs + cs / 2, cs * 0.22, 0, 7); x.fill();
      }
    }
    for (let c = 0; c < cells; c++) if (!tied.has(c % n)) { x.strokeStyle = "#e0413a"; x.lineWidth = 2; x.strokeRect(c * cs + 1, 1, cs - 2, cells * cs - 2); }
    const good = []; for (let j = 2; j < n - 1; j++) if (gcd(n, j) === 1) good.push(j);
    let msg;
    if (gcd(n, k) !== 1) msg = T(`${n} and ${k} share the factor ${gcd(n, k)}. The warp threads outlined in red never get tied down: the cloth falls apart.`,
      `${n} กับ ${k} มีตัวหารร่วมคือ ${gcd(n, k)} เส้นยืนที่ขอบแดงไม่เคยถูกขัดเลย ผ้าจะหลุดลุ่ย`, `${n} និង ${k} មានតួចែករួម ${gcd(n, k)}។ អំបោះបញ្ឈរដែលមានគែមក្រហម មិនដែលឆ្លាស់ជាមួយអំបោះទទឹងទេ ក្រណាត់នឹងរបូតរលុង។`);
    else if (k === 1 || k === n - 1) msg = T(`Step ${k} lines the ties up on a diagonal. That is a twill, not a satin.`, `ก้าว ${k} ทำให้จุดขัดเรียงเป็นแนวเฉียง นี่คือลายสอง ไม่ใช่ผ้าต่วน`, `ជំហាន ${k} តម្រៀបចំណុចឆ្លាស់ជាខ្សែទ្រេត។ នោះជាត្បាញទ្រេត មិនមែនសាតាំងទេ។`);
    else msg = T(`Satin. Every thread is tied once per ${n}, and no two ties touch, so the floats read as one smooth sheen.`, `ผ้าต่วน ทุกเส้นถูกขัดหนึ่งครั้งในทุก ${n} เส้น และจุดขัดไม่ติดกัน ผิวผ้าจึงเรียบเป็นมันวาว`, `សាតាំង។ អំបោះគ្រប់សរសៃឆ្លាស់ម្តងក្នុងរាល់ ${n} សរសៃ ហើយចំណុចឆ្លាស់មិនប៉ះគ្នា ផ្ទៃក្រណាត់ក៏រលោងភ្លឺ។`);
    out.innerHTML = msg + "<br>" + (good.length ? T(`Satin steps for ${n}: `, `ก้าวที่เป็นผ้าต่วนสำหรับ ${n}: `, `ជំហានសាតាំងសម្រាប់ ${n}៖ `) + good.join(", ")
      : T(`${n} has no satin step at all.`, `${n} ไม่มีก้าวที่เป็นผ้าต่วนเลย`, `${n} គ្មានជំហានសាតាំងសោះ។`));
  }
  nI.addEventListener("input", draw); kI.addEventListener("input", draw); addEventListener("resize", draw); draw();
  if (!STILL) loop(cv, dt => { t += dt; draw(); });
}

// ---------- math cloth ----------
function mathCloth() {
  const cv = $("#mcloth"); if (!cv) return;
  const fI = $("#mc-f"), pI = $("#mc-p"), kI = $("#mc-k"), bI = $("#mc-b"), nm = $("#mc-name");
  const PALS = [[0, GOLD, TEAL, PINK, OR, WH], [0, TEAL, GOLD, RUST, WH, PINK], [BK, PINK, GOLD, TEAL, WH, OR]];
  let pal = 0;
  const F = {
    diamond: (x, y, p) => Math.abs(mod(x, 2 * p) - p) + Math.abs(mod(y, 2 * p) - p),
    naga: (x, y, p) => y + Math.abs(mod(x, 2 * p) - p),
    rings: (x, y, p) => Math.floor(Math.hypot(mod(x, 4 * p) - 2 * p, mod(y, 4 * p) - 2 * p)),
    xor: (x, y, p) => (Math.floor(x * 8 / p) ^ Math.floor(y * 8 / p)),
    pascal: (x, y, p) => { const n = mod(y, 8 * p), kk = x - 36 + (n >> 1); return kk >= 0 && kk <= n && (kk & n) === kk ? 1 : 0; },
  };
  function design() {
    const f = fI.value, p = +pI.value, k = +kI.value, W = 72, H = 72, P = PALS[pal];
    if (f === "name") {
      const txt = (nm.value || T("Silk", "ไหม", "សូត្រ")).slice(0, 14);
      return raster(W, H, x => {
        const s = Math.min(24, 120 / Math.max(2, txt.length));
        for (let r = 0; r < 3; r++) word(x, txt, 36, 12 + r * 24, s, P[1 + (r % (P.length - 1))], `${THAI.replace(/,sans-serif$/, "")},${KHMER}`);
      });
    }
    const d = new Uint8Array(W * H);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const v = F[f](x, y, p), band = f === "pascal" ? v : Math.floor(v / Math.max(1, Math.round(p / 3)));
      const idx = mod(band, k);
      d[y * W + x] = idx === 0 ? P[0] : P[1 + ((idx - 1) % (P.length - 1))];
    }
    return { W, H, d };
  }
  let img;
  function draw() {
    const cell = cv.clientWidth < 520 ? 3 : 4, h = Math.min(420, Math.round(cv.clientWidth * 0.62)), st = fit(cv, h);
    const cols = Math.ceil(st.w / cell), rows = Math.ceil(h / cell);
    img = toCanvas(weaveImage(design(), cols, rows, cell, { bleed: +bI.value, seed: 9 }));
    st.x.imageSmoothingEnabled = false; st.x.drawImage(img, 0, 0);
    nm.parentNode.hidden = fI.value !== "name";
  }
  [fI, pI, kI, bI].forEach(el => el.addEventListener("input", draw));
  nm.addEventListener("input", draw);
  $("#mc-pal").addEventListener("click", () => { pal = (pal + 1) % PALS.length; draw(); });
  $("#mc-save").addEventListener("click", () => {
    const a = document.createElement("a"); a.download = "warp-and-weft.png"; a.href = img.toDataURL("image/png"); a.click();
  });
  addEventListener("resize", draw); draw();
}

// ---------- cocoon: a figure eight, over and over ----------
function cocoon() {
  const cv = $("#cocoon"); if (!cv) return;
  const out = $("#cocoon-m"), METRES = 900, HOURS = 72;
  let st, silk, sx, s = 0, u0 = 0, th0 = 0, done = 0, mode = "spin", reel = 0, gold = false, prev = null, rot = 0;
  function setup() {
    st = fit(cv, Math.min(380, Math.max(300, cv.clientWidth * 0.55)));
    silk = document.createElement("canvas"); silk.width = cv.width; silk.height = cv.height;
    sx = silk.getContext("2d"); sx.setTransform(st.dpr, 0, 0, st.dpr, 0, 0); done = 0; prev = null; reel = 0; mode = "spin";
  }
  const cx = () => st.w * (st.w < 520 ? 0.5 : 0.36), cy = () => st.h * 0.5, A = () => Math.min(st.w * 0.26, 150), B = () => A() * 0.6;
  function point(u, th) {
    const r = Math.sqrt(Math.max(0, 1 - u * u)) * B(), y = r * Math.cos(th), z = r * Math.sin(th);
    const tilt = 0.35, y2 = y * Math.cos(tilt) - z * Math.sin(tilt), z2 = y * Math.sin(tilt) + z * Math.cos(tilt);
    return [cx() + u * A(), cy() + y2, z2];
  }
  function spin(steps) {
    const c = gold ? "233,165,60" : "250,246,236";
    for (let i = 0; i < steps; i++) {
      s += 0.09; u0 = 0.72 * Math.sin(s * 0.0071); th0 += 0.013;
      const u = Math.max(-0.97, Math.min(0.97, u0 + 0.28 * Math.sin(s))), th = th0 + 0.55 * Math.sin(2 * s);
      const p = point(u, th);
      if (prev) { sx.strokeStyle = `rgba(${c},${p[2] > 0 ? 0.16 : 0.05})`; sx.lineWidth = 0.7; sx.beginPath(); sx.moveTo(prev[0], prev[1]); sx.lineTo(p[0], p[1]); sx.stroke(); }
      prev = p; done = Math.min(1, done + 1 / 26000);
    }
    return prev;
  }
  function draw(head) {
    const x = st.x; x.clearRect(0, 0, st.w, st.h);
    const g = x.createRadialGradient(cx(), cy(), 10, cx(), cy(), A() * 1.6); g.addColorStop(0, "rgba(120,160,80,.18)"); g.addColorStop(1, "rgba(120,160,80,0)");
    x.fillStyle = g; x.fillRect(0, 0, st.w, st.h);
    // the worm, visible until the walls thicken
    const seen = Math.max(0, 1 - done * 3) * (mode === "spin" ? 1 : 0);
    if (seen > 0) {
      x.fillStyle = `rgba(236,228,210,${0.9 * seen})`;
      for (let i = 0; i < 12; i++) { const a = -1.2 + i * 0.2; x.beginPath(); x.arc(cx() + Math.cos(a) * A() * 0.35, cy() + Math.sin(a) * B() * 0.4, B() * 0.2, 0, 7); x.fill(); }
    }
    if (mode === "reel" || mode === "moth") {
      // the pupa waits inside
      x.fillStyle = "#7a4a22"; x.beginPath(); x.ellipse(cx(), cy(), A() * 0.42, B() * 0.4, 0, 0, 7); x.fill();
      for (let i = -3; i <= 3; i++) { x.strokeStyle = "rgba(40,20,10,.4)"; x.beginPath(); x.moveTo(cx() + i * A() * 0.1, cy() - B() * 0.36); x.lineTo(cx() + i * A() * 0.1, cy() + B() * 0.36); x.stroke(); }
    }
    x.globalAlpha = mode === "reel" ? Math.max(0, 1 - reel) : 1; x.drawImage(silk, 0, 0, st.w, st.h); x.globalAlpha = 1;
    if (mode === "reel") {
      const rx = st.w < 520 ? st.w * 0.85 : st.w * 0.8, ry = st.h * 0.3, rr = Math.min(60, st.w * 0.1);
      rot += 0.25;
      x.strokeStyle = gold ? HEX[GOLD] : "#f5efe2"; x.lineWidth = 1;
      x.beginPath(); x.moveTo(cx() + A() * 0.9, cy()); x.lineTo(rx, ry + rr); x.stroke();
      x.strokeStyle = "#6b4a2e"; x.lineWidth = 3; x.beginPath(); x.arc(rx, ry, rr, 0, 7); x.stroke();
      for (let i = 0; i < 6; i++) { const a = rot + i * Math.PI / 3; x.beginPath(); x.moveTo(rx, ry); x.lineTo(rx + Math.cos(a) * rr, ry + Math.sin(a) * rr); x.stroke(); }
      x.strokeStyle = gold ? "rgba(233,165,60,.8)" : "rgba(245,239,226,.8)"; x.lineWidth = Math.max(1, reel * 14); x.beginPath(); x.arc(rx, ry, rr - 3, 0, 7); x.stroke();
    }
    if (head && mode === "spin" && done < 1) { x.fillStyle = "#e0413a"; x.beginPath(); x.arc(head[0], head[1], 2.5, 0, 7); x.fill(); }
    const m = Math.round((mode === "reel" ? reel : done) * METRES);
    out.textContent = mode === "reel" ? T(`${m} m reeled off one cocoon, in one piece`, `สาวออกจากรังเดียวได้ ${m} เมตร ไม่ขาดเลย`, `ទាញចេញពីសំបុកតែមួយ បាន ${m} ម៉ែត្រ ជាសរសៃតែមួយ`)
      : T(`${m} m of silk spun · hour ${Math.round(done * HOURS)} of about ${HOURS}`, `ปั่นใยไหมแล้ว ${m} เมตร · ชั่วโมงที่ ${Math.round(done * HOURS)} จากราว ${HOURS}`, `បញ្ចេញសរសៃសូត្របាន ${m} ម៉ែត្រ · ម៉ោងទី ${Math.round(done * HOURS)} ក្នុងប្រហែល ${HOURS}`);
  }
  setup();
  if (STILL) { while (done < 0.8) spin(2000); draw(); }
  document.querySelectorAll("[data-cocoon]").forEach(b => b.addEventListener("click", () => {
    const k = b.dataset.cocoon;
    if (k === "reel") { if (done < 0.3) while (done < 1) spin(4000); done = 1; mode = "reel"; reel = 0; }
    else if (k === "again") setup();
    else if (k === "gold") { gold = !gold; setup(); }
    else if (k === "fast") { while (done < 1) spin(4000); }
    draw();
  }));
  addEventListener("resize", () => { setup(); draw(); });
  loop(cv, dt => {
    if (mode === "spin") { const h = done < 1 ? spin(Math.round(dt * 900)) : null; draw(h); }
    else if (mode === "reel") { reel = Math.min(1, reel + dt * 0.12); draw(); }
  });
}

// ---------- the Silk Road ----------
function road() {
  const cv = $("#road-cv"); if (!cv) return;
  const out = $("#road-out");
  const TOWNS = [
    ["Chang'an (Xi'an)", "ฉางอาน (ซีอาน)", 34.34, 108.94, "ឆាងអាន (ស៊ីអាន)"], ["Dunhuang", "ตุนหวง", 40.14, 94.66, "ទុនហួង"], ["Kashgar", "คัชการ์", 39.47, 75.99, "កាស្ហ្គារ"],
    ["Samarkand", "ซามาร์คันด์", 39.65, 66.96, "សាម៉ាកាន់"], ["Merv", "เมิร์ฟ", 37.66, 62.19, "មឺវ"], ["Ctesiphon", "ซีทีฟอน", 33.09, 44.58, "ស៊ីធីផុន"],
    ["Antioch", "แอนติออก", 36.2, 36.16, "អង់ទីយ៉ូក"], ["Constantinople", "คอนสแตนติโนเปิล", 41.01, 28.98, "កុងស្តង់ទីណូប្លឺ"],
    ["Guangzhou", "กว่างโจว", 23.13, 113.26, "ក្វាងចូវ"], ["Oc Eo", "ออกแอว", 10.25, 105.15, "អូរកែវ"], ["Malacca", "มะละกา", 2.19, 102.25, "ម៉ាឡាកា"],
    ["Galle", "กอลล์", 6.03, 80.22, "ហ្គាល"], ["Muziris", "มุซิริส", 10.2, 76.2, "មូស៊ីរីស"], ["Aden", "เอเดน", 12.8, 45.0, "អាដែន"], ["Alexandria", "อเล็กซานเดรีย", 31.2, 29.92, "អាឡិចសង់ឌ្រី"],
    ["Angkor", "นครธม", 13.41, 103.87, "អង្គរ"], ["Ayutthaya", "อยุธยา", 14.35, 100.57, "អយុធ្យា"], ["Chiang Mai", "เชียงใหม่", 18.79, 98.98, "ឈៀងម៉ៃ"],
  ];
  const LAND = [0, 1, 2, 3, 4, 5, 6, 7], SEA = [8, 9, 10, 11, 12, 13, 14];
  let land = null, sel = [], st, t = 0;
  fetch((LANG === "en" ? "" : "../") + "land.json").then(r => r.json()).then(j => { land = j; draw(); }).catch(() => {});
  const LON0 = 18, LON1 = 122, LAT0 = -4, LAT1 = 50;
  const P = (lat, lon) => [(lon - LON0) / (LON1 - LON0) * st.w, (LAT1 - lat) / (LAT1 - LAT0) * st.h];
  function km(a, b) {
    const r = Math.PI / 180, [la1, lo1] = [TOWNS[a][2] * r, TOWNS[a][3] * r], [la2, lo2] = [TOWNS[b][2] * r, TOWNS[b][3] * r];
    const h = Math.sin((la2 - la1) / 2) ** 2 + Math.cos(la1) * Math.cos(la2) * Math.sin((lo2 - lo1) / 2) ** 2;
    return 2 * 6371 * Math.asin(Math.sqrt(h));
  }
  function along(route, a, b) { let i = route.indexOf(a), j = route.indexOf(b); if (i > j) [i, j] = [j, i]; let d = 0; for (let k = i; k < j; k++) d += km(route[k], route[k + 1]); return d; }
  function draw() {
    const x = st.x; x.fillStyle = "#16303a"; x.fillRect(0, 0, st.w, st.h);
    if (land) {
      x.fillStyle = "#3a2a1e"; x.strokeStyle = "rgba(233,165,60,.25)"; x.lineWidth = 0.6;
      for (const ring of land) {
        let inside = false; for (let i = 0; i < ring.length; i += 2) if (ring[i] > LON0 - 30 && ring[i] < LON1 + 30 && ring[i + 1] > LAT0 - 20) { inside = true; break; }
        if (!inside) continue;
        x.beginPath(); for (let i = 0; i < ring.length; i += 2) { const p = P(ring[i + 1], ring[i]); i ? x.lineTo(p[0], p[1]) : x.moveTo(p[0], p[1]); } x.fill(); x.stroke();
      }
    }
    function path(route, col, dash) {
      x.strokeStyle = col; x.lineWidth = 2.2; x.setLineDash(dash); x.lineDashOffset = -t * 20; x.beginPath();
      route.forEach((k, i) => { const p = P(TOWNS[k][2], TOWNS[k][3]); i ? x.lineTo(p[0], p[1]) : x.moveTo(p[0], p[1]); }); x.stroke(); x.setLineDash([]);
    }
    path(LAND, HEX[GOLD], [8, 5]); path(SEA, "#7fd1c7", [3, 5]);
    // a caravan and a ship, moving
    function mover(route, f, col, r) {
      const n = route.length - 1, s = (f % 1) * n, i = Math.floor(s), u = s - i;
      const a = P(TOWNS[route[i]][2], TOWNS[route[i]][3]), b = P(TOWNS[route[i + 1]][2], TOWNS[route[i + 1]][3]);
      x.fillStyle = col; x.beginPath(); x.arc(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, r, 0, 7); x.fill();
    }
    mover(LAND, t * 0.02, "#fff2d0", 4.5); mover(SEA, t * 0.03 + 0.4, "#dff7f3", 4);
    TOWNS.forEach((tw, k) => {
      const p = P(tw[2], tw[3]), on = sel.includes(k), home = k === 17;
      x.fillStyle = on ? "#e0413a" : home ? HEX[PINK] : "#f4ead8"; x.beginPath(); x.arc(p[0], p[1], on ? 6 : 4, 0, 7); x.fill();
      if (st.w > 560 || on || home || k === 0 || k === 7) {
        x.fillStyle = "#f4ead8"; x.font = `${on ? 700 : 400} 12px ${UI}`; x.textBaseline = "middle";
        x.textAlign = p[0] > st.w * 0.8 ? "right" : "left"; x.fillText(T(tw[0], tw[1], tw[4]), p[0] + (p[0] > st.w * 0.8 ? -8 : 8), p[1] - 8);
      }
    });
  }
  function say() {
    if (sel.length < 2) { out.textContent = sel.length ? T(`From ${TOWNS[sel[0]][0]} to …? Tap a second town.`, `จาก${TOWNS[sel[0]][1]} ไป…? แตะเมืองที่สอง`, `ពី${TOWNS[sel[0]][4]} ទៅ…? ចុចទីក្រុងទីពីរ។`) : T("Tap two towns.", "แตะสองเมือง", "ចុចលើទីក្រុងពីរ។"); return; }
    const [a, b] = sel, nA = T(TOWNS[a][0], TOWNS[a][1], TOWNS[a][4]), nB = T(TOWNS[b][0], TOWNS[b][1], TOWNS[b][4]);
    if (LAND.includes(a) && LAND.includes(b)) {
      const d = along(LAND, a, b);
      out.textContent = T(`${nA} → ${nB}: about ${Math.round(d).toLocaleString()} km along the caravan towns, as the crow flies between each. At 30 km a day, ${Math.round(d / 30)} camel days.`,
        `${nA} → ${nB}: ราว ${Math.round(d).toLocaleString()} กม. วัดเส้นตรงจากเมืองคาราวานหนึ่งไปอีกเมือง วันละ 30 กม. ใช้อูฐ ${Math.round(d / 30)} วัน`, `${nA} → ${nB}៖ ប្រហែល ${Math.round(d).toLocaleString()} គ.ម តាមទីក្រុងក្បួនដំណើរ វាស់ត្រង់ពីមួយទៅមួយ។ ដើរ 30 គ.ម ក្នុងមួយថ្ងៃ ត្រូវការអូដ្ឋ ${Math.round(d / 30)} ថ្ងៃ។`);
    } else if (SEA.includes(a) && SEA.includes(b)) {
      const d = along(SEA, a, b);
      out.textContent = T(`${nA} → ${nB}: about ${Math.round(d).toLocaleString()} km port to port. At 5 knots under a monsoon wind, ${Math.round(d / 222)} days at sea.`,
        `${nA} → ${nB}: ราว ${Math.round(d).toLocaleString()} กม. ท่าต่อท่า แล่นใบด้วยลมมรสุม 5 นอต ใช้ ${Math.round(d / 222)} วันในทะเล`, `${nA} → ${nB}៖ ប្រហែល ${Math.round(d).toLocaleString()} គ.ម ពីកំពង់ផែមួយទៅមួយ។ ក្ដោងតាមខ្យល់មូសុង 5 ណុត ត្រូវការ ${Math.round(d / 222)} ថ្ងៃលើសមុទ្រ។`);
    } else {
      const d = km(a, b);
      out.textContent = T(`${nA} → ${nB}: ${Math.round(d).toLocaleString()} km in a straight line over the globe. At 30 km a day, ${Math.round(d / 30)} days.`,
        `${nA} → ${nB}: ${Math.round(d).toLocaleString()} กม. เป็นเส้นตรงบนผิวโลก วันละ 30 กม. ใช้ ${Math.round(d / 30)} วัน`, `${nA} → ${nB}៖ ${Math.round(d).toLocaleString()} គ.ម ជាបន្ទាត់ត្រង់លើផែនដី។ 30 គ.ម ក្នុងមួយថ្ងៃ ត្រូវការ ${Math.round(d / 30)} ថ្ងៃ។`);
    }
  }
  function setup() { st = fit(cv, Math.round(Math.min(520, Math.max(280, cv.clientWidth * 0.55)))); draw(); }
  cv.addEventListener("click", ev => {
    const r = cv.getBoundingClientRect(), mx = ev.clientX - r.left, my = ev.clientY - r.top;
    let best = -1, bd = 26 * 26;
    TOWNS.forEach((tw, k) => { const p = P(tw[2], tw[3]), d = (p[0] - mx) ** 2 + (p[1] - my) ** 2; if (d < bd) { bd = d; best = k; } });
    if (best < 0) return;
    sel = sel.length >= 2 ? [best] : sel.concat(best).filter((v, i, a) => a.indexOf(v) === i);
    say(); draw();
  });
  setup(); say(); addEventListener("resize", setup);
  if (!STILL) loop(cv, dt => { t += dt; draw(); });
}

// ---------- start ----------
function start() {
  const D = shawlDesign();
  hero(D); shawl(D);
  [draft, ikat, frieze, satin, mathCloth, cocoon, road].forEach(f => { try { f(); } catch (e) { console.error(e); } });
}
const ready = document.fonts && document.fonts.load ? Promise.race([document.fonts.load(`700 20px ${KHMER}`, KOU), new Promise(r => setTimeout(r, 1500))]) : Promise.resolve();
ready.then(start, start);
})();
