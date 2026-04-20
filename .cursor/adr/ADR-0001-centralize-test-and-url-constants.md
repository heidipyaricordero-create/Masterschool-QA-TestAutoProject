# ADR-0001: Centralize test and URL constants

- Status: Accepted
- Date: 2026-04-20

## Context

Page objects and tests contained repeated hard-coded values for:
- Application URLs (`/auth`, `/store`, `/cart`, product URL)
- Shared test credentials
- Shared skip reason string for unavailable auth account
- Common date of birth value used in age verification tests

This duplication increases maintenance effort and creates inconsistency risk when environment values change.

## Decision

Create a root-level `constants.py` module as the single source of truth for shared runtime/test constants and migrate all clear duplicates to imports from this module.

The refactor includes:
- URL and path constants
- Test user credentials
- Shared pytest skip reason for auth unavailability
- Shared DOB constant for age verification

## Consequences

### Positive

- Reduces duplicated literals and drift across tests/page objects
- Makes environment changes faster and safer
- Improves readability by naming business-significant constants

### Trade-offs

- Adds one more module dependency for page and test files
- Requires discipline to keep new shared literals in `constants.py`
