# llm-prefill

LLM plugin for managing and using prefill templates with any model.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-prefill
```

## Usage

### Adding a prefill template

```bash
llm prefill add my_template "This is a prefill template"
```

Or to open an editor:

```bash
llm prefill add my_template
```

### Listing prefill templates

```bash
llm prefill list
```

### Removing a prefill template

```bash
llm prefill remove my_template
```

### Using a prefill template with a prompt

```bash
llm -m any-model --prefill my_template "Your prompt here"
```

This will prepend the content of the `my_template` prefill to your prompt.

## Configuration

By default, prefill templates are stored in `~/.llm/prefills`. You can change this location by setting the `LLM_PREFILLS_DIR` environment variable.
