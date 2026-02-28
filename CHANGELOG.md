# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-28

### Added
* shiny, scipy, matplotlib to environment by [@nicolelink33](https://github.com/nicolelink33) in [#29](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/29)
* Created requirements.txt file by [@nicolelink33](https://github.com/nicolelink33) in [#52](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/52)
* Dashboard urls to README by [@nicolelink33](https://github.com/nicolelink33) in [#55](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/55)
* Created m2_spec.md and add job stories by [@nicolelink33](https://github.com/nicolelink33) in [#56](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/56)
* Calculation details to m2_spec by [@nicolelink33](https://github.com/nicolelink33) in [#58](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/58)
* Added 2.2 Component Inventory and 2.3 Reactivity Diagram to m2_spec.md by [@mdskwong](https://github.com/mdskwong) in [#59](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/59)
* Calculation implementation in app.py by [@nicolelink33](https://github.com/nicolelink33) in [#62](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/62)
* Map visualization in app.py by [@sjbalagit](https://github.com/sjbalagit) in [#64](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/64)
* Spatial analysis Jupyter notebook and raw counties geojson and processed housing with counties data by [@sjbalagit](https://github.com/sjbalagit) in [#64](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/64)
* shinywidget, anywidget, ipyleaflet to environment.yml file by [@sjbalagit](https://github.com/sjbalagit) in [#64](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/64)
* shinywidget, geopandas and anywidget to requirement.txt file by [@sjbalagit](https://github.com/sjbalagit) in [#66](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/66)
* Select county multiselect drop down to app.py by by [@sjbalagit](https://github.com/sjbalagit) in [#64](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/64)
* Created CHANGELOG in repo and added 0.1.0 and draft 0.2.0 items by [@sjbalagit](https://github.com/sjbalagit) in [#67](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/67)
* Summary plots in app.py by [@AliBoloor](https://github.com/AliBoloor) in [#68](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/68)
* Set the layout to align with the sketch design in app.py by [@mdskwong](https://github.com/mdskwong) in [#74](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/74)
* Added 0.2.0 items and reflection section to CHANGELOG by [@nicolelink33](https://github.com/nicolelink33) in [#70](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/70)
* Added 0.2.0 items to CHANGELOG by [@mdskwong](https://github.com/mdskwong) in [#75](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/75)
* Added comparisons to value boxes, add footer to dashboard by [@nicolelink33](https://github.com/nicolelink33) in [#72](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/72)
* Added CSS styling for dashboard footer by [@sjbalagit](https://github.com/sjbalagit) in [#72](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/72)
* Added demo and revised README by [@AliBoloor](https://github.com/AliBoloor) in [#76](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/76)
* Added a reset button to reset all the filters of the sidebar by [@mdskwong](https://github.com/mdskwong) in [#78](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/78)


### Changed
* Overhaul dashboard syntax to match lecture notes style by [@nicolelink33](https://github.com/nicolelink33) in [#58](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/58)
* Updated job stories status, component inventory by [@nicolelink33](https://github.com/nicolelink33) in [#70](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/70)
* Updated Reactivity Diagram to m2_spec.md by [@mdskwong](https://github.com/mdskwong) in [#75](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/75)


### Removed
* flask, dash, and plotly from environment.yml by [@sjbalagit](https://github.com/sjbalagit) in [#64](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/64)
* lat and long filters from app.py by [@sjbalagit](https://github.com/sjbalagit) in [#64](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/64)


### Reflection
#### Fully Implemented Job Stories:
* Job Story 1: I want to analyze the relationship between median income and median house value so I can determine whether higher income areas were associated with higher property prices in 1990.
* Job Story 2: I want to compare median house values across ocean proximity categories in order to assess whether coastal access was associated with higher property values in 1990.  
* Job Story 3: I want to visualize the geographic distribution of house values across California to identify spatial clusters of high and low value regions. 

#### Layout comparison
Our final layout matches our M1 sketch and M2 spec quite well. A few color choices have changed, to make the plots more visually understandable. We also removed the latitude and longitude slider inputs, and instead gave the user a drop down selection menu to pick which California counties to display. This is a more intuitive, easily accessible way to filter geographically. 

## [0.1.0] - 2026-02-14

### Added
* Usage scenarios and user stories in proposal.md by [@sjbalagit](https://github.com/sjbalagit) in [#18](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/18)
* Motivation and Purpose and Description of the Data to proposal by [@mdskwong](https://github.com/mdskwong) in [#19](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/19)
* First draft of the dashboard by [@mdskwong](https://github.com/mdskwong) in [#24](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/24)
* Sketch (sketch.png) and proposal section 5 description of sketch by [@nicolelink33](https://github.com/nicolelink33) in [#25](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/25)
* EDA functions, script, outputs, as well as EDA section to proposal by [@AliBoloor](https://github.com/AliBoloor) in [#22](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/22)

### Changed
* File structure updates and README filled out, names added to License by [@nicolelink33](https://github.com/nicolelink33) in [#14](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/14)
* app.py updated to align the sketch by [@mdskwong](https://github.com/mdskwong) in [#28](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/28)
* Proposal section 1 updated to align with the dataset by [@mdskwong](https://github.com/mdskwong) in [#23](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/23)
* Dashboard running set up instructions in README & proposal section 1 and 3/4 tie in by [@sjbalagit](https://github.com/sjbalagit) in [#27](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/27)

### Fixed
* README to say California by [@nicolelink33](https://github.com/nicolelink33) in [#16](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/16)
* Repo metadata by [@nicolelink33](https://github.com/nicolelink33) in [#17](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/17)
* Context for 1990 dataset to README and description.md by [@nicolelink33](https://github.com/nicolelink33) in [#21](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/21)


## Contributors
- [@nicolelink33](https://github.com/nicolelink33)
- [@sjbalagit](https://github.com/sjbalagit)
- [@mdskwong](https://github.com/mdskwong)
- [@AliBoloor](https://github.com/AliBoloor)  

---

[0.2.0]: https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/releases/tag/v0.2.0
[0.1.0]: https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/releases/tag/v0.1.0
