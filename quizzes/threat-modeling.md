# Quiz: Threat Modeling

## An export endpoint takes an account ID from the request and checks that the caller is logged in. What is the main threat?

- [x] Any logged-in user can request another account's data by changing the ID.
- [ ] Attackers can guess passwords faster because the endpoint has no captcha.
- [ ] The export is safe, because only logged-in users can reach the endpoint.
- [ ] The account ID should be encrypted in the request so nobody can read it.

**Why:** Authentication says who someone is; authorization says what they may do. Check that the caller may touch this object, and take the account from the session, not the request. See [[threat-modeling]].

## Where should a team focus when threat modeling a new feature?

- [x] The trust boundaries, where data crosses between differently trusted parts.
- [ ] The most sophisticated attacker they can imagine, regardless of likelihood.
- [ ] Every function in the codebase, reviewed line by line for possible flaws.
- [ ] Only the parts of the system that face the public internet directly.

**Why:** Most attacks cross a trust boundary, so walk each one with STRIDE. Boundaries aren't only public ones: webhooks, uploads, outgoing emails, and jobs that mix many customers' data count too. See [[threat-modeling]].

## A threat model lists eight threats, but nobody has decided what to do about them. What is missing?

- [x] A decision for each: mitigate, remove, transfer, or accept with an owner.
- [ ] A longer list, since eight threats is too few to be taken seriously.
- [ ] A security team sign-off, which makes the list complete as it stands.
- [ ] Nothing; writing threats down is the whole purpose of the exercise.

**Why:** A list with no owner or fix is a worry, not a plan. Decide something for every threat, and give accepted risks an owner and a reason. See [[threat-modeling]].

## A team adds one new field to a form whose design was threat modeled last month. Do they need a new threat modeling session?

- [x] Not usually; a question in code review is enough for a change inside a modeled boundary.
- [ ] Yes; every change to the system needs its own full threat modeling session.
- [ ] Yes, and the security team should run it without the feature team present.
- [ ] No; once a design has been threat modeled it never needs to be revisited.

**Why:** A small change inside an already-modeled boundary doesn't need its own session. Revisit the model when the design changes. See [[threat-modeling]].
