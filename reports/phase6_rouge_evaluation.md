# Phase 6 — ROUGE Evaluation Report

## 1. Project Overview

This evaluation measures the performance of the bilingual AI Text Summarization API.

Two transformer models are evaluated:

- English: `sshleifer/distilbart-cnn-12-6`
- French: `xavierbarbier/t5-small-mlsum-fr`

The evaluation uses 10 test documents: 5 English and 5 French.

## 2. Evaluation Methodology

The ROUGE evaluation library is used to compare generated summaries against reference summaries.

Metrics:
- ROUGE-1: Measures unigram overlap.
- ROUGE-2: Measures bigram overlap.
- ROUGE-L: Measures the longest common subsequence.

The F1 score is used for comparison.

Configuration:
- 5 test documents per language.
- 1 reference summary per document.
- Maximum generation length: 100 tokens.
- Minimum generation length: 30 tokens.
- Stemmer: Disabled (`use_stemmer=False`).

## 3. English Evaluation Results

| Test | Topic | ROUGE-1 | ROUGE-2 | ROUGE-L |
|---|---|---:|---:|---:|
| 1 | Healthcare | 0.7347 | 0.5532 | 0.7347 |
| 2 | Education | 0.5818 | 0.3019 | 0.5091 |
| 3 | Technology | 0.4412 | 0.1515 | 0.3824 |
| 4 | Environment | 0.4483 | 0.2500 | 0.4483 |
| 5 | Business | 0.4528 | 0.1176 | 0.3396 |
| **Average** | | **0.5318** | **0.2748** | **0.4828** |

## 4. French Evaluation Results

| Test | Topic | ROUGE-1 | ROUGE-2 | ROUGE-L |
|---|---|---:|---:|---:|
| 6 | Santé | 0.5185 | 0.2692 | 0.4444 |
| 7 | Éducation | 0.3182 | 0.0952 | 0.2273 |
| 8 | Technologie | 0.4898 | 0.2979 | 0.4490 |
| 9 | Environnement | 0.4000 | 0.1509 | 0.2909 |
| 10 | Commerce | 0.3103 | 0.1071 | 0.2414 |
| **Average** | | **0.4074** | **0.1841** | **0.3306** |

## 5. Comparison

| Metric | English | French |
|---|---:|---:|
| ROUGE-1 | 0.5318 | 0.4074 |
| ROUGE-2 | 0.2748 | 0.1841 |
| ROUGE-L | 0.4828 | 0.3306 |

The English model achieved higher average ROUGE scores across all three metrics in this evaluation.

This indicates greater lexical overlap with the reference summaries in the current test dataset. It does not necessarily mean that every English summary is more informative or semantically accurate.

## 6. Generation Configuration Investigation

Additional experiments were conducted with the French model:

- Increasing the minimum generated length produced longer summaries.
- Reducing the length penalty did not change the tested output.
- Disabling early stopping did not change the tested output.

The longer summary still omitted important information about data protection, security, and medical responsibility.

Therefore, the original generation configuration was retained. Increasing output length alone did not resolve the content-coverage limitation.

## 7. Limitations

The results should be interpreted with caution because:

1. The evaluation dataset contains only 10 documents.
2. Each document has only one reference summary.
3. ROUGE measures lexical overlap and does not fully measure meaning, factual accuracy, or readability.
4. The French model sometimes omits important information from the source text.
5. Results may vary with different documents and reference summaries.

A larger and more diverse evaluation dataset would provide a more reliable assessment.

## 8. Conclusion

Both models successfully generated summaries in their respective languages.

The English model achieved higher average ROUGE scores than the French model on the current dataset. The French model produced readable summaries but showed some limitations in preserving all important information.

The evaluation confirms that the API supports bilingual summarization, while highlighting opportunities to improve French summary coverage and overall evaluation reliability.

**Phase 6 status: Completed.**
