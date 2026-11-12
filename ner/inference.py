from typing import Optional

from gliner import GLiNER


def load_gliner_model(device:Optional) -> GLiNER:
    model = GLiNER.from_pretrained(
        "gliner-community/gliner_small-v2.5"
    )
    model = model.to(device)
    return model


def predict_entities(model:GLiNER,text:str,labels:list,threshold) -> GLiNER:
    entities = model.predict_entities(text, labels, threshold=threshold)
    return entities


def predict_dataset(model, datset, labels,threshold ):

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
