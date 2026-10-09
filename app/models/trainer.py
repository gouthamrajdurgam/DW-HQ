from typing import Dict, List, Any

from sklearn.linear_model import LinearRegression

from app.models.feature_builder import build_feature_vector, feature_columns


class HybridRanker:
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
        self.weights = {
            "price": -0.001,
            "size_m2": 0.01,
            "price_per_m2": -0.01,
            "beds": 0.2,
            "district_match": 2.0,
            "in_preferred_state": 1.5,
            "property_type_match": 1.0,
            "within_budget": 2.0,
            "size_ok": 1.5,
            "beds_ok": 1.0,
        }

    def rule_score(self, listing: Dict[str, Any], prefs: Dict[str, Any]) -> float:
        features = build_feature_vector(listing, prefs)
        score = 0.0
        for key, value in features.items():
            if key in self.weights:
                score += float(value) * self.weights[key]
        return score

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, X: List[List[float]]) -> List[float]:
        if not self.is_trained:
            return [0.0 for _ in X]
        return self.model.predict(X).tolist()

    def score_listing(self, listing: Dict[str, Any], prefs: Dict[str, Any]) -> float:
        features = build_feature_vector(listing, prefs)
        values = [features.get(col, 0.0) for col in feature_columns()]
        rule_score = self.rule_score(listing, prefs)
        if self.is_trained:
            model_score = self.model.predict([values])[0]
            return float(rule_score + model_score)
        return float(rule_score)

    def rank(self, listings: List[Dict[str, Any]], prefs: Dict[str, Any]) -> List[Dict[str, Any]]:
        ranked = []
        for listing in listings:
            item = dict(listing)
            item["score"] = self.score_listing(item, prefs)
            ranked.append(item)
        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked
