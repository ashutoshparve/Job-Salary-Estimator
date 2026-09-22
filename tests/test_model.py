import pickle
import numpy as np
import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def model_data():
    """Load the trained model and encoders."""
    with open("model/model.pkl", "rb") as f:
        data = pickle.load(f)
    return data


def test_model_loads_successfully(model_data):
    """Model file should load without errors."""
    assert model_data is not None
    assert "model" in model_data
    assert "encoders" in model_data
    assert "features" in model_data


def test_model_has_correct_features(model_data):
    """Model should have exactly 3 features."""
    features = model_data["features"]
    assert "job_title" in features
    assert "location" in features
    assert "company" in features


def test_model_prediction_returns_float(model_data):
    """Model should return a numeric salary prediction."""
    model    = model_data["model"]
    encoders = model_data["encoders"]
    features = model_data["features"]

    # Encode a sample input
    encoded = []
    test_input = {
        "job_title": "data scientist",
        "location": "bangalore",
        "company": "Google"
    }
    for col in features:
        le    = encoders[col]
        value = test_input[col]
        encoded.append(le.transform([value])[0])

    prediction = model.predict(np.array(encoded).reshape(1, -1))
    assert isinstance(float(prediction[0]), float)


def test_prediction_is_realistic(model_data):
    """Predicted salary should be within a realistic range (1-100 LPA)."""
    model    = model_data["model"]
    encoders = model_data["encoders"]
    features = model_data["features"]

    encoded = []
    test_input = {
        "job_title": "machine learning engineer",
        "location": "bangalore",
        "company": "Google"
    }
    for col in features:
        le    = encoders[col]
        value = test_input[col]
        encoded.append(le.transform([value])[0])

    salary = float(model.predict(np.array(encoded).reshape(1, -1))[0])
    assert 1.0 <= salary <= 100.0


def test_all_job_titles_are_encodable(model_data):
    """All job titles in the encoder should be transformable."""
    le     = model_data["encoders"]["job_title"]
    titles = le.classes_
    for title in titles:
        encoded = le.transform([title])
        assert len(encoded) == 1


def test_encoder_has_expected_locations(model_data):
    """Location encoder should include major Indian cities."""
    le        = model_data["encoders"]["location"]
    locations = list(le.classes_)
    expected  = ["bangalore", "mumbai", "delhi"]
    for city in expected:
        assert city in locations