<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>SINOBY — Медиаплан</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --black:  #0A0A0A;
  --white:  #F5F3EF;
  --muted:  rgba(245,243,239,.35);
  --border: rgba(245,243,239,.08);
  --surf:   rgba(245,243,239,.05);
  --gold:   #C9A96E;
  --gold-l: rgba(201,169,110,.12);
}

*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; -webkit-tap-highlight-color:transparent; }

html,body {
  width:100%; height:100%;
  background:var(--black);
  color:var(--white);
  font-family:'Jost',sans-serif;
  overflow:hidden;
  -webkit-font-smoothing:antialiased;
}

/* ══ SCREENS ══ */
.screen {
  position:absolute; inset:0; z-index:1;
  display:flex; flex-direction:column;
  align-items:center; justify-content:flex-start;
  padding:0 24px;
  opacity:0; pointer-events:none;
  transition:opacity .38s ease, transform .38s ease;
  transform:translateY(12px);
  overflow-y:auto; overflow-x:hidden;
}
.screen.active { opacity:1; pointer-events:all; transform:translateY(0); }
.screen.exit   { opacity:0; transform:translateY(-10px); pointer-events:none; }
#s0,#s1,#s2,#s3 { padding:0; overflow:hidden; }
#s0 { cursor:pointer; }

/* ══ SPLASH ══ */
.splash-wrap { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.splash-inner { display:flex; flex-direction:column; align-items:center; animation:fadeUp .8s ease both; }
@keyframes fadeUp { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:none} }
.logo-mark { width:200px; height:56px; margin-bottom:28px; animation:fadeUp .8s .1s ease both; }
.logo-mark svg { width:100%; height:100%; }
.logo-word { font-weight:700; font-size:32px; letter-spacing:10px; color:var(--white); animation:fadeUp .8s .2s ease both; }
.logo-line { width:40px; height:1px; background:var(--gold); margin:18px 0; animation:fadeUp .8s .3s ease both; }
.logo-tag  { font-weight:300; font-size:14px; letter-spacing:2px; color:rgba(245,243,239,.75); animation:fadeUp .8s .4s ease both; }
.tap-hint  { position:absolute; bottom:48px; font-size:10px; letter-spacing:3px; text-transform:uppercase; color:var(--muted); animation:blink 2.5s ease-in-out infinite .8s, fadeUp .8s .6s ease both; }
@keyframes blink { 0%,100%{opacity:.2} 50%{opacity:.65} }

/* ═══════════════════════════════════
   S1  — вопрос вверху по центру,
         3 равных блока снизу
═══════════════════════════════════ */
.s1-wrap { position:absolute; inset:0; display:flex; flex-direction:column; }

.s1-q {
  flex:0 0 30%;
  display:flex; align-items:center; justify-content:center;
  padding:0 32px;
  border-bottom:1px solid var(--border);
}
.s1-q-text {
  font-size:24px;
  font-weight:600;
  line-height:1.3;
  color:var(--white);
  text-align:center;
}

.s1-choices { flex:1; display:flex; flex-direction:column; }

.s1-tile {
  flex:1;
  position:relative;
  display:flex; align-items:center; justify-content:center;
  flex-direction:column; gap:6px;
  border:none; border-bottom:1px solid var(--border);
  background:transparent;
  cursor:pointer; -webkit-appearance:none;
  overflow:hidden;
  transition:background .18s;
}
.s1-tile:last-child { border-bottom:none; }

/* фото-подложка */
.s1-photo { position:absolute; inset:0; background-size:cover; background-position:center; filter:brightness(.65); opacity:0; transition:opacity .7s ease; }
.s1-photo.loaded { opacity:1; }
/* затемнение */
.s1-overlay { position:absolute; inset:0; background:rgba(10,10,10,.35); }

/* золотая полоска слева при тапе */
.s1-tile::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; background:var(--gold); transform:scaleY(0); transition:transform .22s ease; transform-origin:center; }
.s1-tile:active { background:rgba(201,169,110,.07); }
.s1-tile:active::before, .s1-tile.flash::before { transform:scaleY(1); }
.s1-tile.flash { background:rgba(201,169,110,.09); }

.s1-label {
  position:relative; z-index:2;
  font-size:34px;
  font-weight:600;
  color:var(--white);
  text-align:center;
}
.s1-sub {
  position:relative; z-index:2;
  font-size:11px;
  font-weight:400;
  letter-spacing:2px;
  text-transform:uppercase;
  color:var(--muted);
  text-align:center;
}

/* ═══════════════════════════════════
   FULLSCREEN WRAPPER (S2, S3)
═══════════════════════════════════ */
.fs-wrap { position:absolute; inset:0; display:flex; flex-direction:column; }

/* Заголовок — по центру, один шрифт, белый */
.fs-q {
  flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  padding:28px 32px 24px;
  border-bottom:1px solid var(--border);
}
.fs-q-text {
  font-size:24px;
  font-weight:600;
  color:var(--white);
  text-align:center;
  line-height:1.3;
}

/* ═══════════════════════════════════
   S2 — регионы 2×4
═══════════════════════════════════ */
.region-grid {
  flex:1;
  display:grid;
  grid-template-columns:1fr 1fr;
  grid-template-rows:repeat(4,1fr);
}

.reg-btn {
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px;
  background:transparent; border:none;
  border-right:1px solid var(--border);
  border-bottom:1px solid var(--border);
  cursor:pointer; -webkit-appearance:none;
  position:relative; overflow:hidden;
  transition:background .15s;
  min-height:80px;
}
.reg-btn:nth-child(even)   { border-right:none; }
.reg-btn:nth-child(n+7)    { border-bottom:none; }
.reg-btn::before { content:''; position:absolute; inset:0; background:var(--gold-l); opacity:0; transition:opacity .18s; }
.reg-btn.selected::before,.reg-btn.flash::before { opacity:1; }
.reg-btn.selected { box-shadow:inset 0 0 0 1.5px rgba(201,169,110,.45); }
.reg-btn:active { background:rgba(201,169,110,.06); }

.reg-short {
  font-size:11px;
  font-weight:400;
  color:var(--muted);
  letter-spacing:1px;
  position:relative; z-index:1;
}
.reg-full {
  font-size:16px;
  font-weight:600;
  color:var(--white);
  letter-spacing:.3px;
  text-align:center;
  padding:0 6px;
  position:relative; z-index:1;
}

/* ═══════════════════════════════════
   S3 — города 2×3
═══════════════════════════════════ */
.city-grid {
  flex:1;
  display:grid;
  grid-template-columns:1fr 1fr;
  grid-template-rows:repeat(3,1fr);
}

.city-btn {
  display:flex; align-items:center; justify-content:center;
  background:transparent; border:none;
  border-right:1px solid var(--border);
  border-bottom:1px solid var(--border);
  cursor:pointer; -webkit-appearance:none;
  position:relative; overflow:hidden;
  transition:background .15s;
  font-size:17px;
  font-weight:500;
  color:var(--white);
  text-align:center;
  padding:0 14px;
}
.city-btn:nth-child(even) { border-right:none; }
.city-btn:nth-child(n+5)  { border-bottom:none; }
.city-btn::before { content:''; position:absolute; inset:0; background:var(--gold-l); opacity:0; transition:opacity .18s; }
.city-btn.selected::before,.city-btn.flash::before { opacity:1; }
.city-btn.selected { box-shadow:inset 0 0 0 1.5px rgba(201,169,110,.45); }
.city-btn:active { background:rgba(201,169,110,.06); }
.city-btn span { position:relative; z-index:1; }

/* ═══════════════════════════════════
   S4+ — скролл-экраны
   ВОПРОС: по центру, Jost, белый
═══════════════════════════════════ */
.scroll-screen-inner {
  width:100%; max-width:420px;
  display:flex; flex-direction:column;
  align-items:center;
  padding-top:0;
}

/* Шапка с номером шага */
.step-bar {
  width:100%; max-width:420px;
  display:flex; align-items:center; justify-content:space-between;
  padding:24px 0 20px;
  border-bottom:1px solid var(--border);
  margin-bottom:28px;
  flex-shrink:0;
}
.step-brand { font-weight:600; font-size:13px; letter-spacing:4px; color:var(--gold); }
.step-num   { font-size:11px; letter-spacing:2px; color:var(--muted); }

/* Вопрос — ПО ЦЕНТРУ, JOST, БЕЛЫЙ */
.q {
  width:100%;
  font-size:24px;
  font-weight:600;
  color:var(--white);
  text-align:center;
  line-height:1.3;
  margin-bottom:28px;
  flex-shrink:0;
}

/* ── БРЕНДЫ (чипы 3 кол) ── */
.brand-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:7px; width:100%; }
.brand-btn {
  background:var(--surf); border:1px solid var(--border); border-radius:3px;
  padding:13px 4px; cursor:pointer; text-align:center;
  font-size:11px; font-weight:600; letter-spacing:.8px;
  color:var(--white);
  transition:background .15s,border-color .15s,color .15s;
  -webkit-appearance:none; position:relative; overflow:hidden;
}
.brand-btn::after { content:''; position:absolute; left:0; top:0; bottom:0; width:2px; background:var(--gold); opacity:0; transition:opacity .15s; }
.brand-btn.selected { border-color:rgba(201,169,110,.4); background:var(--gold-l); color:var(--gold); }
.brand-btn.selected::after { opacity:1; }
.brand-btn:active { transform:scale(.97); }

/* ── SPEC / GOAL / CHANNEL CARDS ── */
.card-list { display:flex; flex-direction:column; gap:8px; width:100%; }
.card-btn {
  display:flex; align-items:center; gap:14px;
  background:var(--surf); border:1px solid var(--border); border-radius:4px;
  padding:16px 18px; cursor:pointer;
  transition:background .15s,border-color .15s;
  -webkit-appearance:none; position:relative; overflow:hidden;
  text-align:left;
}
.card-btn::after { content:''; position:absolute; left:0; top:0; bottom:0; width:2px; background:var(--gold); opacity:0; transition:opacity .15s; }
.card-btn.selected { border-color:rgba(201,169,110,.35); background:var(--gold-l); }
.card-btn.selected::after { opacity:1; }
.card-btn:active { transform:scale(.99); }

.card-num  { font-size:18px; font-weight:700; color:var(--white); opacity:.25; width:20px; flex-shrink:0; transition:opacity .15s; }
.card-btn.selected .card-num { opacity:1; color:var(--gold); }
.card-ico  { font-size:20px; width:28px; flex-shrink:0; }
.card-main { font-size:17px; font-weight:600; color:var(--white); line-height:1.2; flex:1; text-align:left; }
.card-sub  { font-size:11px; font-weight:400; color:var(--muted); margin-top:3px; text-align:left; }
.card-chk  { font-size:14px; color:var(--gold); opacity:0; flex-shrink:0; transition:opacity .15s; margin-left:auto; }
.card-btn.selected .card-chk { opacity:1; }

/* ── КАНАЛЫ 2-кол ── */
.channel-grid { display:grid; grid-template-columns:1fr 1fr; gap:8px; width:100%; }
.ch-btn {
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px;
  background:var(--surf); border:1px solid var(--border); border-radius:4px;
  padding:20px 12px; cursor:pointer;
  transition:background .15s,border-color .15s;
  -webkit-appearance:none; position:relative; overflow:hidden;
}
.ch-btn::after { content:''; position:absolute; left:0; top:0; right:0; height:2px; background:var(--gold); opacity:0; transition:opacity .15s; }
.ch-btn.selected { border-color:rgba(201,169,110,.35); background:var(--gold-l); }
.ch-btn.selected::after { opacity:1; }
.ch-btn:active { transform:scale(.98); }
.ch-ico  { font-size:22px; }
.ch-name { font-size:13px; font-weight:600; color:var(--white); text-align:center; }
.ch-sub  { font-size:10px; font-weight:400; color:var(--muted); text-align:center; }
.channel-grid .ch-btn:last-child:nth-child(odd) { grid-column:1/-1; max-width:calc(50% - 4px); margin:0 auto; }

/* ── CHANNEL NEXT BAR ── */
.ch-next-bar {
  position:fixed; bottom:0; left:0; right:0; z-index:10;
  padding:16px 24px calc(16px + env(safe-area-inset-bottom));
  background:linear-gradient(to top, var(--black) 55%, transparent);
  display:flex; justify-content:center;
}
.ch-next-btn {
  width:100%; max-width:420px;
  background:var(--gold); color:var(--black);
  border:none; border-radius:3px; padding:16px 24px;
  font-size:12px; font-weight:700; letter-spacing:3px; text-transform:uppercase;
  cursor:pointer; transition:opacity .15s,transform .1s;
}
.ch-next-btn:active { transform:scaleY(.97); opacity:.85; }

/* ── ИТОГ ── */
.result-label    { font-size:10px; font-weight:500; letter-spacing:3px; text-transform:uppercase; color:var(--gold); margin-bottom:10px; width:100%; }
.result-headline { font-size:28px; font-weight:600; color:var(--white); line-height:1.2; width:100%; margin-bottom:24px; }
.result-table    { width:100%; border:1px solid var(--border); border-radius:4px; overflow:hidden; margin-bottom:16px; }
.res-row         { display:flex; justify-content:space-between; align-items:center; padding:13px 16px; border-bottom:1px solid var(--border); }
.res-row:last-child { border-bottom:none; }
.res-lbl         { font-size:9px; font-weight:500; letter-spacing:1.5px; text-transform:uppercase; color:var(--muted); flex-shrink:0; }
.res-val         { font-size:14px; font-weight:600; color:var(--white); text-align:right; max-width:62%; line-height:1.2; }
.send-btn        { width:100%; background:var(--gold); color:var(--black); border:none; border-radius:3px; padding:18px 24px; font-size:12px; font-weight:700; letter-spacing:3px; text-transform:uppercase; cursor:pointer; transition:opacity .15s,transform .1s; }
.send-btn:active { transform:scaleY(.97); opacity:.85; }

/* ── PROGRESS ── */
.progress-bar  { position:fixed; top:0; left:0; right:0; z-index:20; height:2px; background:rgba(245,243,239,.06); opacity:0; transition:opacity .3s; pointer-events:none; }
.progress-fill { height:100%; background:var(--gold); transition:width .45s ease; }
.progress-bar.show { opacity:1; }

/* ── BACK ── */
.back-btn { position:fixed; top:16px; left:16px; z-index:30; width:36px; height:36px; border-radius:50%; background:rgba(10,10,10,.75); border:1px solid rgba(245,243,239,.12); backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); display:flex; align-items:center; justify-content:center; cursor:pointer; opacity:0; pointer-events:none; transition:opacity .28s; }
.back-btn.show { opacity:1; pointer-events:all; }
.back-btn:active { background:rgba(35,35,35,.9); }
.back-btn svg { width:15px; height:15px; stroke:var(--white); fill:none; }

/* ── БЮДЖЕТ ── */
.budget-grid { display:flex; flex-direction:column; gap:10px; }
.budget-btn {
  width:100%; display:flex; align-items:center; justify-content:center;
  background:var(--surf); border:1px solid var(--border); border-radius:4px;
  padding:18px 22px; cursor:pointer; -webkit-appearance:none;
  position:relative; overflow:hidden;
  transition:background .15s, border-color .15s, transform .1s;
}
.budget-btn::after { content:''; position:absolute; left:0; top:0; bottom:0; width:2px; background:var(--gold); opacity:0; transition:opacity .15s; }
.budget-btn.selected { border-color:rgba(201,169,110,.4); background:var(--gold-l); }
.budget-btn.selected::after { opacity:1; }
.budget-btn:active { transform:scale(.99); }
.budget-range { font-size:17px; font-weight:600; color:var(--white); letter-spacing:.3px; text-align:center; }
.budget-sub   { display:none; }

/* ── FORECAST CARDS ── */
.forecast-cards {
  display:grid; grid-template-columns:1fr 1fr; gap:10px;
  width:100%;
}
.fc-card {
  background:var(--surf); border:1px solid var(--border); border-radius:4px;
  padding:20px 16px; text-align:center;
  position:relative; overflow:hidden;
}
.fc-card::after {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background:var(--gold);
}
.fc-card-val {
  font-size:32px; font-weight:700; color:var(--white);
  letter-spacing:-1px; line-height:1;
  margin-bottom:8px;
}
.fc-card-lbl {
  font-size:10px; font-weight:500; letter-spacing:1.5px;
  text-transform:uppercase; color:var(--muted);
}

/* ── SPINNER ── */
.spinner {
  width:36px; height:36px;
  border:2px solid var(--border);
  border-top-color:var(--gold);
  border-radius:50%;
  animation:spin .8s linear infinite;
}
@keyframes spin { to{transform:rotate(360deg)} }

.pad { height:36px; flex-shrink:0; }
.screen::-webkit-scrollbar { width:3px; }
.screen::-webkit-scrollbar-thumb { background:rgba(201,169,110,.15); border-radius:2px; }
</style>
</head>
<body>

<div class="progress-bar" id="progressBar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
<button class="back-btn" id="backBtn" onclick="goBack()">
  <svg viewBox="0 0 24 24" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
</button>

<!-- ══ S0: SPLASH ══ -->
<div class="screen active" id="s0" onclick="goTo(1)">
  <div class="splash-wrap">
    <div class="splash-inner">
      <div class="logo-mark">
        <img src="https://sinoby.ru/site/img/logo_white.svg"
             alt="SINOBY"
             style="width:100%;height:100%;object-fit:contain"
             onerror="this.style.display='none';document.getElementById('logo-fallback').style.display='block'">
        <!-- Fallback если svg не загрузится -->
        <svg id="logo-fallback" viewBox="0 0 80 80" fill="none" style="display:none">
          <circle cx="40" cy="40" r="38" stroke="#C9A96E" stroke-width=".7" opacity=".25"/>
          <path d="M54 28C54 28 46 22 38 22C29 22 24 27.5 24 33.5C24 39.5 30 42 40 44C50 46 56 48.5 56 54.5C56 60.5 50 58 40 58C31 58 26 53 26 53" stroke="#C9A96E" stroke-width="3.5" stroke-linecap="round" fill="none"/>
        </svg>
      </div>
      <div class="logo-word" style="display:none">SINOBY</div>
      <div class="logo-line"></div>
      <div class="logo-tag">В тени вашего успеха</div>
    </div>
    <div class="tap-hint">Нажмите, чтобы начать</div>
  </div>
</div>

<!-- ══ S1: КАТЕГОРИЯ ══ -->
<div class="screen" id="s1">
  <div class="s1-wrap">
    <div class="s1-q">
      <div class="s1-q-text">Вы хотите получить<br>Медиаплан для чего?</div>
    </div>
    <div class="s1-choices">
      <button class="s1-tile" onclick="pickCat(this,'Авто')">
        <div class="s1-photo" id="ph-auto" style="background-image:url('https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=900&q=80&auto=format&fit=crop')"></div>
        <div class="s1-overlay"></div>
        <div class="s1-label">Авто</div>
        <div class="s1-sub">дилеры · марки · сервис</div>
      </button>
      <button class="s1-tile" onclick="pickCat(this,'Недвижимость')">
        <div class="s1-photo" id="ph-realty" style="background-image:url('https://images.unsplash.com/photo-1486325212027-8081e485255e?w=900&q=80&auto=format&fit=crop')"></div>
        <div class="s1-overlay"></div>
        <div class="s1-label">Недвижимость</div>
        <div class="s1-sub">ЖК · застройщики · агентства</div>
      </button>
      <button class="s1-tile" onclick="pickCat(this,'Медицина')">
        <div class="s1-photo" id="ph-med" style="background-image:url('https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=900&q=80&auto=format&fit=crop')"></div>
        <div class="s1-overlay"></div>
        <div class="s1-label">Медицина</div>
        <div class="s1-sub">клиники · центры · стоматологии</div>
      </button>
    </div>
  </div>
</div>

<!-- ══ S2: РЕГИОН ══ -->
<div class="screen" id="s2">
  <div class="fs-wrap">
    <div class="fs-q">
      <div class="fs-q-text">Ваш регион</div>
    </div>
    <div class="region-grid" id="regionGrid"></div>
  </div>
</div>

<!-- ══ S3: ГОРОД ══ -->
<div class="screen" id="s3">
  <div class="fs-wrap">
    <div class="fs-q">
      <div class="fs-q-text" id="cityQ">Выберите ваш город</div>
    </div>
    <div class="city-grid" id="cityGrid"></div>
  </div>
</div>

<!-- ══ S4: БРЕНД / КАТЕГОРИЯ / НАПРАВЛЕНИЕ ══ -->
<div class="screen" id="s4">
  <div class="step-bar"><span class="step-brand">SINOBY</span><span class="step-num">04 / 08</span></div>
  <div class="q" id="specQ">Выберите детали</div>
  <div id="specContent" style="width:100%;max-width:420px"></div>
  <div class="pad"></div>
</div>

<!-- ══ S5: ЦЕЛЬ ══ -->
<div class="screen" id="s5">
  <div class="step-bar"><span class="step-brand">SINOBY</span><span class="step-num">05 / 08</span></div>
  <div class="q">Цель кампании?</div>
  <div class="card-list" id="goalList" style="max-width:420px;width:100%"></div>
  <div class="pad"></div>
</div>

<!-- ══ S6: КАНАЛ (множественный выбор) ══ -->
<div class="screen" id="s6">
  <div class="step-bar"><span class="step-brand">SINOBY</span><span class="step-num">06 / 08</span></div>
  <div class="q">Какие каналы интересны?</div>
  <div class="channel-grid" id="channelGrid" style="max-width:420px;width:100%"></div>
  <div style="height:90px"></div>
</div>

<!-- Кнопка Далее для канала (фиксированная) -->
<div class="ch-next-bar" id="chNextBar" style="display:none">
  <button class="ch-next-btn" id="chNextBtn" onclick="confirmChannels()">
    Далее →
  </button>
</div>

<!-- ══ S7: БЮДЖЕТ ══ -->
<div class="screen" id="s7">
  <div class="step-bar"><span class="step-brand">SINOBY</span><span class="step-num">07 / 08</span></div>
  <div class="q">Укажите ваш бюджет</div>
  <div class="budget-grid" id="budgetGrid" style="max-width:420px;width:100%"></div>
  <div class="pad"></div>
</div>

<!-- ══ S8: ПРОГНОЗ (из таблицы) ══ -->
<div class="screen" id="s8">
  <div class="step-bar"><span class="step-brand">SINOBY</span><span class="step-num">Прогноз</span></div>
  <div style="width:100%;max-width:420px">

    <!-- Состояние: загрузка -->
    <div id="fc-loading" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:260px;gap:16px">
      <div class="spinner"></div>
      <div style="font-size:13px;color:var(--muted);letter-spacing:1px">Считаем прогноз...</div>
    </div>

    <!-- Состояние: ошибка -->
    <div id="fc-error" style="display:none;flex-direction:column;align-items:center;gap:16px;padding:40px 0;text-align:center">
      <div style="font-size:32px">⚠️</div>
      <div style="font-size:15px;font-weight:600;color:var(--white)">Данные не найдены</div>
      <div style="font-size:12px;color:var(--muted);line-height:1.6" id="fc-error-text">По выбранной комбинации нет данных в таблице</div>
      <button class="send-btn" style="margin-top:8px" onclick="goTo(9)">Продолжить без прогноза →</button>
    </div>

    <!-- Состояние: результат -->
    <div id="fc-result" style="display:none;flex-direction:column;gap:0">
      <div class="result-label" style="margin-bottom:8px">Прогноз по вашим параметрам</div>
      <div class="result-headline" style="margin-bottom:24px;font-size:24px" id="fc-headline">—</div>

      <!-- Большие цифры -->
      <div class="forecast-cards">
        <div class="fc-card">
          <div class="fc-card-val" id="fc-calls">—</div>
          <div class="fc-card-lbl">звонков в месяц</div>
        </div>
        <div class="fc-card">
          <div class="fc-card-val" id="fc-price">—</div>
          <div class="fc-card-lbl">цена звонка</div>
        </div>
      </div>

      <!-- Детали -->
      <div class="result-table" style="margin-top:16px">
        <div class="res-row"><span class="res-lbl">Город</span>   <span class="res-val" id="fc-city">—</span></div>
        <div class="res-row"><span class="res-lbl">Марка</span>   <span class="res-val" id="fc-brand">—</span></div>
        <div class="res-row"><span class="res-lbl">Бюджет</span>  <span class="res-val" id="fc-bud">—</span></div>
      </div>

      <div style="font-size:10px;color:var(--muted);text-align:center;margin:14px 0;letter-spacing:.5px">
        Среднее за <span id="fc-months">—</span> мес. на основе исторических данных
      </div>

      <button class="send-btn" onclick="buildResult();goTo(9)">Сформировать запрос →</button>
      <div style="height:32px"></div>
    </div>
  </div>
</div>

<!-- ══ S9: ИТОГ ══ -->
<div class="screen" id="s9">
  <div class="step-bar"><span class="step-brand">SINOBY</span><span class="step-num">Готово</span></div>
  <div style="width:100%;max-width:420px">
    <div class="result-label">Запрос сформирован</div>
    <div class="result-headline">Ваш медиаплан уже в работе</div>
    <div class="result-table">
      <div class="res-row"><span class="res-lbl">Сфера</span>              <span class="res-val" id="r-cat">—</span></div>
      <div class="res-row"><span class="res-lbl">Округ</span>              <span class="res-val" id="r-reg">—</span></div>
      <div class="res-row"><span class="res-lbl">Город</span>              <span class="res-val" id="r-city">—</span></div>
      <div class="res-row"><span class="res-lbl" id="r-sl">Выбор</span>   <span class="res-val" id="r-spec">—</span></div>
      <div class="res-row"><span class="res-lbl">Цель</span>               <span class="res-val" id="r-goal">—</span></div>
      <div class="res-row"><span class="res-lbl">Канал</span>              <span class="res-val" id="r-ch">—</span></div>
      <div class="res-row"><span class="res-lbl">Бюджет</span>             <span class="res-val" id="r-bud">—</span></div>
      <div class="res-row"><span class="res-lbl">Звонков ~</span>          <span class="res-val" id="r-calls">—</span></div>
      <div class="res-row"><span class="res-lbl">Цена звонка ~</span>      <span class="res-val" id="r-price">—</span></div>
    </div>
    <button class="send-btn" onclick="sendResult()">Отправить запрос →</button>
    <div style="height:32px"></div>
  </div>
</div>

<script>
// ══ ВСТАВЬТЕ СЮДА URL ВАШЕГО WEB APP из Google Apps Script ══
const SHEETS_URL = 'https://script.google.com/macros/s/AKfycbyiC_-r_z9r_lQQNM7FVTFxH-i_27TOLvyJUeNI8FySgHGjpEz-qGozIgxV3c-USsQtig/exec';

// Бюджеты по целям
const BUDGETS = {
  'Новые а/м': [
    {label:'150 000 — 300 000 ₽',   range:'150 000 — 300 000 ₽',   max:300000},
    {label:'300 000 — 500 000 ₽',   range:'300 000 — 500 000 ₽',   max:500000},
    {label:'700 000 — 1 000 000 ₽', range:'700 000 — 1 000 000 ₽', max:1000000},
    {label:'от 1 000 000 ₽',         range:'от 1 000 000 ₽',         max:1300000},
  ],
  'АСП': [
    {label:'150 000 — 300 000 ₽',   range:'150 000 — 300 000 ₽',   max:300000},
    {label:'300 000 — 500 000 ₽',   range:'300 000 — 500 000 ₽',   max:500000},
    {label:'700 000 — 1 000 000 ₽', range:'700 000 — 1 000 000 ₽', max:1000000},
    {label:'от 1 000 000 ₽',         range:'от 1 000 000 ₽',         max:1300000},
  ],
  'Сервис': [
    {label:'100 000 — 200 000 ₽',   range:'100 000 — 200 000 ₽',   max:200000},
    {label:'200 000 — 400 000 ₽',   range:'200 000 — 400 000 ₽',   max:400000},
    {label:'400 000 — 500 000 ₽',   range:'400 000 — 500 000 ₽',   max:500000},
    {label:'от 600 000 ₽',           range:'от 600 000 ₽',           max:600000},
  ],
  'Комтранспорт': [
    {label:'150 000 — 300 000 ₽',   range:'150 000 — 300 000 ₽',   max:300000},
    {label:'300 000 — 500 000 ₽',   range:'300 000 — 500 000 ₽',   max:500000},
    {label:'700 000 — 1 000 000 ₽', range:'700 000 — 1 000 000 ₽', max:1000000},
    {label:'от 1 000 000 ₽',         range:'от 1 000 000 ₽',         max:1300000},
  ],
  // Недвижимость
  'Лиды — прямые продажи и звонки': [
    {label:'600 000 ₽',   range:'600 000 ₽',   max:600000},
    {label:'800 000 ₽',   range:'800 000 ₽',   max:800000},
    {label:'1 000 000 ₽', range:'1 000 000 ₽', max:1000000},
    {label:'1 400 000 ₽', range:'1 400 000 ₽', max:1400000},
  ],
  'Привлечение новых людей на сайт': [
    {label:'600 000 ₽',   range:'600 000 ₽',   max:600000},
    {label:'800 000 ₽',   range:'800 000 ₽',   max:800000},
    {label:'1 000 000 ₽', range:'1 000 000 ₽', max:1000000},
    {label:'1 400 000 ₽', range:'1 400 000 ₽', max:1400000},
  ],
  'Удержание тех, кто ещё думает': [
    {label:'600 000 ₽',   range:'600 000 ₽',   max:600000},
    {label:'800 000 ₽',   range:'800 000 ₽',   max:800000},
    {label:'1 000 000 ₽', range:'1 000 000 ₽', max:1000000},
    {label:'1 400 000 ₽', range:'1 400 000 ₽', max:1400000},
  ],
  'Узнаваемость нового ЖК': [
    {label:'600 000 ₽',   range:'600 000 ₽',   max:600000},
    {label:'800 000 ₽',   range:'800 000 ₽',   max:800000},
    {label:'1 000 000 ₽', range:'1 000 000 ₽', max:1000000},
    {label:'1 400 000 ₽', range:'1 400 000 ₽', max:1400000},
  ],
  // Медицина — стандартные бюджеты
  'Запись на приём': [
    {label:'150 000 — 300 000 ₽',   range:'150 000 — 300 000 ₽',   max:300000},
    {label:'300 000 — 500 000 ₽',   range:'300 000 — 500 000 ₽',   max:500000},
    {label:'700 000 — 1 000 000 ₽', range:'700 000 — 1 000 000 ₽', max:1000000},
    {label:'от 1 000 000 ₽',         range:'от 1 000 000 ₽',         max:1300000},
  ],
  'Хуемое': [
    {label:'150 000 — 300 000 ₽',   range:'150 000 — 300 000 ₽',   max:300000},
    {label:'300 000 — 500 000 ₽',   range:'300 000 — 500 000 ₽',   max:500000},
    {label:'700 000 — 1 000 000 ₽', range:'700 000 — 1 000 000 ₽', max:1000000},
    {label:'от 1 000 000 ₽',         range:'от 1 000 000 ₽',         max:1300000},
  ],
  'Второй': [
    {label:'150 000 — 300 000 ₽',   range:'150 000 — 300 000 ₽',   max:300000},
    {label:'300 000 — 500 000 ₽',   range:'300 000 — 500 000 ₽',   max:500000},
    {label:'700 000 — 1 000 000 ₽', range:'700 000 — 1 000 000 ₽', max:1000000},
    {label:'от 1 000 000 ₽',         range:'от 1 000 000 ₽',         max:1300000},
  ],
  'Третий': [
    {label:'150 000 — 300 000 ₽',   range:'150 000 — 300 000 ₽',   max:300000},
    {label:'300 000 — 500 000 ₽',   range:'300 000 — 500 000 ₽',   max:500000},
    {label:'700 000 — 1 000 000 ₽', range:'700 000 — 1 000 000 ₽', max:1000000},
    {label:'от 1 000 000 ₽',         range:'от 1 000 000 ₽',         max:1300000},
  ],
};

// Маппинг цели квиза → направление в таблице (только для Авто)
const GOAL_TO_DIRECTION = {
  'Новые а/м':    'Новые',
  'АСП':          'Пробег',
  'Сервис':       'Сервис',
  'Комтранспорт': 'Коммерческие',
};

const REGIONS = [
  {name:'Центральный',       short:'ЦФО',  cities:['Москва','Воронеж','Ярославль','Тула','Рязань','Липецк']},
  {name:'Северо-Западный',   short:'СЗФО', cities:['Санкт-Петербург','Калининград','Мурманск','Архангельск','Вологда','Петрозаводск']},
  {name:'Южный',             short:'ЮФО',  cities:['Ростов-на-Дону','Краснодар','Волгоград','Сочи','Астрахань','Симферополь']},
  {name:'Северо-Кавказский', short:'СКФО', cities:['Ставрополь','Махачкала','Владикавказ','Грозный','Нальчик','Пятигорск']},
  {name:'Приволжский',       short:'ПФО',  cities:['Казань','Нижний Новгород','Уфа','Самара','Пермь','Саратов']},
  {name:'Уральский',         short:'УрФО', cities:['Екатеринбург','Челябинск','Тюмень','Сургут','Магнитогорск','Нижний Тагил']},
  {name:'Сибирский',         short:'СФО',  cities:['Новосибирск','Красноярск','Иркутск','Кемерово','Барнаул','Томск']},
  {name:'Дальневосточный',   short:'ДФО',  cities:['Владивосток','Хабаровск','Благовещенск','Якутск','Улан-Удэ','Магадан']},
];

const AUTO_BRANDS = [
  'Камаз','Москвич','Мультибренд','Aito','Audi','Belgee','BMW','Changan',
  'Chery','Dongfeng','Evolute','Exeed','Foton','Gac','Geely','Haval City',
  'Haval Pro','Hongqi','Hyundai','Infiniti','Jac','Jaecoo','Jetour','Jaguar',
  'Kgm','Kia','Knewstar','Lada','Land Rover','Lexus','Li Xiang','Mazda',
  'Mercedes-Benz','Mini','Nordcross','Omoda','Porsche','Sitrak','Skoda',
  'Solaris','Sollers','Subaru','Tank','Tenet','Toyota','Vag','Voge',
  'Volkswagen','Volvo','Voyah','Wey'
];

const REALTY_OPTS = [
  {num:'01', main:'Новостройки',             sub:'Квартиры в строящихся домах и ЖК'},
  {num:'02', main:'Загородная недвижимость',  sub:'Дома, коттеджи, дачи, участки'},
  {num:'03', main:'Коммерческая',             sub:'Офисы, склады, торговые площади'},
  {num:'04', main:'Инвестиционная',           sub:'Апартаменты, доходные объекты'},
];
const MED_OPTS = [
  {num:'01', main:'Приёмы специалистов',     sub:'Терапевты, узкие специалисты'},
  {num:'02', main:'Диагностика и анализы',   sub:'МРТ, УЗИ, КТ, лабораторные'},
  {num:'03', main:'Хирургия и стоматология', sub:'Операции, имплантация, ортопедия'},
  {num:'04', main:'Реабилитация и эстетика', sub:'Физиотерапия, косметология, spa'},
];

const GOALS = {
  'Авто': [
    {ico:'🚗', main:'Новые а/м'},
    {ico:'🔄', main:'АСП'},
    {ico:'⚙️', main:'Сервис'},
    {ico:'🚛', main:'Комтранспорт'},
  ],
  'Недвижимость': [
    {ico:'📞', main:'Лиды — прямые продажи и звонки'},
    {ico:'🌐', main:'Привлечение новых людей на сайт'},
    {ico:'🔄', main:'Удержание тех, кто ещё думает'},
    {ico:'🏗️', main:'Узнаваемость нового ЖК'},
  ],
  'Медицина': [
    {ico:'📅', main:'Запись на приём'},
    {ico:'💊', main:'Хуемое'},
    {ico:'🏥', main:'Второй'},
    {ico:'❤️', main:'Третий'},
  ],
};

const CHANNELS = [
  {ico:'🎯', name:'Яндекс Директ',  sub:'Контекстная реклама'},
  {ico:'💙', name:'ВКонтакте',       sub:'Таргетированная реклама'},
  {ico:'📍', name:'Гео перформанс',  sub:'Геолокационная реклама'},
  {ico:'🛒', name:'AVITO',           sub:'Площадка объявлений'},
  {ico:'🔍', name:'SEO',             sub:'Поисковое продвижение'},
];

// ══ STATE ══
let st = { scr:0, cat:null, reg:null, regName:null, city:null, spec:null, goal:null, channels:[], bud:null };
let forecast = { calls:null, price:null }; // данные из таблицы
const hist = [];

// ══ NAVIGATION ══
function goTo(n) {
  const c = document.getElementById('s'+st.scr);
  const nx = document.getElementById('s'+n);
  hist.push(st.scr);
  c.classList.add('exit');
  setTimeout(()=>c.classList.remove('active','exit'), 380);
  nx.classList.add('active');
  nx.scrollTop = 0;
  st.scr = n;
  upProg(); upBack(); haptic('light');
}

function goBack() {
  if (!hist.length) return;
  const prev = hist.pop();
  document.getElementById('s'+st.scr).classList.remove('active');
  const pe = document.getElementById('s'+prev);
  pe.classList.add('active'); pe.scrollTop = 0;
  if (prev<=1){st.cat=null;}
  if (prev<=2){st.reg=null; clr('s2');}
  if (prev<=3){st.city=null; clr('s3');}
  if (prev<=4){st.spec=null; clr('s4');}
  if (prev<=5){st.goal=null; clr('s5');}
  if (prev<=6){st.channels=[]; clr('s6'); document.getElementById('chNextBar').style.display='none';}
  if (prev<=7){st.bud=null; clr('s7');}
  if (prev<=8){forecast={calls:null,price:null};}
  st.scr=prev; upProg(); upBack(); haptic('light');
}

function clr(id){ document.querySelectorAll('#'+id+' button').forEach(b=>b.classList.remove('selected','flash')); }

function upProg(){
  const pb=document.getElementById('progressBar'), pf=document.getElementById('progressFill');
  const s=st.scr;
  pb.classList.toggle('show', s>=2&&s<=7);
  const m={2:1,3:2,4:3,5:4,6:5,7:6};
  pf.style.width=(m[s]?m[s]/6*100:0)+'%';
}
function upBack(){ document.getElementById('backBtn').classList.toggle('show',st.scr>0); }

function haptic(t){
  try{
    const h=window.Telegram?.WebApp?.HapticFeedback; if(!h)return;
    if(t==='sel')h.selectionChanged();
    else if(t==='ok')h.notificationOccurred('success');
    else h.impactOccurred(t);
  }catch(e){}
}

// ══ PICKS ══
function pickCat(tile,name){
  st.cat=name; tile.classList.add('flash'); haptic('sel');
  setTimeout(()=>{ buildRegions(); goTo(2); },200);
}
function pickReg(btn,i){
  clr('s2'); btn.classList.add('selected','flash'); st.reg=i; st.regName=REGIONS[i].name; haptic('sel');
  setTimeout(()=>{ buildCities(); goTo(3); },230);
}
function pickCity(btn,name){
  clr('s3'); btn.classList.add('selected','flash'); st.city=name; haptic('sel');
  setTimeout(()=>{ buildSpec(); goTo(4); },230);
}
function pickSpec(btn,v){
  clr('s4'); btn.classList.add('selected'); st.spec=v; haptic('sel');
  setTimeout(()=>{ buildGoals(); goTo(5); },230);
}
function pickGoal(btn,v){
  clr('s5'); btn.classList.add('selected'); st.goal=v; haptic('sel');
  setTimeout(()=>{ buildChannels(); goTo(6); },230);
}
// Множественный выбор каналов
function toggleChannel(btn, name) {
  const idx = st.channels.indexOf(name);
  if (idx >= 0) {
    st.channels.splice(idx, 1);
    btn.classList.remove('selected');
  } else {
    st.channels.push(name);
    btn.classList.add('selected');
  }
  haptic('sel');
  // Показываем кнопку Далее если выбран хотя бы один
  const bar = document.getElementById('chNextBar');
  bar.style.display = st.channels.length > 0 ? 'flex' : 'none';
}
function confirmChannels() {
  if (!st.channels.length) return;
  document.getElementById('chNextBar').style.display = 'none';
  buildBudgets();
  setTimeout(()=>{ goTo(7); },100);
}

function buildBudgets() {
  st.bud = null;
  const grid = document.getElementById('budgetGrid');
  grid.innerHTML = '';
  const budgets = BUDGETS[st.goal] || BUDGETS['Новые а/м'];
  budgets.forEach(b => {
    const btn = document.createElement('button');
    btn.className = 'budget-btn';
    btn.innerHTML = `<div class="budget-range">${b.range}</div>`;
    btn.onclick = () => pickBudget(btn, b.label);
    grid.appendChild(btn);
  });
}
function pickBudget(btn,v){
  clr('s7'); btn.classList.add('selected'); st.bud=v; haptic('sel');
  setTimeout(()=>{ loadForecast(); goTo(8); },230);
}

// ══ ЗАПРОС К GOOGLE SHEETS ══
function loadForecast(){
  // Сбрасываем состояние экрана прогноза
  document.getElementById('fc-loading').style.display = 'flex';
  document.getElementById('fc-error').style.display   = 'none';
  document.getElementById('fc-result').style.display  = 'none';
  forecast = {calls:null, price:null};

  // Прогноз имеет смысл только для Авто (есть марка)
  // Для остальных категорий — сразу переходим к итогу
  if (st.cat !== 'Авто') {
    buildResult();
    goTo(9);
    return;
  }

  const params = new URLSearchParams({
    city:      st.city,
    brand:     st.spec,
    budget:    st.bud,
    direction: GOAL_TO_DIRECTION[st.goal] || '',
    region:    REGIONS[st.reg] ? REGIONS[st.reg].name : '',
    channel:   st.channels[0] || '',
    category:  st.cat || '',
  });

  const url = SHEETS_URL + '?' + params.toString();

  fetch(url)
    .then(r => r.json())
    .then(data => {
      document.getElementById('fc-loading').style.display = 'none';
      if (data.ok) {
        forecast.calls = data.calls;
        forecast.price = data.price;
        // Заполняем карточки
        document.getElementById('fc-headline').textContent = data.city + ' · ' + data.brand;
        document.getElementById('fc-calls').textContent    = data.calls;
        document.getElementById('fc-price').textContent    = data.price;
        document.getElementById('fc-city').textContent     = data.city;
        document.getElementById('fc-brand').textContent    = data.brand;
        document.getElementById('fc-bud').textContent      = data.budget;
        document.getElementById('fc-months').textContent   = data.months || '—';
        document.getElementById('fc-result').style.display = 'flex';
      } else {
        document.getElementById('fc-error-text').textContent = data.error || 'Нет данных';
        document.getElementById('fc-error').style.display    = 'flex';
      }
    })
    .catch(err => {
      document.getElementById('fc-loading').style.display = 'none';
      document.getElementById('fc-error-text').textContent = 'Ошибка соединения. Проверьте URL скрипта.';
      document.getElementById('fc-error').style.display   = 'flex';
      console.error(err);
    });
}

// ══ BUILDERS ══
function buildRegions(){
  const g=document.getElementById('regionGrid'); g.innerHTML='';
  REGIONS.forEach((r,i)=>{
    const b=document.createElement('button'); b.className='reg-btn';
    b.innerHTML=`<div class="reg-full">${r.name}</div><div class="reg-short">${r.short}</div>`;
    b.onclick=()=>pickReg(b,i); g.appendChild(b);
  });
}

function buildCities(){
  const r=REGIONS[st.reg];
  document.getElementById('cityQ').textContent='Выберите ваш город';
  const g=document.getElementById('cityGrid'); g.innerHTML='';
  r.cities.forEach(city=>{
    const b=document.createElement('button'); b.className='city-btn';
    b.innerHTML=`<span>${city}</span>`;
    b.onclick=()=>pickCity(b,city); g.appendChild(b);
  });
}

function buildSpec(){
  st.spec=null;
  const q=document.getElementById('specQ'), c=document.getElementById('specContent');
  c.innerHTML='';
  if(st.cat==='Авто'){
    q.textContent='Выберите ваш бренд';
    const g=document.createElement('div'); g.className='brand-grid';
    AUTO_BRANDS.forEach(br=>{
      const b=document.createElement('button'); b.className='brand-btn';
      b.textContent=br; b.onclick=()=>pickSpec(b,br); g.appendChild(b);
    }); c.appendChild(g);
  } else {
    const opts=st.cat==='Недвижимость'?REALTY_OPTS:MED_OPTS;
    q.textContent=st.cat==='Недвижимость'?'Выберите категорию объекта':'Выберите направление';
    const l=document.createElement('div'); l.className='card-list';
    opts.forEach(o=>{
      const b=document.createElement('button'); b.className='card-btn';
      b.innerHTML=`<div class="card-num">${o.num}</div><div><div class="card-main">${o.main}</div><div class="card-sub">${o.sub}</div></div><div class="card-chk">✓</div>`;
      b.onclick=()=>pickSpec(b,o.main); l.appendChild(b);
    }); c.appendChild(l);
  }
}

function buildGoals(){
  st.goal=null;
  const l=document.getElementById('goalList'); l.innerHTML='';
  (GOALS[st.cat]||[]).forEach(g=>{
    const b=document.createElement('button'); b.className='card-btn';
    b.innerHTML=`<div class="card-ico">${g.ico}</div><div class="card-main">${g.main}</div><div class="card-chk">✓</div>`;
    b.onclick=()=>pickGoal(b,g.main); l.appendChild(b);
  });
}

function buildChannels(){
  st.channels=[];
  document.getElementById('chNextBar').style.display='none';
  const g=document.getElementById('channelGrid'); g.innerHTML='';
  CHANNELS.forEach(ch=>{
    const b=document.createElement('button'); b.className='ch-btn';
    b.innerHTML=`<div class="ch-ico">${ch.ico}</div><div class="ch-name">${ch.name}</div><div class="ch-sub">${ch.sub}</div>`;
    b.onclick=()=>toggleChannel(b,ch.name); g.appendChild(b);
  });
}

function buildResult(){
  const r=REGIONS[st.reg];
  document.getElementById('r-cat').textContent  = st.cat;
  document.getElementById('r-reg').textContent  = r.name+' · '+r.short;
  document.getElementById('r-city').textContent = st.city;
  document.getElementById('r-spec').textContent = st.spec;
  document.getElementById('r-sl').textContent   = st.cat==='Авто'?'Бренд':st.cat==='Недвижимость'?'Категория':'Направление';
  document.getElementById('r-goal').textContent = st.goal;
  document.getElementById('r-ch').textContent   = st.channels.join(', ');
  document.getElementById('r-bud').textContent  = st.bud;
  document.getElementById('r-calls').textContent = forecast.calls || '—';
  document.getElementById('r-price').textContent = forecast.price || '—';
}

function sendResult(){
  const d=JSON.stringify({
    category:       st.cat,
    region:         REGIONS[st.reg].name,
    district:       REGIONS[st.reg].short,
    city:           st.city,
    spec:           st.spec,
    goal:           st.goal,
    channels:       st.channels,
    budget:         st.bud,
    forecast_calls: forecast.calls,
    forecast_price: forecast.price,
    ts:             new Date().toISOString()
  });
  try{window.Telegram?.WebApp?.sendData(d);}catch(e){}
  haptic('ok');
}

document.addEventListener('DOMContentLoaded',()=>{
  try{ const tg=window.Telegram?.WebApp; if(tg){tg.ready();tg.expand();tg.setHeaderColor('#0A0A0A');tg.setBackgroundColor('#0A0A0A');} }catch(e){}
  upProg(); upBack();
  [['ph-auto','https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=900&q=80&auto=format&fit=crop'],
   ['ph-realty','https://images.unsplash.com/photo-1486325212027-8081e485255e?w=900&q=80&auto=format&fit=crop'],
   ['ph-med','https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=900&q=80&auto=format&fit=crop']
  ].forEach(([id,url])=>{ const img=new Image(); img.onload=()=>{ const el=document.getElementById(id); if(el)el.classList.add('loaded'); }; img.src=url; });
});
</script>
</body>
</html>
