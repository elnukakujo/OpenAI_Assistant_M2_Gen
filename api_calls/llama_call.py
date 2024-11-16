# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# top-level folder for each specific model found within the models/ directory at
# the top-level of this source tree.

# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed in accordance with the terms of the Llama 3 Community License Agreement.
import os
from llama_models.llama3.api.datatypes import (
    SystemMessage,
    UserMessage,
)
import torch.distributed as dist

from llama_models.llama3.reference_impl.generation import Llama

def initialize_distributed():
    """
    Initialize distributed processing if necessary.
    """
    if not dist.is_initialized():
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

def llama_call(
    system_role: str,
    prompt: str,
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
        if not dist.is_initialized():
            dist.init_process_group(
                backend='nccl',  # or 'gloo' depending on your setup
                init_method='env://',  # Use the environment variable-based init method
                world_size=1,  # Only one process in this case (single node)
                rank=0,  # The rank of the current process
            )
        generator = Llama.build(
            ckpt_dir=os.path.expanduser("~/.llama/checkpoints/Llama3.2-3B-Instruct"),
            max_seq_len=512,
            max_batch_size=4,
            model_parallel_size=1
        )
        print("System role: ",system_role)
        print("User prompt", prompt)
        result = generator.chat_completion(
            messages=[
                SystemMessage(content=system_role),
                UserMessage(content=prompt)
            ],
            temperature=0.6,
            top_p=0.9
        )
        dist.destroy_process_group()
        print("Result: ",result.generation.content)
        return result.generation.content
    except Exception as e:
        print(f"Error during llama_call processing: {e}")
    finally:
        cleanup_distributed()