import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, LogitsProcessorList

model_name = "gpt2"

model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)


def generate(max_length):
    input = "The capital of France is "
    input_ids = tokenizer.encode(input, return_tensors="pt")
    print(input_ids)
    logits_processor = LogitsProcessorList()
    for i in range(max_length):
        outputs = model(input_ids)
        logits = outputs.logits
        next_token_logits = outputs.logits[:, -1, :]
        print("logits.shape: ", logits.shape)
        next_tokens_scores = logits_processor(input_ids, next_token_logits)
        next_tokens = torch.argmax(next_tokens_scores, dim=-1)
        input_ids = torch.cat([input_ids, next_tokens[:, None]], dim=-1)

    return input_ids
