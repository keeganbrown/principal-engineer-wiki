# Quiz: API Versioning and Evolution

## Which of these changes to a JSON API response is backward-compatible?

- [x] Adding a new optional field that old clients can ignore.
- [ ] Renaming an existing field to a clearer name.
- [ ] Changing a field's type from a number to an object.
- [ ] Reusing a retired field name for a new meaning.

**Why:** Additive changes are safe when clients are tolerant readers. Renames, type changes, and reused fields break callers. See [[api-versioning]].

## A team must change `total` from a float to integer cents with a currency. What is the safest path?

- [x] Ship `/v2` with the new shape, keep `/v1` running with deprecation headers, and track who still calls it.
- [ ] Change `/v1` in place on a Sunday night when traffic is low.
- [ ] Add a query parameter that silently switches the type for everyone.
- [ ] Email partners and remove `/v1` the same day `/v2` ships.

**Why:** A type change can't be made additively, so it needs an explicit version, a published sunset, and per-client usage tracking. See [[api-versioning]].

## A mobile client crashes when the server adds a new enum value. Which practice would have prevented it?

- [x] Making clients tolerant readers that handle unknown values gracefully.
- [ ] Making the server accept any field the client sends without checks.
- [ ] Versioning the API every time a field is added.
- [ ] Removing enums from the API and using free-text strings.

**Why:** Clients should ignore what they don't understand, while servers stay strict about what they accept. Crashing on new enum values is a listed trap. See [[api-versioning]].
