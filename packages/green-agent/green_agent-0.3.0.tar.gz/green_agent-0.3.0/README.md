# Green Agent

Library providing uniform (mostly) abstration across foundation-models APIs + nice "interface" helpsers for running experiments or crafting your own ChatGPT-style UI.

For now it supports chat-tuned LLMs from OpenAI and Google (Vertex AI) - more stuff to come.

## Usage

Inside a jupyter notebook:

```py
import green_agent as ga

ag1 = ga.AgentNbUI(ga.OpenAIAgent(
    "You are a sarcastic but helpful assistant.",
    model="gpt-3.5-turbo"
))
ag1.asks("Which foods would you suggest trying when visiting Lyon, France?")
```

## How to develop

First time:

```sh
poetry install --with test dev
poetry shell
python -m ipykernel install --user --name green-agent
```

In general:

```sh
poetry shell
```

Notebooks:

```sh
jupyter notebook  # classic UI
jupyter lab  # modern UI
```

### Managing dependencies with Poetry

```
poetry add <my-dependency>
poetry add <my-dependency> --group dev
poetry add <my-dependency> --group test
```

```
poetry export -o all-requirements.txt
```
