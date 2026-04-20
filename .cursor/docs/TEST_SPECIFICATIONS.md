# Test Specifications

## Scope

This file defines the test intent and expected behavior for:
- Age verification
- Cart shipping threshold recalculation
- Product ratings and review inputs

Related source tests:
- `tests/test_age_verification.py`
- `tests/test_shopping_cart.py`
- `tests/test_product_page.py`

## 1) Age Verification

### AV-01 Adult user accepted
- **Precondition:** Logged-in user can open store.
- **Input:** DOB `01-01-1990`
- **Steps:** Open shop and submit DOB in age modal.
- **Expected:** "of age" success status is visible.

### AV-02 Exactly 18 years old accepted
- **Precondition:** Logged-in user can open store.
- **Input:** DOB computed as current date minus 18 years.
- **Steps:** Open shop and submit boundary DOB.
- **Expected:** User is treated as adult and can proceed.

### AV-03 One day younger than 18 rejected
- **Precondition:** Logged-in user can open store.
- **Input:** DOB computed as (today minus 18 years) plus 1 day.
- **Steps:** Open shop and submit boundary-minus-one-day DOB.
- **Expected:** Underage status is visible.

### AV-04 Direct product URL still enforces age check
- **Precondition:** Logged-in user.
- **Input:** Navigate directly to alcohol product URL.
- **Steps:** Open product by URL and attempt access.
- **Expected:** Age gate is still enforced (modal shown or protected flow).

## 2) Cart Shipping Threshold & Removal Bug

### SC-01 Shipping threshold at checkout
- **Cases:** 19.99 -> paid shipping, 20.00 -> free shipping, 500.00 -> free shipping.
- **Expected:** Shipping switches exactly at 20.00.

### SC-02 Shipping recalculates after item removal
- **Precondition:** Cart starts above threshold and shipping is free.
- **Steps:** Remove items until cart total is below 20.00.
- **Expected:** Shipping becomes non-zero.
- **Bug targeted:** Shipping remains free below threshold after removals.

## 3) Rating System and Inputs

### RT-01 Review character limits
- **Cases:** 500 chars accepted, >500 constrained/rejected.
- **Expected:** Input/submit path enforces 500-char max behavior.

### RT-02 Average rating rendering
- **Input:** Submit ratings [4, 5, 4].
- **Expected:** Average display approximately 4.5.

### RT-03 Submit without stars
- **Input:** Review text only.
- **Expected:** Validation error shown.

### RT-04 Review unavailable for logged-out user
- **Input:** Open product page while logged out.
- **Expected:** Review action is disabled or login modal is required.

### RT-05 Submit with stars but empty text
- **Input:** Stars selected, empty review body.
- **Expected:** Validation error shown.

### RT-06 Cancel review closes form
- **Input:** Open form then cancel.
- **Expected:** Review input/form is no longer visible.

### RT-07 Special character review input
- **Input:** Review contains `<script>`, quotes, ampersands.
- **Expected:** Form handles input safely and does not break interaction flow.
