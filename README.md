# Project Hyperion 

[Docs](./docs/docs.md)

Project Hyperion aims to be a self-hosted astrophysics pipeline designed to process data from multiple sources.

> **Status: Phase 1 - Active Development / Work in Progress**

## Roadmap

1. Foundation
   - [x] SQLite Database Schema
   - [x] Basic queries via astroquery
   - [x] Basic calculations of distance, magnitude and color index 
   - [ ] Basic CLI
   - [ ] Add levels of filtering to CLI (none, strict, custom, etc)
   - [x] Logging
   - [ ] Quality filters (RUWE, parallax error)
   - [x] HR Diagram to show results
   - [x] Physics Calculation Testing
   - [ ] Add current results to README (hr diagram)
   - [ ] Docs
   - [x] Refactor to use dataclasses to allow other data sources

2. Analytics
   - [ ] Web Dashboard (maybe)
   - [ ] Multiprocessing
   - [ ] Chunking with 1 network pull for larger volumes (100,000+ stars)
   - [ ] Cone search 
   - [ ] Interactive diagrams via Plotly or Matplotlib
   - [ ] Variable star identification
   - [ ] Binary star identification
   - [ ] Further Testing

3. Optimisation
   - [ ] Fully autonomous processing
   - [ ] Anomaly notification
   - [ ] Optimise pipeline
   - [ ] Dockerization

4. Advanced:
   - [ ] Distributed compute
   - [ ] Train Neural Network to recognise variable stars