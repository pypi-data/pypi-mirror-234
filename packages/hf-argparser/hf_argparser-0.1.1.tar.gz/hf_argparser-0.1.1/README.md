# HF Argparser

Standalone Argument Parser from HuggingFace Transformers.

This is a standalone version of the argument parser used in the HuggingFace Transformers library. It is a simple wrapper around the `argparse` library that allows you to easily define your command-line arguments for your scripts using dataclasses.

## Installation

```bash
pip install hf-argparser
```

## Usage

```python
from dataclasses import dataclass
from hf_argparser import HfArgumentParser, HFArg

@dataclass
class AddArgs():
    x: int
    y: int

@dataclass
class OutputArgs():
    output_file: str = field(
        default=None,
        metadata={'help': 'output filename'})

    parser = HfArgumentParser([AddArgs, OutputArgs])
    
    add_args, output_args, unknown_args = parser.parse_args_into_dataclasses(
            return_remaining_strings=True)
    return add_args, output_args, unknown_args
```

> Above code is taken from [this post](https://python.plainenglish.io/how-to-automatically-generate-command-line-interface-for-python-programs-e9fd9b6a99ca) by @kenilc.

See the [Transformers documentation](https://huggingface.co/docs/transformers/v4.34.0/en/internal/trainer_utils#transformers.HfArgumentParser) for more information on how to use the `HfArgumentParser`.

## Todo
- [] Automate pulling new changes to `hf_argparser` from `transformers` repo.
- [] Automate creating new releases on PyPi.
- [] Add tests.
- [] Improve README.

## Acknowledgements
- [HuggingFace Transformers :hugs:]("https://github.com/huggingface/transformers")