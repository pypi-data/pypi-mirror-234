# Klu.ai Python SDK

[![pypi](https://img.shields.io/pypi/v/klu.svg)](https://pypi.org/project/klu/)
[![python](https://img.shields.io/pypi/pyversions/klu.svg)](https://pypi.org/project/klu/)
[![Build Status](https://github.com/klu-ai/klu-sdk/actions/workflows/dev.yml/badge.svg)](https://github.com/klu-ai/klu-sdk/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/klu-ai/klu-sdk/branch/main/graphs/badge.svg)](https://codecov.io/github/klu-ai/klu-sdk)

## Description

The Klu Python SDK is a library that provides access to the Klu platform. With the SDK, quick build AI-enabled apps.

The SDK gives developers the ability to interact with their workspace, including:

- **klu.apps** Managing apps (projects) and 
- **klu.actions** Manage actions (prompt templates with model config) 
- **klu.context** Create and manage context libaries for RAG
- **klu.actions.stream** Deploy actions for generations and chat
- **klu.session** Manage session memory across inference and models
- **klu.feedback** Capture user feedback and behavior
- **klu.experiment** Run 1:1 prompt evals and A/B tests
- **klu.data** Import JSONL data for use, or export for further analysis
- **klu.models** Manage LLM providers and default models
- **klu.finetune** Fine-tune models with on your data

More resources here:

- [Access Your Klu Workspace](https://app.klu.ai/current/)
- [SDK GitHub Repo](https://github.com/klu-ai/klu-sdk)
- [Documentation](https://docs.klu.ai)
- [PyPI](https://pypi.org/project/klu/)

## Installation

To install, run:

```
pip install klu
```

Klu SDK requires Python version 3.7 or later.

## Getting Started

To access Klu via the SDK, first obtain your API key from the [Klu.ai app](https://app.klu.ai/current/settings/developers). Once you have your key, you can create a `Klu` object:

```python
from klu import Klu

klu = Klu("YOUR_API_KEY")
```

### Manage Models

Once you have a `Klu` object, you can access the different models available in the Klu API:

```python
from klu import Klu

klu = Klu("YOUR_API_KEY")
models = await klu.models.get("model_guid")

```

### Get Apps

Each of these objects provides methods for interacting with the corresponding model in the Klu API. For example, to list all apps in your workspace, you can use:

```python
from klu import Klu

klu = Klu("YOUR_API_KEY")
apps = klu.apps.list()
```

### Run Actions w/ Streaming

Run inference with a Klu Action and start streaming generation response.

```python
from klu import Klu

klu = Klu("YOUR_API_KEY")

prompt_response = await klu.actions.prompt("action_guid", "prompt", streaming=True)
async for message in klu.actions.stream(prompt_response.streaming_url):
    print(message)
```

### Get Data

In a similar manner, in order to get a list of data points for an action, you can do the following:

```python
from klu import Klu

klu = Klu("YOUR_API_KEY")
data = klu.data.get_data("action_guid")
```

See the platform docs for more examples.

## Documentation
For more detailed information on how to use the SDK, please refer to the [Klu Platform documentation](https://docs.klu.ai/).

## License

Copyright 2023 Klu, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.