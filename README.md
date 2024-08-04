# Usage
Create `config.toml`.

```toml
[twitch]
app_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
app_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
target_channel = 'xxxxxxxxxx'

[voicevox]
speaker = 6
host = 'host.docker.internal'
port = 50021

[openai]
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

Create `terraform.tfvars`.
```bash
project = "<PROJECT_ID>"
```
