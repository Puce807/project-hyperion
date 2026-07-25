import pytest
from src.physics import find_distance

def test_find_distance():
    assert round(find_distance(1000), 3) == 1, "A parallax value of 1000 should yield a distance of 1"
    assert round(find_distance(782.0665), 3) == 1.279, "A parallax value of 782.0665 should yield a distance of 1.279" # Parallax of Proxima Centauri
    assert round(find_distance(0.000001), 3) == 1000000000, "A parallax value of 0.01 should yield a distance of 1000000000"

    # TODO: Change rounding to pytest.approx

    with pytest.raises(ValueError, match=f"parallax_mas must be positive, got: {None}"):
        find_distance(None)
    with pytest.raises(ValueError, match=f"parallax_mas must be positive, got: {0}"):
        find_distance(0)
    with pytest.raises(ValueError, match=f"parallax_mas must be positive, got: {-100}"):
        find_distance(-100)
