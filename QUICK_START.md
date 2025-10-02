# 🎯 Quick Model Selection Guide

## Choose Your Model in 30 Seconds

### I want the BEST quality answers → **Phi-2**
```bash
LLM_MODEL=microsoft/phi-2
```
- 2.7B params, ~2.5GB VRAM
- Best for: Production use
- Perfect for GTX 1650 4GB ✅

---

### I want the FASTEST responses → **TinyLlama**
```bash
LLM_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
```
- 1.1B params, ~1.2GB VRAM
- Best for: Speed + quality balance
- Great for multitasking

---

### I want BALANCED performance → **StableLM-2**
```bash
LLM_MODEL=stabilityai/stablelm-2-1_6b
```
- 1.6B params, ~1.8GB VRAM
- Best for: Middle ground
- Solid all-rounder

---

### I have LOW memory / OLD hardware → **DialoGPT**
```bash
LLM_MODEL=microsoft/DialoGPT-medium
```
- 0.35B params, ~0.4GB VRAM
- Best for: Limited resources
- CPU fallback option

---

## 📊 At a Glance

| Model | Size | VRAM | Quality | Speed | GTX 1650? |
|-------|------|------|---------|-------|-----------|
| **Phi-2** | 2.7B | 2.5GB | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ | ✅ Perfect |
| **TinyLlama** | 1.1B | 1.2GB | ⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ | ✅ Great |
| **StableLM-2** | 1.6B | 1.8GB | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ | ✅ Good |
| **DialoGPT** | 0.35B | 0.4GB | ⭐⭐⭐ | ⚡⚡⚡⚡⚡ | ✅ OK |

---

## 🔄 How to Change

1. Open `.env` file
2. Find the line: `LLM_MODEL=...`
3. Change to your choice
4. Save and restart: `streamlit run app.py`

---

## 🎯 Recommendation for GTX 1650 4GB

**START WITH:** `microsoft/phi-2`

Why? Best quality, perfect fit for 4GB VRAM.

**IF TOO SLOW, SWITCH TO:** `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

Why? Faster, still excellent quality, more memory headroom.

---

## 📈 Quality Comparison

**Same question asked to different models:**

### DialoGPT (OLD):
> "Defect list prepared by crew. Deck by Master, engine by driver..." 
> *~50 words, incomplete*

### TinyLlama:
> "For annual repair, prepare defect list: 1) Crew prepares initial list 2) Master handles deck side covering equipment, wheelhouse 3) Driver handles engine side covering machinery, pump room 4) T.A/A.D verifies and sends to surveyor..." 
> *~100 words, good detail*

### Phi-2 (NEW):
> "For conducting an annual repair of a vessel, a comprehensive defect/flaws list must be prepared through the following systematic process: 1. Initial Preparation: The vessel's crew initiates defect list preparation. Two separate lists are created. 2. Deck Side Defect List: Prepared by the Master covering all deck machineries, equipment, wheelhouse, and superstructure for ensuring good working condition. 3. Engine Side Defect List: Compiled by the Chief Engineer covering all engine room machinery, pump room, compressor compartment, and cooler compartment. 4. Verification: Lists examined by T.A/A.D onboard, sent to surveyor for professional assessment, main repairs identified and prioritized." 
> *~180 words, comprehensive*

---

## 🚀 Quick Test

Want to see the difference? Run:
```bash
python compare_models.py
```

This tests all models with your actual documents!

---

**Default:** Phi-2 is already configured in `.env` ✅
**Just run:** `streamlit run app.py` and enjoy better answers! 🎉
