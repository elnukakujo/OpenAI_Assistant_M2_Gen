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
    UserMessage,
    CompletionMessage,
    StopReason
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

def llama_dialogs(system_role, prompt):
    dialogs = []
    for shot in prompt["prompt_ex"]:
        # Create the n_prompt examples with dialogs
        dialogs.append(SystemMessage(content=system_role))
        dialogs.append(UserMessage(content=shot[0]))
        dialogs.append(CompletionMessage(content=json.dumps(shot[1]), stop_reason=StopReason.end_of_turn))    
    # Create the real task prompt
    dialogs.append(SystemMessage(content=system_role))
    dialogs.append(UserMessage(content=prompt["user_prompt"]))
    return dialogs

def llama_call(
    system_role: str,
    prompt,
    llm_name: str,
    max_seq_len: int = 3000, # The maximum sequence length supported by the model
    max_batch_size: int = 12, # The maximum batch size supported by the model
    temperature:float =0.6,
    top_p:float =0.9
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
            max_seq_len=max_seq_len,
            max_batch_size=max_batch_size
        )
        dialogs = llama_dialogs(system_role, prompt)
        result = generator.chat_completion(
            messages=dialogs,
            temperature=temperature,
            top_p=top_p
        )
        dist.destroy_process_group()
        print(result.generation.content)
        return result.generation.content
    except Exception as e:
        print(f"Error during llama_call processing: {e}")
    finally:
        cleanup_distributed()