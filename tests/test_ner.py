import json
import unittest
from pathlib import Path

from ner.evaluation import calculate_metrics, evaluate_ner_relaxed, evaluate_ner_strict
from ner.llm import locate_entities
from ner.pdf import extract_pdf_dataset
from ner.utils import load_jsonl, save_responses_to_jsonl

ROOT = Path(__file__).resolve().parent.parent


class MetricsTest(unittest.TestCase):
    def test_calculate_metrics(self):
        m = calculate_metrics(tp=8, fp=2, fn=2)
        self.assertAlmostEqual(m["precision"], 0.8)
        self.assertAlmostEqual(m["recall"], 0.8)
        self.assertAlmostEqual(m["f1"], 0.8)

    def test_zero_division(self):
        self.assertEqual(calculate_metrics(0, 0, 0)["f1"], 0.0)


class UtilsTest(unittest.TestCase):
    def test_jsonl_roundtrip(self):
        path = ROOT / "results" / "_test_roundtrip.jsonl"
        rows = [{"id": "a", "entities": []}, {"id": "b", "entities": [{"x": "é"}]}]
        save_responses_to_jsonl(rows, path)
        try:
            self.assertEqual(load_jsonl(path), rows)
            self.assertEqual(load_jsonl(path, n=1), rows[:1])
        finally:
            path.unlink()


class LlmAnnotationsTest(unittest.TestCase):
    def test_locate_marks_every_occurrence(self):
        text = "Ana vive en Reus. Ana paga 10 €."
        found = locate_entities(text, {"PERSON_NAME": ["Ana"], "AMOUNT": ["10 €"]})
        self.assertEqual([(e["start"], e["label"]) for e in found],
                         [(0, "PERSON_NAME"), (18, "PERSON_NAME"), (27, "AMOUNT")])

    def test_missing_string_raises(self):
        with self.assertRaises(ValueError):
            locate_entities("hola", {"DATE": ["2020-01-01"]})


class PdfTest(unittest.TestCase):
    def test_missing_pdfs_are_skipped(self):
        dataset = [{"id": "test-0001"}, {"id": "does-not-exist"}]
        out = extract_pdf_dataset(dataset, ROOT / "data" / "pdf_clean")
        self.assertEqual([r["id"] for r in out], ["test-0001"])
        self.assertTrue(out[0]["text"].strip())

    def test_scanned_pdf_has_no_text_layer(self):
        out = extract_pdf_dataset([{"id": "test-0001"}], ROOT / "data" / "pdf_scanned", suffix="_scanned")
        self.assertEqual(out[0]["text"].strip(), "")


class EvaluationTest(unittest.TestCase):
    def test_perfect_prediction(self):
        gold = ROOT / "results" / "_gold.jsonl"
        pred = ROOT / "results" / "_pred.jsonl"
        ents = [{"start": 0, "end": 3, "label": "PERSON_NAME", "text": "Ana"}]
        rows = [{"id": "d1", "text": "Ana vive", "entities": ents}]
        save_responses_to_jsonl(rows, gold)
        save_responses_to_jsonl(rows, pred)
        try:
            self.assertEqual(evaluate_ner_strict(gold, pred, print_results=False)["micro"]["f1"], 1.0)
            relaxed = evaluate_ner_relaxed(gold, pred, print_results=False)
            self.assertEqual(relaxed["unique"]["micro"]["f1"], 1.0)
        finally:
            gold.unlink()
            pred.unlink()


if __name__ == "__main__":
    unittest.main()
