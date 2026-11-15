from typing import Optional

from gliner import GLiNER


def load_gliner_model(
    device: Optional[str] = None,
    model_name: str = "gliner-community/gliner_small-v2.5",
) -> GLiNER:
    if device is None:
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
    model = GLiNER.from_pretrained(model_name)
    model = model.to(device)
    return model


def predict_entities(model: GLiNER, text: str, labels: list, threshold: float = 0.5) -> list:
    if not text.strip():  # scanned pdf, no text
        return []
    entities = model.predict_entities(text, labels, threshold=threshold)
    return entities


def predict_dataset(model, datset, labels, threshold=0.5):

    results = []

    for record in datset:
        text = record["text"]
        entities = predict_entities(model,text,labels,threshold)

        results.append({
            "id": record["id"],
            "entities": entities
        }
        )
    return results
