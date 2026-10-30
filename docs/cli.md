# CLI Docs

This doc explains how to use the CLI commands in Project Hyperion.

<!-- TOC -->
* [CLI Docs](#cli-docs)
  * [Inspect](#inspect)
  * [Fetch](#fetch)
  * [hr-diagram](#hr-diagram)
<!-- TOC -->

## Inspect

Pull individual star data from local database.

### Usage

```commandline
python cli.py inspect SOURCE_ID [OPTIONS]
```

### Arguments

| Argument  | Type   | Description                |
|-----------|--------|----------------------------|
| source_id | string | Source ID of target object |


### Options

| Options        | Type   | Default  | Description                                     | 
|----------------|--------|----------|-------------------------------------------------|
| --source (-s)  | STRING | hyperion | ID Belonging to which catalogue                 |
| --raw (-r)     | FLAG   | False    | Display original field names without formatting |
| --json (-j)    | FLAG   | False    | Output in JSON format                           |
| --output (-o)  | PATH   | -        | Path to save output to                          |
| --verbose (-v) | FLAG   | False    | Enables debug logging to terminal               |
| --help         | FLAG   | False    | Shows helpful list of sub commands and flags    |

> When using a source ID belonging to a catalogue (not hyperion), you must specify the source with the `--source` flag

### Example

Basic Look Up: 
```commandline
python cli.py inspect H_c7a8ef8e-60b1-4a66-9613-4b5c1c05b1de
```
Returns:
```
====================================================
 Star Record: H_c7a8ef8e-60b1-4a66-9613-4b5c1c05b1de
====================================================

Identifiers
 Hyperion ID                   : H_c7a8ef8e-60b1-4a66-9613-4b5c1c05b1de
 Gaia ID                       : 137333365999306624
 Ztf ID                        : 1234

Gaia
 Parallax                      : 0.22561767660747395
 Parallax error                : 0.3635902404785156
 Parallax over error           : 0.6205273270606995
 Phot bp mean mag              : 20.0537109375
 Phot rp mean mag              : 18.48678207397461
 Phot g mean mag               : 19.339881896972656
 Bp rp                         : 1.5669288635253906

Ztf
 No data found

Position
 RA                            : 45.003085°
 DEC                           : 35.314218°

```

Look up using Gaia ID and JSON output:

```commandline
python cli.py inspect -s gaia -j 137333365999306624
```

Returns:

```
{
  "hyperion_id": "H_c7a8ef8e-60b1-4a66-9613-4b5c1c05b1de",
  "identifiers": {
    "gaia": "137333365999306624",
    "ztf": "1234"
  },
  "catalogues": {
    "gaia": {
      "parallax": 0.22561767660747395,
      "parallax_error": 0.3635902404785156,
      "parallax_over_error": 0.6205273270606995,
      "phot_bp_mean_mag": 20.0537109375,
      "phot_rp_mean_mag": 18.48678207397461,
      "phot_g_mean_mag": 19.339881896972656,
      "bp_rp": 1.5669288635253906
    },
    "ztf": null
  },
  "position": {
    "ra": 45.003085437246824,
    "dec": 35.31421814401729
  }
}
```

## Fetch

Scrape stars from remote server to be downloaded to local database including calculated fields.

### Usage

```commandline
python cli.py fetch [OPTIONS] {ztf|gia}
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
