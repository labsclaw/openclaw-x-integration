---
name: x-integration
description: "Post tweets to X (Twitter) via browser automation or OAuth 1.0a API."
license: "MIT"
---

# X Integration

Post tweets using browser automation (no API credits required) or OAuth 1.0a credentials.

## Env vars

- `CONSUMER_KEY` - OAuth 1.0 API Key
- `CONSUMER_KEY_SECRET` - OAuth 1.0 API Secret
- `X_ACCESS_TOKEN` - Access Token
- `X_ACCESS_TOKEN_SECRET` - Access Token Secret

## Methods

### Browser automation (default)
Uses OpenClaw browser tool to simulate human tweet composition. No paid credits required.

### API mode
For read-only operations. POST requires $0.015/credit (X API v2).

## Usage

```
x_post "Your tweet text here"
x_post_status "status_id"
x_get_user
```

## Security

Credentials stored in `.env`. Never share tokens. Use browser mode to avoid billing issues.