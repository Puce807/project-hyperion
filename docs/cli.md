# CLI Docs

This doc explains how to use the CLI commands in Project Hyperion.

<!-- TOC -->
* [CLI Docs](#cli-docs)
  * [Inspect](#inspect)
  * [Fetch-Bulk](#fetch-bulk)
  * [hr-diagram](#hr-diagram)
<!-- TOC -->

## Inspect

Pull individual star data from local database or Gaia including calculated fields.
If star is not found locally, command will fetch from Gaia and ask user if star should be saved to local DB.

### Usage

```commandline
python cli.py inspect GAIA_ID [OPTIONS]
```

### Arguments


| Argument | Type       | Description                      | Required |
|----------|------------|----------------------------------|----------|
| GAIA_ID  | INT | Unique Gaia Source ID to look up | Yes      |

### Options

| Options   | Type | Default | Description                                  | 
|-----------|------|---------|----------------------------------------------|
| --verbose | FLAG | False   | Enables debug logging to terminal            |
| --help    | FLAG | False   | Shows helpful list of sub commands and flags |

### Example

Basic Look Up: 
```commandline
python cli.py inspect 139357880437632896
```
Returns:
```commandline
Displaying local database record for star 139357880437632896
id                            : 139357880437632896
ra                            : 47.04619738473817
dec                           : 36.87741300603759
parallax                      : 0.6306388941314822
parallax_error                : 0.05209178850054741
parallax_over_error           : 0.05209178850054741
ruwe                          : 0.9261038899421692
astrometric_excess_noise      : 0.0
phot_g_mean_mag               : 16.143701553344727
phot_bp_mean_mag              : 16.557584762573242
phot_rp_mean_mag              : 15.558953285217285
bp_rp                         : 0.998631477355957
phot_g_mean_flux_over_error   : 1673.8170166015625
phot_g_mean_flux_error        : 3.924262523651123
phot_g_mean_flux              : 6568.497362394624
radial_velocity               : None
radial_velocity_error         : None
phot_variable_flag            : NOT_AVAILABLE
rv_amplitude_robust           : None
has_epoch_photometry          : 0
pmra                          : 0.6270639579300454
pmdec                         : 1.1085061940368366
phot_g_n_obs                  : 231
phot_bp_n_obs                 : 24
phot_rp_n_obs                 : 25
teff_gspphot                  : 5073.71533203125
absolute_magnitude            : 5.142605313296524
distance                      : 1585.6935074979842
colour_index                  : 0.998631477355957
temperature                   : 4746.026354580844
luminosity                    : 0.7498214752734003
```

## Fetch-Bulk

Scrape stars from the Gaia server to be downloaded to local database including calculated fields.

### Usage

```commandline
python cli.py fetch-bulk [OPTIONS]
```

### Options

| Options        | Type       | Default | Description                                  | 
|----------------|------------|---------|----------------------------------------------|
| --limit (-l)   | STRING/INT | 1000    | Number of stars to fetch                     |
| --verbose (-v) | FLAG       | False   | Enables debug logging to terminal            |
| --help         | FLAG       | False   | Shows helpful list of sub commands and flags |

### Example

Basic Ingestion:
```commandline
python cli.py fetch-bulk -l 10000
```
Returns:
```commandline
Ingestion complete. Successfully committed 10000/10000 records to database. 
Total time: 11.91s | Multi-target average: 0.0119s per star.
```

## hr-diagram

Generates a Hertzsprung Russell diagram using stars scraped from Gaia in the local DB plotting luminosity against colour index.
> **IMPORTANT:** Note that generated HR diagrams will not be perfect as they will reflect biases in both your local and Gaia database. 
> For best results, use strict quality filters. 
> The luminosity calculation relies on high quality parallax and apparent magnitude measurements.

### Usage

```commandline
python cli.py hr-diagram [OPTIONS]
```

### Options

| Options            | Type                    | Default | Description                                                         | 
|--------------------|-------------------------|---------|---------------------------------------------------------------------|
| --limit (-l)       | INT                     | 10000   | Number of stars to include in diagram                               |
| --style (-s)       | STRING [colour/density] | colour  | Style of diagram                                                    |
| --save             | FLAG OR PATH (optional) | None    | Filepath to save HR image to or leave blank to generate             |
| --annotations (-a) | FLAG                    | False   | **EXPERIMENTAL:** Shows annotations for different parts of diagram. |
| --help             | FLAG                    | False   | Shows helpful list of sub commands and flags                        |

### Examples

Basic Colour Diagram:
```commandline
python cli.py hr-diagram -l 20000 --save
```
Returns:
![Colour HR Diagram](../assets/HR_20000_C.png "Colour HR Diagram")

Basic Density Diagram:
```commandline
python cli.py hr-diagram -l 20000 
```
Returns:
![Density HR Diagram](../assets/HR_20000_D.png "Density HR Diagram")

Annotated Colour Diagram:
```commandline
python cli.py hr-diagram -l 20000 -a 
```

Returns:
![Colour HR Diagram + Annotations](../assets/HR_20000_CA.png "Colour HR Diagram With Annoations")
