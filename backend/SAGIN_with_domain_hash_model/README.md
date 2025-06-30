---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:501
- loss:HybridLoss
widget:
- source_sentence: 空基网络地基层包括哪些网络？
  sentences:
  - 地面蜂窝网络、光纤网络等，支持高密度用户接入与数据处理。
  - 空基网络独立架构通常聚焦单层优化，如无人机自组网或激光通信链路设计;一体化组网架构需解决多层协议兼容、动态资源调度及安全认证等问题。
  - 国内典型的卫星激光通信技术验证计划有：2011年"海洋二号"卫星成功入轨，实现2000km星地通信距离，最高通信速率可达504Mbps;2016年"墨子号"量子卫星成功发射，实现了512Gbps的通信速率;2016年"天宫二号"与新疆南山地面站成功实现激光通信实验，数据下行速率为16Gbps;2017年"实践十三号"卫星发射成功，实现全球第一次同步轨道卫星与地面的双向高速激光通信，最高速率可达5Gbps;2019年"实践二十号"卫星发射成功，2020年与丽江地面站成功建立基于QPSK调制体制的激光通信链路，下行传输速率最高10Gbps;"行云"系列卫星于2020年发射成功，进行低轨卫星星间激光链路技术试验，通信距离大于3000km，通信速率可达100Mbps。
- source_sentence: 空天地一体化网络6G的感知定位精度指标是多少？
  sentences:
  - 在空天地一体化通信系统中，AI技术用于解决复杂的异构通信系统问题，提供感知、学习、推理、预测和决策等核心能力，提升网络的智能化水平。
  - 6G的AI服务精度效率要求超过90，满足高实时性和高精度智能服务需求。
  - 6G的感知定位精度目标为厘米级，支持高精度导航和环境重构。
- source_sentence: 空天地一体化网络空天地一体化网络在内容分发中的作用是什么？
  sentences:
  - 星地信道环境差异巨大主要体现在传输时延、多普勒频偏和信道多径等方面。卫星通信以视距传输为主，而地面蜂窝网络因障碍物较多，信道容易遭遇快衰落。这些差异对信号的时频同步、链路稳定性和数据传输可靠性提出了严峻的挑战，需要通过技术优化来提升通信质量。
  - 空天地一体化网络通过天基和地基网络的协同，优化内容分发路径，支持基于内容缓存的应用程序传递内容，提升内容分发的效率和用户体验。
  - 6G网络中的分布式自治网络（DAN）具有分布式、自治、自包含的特征，支持按需定制、即插即用、灵活部署，能够实现网络的智能自治和高效协同。
- source_sentence: 地基网络跨层协同在边缘计算中的作用是什么？
  sentences:
  - 天地一体融合网络的技术挑战包括网络拓扑高速动态变化、星地信道环境差异巨大、星地一体组网复杂度高、星上网元平台能力受限以及通感算异构网融合困难。这些难点对网络的稳健性、资源管理和业务连续性提出了更高的要求，需要通过技术创新和协同优化来解决。
  - 与空基（无人机、高空平台）和天基（卫星）网络节点协作，实现任务分流与数据融合，例如将高计算量任务分流至卫星边缘服务器，同时处理本地实时任务。
  - 边缘计算节点的架构设计包括硬件层、虚拟化层和控制层。
- source_sentence: 地基网络如何保障物联网的安全与可靠性？
  sentences:
  - 通过分层加密机制和冗余设计保障物联网的安全与可靠性。
  - 针对感知层设备资源受限的特点，采用轻量级加密算法（如ECC）。
  - 天星地网是指天基（卫星）、星间（如低轨卫星星座）与地面网络的协同组网，通过卫星互联网与地面5G6G网络的深度融合，实现覆盖扩展和资源互补。
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer

This is a [sentence-transformers](https://www.SBERT.net) model trained. It maps sentences & paragraphs to a 384-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, text classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
<!-- - **Base model:** [Unknown](https://huggingface.co/unknown) -->
- **Maximum Sequence Length:** 128 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/UKPLab/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'max_seq_length': 128, 'do_lower_case': False}) with Transformer model: BertModel 
  (1): Pooling({'word_embedding_dimension': 384, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, 'include_prompt': True})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    '地基网络如何保障物联网的安全与可靠性？',
    '通过分层加密机制和冗余设计保障物联网的安全与可靠性。',
    '针对感知层设备资源受限的特点，采用轻量级加密算法（如ECC）。',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities.shape)
# [3, 3]
```

<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 501 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>sentence_2</code>
* Approximate statistics based on the first 501 samples:
  |         | sentence_0                                                                         | sentence_1                                                                          | sentence_2                                                                          |
  |:--------|:-----------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|
  | type    | string                                                                             | string                                                                              | string                                                                              |
  | details | <ul><li>min: 10 tokens</li><li>mean: 18.01 tokens</li><li>max: 51 tokens</li></ul> | <ul><li>min: 10 tokens</li><li>mean: 51.43 tokens</li><li>max: 128 tokens</li></ul> | <ul><li>min: 10 tokens</li><li>mean: 51.43 tokens</li><li>max: 128 tokens</li></ul> |
* Samples:
  | sentence_0                         | sentence_1                                                                                    | sentence_2                                                                                                       |
  |:-----------------------------------|:----------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
  | <code>空天地一体化网络6G的成本控制目标是什么？</code> | <code>6G的成本控制目标是将网络建设和运营维护支出控制在合理水平，平衡性能与经济性。</code>                                          | <code>天基网络通过天上的卫星节点之间的星间链路互联，构建覆盖全球的信息服务网络。该网络形态不依赖地面网络，通过卫星节点的协同工作，实现全球无缝覆盖，例如美国军方的先进极高频（AEHF）卫星通信系统。</code>    |
  | <code>地基网络地基网络的关键组成部分有哪些？</code>   | <code>地基网络的关键组成部分包括地面基站（TerrestrialBaseStationsBSs）、光纤网络、数据中心与边缘计算节点、用户终端设备、SDN控制器与网关。</code> | <code>地基网络的技术架构通常采用分层设计，结合云雾边缘计算模型，包括云层（集中式数据中心）、雾层（分布式边缘节点）和地面层（物理基础设施）。在SDNenabled架构中，地基网络还承担控制平面的核心角色。</code> |
  | <code>天基网络卫星通信系统的意义是什么？</code>     | <code>卫星通信系统的意义在于实现全球无缝通信，支持应急通信、远程教育、医疗、军事指挥等关键应用，同时促进全球化信息共享和经济发展。</code>                   | <code>卫星通信系统主要由三部分组成：空间段（卫星）、地面段（地面站）和用户段（终端设备）。空间段负责信号转发，地面段负责信号处理和网络管理，用户段负责信号的接收和发送。</code>                   |
* Loss: <code>__main__.HybridLoss</code>

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `num_train_epochs`: 5
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `overwrite_output_dir`: False
- `do_predict`: False
- `eval_strategy`: no
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `per_gpu_train_batch_size`: None
- `per_gpu_eval_batch_size`: None
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1
- `num_train_epochs`: 5
- `max_steps`: -1
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: {}
- `warmup_ratio`: 0.0
- `warmup_steps`: 0
- `log_level`: passive
- `log_level_replica`: warning
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `save_safetensors`: True
- `save_on_each_node`: False
- `save_only_model`: False
- `restore_callback_states_from_checkpoint`: False
- `no_cuda`: False
- `use_cpu`: False
- `use_mps_device`: False
- `seed`: 42
- `data_seed`: None
- `jit_mode_eval`: False
- `use_ipex`: False
- `bf16`: False
- `fp16`: False
- `fp16_opt_level`: O1
- `half_precision_backend`: auto
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `local_rank`: 0
- `ddp_backend`: None
- `tpu_num_cores`: None
- `tpu_metrics_debug`: False
- `debug`: []
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_prefetch_factor`: None
- `past_index`: -1
- `disable_tqdm`: False
- `remove_unused_columns`: True
- `label_names`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `fsdp`: []
- `fsdp_min_num_params`: 0
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `fsdp_transformer_layer_cls_to_wrap`: None
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `deepspeed`: None
- `label_smoothing_factor`: 0.0
- `optim`: adamw_torch
- `optim_args`: None
- `adafactor`: False
- `group_by_length`: False
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `skip_memory_metrics`: True
- `use_legacy_prediction_loop`: False
- `push_to_hub`: False
- `resume_from_checkpoint`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_private_repo`: None
- `hub_always_push`: False
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `include_inputs_for_metrics`: False
- `include_for_metrics`: []
- `eval_do_concat_batches`: True
- `fp16_backend`: auto
- `push_to_hub_model_id`: None
- `push_to_hub_organization`: None
- `mp_parameters`: 
- `auto_find_batch_size`: False
- `full_determinism`: False
- `torchdynamo`: None
- `ray_scope`: last
- `ddp_timeout`: 1800
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `dispatch_batches`: None
- `split_batches`: None
- `include_tokens_per_second`: False
- `include_num_input_tokens_seen`: False
- `neftune_noise_alpha`: None
- `optim_target_modules`: None
- `batch_eval_metrics`: False
- `eval_on_start`: False
- `use_liger_kernel`: False
- `eval_use_gather_object`: False
- `average_tokens_across_devices`: False
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin

</details>

### Framework Versions
- Python: 3.10.16
- Sentence Transformers: 3.4.1
- Transformers: 4.49.0
- PyTorch: 2.1.1+cu118
- Accelerate: 1.4.0
- Datasets: 3.3.1
- Tokenizers: 0.21.0

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->