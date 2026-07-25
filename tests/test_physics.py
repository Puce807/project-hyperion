import pytest
from src.physics import find_distance

def test_find_distance():
    assert find_distance(1000) == pytest.approx(1.0, rel=1e-3), "A parallax value of 1000 should yield a distance of ~1"
    assert find_distance(782.0665) == pytest.approx(1.2787, rel=1e-3), "A parallax value of 782.0665 should yield a distance of ~1.279" # Parallax of Proxima Centauri
    assert find_distance(0.000001) == pytest.approx(1000000000, rel=1e-3), "A parallax value of 0.01 should yield a distance of ~1000000000"

    with pytest.raises(ValueError, match=f"parallax_mas must be positive float, got: {None}"):
        find_distance(None)
    with pytest.raises(ValueError, match=f"parallax_mas must be positive float, got: {0}"):
        find_distance(0)
    with pytest.raises(ValueError, match=f"parallax_mas must be positive float, got: {-100}"):
        find_distance(-100)
    with pytest.raises(ValueError, match=f"parallax_mas must be positive float, got: {'test'}"):
        find_distance("test")
    with pytest.raises(ValueError, match=f"parallax_mas must be positive float, got: {True}"):
        find_distance(True)
