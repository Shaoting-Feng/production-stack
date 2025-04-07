import time
from openai import OpenAI
import multiprocessing

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1/"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

model = "HuggingFaceTB/SmolLM2-135M-Instruct"

def send_request(_):
    st = time.monotonic()
    completion = client.completions.create(
        model=model,
        prompt="hi" * 8,
        echo=False,
        n=1,
        stream=False,
        logprobs=3,
        max_tokens=1
    )
    end = time.monotonic() - st
    return end, completion

if __name__ == "__main__":
    num_requests = 100  # number of total requests
    num_workers = 50  # number of concurrent processes

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(send_request, range(num_requests))

    times = [res[0] for res in results]
    completions = [res[1] for res in results]

    print("average time: ", sum(times) / len(times))
    # print("Completion results:")
    # for completion in completions:
    #     print(completion)
