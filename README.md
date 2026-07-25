# Project Hyperion 

[Docs](./docs/docs.md)

Project Hyperion aims to be a self-hosted astrophysics pipeline designed to process data from the European Space Agency's (ESA) Gaia mission.


## Roadmap

1. Foundation
   - [x] SQLite Database Schema
   - [x] Basic queries via astroquery
   - [x] Basic calculations of distance, magnitude and color index 
   - [ ] Basic CLI
   - [x] Logging
   - [ ] Quality filters (RUWE, parallax error)
   - [ ] HR Diagram to show results
   - [ ] Testing


2. Analytics
   - [ ] Web Dashboard (maybe)
   - [ ] Multiprocessing
   - [ ] Chunking with 1 network pull for larger volumes (100,000+ stars)
   - [ ] Cone search 
   - [ ] Interactive diagrams via Plotly or Matplotlib
   - [ ] Variable star identification
   - [ ] Binary star identification

3. Optimisation
   - [ ] Fully autonomous processing
   - [ ] Anomaly notification
   - [ ] Optimise pipeline
   - [ ] Dockerization

4. Advanced: 
   - [ ] Pull from other data sources 
   - [ ] Distributed compute
   - [ ] Train Neural Network to recognise variable stars