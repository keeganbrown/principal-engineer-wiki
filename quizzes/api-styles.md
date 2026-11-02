# Quiz: API Styles (REST, gRPC, GraphQL)

## Which style is the usual default for a public API used by outside partners?

- [x] REST
- [ ] gRPC
- [ ] GraphQL
- [ ] Direct database access

**Why:** REST works with any HTTP tool and is familiar to every partner. gRPC suits internal service calls; GraphQL suits many clients with different data needs. See [[api-styles]].

## A mobile screen makes seven REST calls and feels slow on phone networks. What did the team choose?

- [x] Add a GraphQL gateway for the apps only, leaving the partner REST API alone.
- [ ] Convert every API in the company to GraphQL.
- [ ] Replace the partner REST API with gRPC.
- [ ] Merge the seven endpoints into one large REST response for everyone.

**Why:** One query fetches what a screen needs, and partners aren't forced through a rewrite. Pick by who the callers are. See [[api-styles]].

## Two modules inside one deployable application need to talk. Which API style fits best?

- [x] None; plain function calls beat any network API.
- [ ] gRPC, for its fast binary encoding.
- [ ] REST, so the modules can be split out later.
- [ ] GraphQL, so each module fetches only what it needs.

**Why:** Not every integration needs a network API. Inside one process, function calls are simpler and faster. See [[api-styles]] and [[modular-monolith]].
