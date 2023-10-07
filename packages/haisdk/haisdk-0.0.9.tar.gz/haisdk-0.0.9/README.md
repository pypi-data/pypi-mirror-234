<h1>
<img src="docs/holistic_ai.png" width="100"><br>Holistic AI
</h1>

The Holistic AI SDK is a library that provides integration with the HAI Platform   

- Holistic Ai website: https://holisticai.com

## Installation

Install the library with:
```bash
    pip install haisdk
```

## How to use the haisdk

Create a config
```bash
    from haisdk.config import Config
    config = {
        'tenant_id': '',
        'api_key': '',
        'project_id': '',
        'solution_id': '',
        'instance_id': ''
    }
    session = Config(config=config)
```

Create an assessment
```bash
    from haisdk.assessment import Assess
    settings = {
        'task': '',
        'tbd': 'tbd'
    }
    assess = Assess(session=session, settings=settings)
    assess.run(input=...,output=...,pred=...,model=...)
```