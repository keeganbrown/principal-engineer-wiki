// The reader site's shell: renders views from window.WIKI into the DOM.
// Pure logic (routing, search, physics) lives in core.js and is unit-tested;
// this file only wires data to elements and events.
(function () {
  "use strict";

  const core = window.WikiCore;
  const data = window.WIKI;
  const articles = data.articles;
  const categories = data.categories;
  const categoryLabel = Object.fromEntries(categories.map((c) => [c.slug, c.label]));
  const view = document.getElementById("view");
  const preview = document.getElementById("preview");
  const SEEN_KEY = "pe-wiki:seen";
  const THEME_KEY = "pe-wiki:theme";

  // ---------- Small helpers ----------

  const escapeHtml = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  function storageGet(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw === null ? fallback : JSON.parse(raw);
    } catch (_) {
      return fallback;
    }
  }
  function storageSet(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (_) { /* private mode: progress just isn't kept */ }
  }

  const seen = new Set(storageGet(SEEN_KEY, []).filter((s) => s in articles));
  function markSeen(slug) {
    if (seen.has(slug)) return;
    seen.add(slug);
    storageSet(SEEN_KEY, [...seen]);
  }

  function cssVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function card(slug, extraClass) {
    const a = articles[slug];
    return `<a class="link-card ${seen.has(slug) ? "seen" : ""} ${extraClass || ""}" data-cat="${a.category}" href="#/a/${slug}">
      <strong>${escapeHtml(a.title)}</strong><span>${escapeHtml(a.summary)}</span></a>`;
  }

  function decorateLinks(root) {
    root.querySelectorAll("a.wikilink").forEach((link) => {
      const target = articles[link.dataset.slug];
      if (!target) return;
      link.dataset.cat = target.category;
      link.classList.toggle("unseen", !seen.has(target.slug));
    });
  }

  function pickSurprise(exclude) {
    const pool = Object.keys(articles).filter((s) => s !== exclude);
    const unseen = pool.filter((s) => !seen.has(s));
    const from = unseen.length ? unseen : pool;
    return from[Math.floor(Math.random() * from.length)];
  }

  // ---------- Theme ----------

  function applyTheme(theme) {
    if (theme) document.documentElement.dataset.theme = theme;
    else delete document.documentElement.dataset.theme;
    window.dispatchEvent(new Event("themechange"));
  }
  applyTheme(storageGet(THEME_KEY, null));
  document.getElementById("theme-toggle").addEventListener("click", () => {
    const current = document.documentElement.dataset.theme ||
      (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const next = current === "dark" ? "light" : "dark";
    storageSet(THEME_KEY, next);
    applyTheme(next);
  });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => window.dispatchEvent(new Event("themechange")));

  // ---------- Home ----------

  function progressCard() {
    const { seen: count, total } = core.progress([...seen], articles);
    const pct = Math.round((count / total) * 100);
    const line = count === 0
      ? "Start with the path below, or tap <b>Surprise</b>."
      : count === total ? "You've read the whole wiki. 🎉" : `${total - count} to go — the graph shows what's left.`;
    return `<div class="progress-card">
      <div class="ring" style="--p:${pct}" data-label="${pct}%"></div>
      <div><strong>You've explored ${count} of ${total} articles</strong><span>${line}</span></div>
    </div>`;
  }

  function catalogHtml() {
    // index.md is the source of truth for grouping; wrap each "## Category"
    // and what follows it in a section tagged with that category.
    const template = document.createElement("template");
    template.innerHTML = data.home;
    const sections = [];
    let current = null;
    for (const node of [...template.content.children]) {
      if (node.tagName === "H2") {
        current = document.createElement("section");
        sections.push(current);
      }
      if (current) current.appendChild(node);
    }
    // A section takes the category of the first article listed in it.
    for (const section of sections) {
      const first = section.querySelector("li > a.wikilink:first-child");
      const target = first && articles[first.dataset.slug];
      if (target) section.dataset.cat = target.category;
    }
    for (const section of sections) {
      section.querySelectorAll("li").forEach((li) => {
        const first = li.firstElementChild;
        if (first && first.matches("a.wikilink") && li.firstChild === first) {
          const target = articles[first.dataset.slug];
          if (target) {
            li.dataset.cat = target.category;
            li.classList.toggle("seen", seen.has(target.slug));
            // "[[kiss]] — Choose..." → title on top, blurb below.
            const rest = li.innerHTML.slice(first.outerHTML.length).replace(/^\s*—\s*/, "");
            first.textContent = target.title;
            li.innerHTML = first.outerHTML + rest;
          }
        }
      });
    }
    return sections.map((s) => s.outerHTML).join("");
  }

  function renderHome() {
    const total = Object.keys(articles).length;
    const path = data.path.map((slug, i) => {
      const a = articles[slug];
      return `<a class="path-stop ${seen.has(slug) ? "seen" : ""}" data-cat="${a.category}" href="#/a/${slug}">
        <span class="num">Stop ${i + 1}</span><h3>${escapeHtml(core.shortTitle(a.title))}</h3><p>${escapeHtml(a.summary)}</p></a>`;
    }).join("");
    const tabs = [`<button type="button" aria-pressed="true" data-filter="">All</button>`]
      .concat(categories.map((c) => `<button type="button" aria-pressed="false" data-cat="${c.slug}" data-filter="${c.slug}">${c.label}</button>`))
      .join("");

    view.innerHTML = `<div class="page home">
      <section class="hero">
        <p class="eyebrow">A field guide</p>
        <h1>Think like a <span>principal engineer</span>.</h1>
        <p>${total} five-minute reads on principles, practices, and architecture — each one linked to the ideas around it.</p>
        ${progressCard()}
      </section>
      <div class="section-title"><h2>Start here</h2><a href="#/graph">See the map →</a></div>
      <div class="path-strip">${path}</div>
      <a class="glossary-card" href="#/terms"><strong>Terms to know</strong>
        <span>${(data.glossary || []).length} plain-English definitions, from ACID to zero-downtime deploys.</span></a>
      <div class="section-title"><h2>Browse</h2></div>
      <div class="category-tabs" role="group" aria-label="Filter by category">${tabs}</div>
      <div class="catalog prose">${catalogHtml()}</div>
    </div>`;

    const catalog = view.querySelector(".catalog");
    decorateLinks(catalog);
    view.querySelector(".category-tabs").addEventListener("click", (event) => {
      const button = event.target.closest("button");
      if (!button) return;
      const filter = button.dataset.filter;
      view.querySelectorAll(".category-tabs button").forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
      catalog.querySelectorAll("section").forEach((s) => { s.hidden = Boolean(filter) && s.dataset.cat !== filter; });
    });
    document.title = "Principal Engineer Wiki";
  }

  // ---------- Article ----------

  function truncate(text, max) {
    return text.length > max ? `${text.slice(0, max - 1).trimEnd()}…` : text;
  }

  // One ring of neighbours around the article; labels sit outside the ring,
  // anchored away from the centre so they don't run into each other.
  function localGraphSvg(article) {
    const ids = core.neighbors(article);
    const radius = ids.length > 10 ? 150 : 125;
    // Squash the ring sideways so side labels fit on a narrow screen.
    const ring = core.radialLayout(ids.length, radius).map((p) => ({ x: p.x * 0.62, y: p.y }));
    const lines = ids.map((id, i) =>
      `<line x1="0" y1="0" x2="${ring[i].x.toFixed(1)}" y2="${ring[i].y.toFixed(1)}" class="${article.links.includes(id) ? "out" : ""}"/>`);
    const nodes = ids.map((id, i) => {
      const a = articles[id];
      const { x, y } = ring[i];
      const ux = x / (radius * 0.62);
      const uy = y / radius;
      const anchor = ux > 0.3 ? "start" : ux < -0.3 ? "end" : "middle";
      const lx = x + ux * 16;
      const ly = y + uy * 16 + 4 + (anchor === "middle" ? uy * 6 : 0);
      return `<a href="#/a/${id}" data-cat="${a.category}"><title>${escapeHtml(a.title)}</title>
        <circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="9" ${seen.has(id) ? "" : 'fill-opacity=".45"'}/>
        <text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" style="text-anchor:${anchor}">${escapeHtml(truncate(core.shortTitle(a.title), 17))}</text></a>`;
    });
    const half = radius * 0.62 + 175;
    const center = `<g class="center" data-cat="${article.category}"><circle cx="0" cy="0" r="16"/></g>`;
    return `<svg class="local-graph" viewBox="${-half} ${-(radius + 34)} ${half * 2} ${(radius + 34) * 2}" role="img" aria-label="Articles connected to ${escapeHtml(article.title)}">
      ${lines.join("")}${nodes.join("")}${center}</svg>`;
  }

  function pathBanner(slug) {
    const position = core.pathPosition(data.path, slug);
    if (!position) return "";
    const dots = data.path.map((_, i) => `<i class="${i <= position.index ? "on" : ""}"></i>`).join("");
    const next = position.next
      ? `<a href="#/a/${position.next}">Next: ${escapeHtml(core.shortTitle(articles[position.next].title))} →</a>`
      : `<a href="#/graph">Path done — explore the map →</a>`;
    return `<div class="path-banner"><span class="dots" aria-hidden="true">${dots}</span>
      <span>Starter path ${position.index + 1}/${position.total}</span>${next}</div>`;
  }

  function renderArticle(slug) {
    const a = articles[slug];
    if (!a) {
      view.innerHTML = `<div class="page empty"><h1>Not found</h1><p>No article called “${escapeHtml(slug)}”.</p>
        <p><a class="button primary" href="#/">Go home</a></p></div>`;
      return;
    }
    const linksOut = a.links;
    const linksIn = a.backlinks.filter((s) => !linksOut.includes(s));
    const both = a.backlinks.filter((s) => linksOut.includes(s));
    const groups = [
      ["Two-way links", both],
      ["Leads to", linksOut.filter((s) => !both.includes(s))],
      ["Mentioned in", linksIn],
    ].filter(([, list]) => list.length);

    view.innerHTML = `<article class="page" data-cat="${a.category}">
      <header class="article-head">
        <span class="pill">${categoryLabel[a.category]}</span>
        <h1>${escapeHtml(a.title)}</h1>
        <div class="meta"><span>${a.minutes} min read</span>${a.tags.map((t) => `<a class="tag" href="#/search/${encodeURIComponent(t)}">#${escapeHtml(t)}</a>`).join("")}</div>
        ${pathBanner(slug)}
      </header>
      <div class="prose">${a.html}</div>
      <section class="connections" aria-labelledby="connections-title">
        <h2 id="connections-title">Connections</h2>
        <p>${core.neighbors(a).length} ideas connect to this one. Tap one to jump there.</p>
        <div class="legend-line">
          <span><svg viewBox="0 0 26 8"><line x1="0" y1="4" x2="26" y2="4" style="stroke:var(--muted)"/></svg>links from here</span>
          <span><svg viewBox="0 0 26 8"><line x1="0" y1="4" x2="26" y2="4" style="stroke:var(--border);stroke-width:2"/></svg>links here</span>
          <span>faded = not read yet</span>
        </div>
        ${localGraphSvg(a)}
        <div class="link-cards">${groups.map(([title, list]) => `<h3>${title}</h3>${list.map((s) => card(s)).join("")}`).join("")}</div>
        <div class="article-actions">
          <a class="button primary" href="#/graph/${slug}">
            <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="6" cy="7" r="2.6"/><circle cx="18" cy="6" r="2.6"/><circle cx="12" cy="18" r="2.6"/><path d="M8.5 7.5 15.5 6.3M7.3 9.2l3.5 6.5M16.8 8.4 13.3 15.7"/></svg>
            Find it on the map</a>
          <button class="button" type="button" data-surprise>Surprise me</button>
        </div>
      </section>
    </article>`;

    decorateLinks(view.querySelector(".prose"));
    view.querySelector("[data-surprise]").addEventListener("click", () => { location.hash = `#/a/${pickSurprise(slug)}`; });
    markSeen(slug);
    document.title = `${core.shortTitle(a.title)} · Principal Engineer Wiki`;
  }

  // ---------- Search ----------

  function highlight(text, terms) {
    let out = escapeHtml(text);
    for (const term of terms) {
      if (!term) continue;
      const safe = escapeHtml(term).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      out = out.replace(new RegExp(`(${safe})(?![^<]*>)`, "gi"), "<mark>$1</mark>");
    }
    return out;
  }

  function renderSearch(query) {
    const tagCounts = {};
    Object.values(articles).forEach((a) => a.tags.forEach((t) => { tagCounts[t] = (tagCounts[t] || 0) + 1; }));
    const popular = Object.entries(tagCounts).sort((x, y) => y[1] - x[1] || x[0].localeCompare(y[0])).slice(0, 18);

    view.innerHTML = `<div class="page">
      <p class="eyebrow">Search</p>
      <form class="search-box" role="search"><label class="visually-hidden" for="search-input">Search articles</label>
        <input id="search-input" type="search" placeholder="Try “retries” or “testing”" autocomplete="off" enterkeyhint="search"></form>
      <div class="search-empty"><p class="search-hint">Search titles, tags, and summaries. Or start from a tag:</p>
        <div class="tag-cloud">${popular.map(([t]) => `<button type="button" data-tag="${escapeHtml(t)}">#${escapeHtml(t)}</button>`).join("")}</div></div>
      <div class="results" aria-live="polite"></div>
    </div>`;

    const input = view.querySelector("#search-input");
    const results = view.querySelector(".results");
    const empty = view.querySelector(".search-empty");

    function update(q, updateUrl) {
      const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
      const hits = core.search(articles, q);
      const termHits = terms.length ? core.searchTerms(glossary, q).slice(0, 4) : [];
      empty.hidden = terms.length > 0;
      const termCards = termHits.map((e) => `<a class="link-card term-card" href="#/terms/${encodeURIComponent(e.term)}">
            <strong>${highlight(e.term, terms)}</strong><span>${escapeHtml(e.html.replace(/<[^>]*>/g, ""))}</span></a>`).join("");
      const articleCards = hits.map((a) => `<a class="link-card ${seen.has(a.slug) ? "seen" : ""}" data-cat="${a.category}" href="#/a/${a.slug}">
            <strong>${highlight(a.title, terms)}</strong><span>${highlight(a.summary, terms)}</span></a>`).join("");
      results.innerHTML = !terms.length ? "" : hits.length || termHits.length
        ? (termHits.length ? `<h3 class="results-label">Terms</h3>${termCards}` : "") +
          (hits.length ? `<h3 class="results-label">Articles</h3>${articleCards}` : "")
        : `<p class="search-hint">Nothing matches “${escapeHtml(q)}”. Try a shorter word.</p>`;
      if (updateUrl) history.replaceState(null, "", `#/search/${encodeURIComponent(q)}`);
    }

    input.value = query;
    update(query, false);
    input.addEventListener("input", () => update(input.value, true));
    view.querySelector(".search-box").addEventListener("submit", (event) => {
      event.preventDefault();
      const first = results.querySelector("a");
      if (first) location.hash = first.getAttribute("href");
    });
    view.querySelector(".tag-cloud").addEventListener("click", (event) => {
      const button = event.target.closest("[data-tag]");
      if (!button) return;
      input.value = button.dataset.tag;
      update(input.value, true);
    });
    if (matchMedia("(min-width: 760px)").matches) {
      document.getElementById("top-search-input").focus();
    } else if (!query) {
      input.focus();
    }
    document.title = "Search · Principal Engineer Wiki";
  }

  // ---------- Glossary ----------

  const glossary = data.glossary || [];

  function termHtml(entry) {
    return `<div class="term" id="term-${entry.id}"><dt>${escapeHtml(entry.term)}</dt><dd>${entry.html}</dd></div>`;
  }

  function renderTerms(query) {
    const letters = [...new Set(glossary.map((e) => e.letter))];
    view.innerHTML = `<div class="page terms-page">
      <p class="eyebrow">Glossary</p>
      <h1>Terms to know</h1>
      <p class="lede">${glossary.length} short definitions. Each links to the article that explains it properly.</p>
      <form class="search-box" role="search"><label class="visually-hidden" for="terms-input">Filter terms</label>
        <input id="terms-input" type="search" placeholder="Filter, e.g. “SLO” or “consistency”" autocomplete="off" enterkeyhint="search"></form>
      <nav class="letter-strip" aria-label="Jump to letter">${letters.map((l) => `<a href="#term-letter-${l === "#" ? "num" : l}">${l}</a>`).join("")}</nav>
      <div class="glossary prose"></div>
    </div>`;

    const input = view.querySelector("#terms-input");
    const list = view.querySelector(".glossary");
    const strip = view.querySelector(".letter-strip");

    function update(q, updateUrl) {
      const filtering = q.trim().length > 0;
      strip.hidden = filtering;
      if (filtering) {
        const hits = core.searchTerms(glossary, q);
        list.innerHTML = hits.length
          ? `<dl>${hits.map(termHtml).join("")}</dl>`
          : `<p class="search-hint">No term matches “${escapeHtml(q)}”. Try <a href="#/search/${encodeURIComponent(q)}">searching the articles</a>.</p>`;
      } else {
        list.innerHTML = letters.map((l) => `<h2 id="term-letter-${l === "#" ? "num" : l}">${l}</h2>
          <dl>${glossary.filter((e) => e.letter === l).map(termHtml).join("")}</dl>`).join("");
      }
      decorateLinks(list);
      if (updateUrl) history.replaceState(null, "", q ? `#/terms/${encodeURIComponent(q)}` : "#/terms");
    }

    input.value = query;
    update(query, false);
    input.addEventListener("input", () => update(input.value, true));
    view.querySelector(".search-box").addEventListener("submit", (e) => e.preventDefault());
    strip.addEventListener("click", (e) => {
      const link = e.target.closest("a");
      if (!link) return;
      e.preventDefault();
      const target = document.getElementById(link.getAttribute("href").slice(1));
      if (target) target.scrollIntoView({ behavior: "smooth" });
    });
    document.title = "Terms · Principal Engineer Wiki";
  }

  // ---------- Graph ----------

  let graphState = null; // survives between visits so the layout doesn't reshuffle

  function createGraphState() {
    const slugs = Object.keys(articles);
    const catIndex = Object.fromEntries(categories.map((c, i) => [c.slug, i]));
    const nodes = slugs.map((slug, i) => {
      const a = articles[slug];
      // Start each category in its own quadrant so clusters form naturally.
      const angle = (catIndex[a.category] / categories.length) * Math.PI * 2;
      const jitter = i * 2.39996;
      const spread = 30 + (i % 7) * 12;
      return {
        id: slug,
        article: a,
        degree: core.neighbors(a).length,
        x: Math.cos(angle) * 170 + Math.cos(jitter) * spread,
        y: Math.sin(angle) * 170 + Math.sin(jitter) * spread,
      };
    });
    const aspect = Math.min(2, Math.max(0.6, innerHeight / innerWidth));
    for (const n of nodes) n.y *= aspect;
    const sim = core.createSimulation(nodes, data.edges, { aspect });
    for (let i = 0; i < 120; i++) sim.step();
    return { nodes, byId: new Map(nodes.map((n) => [n.id, n])), sim, camera: null, hidden: new Set(), selected: null };
  }

  function nodeRadius(node) {
    return 6 + Math.sqrt(node.degree) * 2.2;
  }

  function renderGraph(focus) {
    if (!graphState) graphState = createGraphState();
    const state = graphState;
    document.body.classList.add("graph-mode");

    const filters = categories.map((c) =>
      `<button type="button" data-cat="${c.slug}" aria-pressed="${!state.hidden.has(c.slug)}">${c.label}</button>`).join("");
    view.innerHTML = `<div class="graph-view">
      <canvas aria-label="Map of all articles and their links. Use the search to find an article by name." role="img"></canvas>
      <div class="graph-filters" role="group" aria-label="Show categories">${filters}</div>
      <div class="graph-zoom"><button type="button" data-zoom="in" aria-label="Zoom in">+</button><button type="button" data-zoom="out" aria-label="Zoom out">−</button><button type="button" data-zoom="fit" aria-label="Fit everything">⤢</button></div>
      <div class="graph-hint">Drag to pan · pinch or scroll to zoom · tap a dot</div>
      <div class="sheet" aria-live="polite"></div>
    </div>`;

    const container = view.querySelector(".graph-view");
    const canvas = container.querySelector("canvas");
    const ctx = canvas.getContext("2d");
    const sheet = container.querySelector(".sheet");
    const hint = container.querySelector(".graph-hint");
    let width = 0;
    let height = 0;
    let colors = {};
    let hovered = null;
    let dirty = true;
    let frame = 0;
    let tween = null;

    function readColors() {
      colors = {
        text: cssVar("--text"), muted: cssVar("--muted"), border: cssVar("--border"),
        surface: cssVar("--surface"), accent: cssVar("--accent"),
      };
      for (const c of categories) colors[c.slug] = cssVar(`--c-${c.slug}`);
      dirty = true;
    }

    const visible = (n) => !state.hidden.has(n.article.category);
    const toWorld = (p) => ({
      x: (p.x - width / 2) / state.camera.k + state.camera.x,
      y: (p.y - height / 2) / state.camera.k + state.camera.y,
    });
    const toScreen = (n) => ({
      x: (n.x - state.camera.x) * state.camera.k + width / 2,
      y: (n.y - state.camera.y) * state.camera.k + height / 2,
    });
    const clampZoom = (k) => Math.min(4, Math.max(0.25, k));

    function fitCamera() {
      const shown = state.nodes.filter(visible);
      if (!shown.length || !width) return { x: 0, y: 0, k: 1 };
      const xs = shown.map((n) => n.x);
      const ys = shown.map((n) => n.y);
      const minX = Math.min(...xs); const maxX = Math.max(...xs);
      const minY = Math.min(...ys); const maxY = Math.max(...ys);
      const pad = 70;
      const k = clampZoom(Math.min((width - pad) / (maxX - minX || 1), (height - pad * 2) / (maxY - minY || 1)));
      return { x: (minX + maxX) / 2, y: (minY + maxY) / 2, k };
    }

    function flyTo(target) {
      tween = { from: { ...state.camera }, to: target, start: performance.now(), duration: 450 };
      dirty = true;
    }

    function resize() {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      width = rect.width;
      height = rect.height;
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (!state.camera) state.camera = fitCamera();
      dirty = true;
    }

    function isNeighbor(a, b) {
      return a.article.links.includes(b.id) || b.article.links.includes(a.id);
    }

    function draw() {
      const { camera: cam, selected } = state;
      ctx.clearRect(0, 0, width, height);
      ctx.save();
      ctx.translate(width / 2, height / 2);
      ctx.scale(cam.k, cam.k);
      ctx.translate(-cam.x, -cam.y);

      for (const [s, t] of data.edges) {
        const a = state.byId.get(s);
        const b = state.byId.get(t);
        if (!visible(a) || !visible(b)) continue;
        const lit = selected && (a === selected || b === selected);
        ctx.globalAlpha = selected && !lit ? 0.12 : lit ? 0.95 : 0.55;
        ctx.strokeStyle = lit ? colors[selected.article.category] : colors.border;
        ctx.lineWidth = (lit ? 2.2 : 1.2) / Math.sqrt(cam.k);
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }

      for (const n of state.nodes) {
        if (!visible(n)) continue;
        const near = !selected || n === selected || isNeighbor(n, selected);
        const r = nodeRadius(n) * (n === selected || n === hovered ? 1.35 : 1);
        const color = colors[n.article.category];
        ctx.globalAlpha = near ? 1 : 0.2;
        ctx.beginPath();
        ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
        if (seen.has(n.id)) {
          ctx.fillStyle = color;
          ctx.fill();
        } else {
          ctx.fillStyle = colors.surface;
          ctx.fill();
          ctx.lineWidth = 2.4;
          ctx.strokeStyle = color;
          ctx.stroke();
        }
        if (n === selected) {
          ctx.globalAlpha = 0.25;
          ctx.beginPath();
          ctx.arc(n.x, n.y, r + 7, 0, Math.PI * 2);
          ctx.fillStyle = color;
          ctx.fill();
        }
      }
      ctx.restore();

      // Labels in screen space so text stays crisp at any zoom.
      ctx.font = "600 12.5px ui-sans-serif, system-ui, -apple-system, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      ctx.lineJoin = "round";
      const candidates = state.nodes.filter((n) => {
        if (!visible(n)) return false;
        const near = selected && (n === selected || isNeighbor(n, selected));
        return n === hovered || near || (!selected && (cam.k > 1.15 || n.degree >= 10));
      });
      // Most important labels first; skip any that would overlap one already drawn.
      const priority = (n) => (n === selected ? 3 : n === hovered ? 2 : 0) * 1000 + n.degree;
      candidates.sort((a, b) => priority(b) - priority(a));
      const placed = [];
      for (const n of candidates) {
        const p = toScreen(n);
        const label = core.shortTitle(n.article.title);
        const textWidth = ctx.measureText(label).width;
        const y = p.y + nodeRadius(n) * cam.k + 5;
        const box = { x1: p.x - textWidth / 2 - 3, x2: p.x + textWidth / 2 + 3, y1: y - 1, y2: y + 16 };
        if (placed.some((b) => box.x1 < b.x2 && box.x2 > b.x1 && box.y1 < b.y2 && box.y2 > b.y1)) continue;
        placed.push(box);
        ctx.globalAlpha = 1;
        ctx.lineWidth = 4;
        ctx.strokeStyle = colors.surface;
        ctx.strokeText(label, p.x, y);
        ctx.fillStyle = n === selected ? colors[n.article.category] : colors.text;
        ctx.fillText(label, p.x, y);
      }
      ctx.globalAlpha = 1;
    }

    function tick(now) {
      if (tween) {
        const t = Math.min(1, (now - tween.start) / tween.duration);
        const e = 1 - Math.pow(1 - t, 3);
        state.camera = {
          x: tween.from.x + (tween.to.x - tween.from.x) * e,
          y: tween.from.y + (tween.to.y - tween.from.y) * e,
          k: tween.from.k + (tween.to.k - tween.from.k) * e,
        };
        if (t === 1) tween = null;
        dirty = true;
      }
      if (state.sim.step()) dirty = true;
      if (dirty && width) { draw(); dirty = false; }
      frame = requestAnimationFrame(tick);
    }

    function select(node, fly) {
      state.selected = node;
      dirty = true;
      if (!node) {
        sheet.classList.remove("open");
        history.replaceState(null, "", "#/graph");
        return;
      }
      const a = node.article;
      sheet.dataset.cat = a.category;
      sheet.innerHTML = `<button class="close" type="button" aria-label="Close">×</button>
        <span class="pill">${categoryLabel[a.category]}</span>
        <h2>${escapeHtml(a.title)}</h2><p>${escapeHtml(a.summary)}</p>
        <div class="row"><a class="button primary" href="#/a/${a.slug}">Read · ${a.minutes} min</a>
        <span class="tag">${node.degree} connections${seen.has(a.slug) ? " · read ✓" : ""}</span></div>`;
      sheet.classList.add("open");
      sheet.querySelector(".close").addEventListener("click", () => select(null));
      history.replaceState(null, "", `#/graph/${a.slug}`);
      if (fly) flyTo({ x: node.x, y: node.y + 60 / Math.max(state.camera.k, 1.3), k: Math.max(state.camera.k, 1.3) });
    }

    function hitTest(p, pointerType) {
      const slop = pointerType === "touch" ? 14 : 6;
      let best = null;
      let bestDistance = Infinity;
      for (const n of state.nodes) {
        if (!visible(n)) continue;
        const s = toScreen(n);
        const d = Math.hypot(s.x - p.x, s.y - p.y);
        if (d < nodeRadius(n) * state.camera.k + slop && d < bestDistance) { best = n; bestDistance = d; }
      }
      return best;
    }

    // ----- Gestures: tap, drag node, pan, pinch, wheel -----
    const pointers = new Map();
    let gesture = null;
    let lastTap = { node: null, time: 0 };
    const local = (e) => { const r = canvas.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; };

    function startPinch() {
      const [a, b] = [...pointers.values()];
      const mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
      gesture = { type: "pinch", dist: Math.hypot(a.x - b.x, a.y - b.y), k: state.camera.k, anchor: toWorld(mid), moved: Infinity };
    }

    function dismissHint() { hint.style.opacity = "0"; }

    canvas.addEventListener("pointerdown", (e) => {
      canvas.setPointerCapture(e.pointerId);
      const p = local(e);
      pointers.set(e.pointerId, p);
      tween = null;
      dismissHint();
      if (pointers.size === 1) {
        const node = hitTest(p, e.pointerType);
        gesture = { type: node ? "node" : "pan", node, last: p, moved: 0, time: performance.now() };
        if (node) node.pinned = true;
        canvas.classList.add("dragging");
      } else if (pointers.size === 2) {
        if (gesture && gesture.node) gesture.node.pinned = false;
        startPinch();
      }
    });

    canvas.addEventListener("pointermove", (e) => {
      const p = local(e);
      if (!pointers.has(e.pointerId)) {
        if (e.pointerType === "mouse") {
          const node = hitTest(p, "mouse");
          if (node !== hovered) { hovered = node; dirty = true; canvas.style.cursor = node ? "pointer" : ""; }
        }
        return;
      }
      pointers.set(e.pointerId, p);
      if (!gesture) return;
      if (gesture.type === "pinch" && pointers.size >= 2) {
        const [a, b] = [...pointers.values()];
        const mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
        const k = clampZoom(gesture.k * Math.hypot(a.x - b.x, a.y - b.y) / (gesture.dist || 1));
        state.camera = { k, x: gesture.anchor.x - (mid.x - width / 2) / k, y: gesture.anchor.y - (mid.y - height / 2) / k };
        dirty = true;
        return;
      }
      const dx = p.x - gesture.last.x;
      const dy = p.y - gesture.last.y;
      gesture.moved += Math.hypot(dx, dy);
      gesture.last = p;
      if (gesture.moved < 5) return;
      if (gesture.type === "node") {
        const w = toWorld(p);
        gesture.node.x = w.x;
        gesture.node.y = w.y;
        state.sim.reheat(0.3);
      } else {
        state.camera = { ...state.camera, x: state.camera.x - dx / state.camera.k, y: state.camera.y - dy / state.camera.k };
      }
      dirty = true;
    });

    function endPointer(e) {
      pointers.delete(e.pointerId);
      if (!gesture) return;
      const wasTap = gesture.type !== "pinch" && gesture.moved < 5 && performance.now() - gesture.time < 500;
      if (gesture.node) gesture.node.pinned = false;
      if (wasTap) {
        const node = gesture.node;
        const now = performance.now();
        if (node && lastTap.node === node && now - lastTap.time < 350) {
          location.hash = `#/a/${node.id}`;
        } else {
          select(node, false);
        }
        lastTap = { node, time: now };
      }
      if (pointers.size === 1) {
        const [p] = pointers.values();
        gesture = { type: "pan", node: null, last: p, moved: Infinity, time: 0 };
      } else if (pointers.size === 0) {
        gesture = null;
        canvas.classList.remove("dragging");
      }
    }
    canvas.addEventListener("pointerup", endPointer);
    canvas.addEventListener("pointercancel", endPointer);
    canvas.addEventListener("pointerleave", () => { if (hovered) { hovered = null; dirty = true; } });

    canvas.addEventListener("wheel", (e) => {
      e.preventDefault();
      dismissHint();
      const p = local(e);
      const anchor = toWorld(p);
      const k = clampZoom(state.camera.k * Math.exp(-e.deltaY * 0.0015));
      state.camera = { k, x: anchor.x - (p.x - width / 2) / k, y: anchor.y - (p.y - height / 2) / k };
      tween = null;
      dirty = true;
    }, { passive: false });

    container.querySelector(".graph-zoom").addEventListener("click", (e) => {
      const button = e.target.closest("button");
      if (!button) return;
      const { zoom } = button.dataset;
      if (zoom === "fit") flyTo(fitCamera());
      else flyTo({ ...state.camera, k: clampZoom(state.camera.k * (zoom === "in" ? 1.4 : 1 / 1.4)) });
    });

    container.querySelector(".graph-filters").addEventListener("click", (e) => {
      const button = e.target.closest("button");
      if (!button) return;
      const cat = button.dataset.cat;
      if (state.hidden.has(cat)) state.hidden.delete(cat);
      else if (state.hidden.size < categories.length - 1) state.hidden.add(cat);
      container.querySelectorAll(".graph-filters button").forEach((b) => b.setAttribute("aria-pressed", String(!state.hidden.has(b.dataset.cat))));
      if (state.selected && !visible(state.selected)) select(null);
      dirty = true;
    });

    const observer = new ResizeObserver(resize);
    observer.observe(canvas);
    window.addEventListener("themechange", readColors);
    const hintTimer = setTimeout(dismissHint, 5000);
    readColors();
    resize();

    const focusNode = focus && state.byId.get(focus);
    if (focusNode) {
      state.hidden.delete(focusNode.article.category);
      select(focusNode, true);
    } else if (state.selected) {
      select(state.selected, false);
    }
    frame = requestAnimationFrame(tick);
    document.title = "Map · Principal Engineer Wiki";

    return function cleanup() {
      cancelAnimationFrame(frame);
      observer.disconnect();
      clearTimeout(hintTimer);
      window.removeEventListener("themechange", readColors);
      document.body.classList.remove("graph-mode");
    };
  }

  // ---------- Hover previews (mouse only) ----------

  const canHover = matchMedia("(hover: hover) and (pointer: fine)");
  document.addEventListener("mouseover", (e) => {
    if (!canHover.matches) return;
    const link = e.target.closest("a.wikilink");
    if (!link || !articles[link.dataset.slug]) return;
    const a = articles[link.dataset.slug];
    preview.dataset.cat = a.category;
    preview.innerHTML = `<span class="pill">${categoryLabel[a.category]}</span><strong>${escapeHtml(a.title)}</strong><span>${escapeHtml(a.summary)}</span>`;
    preview.hidden = false;
    const rect = link.getBoundingClientRect();
    const top = rect.bottom + 8 + preview.offsetHeight > innerHeight ? rect.top - preview.offsetHeight - 8 : rect.bottom + 8;
    preview.style.top = `${Math.max(8, top)}px`;
    preview.style.left = `${Math.min(Math.max(8, rect.left), innerWidth - preview.offsetWidth - 8)}px`;
  });
  document.addEventListener("mouseout", (e) => {
    if (e.target.closest && e.target.closest("a.wikilink")) preview.hidden = true;
  });

  // ---------- Router ----------

  let cleanup = null;
  let forward = true;
  const scrollPositions = new Map();

  document.addEventListener("click", (e) => {
    const link = e.target.closest('a[href^="#/"]');
    if (link) forward = true;
  });
  window.addEventListener("popstate", () => { forward = false; });

  function render() {
    scrollPositions.set(render.lastHash, scrollY);
    if (cleanup) { cleanup(); cleanup = null; }
    preview.hidden = true;
    const route = core.parseRoute(location.hash);
    const tab = route.view === "article" ? null : route.view;
    document.querySelectorAll(".tabbar [data-tab]").forEach((el) => {
      if (el.dataset.tab === tab) el.setAttribute("aria-current", "page");
      else el.removeAttribute("aria-current");
    });

    if (route.view === "article") renderArticle(route.slug);
    else if (route.view === "graph") cleanup = renderGraph(route.focus);
    else if (route.view === "search") renderSearch(route.query);
    else if (route.view === "terms") renderTerms(route.query);
    else renderHome();

    const topInput = document.getElementById("top-search-input");
    if (route.view !== "search") topInput.value = "";

    const saved = scrollPositions.get(location.hash);
    window.scrollTo(0, !forward && saved ? saved : 0);
    if (forward && route.view === "article") view.focus({ preventScroll: true });
    forward = true;
    render.lastHash = location.hash;
  }

  window.addEventListener("hashchange", render);

  // ---------- Global controls ----------

  document.getElementById("surprise").addEventListener("click", () => {
    const route = core.parseRoute(location.hash);
    location.hash = `#/a/${pickSurprise(route.slug)}`;
  });

  const topSearch = document.getElementById("top-search-input");
  topSearch.addEventListener("input", () => {
    const q = topSearch.value;
    if (core.parseRoute(location.hash).view === "search") {
      const input = document.getElementById("search-input");
      input.value = q;
      input.dispatchEvent(new Event("input"));
    } else if (q.trim()) {
      location.hash = `#/search/${encodeURIComponent(q)}`;
    }
  });
  document.getElementById("top-search").addEventListener("submit", (e) => {
    e.preventDefault();
    const first = view.querySelector(".results a");
    if (first) location.hash = first.getAttribute("href");
  });

  document.addEventListener("keydown", (e) => {
    const typing = /^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName);
    if (e.key === "/" && !typing) {
      e.preventDefault();
      if (matchMedia("(min-width: 760px)").matches) topSearch.focus();
      else location.hash = "#/search";
    } else if (e.key === "Escape" && typing) {
      document.activeElement.blur();
    }
  });

  render();
})();
