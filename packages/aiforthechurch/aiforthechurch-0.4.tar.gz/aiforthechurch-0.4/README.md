# AI for the Church
Modern LLMs are rooted in secular value systems that are often misaligned with religious organisations. This PyPI package allows anyone to train and deploying doctrinally correct LLMs based on Llama2. Effectively, we are aligning models to a set of values.

```python
from aiforthechurch import align_llama2
doctrinal_dataset = "/path/to/csv"
align_llama2(doctrinal_dataset)
```

`aiforthechurch` is integrated with HuggingFace shuch that the aligned model will be automatically pushed to your HuggingFace repo of choice at the end of the training.

At aiforthechurch.org we provide tools for generating doctrinal datasets, a few examples are available at huggingface.co/AiForTheChurch.

## Model Training requirements
If you wish to train your models using this repo you will need access to a machine with over 16GB of GPU memory and 30GB RAM. The full model weights for Llama2-7B amount to almost 30GB, but we use parameter-efficient fine-tuning (PEFT) LoRA to save memory and avoid any catastrophic forgetting during the fine-tuning procedure.

## References
We leaned heavily on open-source libraries like `transformers`, `peft`, and
`bitsandbytes` for this project.
- Dettmers, Tim, Mike Lewis, Younes Belkada, and Luke Zettlemoyer. 2022. "[LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale](https://arxiv.org/abs/2208.07339)." *arXiv preprint arXiv:2208.07339*.
- Hu, Edward J., Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. "[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)." *arXiv preprint arXiv:2106.09685*.
