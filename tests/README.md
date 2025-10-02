# Test Files

This folder contains test scripts for the SOP Knowledge Assistant.

## Essential Tests

### `test_advanced.py`
Comprehensive test of all features:
- Q&A mode
- Step-by-step instructions
- Multiple query types
- Confidence scoring

**Run:** `python tests/test_advanced.py`

### `final_test.py`
Basic functionality test:
- Document loading
- Vector search
- Answer generation
- Quick verification

**Run:** `python tests/final_test.py`

### `test_app.py`
Streamlit app component testing:
- Document processing
- Vector store operations
- Query engine functionality

**Run:** `python tests/test_app.py`

## Quick Test (Root Level)

### `../test_phi2.py`
Quick Phi-2 verification:
- Model loading check
- Simple query test
- Performance check

**Run:** `python test_phi2.py`

---

## Usage

### Run All Tests
```bash
# Quick test
python test_phi2.py

# Comprehensive
python tests/test_advanced.py

# Basic
python tests/final_test.py
```

### Before Committing
Always run tests to verify changes:
```bash
python test_phi2.py && python tests/test_advanced.py
```

---

**Note:** The main application runs via `streamlit run app.py` from the root directory.