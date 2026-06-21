import pytest
from pipeline.preprocessor import TextPreprocessor

def test_preprocessor_normalize():
    prep = TextPreprocessor()
    assert prep.normalize("Hello World!!!") == "hello world"

def test_preprocessor_tokenize():
    prep = TextPreprocessor()
    tokens = prep.tokenize("gradient descent")
    assert "gradient" in tokens
    assert "descent" in tokens
