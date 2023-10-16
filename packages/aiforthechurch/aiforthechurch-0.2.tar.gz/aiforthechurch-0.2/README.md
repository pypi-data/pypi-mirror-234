# aiforthechurch
Modern LLMs are rooted in secular value systems that are often misaligned with religious organisations. This PyPI package allows anyone to train and deploying doctrinally correct LLMs based on Llama2. Effectively, we are aligning models to a set of values.

```python
from aiforthecurch import align_llama2
doctrinal_dataset = "/path/to/csv"
align_llama2(doctrinal_dataset)
```

`aiforthechurch` is integrated with HuggingFace shuch that the aligned model will be automatically pushed to your HuggingFace repo of choice at the end of the training.

At aiforthechurch.org we provide tools for generating doctrinal datasets, a few examples are available at huggingface.co/AiForTheChurch.
