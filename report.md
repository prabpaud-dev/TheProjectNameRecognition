# NER Project - Report

## Group members
- Prabin Paudel (individual work).
- AI assistance: Claude Code was used to help debug the code, write the tests and draft this report, and as the LLM chat for Task 4.

## System and configuration
- **Pipeline:** input (JSONL text, or PDF -> PyMuPDF text) -> GLiNER `predict_entities` -> predictions JSONL -> strict and relaxed evaluation (`ner/evaluation.py`).
- **GLiNER model:** small, `gliner-community/gliner_small-v2.5`, threshold 0.5, the 7 entity labels used as plain label names.
- **Label descriptions:** not used.
- **PDF extraction:** PyMuPDF (`page.get_text()`), no OCR.
- **Other:** Python 3.12, uv, `gliner`, `pymupdf`, Jupyter notebooks. **TODO: add hardware (CPU/GPU).**
- **LLM experiment (no API):** an LLM chat read the document text and listed the entities per label; offsets were computed afterwards by script (`ner/llm.py`), marking every occurrence of each listed string.

## Results summary

| Input | Model | Label descriptions | Extraction | Evaluation | Docs | P | R | F1 |
|---|---|---|---|---|---|---|---|---|
| Plain text | GLiNER small | No | - | Strict | 50 | 0.76 | 0.86 | 0.81 |
| Plain text | GLiNER small | No | - | Relaxed occurrences | 50 | 0.76 | 0.86 | 0.81 |
| Plain text | GLiNER small | No | - | Relaxed unique | 50 | 0.77 | 0.88 | 0.82 |
| Clean PDF | GLiNER small | No | PyMuPDF | Strict | 50 | 0.52 | 0.59 | 0.56 |
| Clean PDF | GLiNER small | No | PyMuPDF | Relaxed occurrences | 50 | 0.76 | 0.86 | 0.81 |
| Clean PDF | GLiNER small | No | PyMuPDF | Relaxed unique | 50 | 0.77 | 0.88 | 0.82 |
| Scanned PDF | GLiNER small | No | PyMuPDF | Strict / Relaxed occ. / Relaxed unique | 10 | 0.00 | 0.00 | 0.00 |
| Plain text | LLM chat | - | - | Strict / Relaxed occ. / Relaxed unique | 10 | 1.00 | 1.00 | 1.00 |

Note: the scanned-PDF and LLM rows cover only the first 10 documents (only 10 scanned PDFs were provided; the LLM was run by hand on 10 texts), so they are not directly comparable with the 50-document rows.

Per entity type for GLiNER on clean PDFs (relaxed occurrences F1): PERSON_NAME 1.00, DATE 1.00, REGISTRATION_NUMBER 0.97, ID_CARD_NUMBER 0.96, AMOUNT 0.94, ORGANIZATION 0.77, ADDRESS 0.00. Plain text gives the same figures.

## Difficulties and decisions
- **Only 10 scanned PDFs for 50 records.** The first notebook run crashed on `test-0011_scanned.pdf`. `extract_pdf_dataset` now skips records with no PDF, and the evaluator compares the first N gold documents against the N predictions.
- **Scanned PDFs have no text layer.** They are single images, so PyMuPDF returns an empty string and GLiNER predicts nothing (0.00). Tesseract is not installed, so OCR was not tried.
- **`load_gliner_model()` required a `device` argument.** It now defaults to GPU if available, otherwise CPU.
- **Stale notebook kernel.** After editing `ner/pdf.py` the kernel kept the old module; restarting the kernel (or `%autoreload`) fixes it.
- **Strict vs relaxed on PDFs.** Strict F1 drops from 0.81 (plain) to 0.56 (clean PDF) while relaxed is identical. The entities are found but the character offsets differ from the gold ones, because PDF text extraction changes the text (line breaks), so spans no longer line up.
- **LLM run is small and partly exposed.** The LLM saw only the text, except that the gold entities of document 1 had been shown to it earlier in the session, so document 1 is not a blind test. Its perfect score also reflects how regular the template-generated documents are; with 10 documents it should not be read as a general result.

## Conclusions
- On plain text GLiNER small reaches about 0.81 F1. Text from clean PDFs gives the same relaxed result, so PyMuPDF extraction is lossless for text-based PDFs. Only strict scoring suffers, through offset changes.
- Scanned PDFs need OCR; without it the pipeline returns nothing.
- Hardest entity types: ADDRESS is by far the worst (about 1 true positive against 415 false positives on 50 documents; the cause was not investigated, so it is open whether a label description or different label wording would help). ORGANIZATION is next (F1 about 0.77). Names, dates, ID and registration numbers and amounts are easy because they follow strong patterns.
- The LLM matched every gold entity on the 10 documents it was run on, but it needed manual work per document, whereas GLiNER ran on all 50 automatically.
