from src.physics import find_distance, find_luminosity, find_colour_index, find_absolute_magnitude, estimate_temperature
from src.scraper import fetch_data

results = fetch_data()
results.pprint_all()
distance = find_distance(results["parallax"][0])
ci = find_colour_index(results["phot_bp_mean_mag"][0],results["phot_rp_mean_mag"][0])
temp = estimate_temperature(ci)
abs_mag = find_absolute_magnitude(results["phot_g_mean_mag"][0], distance)
luminosity = find_luminosity(abs_mag)
print("Distance: ", distance)
print("CI: ", ci)
print("Temp: ", temp)
print("Absolute Magnitude: ", abs_mag)
print("Luminosity: ", luminosity)

# Next: Error handling, SQL database1
# TODO: Make config file