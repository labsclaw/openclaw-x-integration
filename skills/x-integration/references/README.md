# X Integration Skill

For OpenClaw agents to post tweets via browser automation (no API credits required).

## Setup

1. Configure OAuth credentials in `.env`:
   - CONSUMER_KEY
   - CONSUMER_KEY_SECRET
   - X_ACCESS_TOKEN
   - X_ACCESS_TOKEN_SECRET

2. Ensure OpenClaw browser is available (playwright)

## Usage

Call via `browser act:evaluate` with tweet composition JavaScript.

## Method

Uses `document.querySelector('[data-testid="tweetButton"]').click()` to submit tweets without requiring X API credits.