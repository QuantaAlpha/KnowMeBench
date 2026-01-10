<img width="1169" height="662" alt="image" src="images/difference5.png" />


# KnowMe-Bench: Benchmarking Person Understanding for Lifelong Digital Companions

[![arXiv](https://img.shields.io/badge/arXiv-2601.04745-B31B1B.svg?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2601.04745)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**KnowMe-Bench** is a benchmark designed to evaluate **person understanding** in lifelong digital companions. Unlike existing benchmarks that rely on sparse dialogue logs, KnowMe-Bench is built from long-form autobiographical narratives (4.7M tokens), preserving the "micro-texture" of human experience—actions, inner thoughts, and environmental context.

This repository contains the dataset, the multi-agent generation pipeline, and the evaluation scripts described in our paper.

## 🌟 Key Features

* **Autobiographical Narrative Substrate**: Built from diverse literary sources (including Knausgård's *My Struggle*), retaining high-density internal monologues and situational details often lost in chat-based datasets.
* **Cognitive-Stream Construction**: Reconstructs narratives into time-anchored streams with 5 distinct fields: Visual, Auditory, Context, Background, and Inner Monologue.
* **Mnestic Realignment**: Specifically handles non-linear temporal structures (flashbacks) to prevent "Update Paradox" errors in memory systems.
* **Hierarchical Evaluation**: A 3-tier evaluation suite covering 7 tasks, from factual recall to psychoanalytic reasoning.

## 📂 Repository Structure

## 📊 Dataset Statistics

The benchmark consists of **2,580 evaluation queries** derived from **4.7M tokens** of source text.

| Dataset | Source | Characteristics | Key Challenge |
| --- | --- | --- | --- |
| **D1** | *My Struggle* | Flashback-Intensive | Handling non-linear time & mnestic triggers 
| **D2** | *Neapolitan Novels* | Event-Driven | Tracking linear causal chains & entity updates 
| **D3** | *In Search of Lost Time* | Psychological Depth | Interpreting abstract internal monologues 

## 🧠 Evaluation Tasks

KnowMe-Bench evaluates models across three cognitive levels:

### Level I: Precision & Factuality (The "Memory" Layer)
**T1: Context-Aware Extraction**: Entity recall under spatiotemporal constraints.

**T2: Adversarial Abstention**: Testing resistance to "Mismatching Trap" hallucinations.

**T3: Temporal Reasoning**: Duration calculation and timeline reconstruction.



### Level II: Narrative Logic & Causality (The "Reasoning" Layer)


**T4: Logical Event Ordering**: Ordering based on semantic dimensions (e.g., danger escalation).



**T5: Mnestic Trigger Analysis**: Identifying sensory cues that trigger memories.



### Level III: Psychoanalytic Depth (The "Insight" Layer)


**T6: Mind-Body Interaction**: Explaining ironic/contradictory behaviors.


  
**T7: Expert-Annotated Psychoanalysis**: Deep reasoning about motivations and identity.



## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/QuantaAlpha/KnowMeBench.git
cd KnowMeBench
pip install -r requirements.txt

```

## 🏆 Baselines & Results

We evaluated several systems including Naive RAG, Mem0, and MemOS. Our findings show that while retrieval systems improve factual accuracy, they struggle with temporal logic and deep insight.

| Model | System | T1 (Detail) | T3 (Time) | T6 (Insight) |
| --- | --- | --- | --- | --- |
| **Qwen3-32B** | Base | 59.9 | 44.4 | 14.3 |
|  | + MemOS | **70.6** | **52.7** | **18.2** |
| **GPT-5-mini** | Base | 65.4 | 54.1 | 18.6 |
|  | + MemOS | **76.1** | **63.1** | **22.5** |


<div align="center">
<img src="images/result_table1.png" alt="Experimental Results Table 1" width="800"/>
</div>

<br/>

<div align="center">
<img src="images/result_table2.png" alt="Experimental Results Table 2" width="800"/>
</div>

See the paper for full results.

## 🛡️ Privacy & Ethics

All data in this benchmark has undergone a rigorous **Context-Aware De-identification Pipeline**. Key entities were mapped to pseudonyms (e.g., "Elena" → "Subject_A") and geolocation markers were coarsened to ensure privacy.

## 🖊️ Citation

If you use KnowMe-Bench in your research, please cite our paper:

```bibtex
@article{wu2026knowme,
  title={KnowMe-Bench: Benchmarking Person Understanding for Lifelong Digital Companions},
  author={Wu, Tingyu and Chen, Zhisheng and Weng, Ziyan and Wang, Shuhe and Li, Chenglong and Zhang, Shuo and Hu, Sen and Wu, Silin and Lan, Qizhen and Wang, Huacan and Chen, Ronghao},
  journal={arXiv preprint},
  year={2026}
}

```

## ✉️ Contact

For questions, please contact:

* Qizhen Lan: `Qizhen.Lan@uth.tmc.edu`
* Ronghao Chen: `chenronghao@alumni.pku.edu.cn`
* Huacan Wang: `wanghuacan17@mails.ucas.ac.cn`

```
