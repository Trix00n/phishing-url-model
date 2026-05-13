import os, json, joblib

def model_fn(model_dir):
    """Ładowanie modelu i wektoryzatora z zapisanego archiwum"""
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    vectorizer = joblib.load(os.path.join(model_dir, "vectorizer.joblib"))
    return (model, vectorizer)

def input_fn(request_body, request_content_type):
    """Obsługa formatu JSON: {"texts": ["url1", "url2"]}"""
    if request_content_type == "application/json":
        data = json.loads(request_body)
        texts = data.get("texts") or data.get("inputs") or []
        if isinstance(texts, str):
            texts = [texts]
        return texts
    raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(text_list, model_and_vectorizer):
    """Faktyczne rozpoznawanie phishingowych linków"""
    model, vectorizer = model_and_vectorizer
    X = vectorizer.transform(text_list)
    preds = model.predict(X)
    
    probas = None
    if hasattr(model, "predict_proba"):
        probas = model.predict_proba(X).max(axis=1)
        
    results = ["phishing" if p == 1 else "bezpieczny" for p in preds]
    return {"predictions": results, "confidences": probas.tolist() if probas is not None else None}

def output_fn(prediction_dict, accept):
    """Zwrócenie wyniku w formacie JSON"""
    body = json.dumps(prediction_dict)
    return body, "application/json"
