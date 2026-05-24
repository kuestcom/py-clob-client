## Pull Request Rules

Please make sure your PR follows these rules:

- One PR should address one feature, bugfix, or maintenance change.
- Keep PRs small, focused, and easy to review.
- Use commit prefixes such as `fix:`, `feat:`, `refactor:`, `docs:`, `test:`, and `chore:`.
- Use English for branch names and commit subjects.
- Review your own diff before opening the PR.
- Rebase on the latest `main` before pushing.
- If dependencies changed, include the updated `requirements.txt`.
- If public SDK APIs changed, update Python types, README snippets, examples, or tests when relevant.
- If signing, authentication, RFQ, order building, order utilities, headers, or HTTP behavior changed, include focused regression coverage whenever feasible.
- Avoid unrelated refactors, drive-by fixes, or config/policy changes in the same PR.
- Avoid commented-out code and unnecessary inline comments. Keep comments only when they explain non-obvious constraints or decisions.
- If you use AI/LLM tools, use the highest reasoning mode available and full repository context/access when safe, then manually review and test the final diff before submitting.
- Bugfix PRs should include a regression test whenever feasible.
- PR descriptions should clearly state scope, reason for the change, testing performed, and any relevant risks.

## Summary

Describe what changed and why. Mention affected SDK areas such as CLOB client methods, RFQ, order building, order utilities, authentication/signing, headers, HTTP helpers, examples, or package/config files.

## Testing

Describe how this was tested. Include the commands you ran and any examples or integration flows you exercised.

## Risks

Describe any relevant risks, tradeoffs, compatibility concerns, or follow-up work.

## Checklist

- [ ] I ran `python -m pip install -r requirements.txt`, or dependency changes were intentional and `requirements.txt` is updated.
- [ ] I ran `python -m black --check .`.
- [ ] I ran `python -m pytest -s`.
- [ ] I ran `python -m build --sdist --wheel`.
- [ ] I updated docs, examples, and/or tests for user-facing behavior changes, or this PR does not need them.
- [ ] I confirmed no secrets, private keys, or real API credentials were added.
