// Tests for web/core.js — the pure logic behind the reader site.
// Run: node --test 'tests/web/*.test.js'
const test = require("node:test");
const assert = require("node:assert/strict");
const core = require("../../web/core.js");

const articles = {
  kiss: { slug: "kiss", title: "Keep It Simple, Stupid (KISS)", summary: "Choose the simplest design.", tags: ["simplicity"], links: ["yagni"], backlinks: ["dry", "yagni"] },
  yagni: { slug: "yagni", title: "You Aren't Gonna Need It (YAGNI)", summary: "Don't build for imagined futures.", tags: ["simplicity", "scope"], links: ["kiss"], backlinks: ["kiss"] },
  dry: { slug: "dry", title: "Don't Repeat Yourself (DRY)", summary: "One home for each piece of knowledge, simplest.", tags: ["design"], links: ["kiss"], backlinks: [] },
};

test("parseRoute: home, article, graph, search, unknown", () => {
  assert.deepEqual(core.parseRoute(""), { view: "home" });
  assert.deepEqual(core.parseRoute("#/"), { view: "home" });
  assert.deepEqual(core.parseRoute("#/a/kiss"), { view: "article", slug: "kiss" });
  assert.deepEqual(core.parseRoute("#/graph"), { view: "graph", focus: null });
  assert.deepEqual(core.parseRoute("#/graph/kiss"), { view: "graph", focus: "kiss" });
  assert.deepEqual(core.parseRoute("#/search/two%20words"), { view: "search", query: "two words" });
  assert.deepEqual(core.parseRoute("#/nope"), { view: "home" });
});

test("search ranks title matches above tag and summary matches", () => {
  const results = core.search(articles, "simpl");
  assert.deepEqual(results.map((a) => a.slug), ["kiss", "yagni", "dry"]);
});

test("search requires every term to match", () => {
  assert.deepEqual(core.search(articles, "simpl imagined").map((a) => a.slug), ["yagni"]);
});

test("search with an empty query returns nothing", () => {
  assert.deepEqual(core.search(articles, "   "), []);
});

test("search matches the acronym inside the title", () => {
  assert.deepEqual(core.search(articles, "yagni").map((a) => a.slug), ["yagni"]);
});

test("neighbors merges links and backlinks without duplicates", () => {
  assert.deepEqual(core.neighbors(articles.kiss), ["yagni", "dry"]);
});

test("pathPosition finds previous and next stops on the starter path", () => {
  const path = ["kiss", "yagni", "dry"];
  assert.deepEqual(core.pathPosition(path, "yagni"), { index: 1, total: 3, prev: "kiss", next: "dry" });
  assert.deepEqual(core.pathPosition(path, "kiss"), { index: 0, total: 3, prev: null, next: "yagni" });
  assert.equal(core.pathPosition(path, "other"), null);
});

test("radialLayout spaces points evenly on a circle", () => {
  const points = core.radialLayout(4, 10);
  assert.equal(points.length, 4);
  for (const p of points) assert.ok(Math.abs(Math.hypot(p.x, p.y) - 10) < 1e-9);
  assert.ok(Math.abs(points[0].x - 0) < 1e-9 && Math.abs(points[0].y + 10) < 1e-9);
});

test("simulation pulls linked nodes together and pushes overlapping nodes apart", () => {
  const nodes = [
    { id: "a", x: -300, y: 0 },
    { id: "b", x: 300, y: 0 },
    { id: "c", x: 0, y: 0 },
    { id: "d", x: 0, y: 0 },
  ];
  const sim = core.createSimulation(nodes, [["a", "b"]]);
  for (let i = 0; i < 300; i++) sim.step();
  const dist = (p, q) => Math.hypot(p.x - q.x, p.y - q.y);
  assert.ok(dist(nodes[0], nodes[1]) < 300, "linked nodes moved closer");
  assert.ok(dist(nodes[2], nodes[3]) > 10, "overlapping nodes separated");
  for (const n of nodes) assert.ok(Number.isFinite(n.x) && Number.isFinite(n.y));
});

test("simulation cools down and stops", () => {
  const nodes = [{ id: "a", x: 0, y: 0 }, { id: "b", x: 10, y: 0 }];
  const sim = core.createSimulation(nodes, [["a", "b"]]);
  let steps = 0;
  while (sim.step() && steps < 10000) steps++;
  assert.ok(steps < 10000);
  assert.equal(sim.isActive(), false);
  sim.reheat();
  assert.equal(sim.isActive(), true);
});

test("simulation leaves pinned nodes where they are", () => {
  const nodes = [{ id: "a", x: 5, y: 5, pinned: true }, { id: "b", x: 50, y: 0 }];
  const sim = core.createSimulation(nodes, [["a", "b"]]);
  for (let i = 0; i < 50; i++) sim.step();
  assert.deepEqual([nodes[0].x, nodes[0].y], [5, 5]);
});

test("explored progress counts only known articles", () => {
  assert.deepEqual(core.progress(["kiss", "ghost"], articles), { seen: 1, total: 3 });
});

test("shortTitle prefers a trailing acronym, else drops the parenthetical", () => {
  assert.equal(core.shortTitle("Command Query Responsibility Segregation (CQRS)"), "CQRS");
  assert.equal(core.shortTitle("Hexagonal Architecture (Ports and Adapters)"), "Hexagonal Architecture");
  assert.equal(core.shortTitle("Reversible Decisions (One-Way and Two-Way Doors)"), "Reversible Decisions");
  assert.equal(core.shortTitle("Conway's Law"), "Conway's Law");
  assert.equal(core.shortTitle("SOLID Principles"), "SOLID Principles");
});

test("simulation with a tall aspect lays nodes out taller than wide", () => {
  const nodes = Array.from({ length: 20 }, (_, i) => ({ id: String(i), x: Math.cos(i) * 50, y: Math.sin(i) * 50 }));
  const sim = core.createSimulation(nodes, [], { aspect: 2 });
  for (let i = 0; i < 400; i++) sim.step();
  const span = (key) => Math.max(...nodes.map((n) => n[key])) - Math.min(...nodes.map((n) => n[key]));
  assert.ok(span("y") > span("x") * 1.3, `y span ${span("y")} vs x span ${span("x")}`);
});

const glossary = [
  { term: "Idempotency key", id: "idempotency-key", letter: "I", html: "A unique ID for one <em>intended</em> action." },
  { term: "Saga", id: "saga", letter: "S", html: "A multi-step workflow with compensating actions; see idempotency." },
  { term: "SLO", id: "slo", letter: "S", html: "Service level objective." },
];

test("searchTerms ranks term matches above definition matches and ignores markup", () => {
  assert.deepEqual(core.searchTerms(glossary, "idempotency").map((e) => e.id), ["idempotency-key", "saga"]);
  assert.deepEqual(core.searchTerms(glossary, "<em>"), []);
  assert.deepEqual(core.searchTerms(glossary, " "), []);
});

test("parseRoute: terms view with optional query", () => {
  assert.deepEqual(core.parseRoute("#/terms"), { view: "terms", query: "" });
  assert.deepEqual(core.parseRoute("#/terms/slo"), { view: "terms", query: "slo" });
});

// ---------- Quiz ----------

// A deterministic stand-in for Math.random: walks through the given values.
function sequence(...values) {
  let i = 0;
  return () => values[i++ % values.length];
}

const q = (question, answer = 0) => ({ question, options: ["A", "B", "C", "D"], answer, why: "because" });
const quizArticles = {
  kiss: { slug: "kiss", category: "principles", quiz: [q("k1"), q("k2"), q("k3")] },
  dry: { slug: "dry", category: "principles", quiz: [q("d1"), q("d2")] },
  tdd: { slug: "tdd", category: "practices", quiz: [q("t1")] },
  none: { slug: "none", category: "practices", quiz: [] },
};

test("parseRoute: quiz, optionally scoped to a category", () => {
  assert.deepEqual(core.parseRoute("#/quiz"), { view: "quiz", category: null });
  assert.deepEqual(core.parseRoute("#/quiz/practices"), { view: "quiz", category: "practices" });
});

test("shuffle returns a new array with the same items and leaves the input alone", () => {
  const input = [1, 2, 3, 4, 5];
  const out = core.shuffle(input, sequence(0.9, 0.1, 0.5, 0.3));
  assert.deepEqual(input, [1, 2, 3, 4, 5]);
  assert.deepEqual([...out].sort(), [1, 2, 3, 4, 5]);
  assert.notDeepEqual(out, input);
});

test("shuffle with Math.random-like 0.999 keeps every index in range", () => {
  assert.deepEqual(core.shuffle([1, 2, 3], () => 0.999).length, 3);
});

test("prepareQuestion shuffles options and tracks which one is correct", () => {
  const prepared = core.prepareQuestion(q("k1", 2), sequence(0.1, 0.6, 0.3));
  assert.equal(prepared.question, "k1");
  assert.equal(prepared.why, "because");
  assert.deepEqual([...prepared.options.map((o) => o.html)].sort(), ["A", "B", "C", "D"]);
  const correct = prepared.options.filter((o) => o.correct);
  assert.equal(correct.length, 1);
  assert.equal(correct[0].html, "C");
});

test("quizDeck draws across articles before repeating one", () => {
  const deck = core.quizDeck(quizArticles, { count: 3, rng: sequence(0.4, 0.8, 0.2, 0.6) });
  assert.equal(deck.length, 3);
  assert.deepEqual([...deck.map((c) => c.slug)].sort(), ["dry", "kiss", "tdd"]);
});

test("quizDeck can be scoped to one category", () => {
  const deck = core.quizDeck(quizArticles, { category: "principles", count: 10, rng: Math.random });
  assert.equal(deck.length, 5);
  assert.ok(deck.every((c) => c.slug === "kiss" || c.slug === "dry"));
  assert.equal(new Set(deck.map((c) => c.question)).size, 5);
});

test("quizDeck cards are prepared questions tagged with their article", () => {
  const [card] = core.quizDeck(quizArticles, { category: "practices", count: 1, rng: Math.random });
  assert.equal(card.slug, "tdd");
  assert.equal(card.question, "t1");
  assert.equal(card.options.filter((o) => o.correct).length, 1);
});

test("quizCounts counts available questions per category", () => {
  assert.deepEqual(core.quizCounts(quizArticles), { all: 6, principles: 5, practices: 1 });
});
