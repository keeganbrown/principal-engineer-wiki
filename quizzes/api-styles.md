# Quiz: API Styles

## Partners in many languages will integrate with your public API, and an internal team proposes gRPC for it. What's the usual choice?

- [x] REST, which works with any HTTP tool partners have.
- [ ] gRPC, since its binary encoding is faster for everyone.
- [ ] GraphQL, so that partners can shape every response.
- [ ] Both gRPC and REST, so partners can choose either.

**Why:** REST is familiar to every partner and needs no special tooling. gRPC suits internal service calls; GraphQL suits many clients with different data needs. See [[api-styles]].

## A mobile screen makes seven REST calls and feels slow on phone networks. The company also has a public REST API for partners. What fits best?

- [x] A GraphQL gateway for the apps only, leaving partners' REST alone.
- [ ] Converting every API in the company to GraphQL in one migration.
- [ ] Replacing the partner REST API with gRPC for faster responses.
- [ ] One mobile-only REST endpoint that bundles the seven calls.

**Why:** One query fetches what a screen needs, and partners aren't forced through a rewrite; a bundled endpoint fixes one screen, but each new screen needs another. The gateway's costs: running it, query cost limits, and per-field authorization. See [[api-styles]].

## Two modules inside one deployable application need to talk. Which API style fits best?

- [x] None; plain function calls beat any network API.
- [ ] gRPC, for its fast binary encoding between modules.
- [ ] REST, so the modules can be split out later on.
- [ ] GraphQL, so each module fetches only what it needs.

**Why:** Not every integration needs a network API. Inside one process, function calls are simpler and faster. See [[api-styles]] and [[modular-monolith]].
