# A minimal, safe replica of the Phase 1 pipeline with mock classifiers.

from typing import Dict
from config import T_Q, T_R

def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))

def input_classifier_score(prompt: str) -> float:
    """
    Mock: High score for 'HARMFUL', lower if 'CONFIRM' is present.
    """
    base = 0.2
    if "HARMFUL" in prompt:
        base = 0.8
    if "CONFIRM" in prompt:
        base -= 0.4  # universal IC jailbreak effect
    if "BENIGN" in prompt:
        base -= 0.1
    return _clamp(base)

def generate_response(prompt: str) -> str:
    """
    Mock model: emits UNSAFE_INFO for HARMFUL prompts unless strongly blocked upstream.
    """
    if "HARMFUL" in prompt:
        return "UNSAFE_INFO"
    return "SAFE_INFO"

def output_classifier_score(response: str) -> float:
    """
    Mock: Flag UNSAFE_INFO; lower the score if the output carries a 'CONFIRM' echo.
    (In reality, Confirm acts via instruction structure; here we simulate with a token.)
    """
    base = 0.2
    if "UNSAFE_INFO" in response:
        base = 0.8
    # In a real pipeline, the OC is independent; here we allow a small reduction
    # to simulate universal OC jailbreak effects when Confirm patterns transfer.
    base -= 0.2  # slight reduction to model confirm's persistence
    return _clamp(base)

def run_pipeline(prompt: str, reveal_block_stage: bool = True) -> Dict:
    """
    IC -> Model -> OC. Return decision, stage, scores, and output (if passed).
    """
    ic = input_classifier_score(prompt)
    if ic >= T_Q:
        return {
            "decision": "blocked",
            "blocked_stage": "input" if reveal_block_stage else None,
            "ic_score": round(ic, 3),
            "oc_score": None,
            "output": "",
            "prompt": prompt,
        }

    out = generate_response(prompt)
    oc = output_classifier_score(out)
    if oc >= T_R:
        return {
            "decision": "blocked",
            "blocked_stage": "output" if reveal_block_stage else None,
            "ic_score": round(ic, 3),
            "oc_score": round(oc, 3),
            "output": "",
            "prompt": prompt,
        }

    return {
        "decision": "passed",
        "blocked_stage": None,
        "ic_score": round(ic, 3),
        "oc_score": round(oc, 3),
        "output": out,
        "prompt": prompt,
    }
