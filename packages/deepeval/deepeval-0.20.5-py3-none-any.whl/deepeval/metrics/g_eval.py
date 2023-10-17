"""G-Eval from https://arxiv.org/pdf/2303.16634.pdf
"""

# Evaluating Coherence

import openai
import tqdm
import time

# "scores": {
#             "coherence": 1.3333333333333333,
#             "consistency": 1.0,
#             "fluency": 3.0,
#             "relevance": 1.6666666666666667,
#             "overall": 1.75
#         }
#     },

system_prompt = """You will be given one summary written
for a news article. Your task is to rate
the summary on one metric.
Please make sure you read and understand these instructions carefully. Please
keep this document open while reviewing,
and refer to it as needed."""

prompt = """Evaluation Criteria:
Coherence (1-5) - the collective quality
of all sentences. We align this dimension with the DUC quality question of
structure and coherence whereby ”the
summary should be well-structured and
well-organized. The summary should not
just be a heap of related information, but
should build from sentence to sentence
to a coherent body of information about
a topic.”"""

new_json = []
for instance in tqdm.tqdm(summeval):
    source = instance["source"]
    system_output = instance["system_output"]
    cur_prompt = prompt.replace("{{Document}}", source).replace(
        "{{Summary}}", system_output
    )
    instance["prompt"] = cur_prompt
    while True:
        try:
            _response = openai.ChatCompletion.create(
                model=args.model,
                messages=[{"role": "system", "content": cur_prompt}],
                temperature=2,
                max_tokens=5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                # logprobs=40,
                n=20,
            )
            time.sleep(0.5)

            all_responses = [
                _response["choices"][i]["message"]["content"]
                for i in range(len(_response["choices"]))
            ]
            instance["all_responses"] = all_responses
            new_json.append(instance)
            ct += 1
            break
        except Exception as e:
            print(e)
            if "limit" in str(e):
                time.sleep(2)
            else:
                ignore += 1
                print("ignored", ignore)

                break
