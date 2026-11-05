# Quiz: Secrets Management

## A database password was committed to a private repository last year. The team removes it in a new commit. Is that enough?

- [x] No; rotate it, since the history and every clone still hold it.
- [ ] Yes, as long as the repository stays private to the company.
- [ ] Yes, once the old commits are squashed so it's gone from history.
- [ ] No; delete the repository and recreate it from a clean copy.

**Why:** Removing a secret from the latest version doesn't remove the copies in history, clones, and logs. Treat any committed secret as leaked, and rotate it. See [[secrets-management]].

## A pipeline deploys to the cloud using a long-lived access key stored in its settings. What is the stronger setup?

- [x] Have the pipeline prove its identity to get short-lived credentials each run.
- [ ] Move the key into an encrypted file in the repository beside the code.
- [ ] Rotate the key once a year and share the new value with the platform team.
- [ ] Give the key admin rights, so deploys never fail on a missing permission.

**Why:** A credential that expires in minutes leaves nothing long-lived to leak. The cost is per-platform setup and harder debugging when authentication fails. See [[secrets-management]].

## Five services share a database credential, and the team needs to rotate it. What keeps the rotation from causing an outage?

- [x] Let old and new versions both work until every caller has moved.
- [ ] Revoke the old version first, so no service can keep using it.
- [ ] Rotate it at night, when fewer requests depend on the credential.
- [ ] Email each owning team the new value a day before the switch.

**Why:** An overlap lets callers switch without breaking. Watch for the old credential to go quiet before revoking it, and give each service its own credential next time. See [[secrets-management]].

## A developer's local prototype talks only to fakes and has no real credentials. Should they set up a secrets manager now?

- [x] Not yet; add one before the first real credential appears.
- [ ] Yes; every project needs a secrets manager from its first commit.
- [ ] Yes, and have it rotate the fake credentials every week.
- [ ] No; a prototype can keep real credentials in its code safely.

**Why:** With no real credentials there's nothing to protect yet. The moment a real one is needed, deliver it at run time rather than writing it into the code. See [[secrets-management]].
