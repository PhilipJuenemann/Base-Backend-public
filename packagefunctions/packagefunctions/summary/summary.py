import os
import openai

openai.api_key = "openai key"

#get summary
def summary_func(input_text, model="text-davinci-002", temperature=0.7, max_tokens=500):
    response = openai.Completion.create(
    model= model,
    prompt=f"Summarise this text: {input_text}",
    temperature= temperature,
    max_tokens= max_tokens,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    return response["choices"][0]["text"]

#shortining the summary
def preprocess_summary(summary):
    sum_sentences_list = []
    sum_sentences_list.append(summary.strip().split("."))
    short_text = sum_sentences_list[0][0:4]
    final_sum = ".".join(short_text)
    final_sum = final_sum + "."
    return final_sum
