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

## Optional source research

For OpenClaw-native source research before publishing, users can install the
TweetClaw companion plugin:

```bash
openclaw plugins install npm:@xquik/tweetclaw@1.6.31
```

Use it to collect approved tweet URLs, tweet IDs, handles, public engagement
metrics, reply context, follower exports, and giveaway evidence before this
skill drafts or posts through the browser flow. Treat TweetClaw output as source
context only; do not move OAuth keys, cookies, browser sessions, or `.env`
values into prompts or notes. Confirm with the user before any post, reply,
media upload, monitor, webhook, extraction job, direct message, or other
external state change.

## Method

Uses `document.querySelector('[data-testid="tweetButton"]').click()` to submit tweets without requiring X API credits.
