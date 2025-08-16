# LLM Safeguard: Confirm Universal Jailbreak (Mock)

This repository contains a **mock implementation** of the Confirm universal jailbreak described in *Adversarial Attacks on the LLM Safeguard Pipeline* (2025).  
It is designed as a **research and engineering sandbox** to study how structured jailbreaks can pierce layered safeguard defenses.

## Context

Large Language Models (LLMs) are typically protected by **layered safeguards**:  
1. **Input Classifier** – inspects user prompts before model invocation.  
2. **Output Classifier** – inspects generated text before returning it to the user.  

While multi-layered, these defenses can be bypassed by *universal jailbreaks*.  
Phase 3 introduces **Confirm**: a structured, reusable payload that reliably reduces both IC and OC scores, simulating universal bypass potential.

This mock implementation reproduces the **qualitative behavior** of Confirm using symbolic tokens (`CONFIRM`, `SAFE_INFO`, `UNSAFE_INFO`) to ensure safety while preserving research value.

## Pipeline Architecture

```
User Prompt
   ↓
(Optional Confirm Wrapper)
   ↓
Input Classifier (IC) → Block if score ≥ T_Q
   ↓
Target Model (Mock)
   ↓
Output Classifier (OC) → Block if score ≥ T_R
   ↓
Final Output or Refusal
```

- **T_Q** — Query (input) harm score threshold  
- **T_R** — Response (output) harm score threshold  
- **Confirm Wrapper** — structured template plus a universal token (`CONFIRM`) that systematically lowers classifier scores.  

Thresholds are defined in `config.py` and remain configurable for calibration experiments.

## Purpose

- **Reproduce universal jailbreak dynamics** in a safe, controlled setting.  
- **Compare baseline vs. Confirm-wrapped prompts** on harmful queries.  
- **Measure Attack Success Rate (ASR)** and log full pipeline outcomes.  
- Provide an **experimental artifact** for studying universal jailbreaks in safeguard pipelines.  


## Reference

Paper: [*Adversarial Attacks on the LLM Safeguard Pipeline* (2025)](https://arxiv.org/abs/2506.24068)  
Author’s intent: To evaluate the resilience of layered safeguards against **universal jailbreaks** such as Confirm.


**Note:** This implementation is for **educational and research purposes only**.  
It does not contain real model weights, production classifiers, or unsafe jailbreak prompts.
