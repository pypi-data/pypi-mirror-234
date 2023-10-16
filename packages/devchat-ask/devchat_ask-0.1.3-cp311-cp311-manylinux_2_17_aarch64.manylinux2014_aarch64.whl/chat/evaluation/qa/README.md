# Evaluation

A auto evaluation workflow for question answering application.

## `cli.py`

A cli tool for evaluation related tasks.

```console
$ python chat/evaluation/cli.py --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

  CLI to run evaluations.

Options:
  --help  Show this message and exit.

Commands:
  evaluate  Run evaluations.
  markdown  Generate a markdown report from the json report in JSON_PATH.
  resume    Resume an evaluation from the json report in JSON_PATH.
  show      Show available evaluators and evaluable subjects.
```
