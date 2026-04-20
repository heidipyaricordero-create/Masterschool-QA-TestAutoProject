# ADR-0002: Expand automated coverage for age gate, shipping recalculation, and rating inputs

- Status: Accepted
- Date: 2026-04-20

## Context

Recent refactoring improved page object consistency and centralized constants, but core feature risk areas still lacked complete test coverage:
- Age verification had only one active test and missing boundary coverage.
- Shipping behavior below 20.00 after cart item removal was reported as buggy.
- Rating/review workflows did not fully validate input edge cases.

The existing suite also depends on a stable product URL for celery/review flows, and flaky cart removal behavior can appear when DOM updates are not synchronized.

## Decision

Adopt a test-first expansion for three critical feature areas:
1. Age verification with adult and boundary-age cases.
2. Shipping threshold recalculation after removals (bug-focused regression check).
3. Rating/review input validation and interaction edge cases.

Support these tests by:
- Confirming a correct celery product URL constant.
- Hardening cart item removal against stale element race conditions.
- Keeping test behavior explicit in a dedicated test specification document.

## Consequences

### Positive
- Stronger regression protection around known business-critical failures.
- Clearer expected behavior at boundaries (age 18 and shipping threshold 20.00).
- Better confidence that review UX validates user input correctly.

### Trade-offs
- Additional tests increase execution time.
- Product/review tests remain sensitive to target environment data and auth state.
