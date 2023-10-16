<div align="left">
  <img src="assets/images/pygraphgpt_logo.svg" width = 200><br>
</div>

---

`PyGraphGPT`: A package to empower development of Knowledge Graph based GenAI application.
* Template prompts for graph extraction 
* Interactive GUI for visualization
* Python compatible


# Installation

* Install with `poetry`: `poetry add pygraphgpt`
* Install with `pip`: `pip install pygraphgpt`

# Quickstart
After installing `pygraphgpt`, to start the front-end webapp in the local server, user can use:

```
poetry run graphgpt
```

Experienced user or contributor can start the application from the cloned repository via `Makefile`:
`make graphgpt`


# Contribution
This tool is designed to share knowledge and facilitate the development of GenAI with Graph Knowledge.
As new ideas and requirements only come with usage, any suggestions or contributions 
will be more than welcome.

## How to
To contribute, you are invited to:
- Create a new `issue` for suggesting new feature from [issues'page](https://github.com/diy2learn/pygraphgpt/issues).
- Create `PR` to address the created issues.

For each `PR`, please:
* checkout from the branch `develop`
* name the branch as: `feat/<feature_name_here>`
* should merge only to the `develop` branch (not master)
* please delete the merged feature branch to avoid messy branches.

## Sanity check
To facilitate the development and assure the code quality, please activate the automatic sanity check tool: black, isort etc…
For this purpose:
* In the virtual environment, activate the `pre-commit`: `pre-commit install`.


