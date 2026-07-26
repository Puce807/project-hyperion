import pytest
from src.physics import find_distance, find_colour_index, find_absolute_magnitude, find_luminosity

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

def test_find_colour_index():
    assert find_colour_index(14, 13) == pytest.approx(1,rel=1e-3), "A bp of 14 and rp of 13 should yield colour index distance of ~1"
    assert find_colour_index(14.617077827453613, 13.681351661682129) == pytest.approx(0.9357,rel=1e-3), "A bp of 14.617 and rp of 13.681 should yield colour index distance of ~0.9357" # BP, RP of Gaia star ID 137333026694877824
    assert find_colour_index(140_000_000, 130_000_000) == pytest.approx(10_000_000,rel=1e-3), "A bp of 140,000,000 and rp of 130,000,000 should yield colour index distance of ~10,000,000"

    with pytest.raises(ValueError):
        find_colour_index(None, None)
    with pytest.raises(ValueError):
        find_colour_index("test", "test")
    with pytest.raises(ValueError):
        find_colour_index(True, False)

def test_find_absolute_magnitude():
    assert find_absolute_magnitude(10, 1) == pytest.approx(15, rel=1e-3), "An apparent magnitude of 10 and distance of 1 should yield an absolute magnitude of ~15"
    assert find_absolute_magnitude(11.1301970258, 1.3) == pytest.approx(15.56, rel=1e-3), "An apparent magnitude of 11.1302 and distance of 1.3 should yield an absolute magnitude of ~15.56" # Apparent magnitude and distance of Proxima Centauri
    assert find_absolute_magnitude(100, 10) == pytest.approx(100, rel=1e-3), "An apparent magnitude of 100 and distance of 10 should yield an absolute magnitude of ~100"

    with pytest.raises(ValueError):
        find_absolute_magnitude(None, None)
    with pytest.raises(ValueError):
        find_absolute_magnitude(0, 0)
    with pytest.raises(ValueError):
        find_absolute_magnitude(-100, -100)
    with pytest.raises(ValueError):
        find_absolute_magnitude("test", "test")
    with pytest.raises(ValueError):
        find_absolute_magnitude(True, False)

def test_find_luminosity():
    assert find_luminosity(10) == pytest.approx(0.00855067, rel=1e-3), "An apparent magnitude of 10 should yield a luminosity of ~0.0000855"
    assert find_luminosity(15.560480264265815) == pytest.approx(0.00005105, rel=1e-3), "An apparent magnitude of 15.56 should yield a luminosity of ~0.00005" # Apparent magnitude of Proxima Centauri

    with pytest.raises(ValueError):
        find_luminosity(None)
    with pytest.raises(ValueError):
        find_luminosity(0)
    with pytest.raises(ValueError):
        find_luminosity(-100)
    with pytest.raises(ValueError):
        find_luminosity("test")
    with pytest.raises(ValueError):
        find_luminosity(True)