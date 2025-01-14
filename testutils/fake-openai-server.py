"""
Args:
    --port: Port to run the server on
    --host: Host to run the server on
    --max-tokens: maximum number of tokens to generate in the response if max_tokens is not provided in the request
    --speed: number of tokens per second per request
"""
from typing import (AsyncGenerator, AsyncIterator, Callable, Dict, Final, List,
                    Optional)
import asyncio
import argparse
import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, Response

from vllm.entrypoints.chat_utils import (ChatTemplateContentFormatOption,
                                         ConversationMessage)
from vllm.entrypoints.logger import RequestLogger
from vllm.entrypoints.openai.protocol import (
    ChatCompletionLogProb, ChatCompletionLogProbs,
    ChatCompletionLogProbsContent, ChatCompletionNamedToolChoiceParam,
    ChatCompletionRequest, ChatCompletionResponse,
    ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice,
    ChatCompletionStreamResponse, ChatMessage, DeltaFunctionCall, DeltaMessage,
    DeltaToolCall, ErrorResponse, FunctionCall, PromptTokenUsageInfo,
    RequestResponseMetadata, ToolCall, UsageInfo)

app = FastAPI()
REQUEST_ID = 0
GLOBAL_ARGS = None

async def generate_fake_response(
        request_id: str,
        model_name: str,
        num_tokens: int,
        tokens_per_sec: float,
    ):
    created_time = int(time.time())
    chunk_object_type: Final = "chat.completion.chunk"

    choice_data = ChatCompletionResponseStreamChoice(
            index = 0,
            delta = DeltaMessage(
                role = "assistant",
                content="",
            ),
            logprobs = None,
            finish_reason = None)
    chunk = ChatCompletionStreamResponse(
            id = request_id,
            object = chunk_object_type,
            created = created_time,
            choices = [choice_data],
            model = model_name)
    data = chunk.model_dump_json(exclude_unset=True)


    for i in range(num_tokens):
        await asyncio.sleep(1/tokens_per_sec)
        text = "Hello "
        choice_data = ChatCompletionResponseStreamChoice(
            index = 0,
            delta = DeltaMessage(content=text),
            logprobs = None,
            finish_reason = None)
        chunk = ChatCompletionStreamResponse(
            id = request_id,
            object = chunk_object_type,
            created = created_time,
            choices = [choice_data],
            model = model_name)
        data = chunk.model_dump_json(exclude_unset=True)
        yield f"data: {data}\n\n"

    choice_data = ChatCompletionResponseStreamChoice(
            index = 0,
            delta = DeltaMessage(
                content="\n",
            ),
            logprobs = None,
            finish_reason = "length")

    chunk = ChatCompletionStreamResponse(
            id = request_id,
            object = chunk_object_type,
            created = created_time,
            choices = [choice_data],
            model = model_name)

    yield f"data: {data}\n\n"
    yield "data: [DONE]\n\n"

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, raw_request: Request):
    global REQUEST_ID
    REQUEST_ID += 1
    request_id = f"fake_request_id_{REQUEST_ID}"
    model_name = "fake_model_name"
    num_tokens = request.max_completion_tokens if request.max_completion_tokens else 100
    tokens_per_sec = GLOBAL_ARGS.speed
    return StreamingResponse(generate_fake_response(request_id, model_name, num_tokens, tokens_per_sec),
                             media_type="text/event-stream")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--max-tokens", type=int, default=100)
    parser.add_argument("--speed", type=int, default=100)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    import uvicorn
    GLOBAL_ARGS = parse_args()
    uvicorn.run(app, host=GLOBAL_ARGS.host, port=GLOBAL_ARGS.port)
