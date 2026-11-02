// Pure logic for the reader site: routing, search, graph layout and physics.
// No DOM access here — app.js owns the screen. Works in the browser
// (window.WikiCore) and in Node (module.exports) so it can be unit-tested.
(function (root) {
  "use strict";

  function parseRoute(hash) {
    const parts = (hash || "").replace(/^#\/?/, "").split("/");
    const [head, ...rest] = parts;
    const arg = rest.length ? decodeURIComponent(rest.join("/")) : null;
    if (head === "a" && arg) return { view: "article", slug: arg };
    if (head === "graph") return { view: "graph", focus: arg };
    if (head === "search") return { view: "search", query: arg || "" };
    return { view: "home" };
  }

  // Higher score = better match. Every term must match somewhere.
  const FIELD_WEIGHTS = { title: 10, tags: 4, summary: 1 };

  function search(articles, query) {
    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    const scored = [];
    for (const a of Object.values(articles)) {
      const fields = {
        title: a.title.toLowerCase(),
        tags: (a.tags || []).join(" ").toLowerCase(),
        summary: (a.summary || "").toLowerCase(),
      };
      let score = 0;
      let allMatch = true;
      for (const term of terms) {
        let best = 0;
        for (const [name, text] of Object.entries(fields)) {
          if (text.includes(term)) best = Math.max(best, FIELD_WEIGHTS[name]);
        }
        if (!best) { allMatch = false; break; }
        score += best;
      }
      if (allMatch) scored.push({ a, score });
    }
    scored.sort((x, y) => y.score - x.score || x.a.title.localeCompare(y.a.title));
    return scored.map((s) => s.a);
  }

  function neighbors(article) {
    return [...new Set([...(article.links || []), ...(article.backlinks || [])])];
  }

  function pathPosition(path, slug) {
    const index = path.indexOf(slug);
    if (index === -1) return null;
    return {
      index,
      total: path.length,
      prev: index > 0 ? path[index - 1] : null,
      next: index < path.length - 1 ? path[index + 1] : null,
    };
  }

  // Points on a circle, starting at 12 o'clock and going clockwise.
  function radialLayout(count, radius) {
    const points = [];
    for (let i = 0; i < count; i++) {
      const angle = -Math.PI / 2 + (2 * Math.PI * i) / count;
      points.push({ x: radius * Math.cos(angle), y: radius * Math.sin(angle) });
    }
    return points;
  }

  // A small force-directed layout: springs on edges, repulsion between all
  // nodes, a gentle pull to the centre. Mutates node.x / node.y in place.
  const PHYSICS = {
    springLength: 110,
    springStrength: 0.02,
    repulsion: 4200,
    centering: 0.004,
    damping: 0.82,
    alphaDecay: 0.985,
    alphaMin: 0.005,
    maxSpeed: 40,
    aspect: 1, // height / width of the screen; > 1 pulls harder sideways so the layout fills a tall phone
  };

  function createSimulation(nodes, edges, options) {
    const p = Object.assign({}, PHYSICS, options || {});
    const byId = new Map(nodes.map((n) => [n.id, n]));
    const links = edges
      .map(([s, t]) => [byId.get(s), byId.get(t)])
      .filter(([s, t]) => s && t);
    for (const [i, n] of nodes.entries()) {
      n.vx = n.vx || 0;
      n.vy = n.vy || 0;
      if (n.pinned) continue;
      // Nudge exact overlaps apart deterministically so forces have a direction.
      n.x += Math.cos(i * 2.39996) * 0.01;
      n.y += Math.sin(i * 2.39996) * 0.01;
    }
    let alpha = 1;

    function step() {
      if (alpha < p.alphaMin) return false;
      for (let i = 0; i < nodes.length; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < nodes.length; j++) {
          const b = nodes[j];
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const d2 = Math.max(dx * dx + dy * dy, 25);
          const d = Math.sqrt(d2);
          const f = (p.repulsion / d2) * alpha;
          const fx = (dx / d) * f;
          const fy = (dy / d) * f;
          a.vx -= fx; a.vy -= fy;
          b.vx += fx; b.vy += fy;
        }
      }
      for (const [s, t] of links) {
        const dx = t.x - s.x;
        const dy = t.y - s.y;
        const d = Math.max(Math.hypot(dx, dy), 0.01);
        const f = (d - p.springLength) * p.springStrength * alpha;
        const fx = (dx / d) * f;
        const fy = (dy / d) * f;
        s.vx += fx; s.vy += fy;
        t.vx -= fx; t.vy -= fy;
      }
      for (const n of nodes) {
        if (n.pinned) { n.vx = 0; n.vy = 0; continue; }
        n.vx = (n.vx - n.x * p.centering * p.aspect * alpha) * p.damping;
        n.vy = (n.vy - (n.y * p.centering * alpha) / p.aspect) * p.damping;
        const speed = Math.hypot(n.vx, n.vy);
        if (speed > p.maxSpeed) { n.vx *= p.maxSpeed / speed; n.vy *= p.maxSpeed / speed; }
        n.x += n.vx;
        n.y += n.vy;
      }
      alpha *= p.alphaDecay;
      return true;
    }

    return {
      step,
      isActive: () => alpha >= p.alphaMin,
      reheat: (value) => { alpha = Math.max(alpha, value || 0.5); },
    };
  }

  // Compact label for graph nodes: "Long Name (ACRONYM)" -> "ACRONYM".
  function shortTitle(title) {
    const match = /^(.*?)\s*\(([^)]*)\)$/.exec(title);
    if (!match) return title;
    return /^[A-Z0-9-]+$/.test(match[2]) ? match[2] : match[1];
  }

  function progress(seenSlugs, articles) {
    const seen = seenSlugs.filter((s) => s in articles).length;
    return { seen, total: Object.keys(articles).length };
  }

  const api = { parseRoute, search, neighbors, pathPosition, radialLayout, createSimulation, progress, shortTitle };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.WikiCore = api;
})(typeof window !== "undefined" ? window : globalThis);
