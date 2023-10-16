# Description of CLI for Storage at Merklebot

This is a CLI-wrapper for Merklebot's Storage API.

# Installation 
```bash
pip install storagecli
```

# Authorization

When you get your **ORGANIZATION NAME** and **BUCKET TOKEN** at [app.merklebot.com](https://app.merklebot.com), you could use them to authorize in 3 places, with priority from higher to lower:

1. Direct insert in command as options
2. Use with environmental variables `STORAGECLI_ORGANIZATION` and `STORAGECLI_BUCKET_TOKEN`
3. With config (via command `storagecli config init`)

# Content interactions
Check available commands with 
```bash
storagecli content --help
```

