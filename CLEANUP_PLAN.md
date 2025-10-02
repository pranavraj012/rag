# 🗑️ Repository Cleanup Plan

## Files to REMOVE (Unnecessary after Phi-2 upgrade)

### Root Directory - Remove:
1. ❌ `MODEL_GUIDE.md` - Multi-model comparison (we only use Phi-2 now)
2. ❌ `UPGRADE_SUMMARY.md` - Historical upgrade info (no longer relevant)
3. ❌ `QUICK_START.md` - Multi-model selection guide (obsolete)
4. ❌ `compare_models.py` - Compares multiple models (not needed)
5. ❌ `.env.rtx4060` - Alternative config (not needed, we use .env)
6. ❌ `check_content.py` - Debug script (one-time use)
7. ❌ `inspect_vector_store.py` - Debug script (one-time use)
8. ❌ `list_collections.py` - Debug script (one-time use)
9. ❌ `test_improved_response.py` - Old test (superseded)
10. ❌ `test_specific_fix.py` - Old test (superseded)

### tests/ Directory - Remove:
11. ❌ `tests/test_flan.py` - Tests old Flan-T5 model (never used)
12. ❌ `tests/test_complete.py` - Tests old answer generation (obsolete)
13. ❌ `tests/test_ship.py` - Old ship repair test (obsolete)
14. ❌ `tests/test_interactive.py` - Broken/needs fixes (not maintained)
15. ❌ `tests/quick_test.py` - Broken/needs fixes (not maintained)
16. ❌ `tests/gpu_test.py` - Basic GPU check (covered by app startup)
17. ❌ `tests/test_search.py` - Basic search test (covered by main tests)
18. ❌ `tests/utils.py` - Unused utilities (no references)

---

## Files to KEEP (Essential)

### Core Application:
✅ `app.py` - Main Streamlit application
✅ `query_engine.py` - Phi-2 query engine
✅ `vector_store.py` - ChromaDB vector store
✅ `document_processor.py` - Document processing
✅ `.env` - Configuration
✅ `.gitignore` - Git configuration
✅ `requirements.txt` - Dependencies

### Documentation:
✅ `README.md` - Main documentation (needs update)
✅ `FIX_SUMMARY.md` - Recent fix documentation (useful reference)

### Tests (Keep essential ones):
✅ `tests/test_advanced.py` - Comprehensive test of all features
✅ `tests/final_test.py` - Working test for basic functionality
✅ `tests/test_app.py` - Streamlit app testing
✅ `tests/README.md` - Test documentation
✅ `test_phi2.py` - Quick Phi-2 verification test (root level)

### Project Files:
✅ `documents/` - Your SOP documents
✅ `chroma_db/` - Vector database
✅ `venv/` - Virtual environment
✅ `__pycache__/` - Python cache (auto-generated)
✅ `.git/` - Git repository

---

## Summary

**Remove:** 18 files (old tests, debug scripts, multi-model docs)
**Keep:** 13 essential files + directories

**Space saved:** ~50-100KB (documentation) + cleaner repo

---

## Recommended Clean Repo Structure

```
sop_project/
├── app.py                      # Main application
├── query_engine.py             # Phi-2 engine
├── vector_store.py             # Vector database
├── document_processor.py       # Document processing
├── .env                        # Configuration
├── .gitignore                  # Git config
├── requirements.txt            # Dependencies
├── README.md                   # Main docs
├── FIX_SUMMARY.md              # Recent fixes
├── test_phi2.py                # Quick test
├── tests/
│   ├── test_advanced.py        # Full feature test
│   ├── final_test.py           # Basic test
│   ├── test_app.py             # App test
│   └── README.md               # Test docs
├── documents/                  # Your SOPs
├── chroma_db/                  # Vector DB
└── venv/                       # Virtual env
```

---

## Action Items

1. **Remove unnecessary files** (18 files)
2. **Update README.md** - Remove multi-model references, simplify to Phi-2 only
3. **Update tests/README.md** - Remove references to removed tests
4. **Git commit** - "Clean up repository: Remove obsolete files and documentation"
