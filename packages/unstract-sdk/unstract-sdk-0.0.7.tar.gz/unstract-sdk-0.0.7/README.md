# Unstract SDK

### Tools

#### Create a  scaffolding for a new tool

Example

```bash
unstract-tool-gen --command NEW --tool-name <name of tool> \
 --location ~/Devel/Github/pandora/tools/ --overwrite false
```

Supported commands:

- `NEW` - Create a new tool

#### Environment variables required for all Tools

- `PLATFORM_HOST`
- `PLATFORM_PORT`
- `PLATFORM_API_KEY`

#### Environment variables required for various LLMs

- Azure OpenAI
    - `OPENAI_API_KEY`
    - `OPENAI_API_BASE`
    - `OPENAI_API_VERSION`
    - `OPENAI_API_ENGINE`
    - `OPENAI_API_MODEL`
