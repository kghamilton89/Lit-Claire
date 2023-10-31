---
language:
- fr
license: apache-2.0
pipeline_tag: text-generation
tags:
- pretrained
inference:
    parameters:
        temperature: 1.0
        max_new_tokens: 200
        top_k: 10
---

# Claire-Falcon-7B

**Claire-Falcon-7B is a 7B parameters causal decoder-only model built by [OpenLLM-France](https://github.com/OpenLLM-France) adapted from [Falcon-7b](https://huggingface.co/tiiuae/falcon-7b) on French conversational data. It is made available under the Apache 2.0 license.**


## How to use

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

model = "OpenLLM-France/Claire-Falcon-7B-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
)
sequences = pipeline(
   "[Intervenant 1:] Bonjour, pouvez-vous nous parler de votre sport préféré ?\n[Intervenant 2:] Alors euh oui,",
    max_new_tokens=200,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")

```

For fast inference with Claire, check-out [Text Generation Inference](https://github.com/huggingface/text-generation-inference).

You will need **at least 16GB of memory** to swiftly run inference with Claire-Falcon-7B.

## Training Details

### Training Data

Claire-Falcon-7B was tuned from Falcon-7B on the following data distribution:

| **Data source**               | **Words**  | **Training Sampling Weight** | **Sources**                                         |
|-------------------------------|------------|------------------------------|-----------------------------------------------------|
| Assemblée Nationale           | 135M       | 35%                          | assemblee-nationale.fr                              |
| Theatre                       |  16M       | 18%                          | theatre-classique.fr, theatregratuit.com            |
| Interviews                    |   6.4M     | 29%                          | TCOF, CFPP, CFPB, ACSYNT, PFC, Valibel              |
| Free Conversations            |   2.2M     | 10%                          | CRFP, OFROM, CID, Rhapsodie, ParisStories, PFC, CLAPI C-ORAL-ROM, LinTO, ESLO |
| Meetings                      |   1.2M     |  5%                          | SUMM-RE, LinTO, ORFEO réunions de travail |
| Debates                       |   402k     | <2%                          | FreD, ESLO                                |
| Assistance                    |   159k     | <1%                          | ORFEO fleuron, UBS, OTG, ESLO             |
| Presentation, Free Discourse  |    86k     | <0.5%                        | Valibel, LinTO, ESLO                      |

The data was tokenized with the [Falcon-7B](https://huggingface.co/tiiuae/falcon-7b) tokenizer.

### Training Procedure 

Claire-Falcon-7B is a causal decoder-only model trained on a causal language modeling task (i.e., predict the next token).
See [Falcon-7b](https://huggingface.co/tiiuae/falcon-7b) for more details.

Claire-Falcon-7B was trained on A100 80GB GPUs.

Training happened in October 2023.

Hyperparameters were the following:

| **Hyperparameter** | **Value**  |
|--------------------|------------|
| Precision          | `bfloat16` |
| Optimizer          | AdamW      |
| Learning rate      | 1e-4       |
| Weight decay       | 1e-2       |
| Batch size         | 132        |
| LoRA rank          | 16         |
| LoRA alpha         | 16         |
| Dropout            | 0.05       |
| gradient clipping  | 1          |

## License

Claire-Falcon-7B is made available under the Apache 2.0 license.

## Contact

contact@openllm-france.fr