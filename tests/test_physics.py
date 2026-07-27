import pytest
from src.physics import find_distance, find_colour_index, find_absolute_magnitude, find_luminosity, estimate_temperature

def test_find_distance():
    assert find_distance(1000) == pytest.approx(1.0, rel=1e-3), "A parallax value of 1000 should yield a distance of ~1"
    assert find_distance(782.0665) == pytest.approx(1.2787, rel=1e-3), "A parallax value of 782.0665 should yield a distance of ~1.279" # Parallax of Proxima Centauri
    assert find_distance(0.000001) == pytest.approx(1000000000, rel=1e-3), "A parallax value of 0.000001 should yield a distance of ~1000000000"

@pytest.mark.parametrize("invalid_val", [None, "test", True, 0, -100])
def test_find_distance_invalid(invalid_val):
    with pytest.raises(ValueError):
        find_distance(invalid_val)

def test_find_colour_index():
    assert find_colour_index(14, 13) == pytest.approx(1,rel=1e-3), "A bp of 14 and rp of 13 should yield colour index distance of ~1"
    assert find_colour_index(14.617077827453613, 13.681351661682129) == pytest.approx(0.9357,rel=1e-3), "A bp of 14.617 and rp of 13.681 should yield colour index distance of ~0.9357" # BP, RP of Gaia star ID 137333026694877824
    assert find_colour_index(140_000_000, 130_000_000) == pytest.approx(10_000_000,rel=1e-3), "A bp of 140,000,000 and rp of 130,000,000 should yield colour index distance of ~10,000,000"

def test_find_absolute_magnitude():
    assert find_absolute_magnitude(10, 1) == pytest.approx(15, rel=1e-3), "An apparent magnitude of 10 and distance of 1 should yield an absolute magnitude of ~15"
    assert find_absolute_magnitude(11.1301970258, 1.2787) == pytest.approx(15.5964, rel=1e-3), "An apparent magnitude of 11.1302 and distance of 1.2787 should yield an absolute magnitude of ~15.5964" # Apparent magnitude and distance of Proxima Centauri
    assert find_absolute_magnitude(100, 10) == pytest.approx(100, rel=1e-3), "An apparent magnitude of 100 and distance of 10 should yield an absolute magnitude of ~100"

def test_find_luminosity():
    assert find_luminosity(10) == pytest.approx(0.00855067, rel=1e-3), "An apparent magnitude of 10 should yield a luminosity of ~0.0000855"
    assert find_luminosity(15.560480264265815) == pytest.approx(0.00005105, rel=1e-3), "An apparent magnitude of 15.56 should yield a luminosity of ~0.00005" # Apparent magnitude of Proxima Centauri

def test_estimate_temperature():
    assert estimate_temperature(0.5) == pytest.approx(6388.8889, rel=1e-3), "A colour index of 0.5 should yield a temperature estimate of ~6388.8889"
    assert estimate_temperature(1.82) == pytest.approx(3368.0868, rel=1e-3), "An colour index of 1.82 should yield a temperature estimate of ~3368.0868"# Colour index of Proxima Centauri

    with pytest.raises(ValueError):
        estimate_temperature(None)
    with pytest.raises(ValueError):
        estimate_temperature("test")
    with pytest.raises(ValueError):
        estimate_temperature(True)

@pytest.mark.parametrize("invalid_val", [None, "test", True])
def test_physics_type_safety(invalid_val):
    with pytest.raises(ValueError):
        find_colour_index(invalid_val, 10)
    with pytest.raises(ValueError):
        find_absolute_magnitude(invalid_val, 10)
    with pytest.raises(ValueError):
        find_luminosity(invalid_val)
    with pytest.raises(ValueError):
        estimate_temperature(invalid_val)

def test_full_physics_pipeline_proxima():
    # Real Proxima Centauri parameters
    parallax = 768.0665
    apparent_mag = 11.13
    b_mag = 12.95 # Note: These use Johnson B-V rather than Gaia
    v_mag = 11.13 # Note: These use Johnson B-V rather than Gaia

    distance = find_distance(parallax)
    absolute_mag = find_absolute_magnitude(apparent_mag, distance)
    luminosity = find_luminosity(absolute_mag)

    colour_index = find_colour_index(b_mag, v_mag)
    temperature = estimate_temperature(colour_index)

    assert distance == pytest.approx(1.3019, rel=1e-3)
    assert colour_index == pytest.approx(1.82, rel=1e-3)
    assert temperature == pytest.approx(3368.0, rel=1e-3)
    assert absolute_mag == pytest.approx(15.5570, rel=1e-3)
    assert luminosity == pytest.approx(5.1192e-05, rel=1e-3)
