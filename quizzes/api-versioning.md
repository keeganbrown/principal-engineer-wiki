# Quiz: API Versioning and Evolution

## Which of these changes to a JSON API response is backward-compatible?

- [x] Adding a new optional field that old clients can ignore.
- [ ] Renaming an existing field to a clearer name.
- [ ] Changing a field's type from a number to an object.
- [ ] Reusing a retired field name for a new meaning.

**Why:** Additive changes are safe when clients are tolerant readers. Renames, type changes, and reused fields break callers. See [[api-versioning]].

## Money appears on every resource in an API as a float, and it must become integer cents with a currency. What is the safest path?

- [x] Ship `/v2`, keep `/v1` with deprecation headers, and track its callers.
- [ ] Change `/v1` in place on a Sunday night, when traffic is at its lowest.
- [ ] Add a query parameter that silently switches the type for every client.
- [ ] Stop sending the float in `/v1` next month and email partners today.

**Why:** Changing `total`'s type in place breaks callers. For one field, a new field beside the old one can work; when the whole money shape changes everywhere, a new version with a published sunset is cleaner. See [[api-versioning]] and [[expand-and-contract]].

## A mobile client crashes when the server adds a new enum value. Which practice would have prevented it?

- [x] Making clients tolerant readers that handle unknown values.
- [ ] Making the server accept any field a client sends, unchecked.
- [ ] Sending the enum as an integer instead of as a string.
- [ ] Replacing enums in the API with free-text strings.

**Why:** Clients that handle every value explicitly break when one is added. Document that enums may grow, give unknown values a default, and keep the server strict about what it accepts. See [[api-versioning]].

## A backend API is used only by one web app, which ships in the same release. The team wants to rename a response field. Do they need a new API version?

- [x] Usually not; change both in lockstep, but rolling deploys still favor additive steps.
- [ ] Yes; every breaking change to any API needs a new major version first.
- [ ] Yes, and keep the old version running for a year for safety.
- [ ] No, and old and new code never run at the same time, so any change is safe.

**Why:** When you control every client and deploy them together, you can change in lockstep. Rolling deploys still mean old and new versions briefly coexist, so additive changes remain the safer habit. See [[api-versioning]].
