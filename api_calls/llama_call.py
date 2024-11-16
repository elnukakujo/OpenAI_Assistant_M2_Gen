# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# top-level folder for each specific model found within the models/ directory at
# the top-level of this source tree.

# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed in accordance with the terms of the Llama 3 Community License Agreement.
import os
import json
from llama_models.llama3.api.datatypes import (
    SystemMessage,
    UserMessage
)
import torch.distributed as dist

from llama_models.llama3.reference_impl.generation import Llama

def initialize_distributed():
    """
    Initialize distributed processing if necessary.
    """
    if not dist.is_initialized():
        os.environ['MASTER_ADDR'] = 'localhost'  # Set this to the IP of the master node
        os.environ['MASTER_PORT'] = '29500'      # Use any available port
        dist.init_process_group(
            backend='nccl',  # or 'gloo' depending on your setup
            init_method='env://',  # Use the environment variable-based init method
            world_size=1,  # Only one process in this case (single node)
            rank=0,  # The rank of the current process
        )

def cleanup_distributed():
    """
    Clean up the distributed process group after usage.
    """
    if dist.is_initialized():
        dist.destroy_process_group()

def llama_messages(system_role, prompt):
    messages = [SystemMessage(content=system_role)]
    for shot in prompt["prompt_ex"]:
        messages.append(UserMessage(content=shot[0]))
        messages.append(SystemMessage(content=json.dumps(shot[1])))
    messages.append(UserMessage(content=prompt["user_prompt"]))
    return messages

def llama_call(
    system_role: str,
    prompt,
    llm_name: str
):
    """
    Examples to run with the models finetuned for chat. Prompts correspond of chat
    turns between the user and assistant with the final one always being the user.

    An optional system prompt at the beginning to control how the model should respond
    is also supported.

    `max_gen_len` is optional because finetuned models are able to stop generations naturally.
    """
    
    initialize_distributed()
    try:
        print("Building the Llama generator ...")
        generator = Llama.build(
            ckpt_dir=os.path.expanduser(f"~/.llama/checkpoints/{llm_name}"),
            max_seq_len=2024, # The maximum sequence length supported by the model
            max_batch_size=8,
            model_parallel_size=1
        )
        messages = llama_messages(system_role, prompt)
        result = generator.chat_completion(
            messages=messages,
            temperature=0.6,
            top_p=0.9
        )
        dist.destroy_process_group()
        return result.generation.content
    except Exception as e:
        print(f"Error during llama_call processing: {e}")
    finally:
        cleanup_distributed()