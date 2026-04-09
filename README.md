# App Framework Studio


Tooling to apply and update App Framework Components.


## Installing Skills

Install all skills from this repository into your AI agent using [`ai-agent-skills`](https://github.com/datarobot-community/ai-agent-skills):

```bash
npx ai-agent-skills install datarobot-community/app-framework
```


* Program that runs copier with the appropriate settings such that
  they can share items and put answers in expected places.

* https://datarobot.atlassian.net/wiki/spaces/BOPS/pages/6542032899/App+Framework+-+Studio


## Components

* Base: https://github.com/datarobot/af-component-base
* React Frontend: https://github.com/datarobot/af-component-react
* FastAPI Backend: https://github.com/datarobot/af-component-fastapi-backend
* LLM: https://github.com/datarobot/af-component-llm
* Tool: https://github.com/datarobot/af-component-tool
* Agent: https://github.com/datarobot/af-component-agent


## Copier Watch

This script is useful for iterating on [copier](https://copier.readthedocs.io/en/stable/) templates like the components here.

Essentially this script watches all files changes in a source
template. When you edit the source template repo, it then creates a
local commit that all future iterations amend on the copier source
repo, it then uses that local commit to run copier update on the
destination repo. This enables you to iterate rapidly with jinja files
without pushing commits remotely.

Additionally, for each change in the source repo, it resets the
destination repo (make sure your destination has a clean `git status`)
and applies the total change set from the beginning of the commit so
you don't have to worry too much about the destination repo.

> [!WARNING]
>  This script monkeys with git repositories and
>  can cause data loss. Use with caution and ensure you have backups of
>  your repositories. Essentially it runs git reset and git clean on
>  the destination repo.**


### Sample usage:

```
uv run tools/copier-watch/copier-watch.py --commit-message 'Adjusted backend' --answers-file .datarobot/answers/fastapi-web.yml ~/code/af-component-fastapi-backend ~/code/recipe-talk-to-my-docs
```

### Demo:

- Top shell is running pytest watcher in the destination repo
- Bottom left is this script watching for changes in af-component-fastapi-backend
- Bottom right is me changing the template. When changing the tests it automatically applies the updated template to the TTMDocs repo, the pytest-watcher picks it up and runs them as they are changing

![copier-watcher-demo](https://github.com/user-attachments/assets/0f1715e9-fa3e-4226-a43a-880a203afef9)
