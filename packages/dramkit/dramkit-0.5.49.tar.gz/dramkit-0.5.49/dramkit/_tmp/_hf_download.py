# -*- coding: utf-8 -*-

# https://blog.csdn.net/ljp1919/article/details/131925099

from huggingface_hub import snapshot_download


hf_token = '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'


if __name__ == '__main__':

    # 模型在HuggingFace上的名称
    repo_id = 'meta-llama/Llama-2-7b-chat-hf'
    # 本地模型存储的地址
    local_dir = 'D:/Genlovy_Hoo/HooProjects/llm/llama/Llama-2-7b-chat-hf'
    # 本地模型使用文件保存，而非blob形式保存？
    local_dir_use_symlinks = False
    
    # 代理
    proxies = {
        'http': 'xxxx',
        'https': 'xxxx',
    }
    proxies = None
    
    snapshot_download(
        repo_id=repo_id,
        local_dir=local_dir,
        local_dir_use_symlinks=local_dir_use_symlinks,
        token=hf_token,
        proxies=proxies
    )
    
    
    
    
    
    
