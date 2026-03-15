# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-03-14

### Added

* Added a button to the map to reset the zoom by [@AliBoloor](https://github.com/AliBoloor) in [#135](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/135)
* Added tests by [@AliBoloor](https://github.com/AliBoloor) in [#131](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/131)
* Advanced feature: select features on map and filter dashboard by [@sjbalagit](https://github.com/sjbalagit) in [#137](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/137)
* Set up duckdb/parquet/ibis functionality by [@nicolelink33](https://github.com/nicolelink33) in [#145](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/145)
* Added error handling for querychat_geo_cluster_plot, querychat_median_house, querychat_median_income and querychat_distribution_plot in AI Chatbot tab by [@mdskwong](https://github.com/mdskwong) in [#148](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/148)
* Reactive county banner, info icon in filters and renames manual filtering tab by [@sjbalagit](https://github.com/sjbalagit) in [#147](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/147)
* Added 0.4.0 items to CHANGELOG by [@sjbalagit](https://github.com/sjbalagit) in [#152](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/152)

### Changed

* Update CONTRIBUTING.md by [@nicolelink33](https://github.com/nicolelink33) in [#126](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/126)
* Update App Specification for AI Chatbot Tab by [@mdskwong](https://github.com/mdskwong) in [#127](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/127)
* Change titles for plots, add title to ocean plot, unify formatting by [@nicolelink33](https://github.com/nicolelink33) in [#144](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/144)
* Resize plots area in Manual Filtering Tab by [@mdskwong](https://github.com/mdskwong) in [#150](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/150)
* Update demo.gif by [@mdskwong](https://github.com/mdskwong) in [#153](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/153)
- Addressed feedback items: 
   - Fail gracefully - nice error message in query chat if user requests data not in dataset (Item 1 in prioritization issue [#121](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/121)). [#148](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/148)
   - Formatting of the axis units on the Distribution plot - when the user selects House Age, the x axis units are still $0k (Item 2 in prioritization issue [#121](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/121)). [#133](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/133)
   - Clarify context of socio-economic filters (Item 3 in prioritization issue [#121](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/121)) [#147](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/147)
   - Add titles to each of the charts to quickly tell the user what it shows (Item 4 in prioritization issue [#121](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/121)). [#144](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/144)
   - Add a map "reset" button or method (eg. when double-clicking on the map) to reset to the original zoom (Item 5 in prioritization issue [#121](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/121)). [#135](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/135)
   - Rename 'manual filtering' tab (Item 6 in prioritization issue [#121](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/121)). [#147](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/147)
   - Reactive text to show current state of filters. Our dashboard now shows county banner. This is a deviation from the original layout specification. (Item 7 in prioritization issue [#121](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/121)) [#147](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/147)
   - Size of plots are too small (TA feedback issue [#125](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/125)) [#150](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/150)

### Fixed

* Addresses milestone 3 known issue: `county_name_alt` column was removed from the dataframe so that the LLM querychat does not confuse it for `county` column by [@nicolelink33](https://github.com/nicolelink33) in [#145](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/145)
* Corrects the formatting on the x-axis of Distribution and Comparison … by [@AliBoloor](https://github.com/AliBoloor) in [#133](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/133)
* Fixes the failing tests by [@AliBoloor](https://github.com/AliBoloor) in [#146](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/146)
* Changes the tests to cover recent changes to the code by [@AliBoloor](https://github.com/AliBoloor) in [#149](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/149)
* Removes comment in readme and fixes gap between cards in layout by [@sjbalagit](https://github.com/sjbalagit) in [#151](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/151)
- **Feedback prioritization issue link:** [#121](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/121)

### Known Issues

- In the default opinionated view of the dashboard we filter the data to three ocean proximity categories and high median income values. If 'inland' and 'island' counties are selected on the map or 'select' drop down, it shows 'no data for current filters'. In this scenario, if all ocean proximity types and all median income values are enabled again, the map works as intended.

### Removed
* Remove old_app.py by [@mdskwong](https://github.com/mdskwong) in [#156](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/156)

### Release Highlight: Component click event interaction

We made the map reactive to user clicks. User can select one or multiple counties at a time and this updates the county banner at the top of the dashboard, the county selection drop down, the value boxes and plots. When a county is selected on the map, it is highlighted in a different color to distinguish from the unselected counties. An info icon, when hovered on, shows instructions on selection.

- **Option chosen:** D
- **PR:** [#137](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/137)
- **Why this option over the others:** Having a reactive map is useful for users as we are working with spatial distribution of block level housing data from 1990s and the dashboard is intended to facilitate this exploration. User can click on a county or multiple counties on the map and the value boxes, county banner and plots update based on the counties selected. Given our nature of data, this feature seemed a better fit over the other features.
- **Feature prioritization issue link:** [#119](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/119), [#121](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/121)

### Collaboration

- **CONTRIBUTING.md:** [#126](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/126)
- **M3 retrospective:** Our Milestone 3 collaboration worked quite well. All of our pull requests received at least one review by a team member other than the author of the pull request. We also completed the majority of work about 12 hours before the deadlines, with just final creations of the Changelog and documentations remaining closer to the due date. Also, all commits had meaningful commit messages, and all pull requests had helpful titles and descriptions, which helped teammates understand what was being changed each time. This made reviews much quicker and easier to carry out. We also did a good job of including "Closes #" or "Addresses #_" in our pull requests, which helps cross-link our issues and pull-requests.
- **M4:** In milestone 4, we tried to update the specification document regularly. First, we updated the m2_spec.md document to reflect the state of the dashboard after milestone 3, before writing any new code. Then, each team member updated the specifications in their branch, before writing any new code or changing anything on the dashboard. This way each PR had an initial commit which detailed what the changes were to be made. Then the code was updated and then the specifications were reviewed and updated based on the implementation of the code to correctly reflect the state of the dashboard. For a few PRs we did not update the specification first because we were unsure if the change was major enough to include in the specification document. However, we decided to include all changes and updated the specification document before merging the PR.

### Reflection

The dashboard provides an intuitive, multi-layered exploration of 1990 California housing data. The reactive map is a standout feature — clicking counties to filter the dashboard feels natural for spatial data. The county banner, value boxes with state comparisons, and the distribution plot that overlays selected vs. state-wide data all work together to give users immediate context for what they are exploring. The AI Chatbot tab adds a natural language interface that lowers the barrier for non-technical users to query the data. Error handling in the AI tab ensures graceful degradation when queries return unexpected results.

The default opinionated view (coastal proximity + high income filter) can cause confusion — if a user selects an inland county from the map or dropdown, the "no data for current filters" message appears because the ocean proximity and income filters are still active. This mismatch between the map selection and sidebar filters is not immediately obvious. Additionally, the dashboard is optimized for desktop and may not render well on smaller screens. 

The filtered opinionated view is deviation from DSCI 531 best practices. While best practices suggest showing all data by default, this opinionated view was chosen to highlight the coastal premium story and guide users toward a meaningful starting point for exploration.

We prioritized user-facing feedback items such axis formatting, chart titles, map reset, tab. We chose to de-prioritize or reject some fixes that felt not aligned with our goals. For example, we chose to not rearrange the layout of our dashboard into a Z layout, as we want the main statistics to be first, the map second, and the charts on the side to be supplementary. Full rationale is in [#121](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/issues/121) and **Changed** above.

The lecture on lazy loading and DuckDB/parquet was the most directly applicable — switching from pandas CSV loading to ibis + parquet required rethinking how filters are wired to the data layer. The instructor, TA and peer feedback from M3 also shaped our work significantly. We wish there had been more coverage of how to handle Shiny reactivity with ibis lazy expressions, as debugging the two-step `filtered_expr` → `filtered_data` pattern took meaningful time.


## [0.3.0] - 2026-03-08

### Added
* Querychat by [@nicolelink33](https://github.com/nicolelink33) in [#93](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/93)
* Feat/opinionated view by [@sjbalagit](https://github.com/sjbalagit) in [#101](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/101)
* Query chat download button by [@sjbalagit](https://github.com/sjbalagit) in [#97](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/97)
* Feat/dynamic map by [@sjbalagit](https://github.com/sjbalagit) in [#105](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/105)
* Adds filtered data frame for the AI tab by [@AliBoloor](https://github.com/AliBoloor) in [#102](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/102)
* Added table view, map, median_house and median_income value boxes, distribution_plot, updated the layout for the AI tab by [@mdskwong](https://github.com/mdskwong) in [#110](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/110)
* Added 0.3.0 items and reflection section to CHANGELOG by [@nicolelink33](https://github.com/nicolelink33) in [#111](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/111)


### Changed
* creates two groups for the filters - one for house properties and one… by [@AliBoloor](https://github.com/AliBoloor) in [#103](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/103)

### Fixed
* Fix dev deployment failure by [@nicolelink33](https://github.com/nicolelink33) in [#95](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/95)
* update python-dotenv version number by [@nicolelink33](https://github.com/nicolelink33) in [#96](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/96)
* TA improvements to dashboard by [@nicolelink33](https://github.com/nicolelink33) in [#108](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/108)
* Added empty dataframe handling for the value boxes by [@mdskwong](https://github.com/mdskwong) in [#110](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/110)



### Known Issues
* AI querychat occasionally uses the wrong column when filtering by county (`county_name_alt` instead of `county`) and returns 0 rows 


### Removed
* Removed static map [@sjbalagit](https://github.com/sjbalagit) in [#105](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/105)

### Reflection
* We addressed the top improvements suggested by our TA. We refined axis formatting on density plot, removed non-informative options on scatterplot, and shortened footer - by [@nicolelink33](https://github.com/nicolelink33) in [#108](https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/pull/108)
* We also addressed the improvements suggested by Ilya. We created an opinionated default filtered state for our dashboard, which shows coastal areas instead of all proximity categories, and limits to a higher income status. This default state helps with our job story #2, where an economics researcher wants to investigate coastal area housing prices. 



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

[0.4.0]: https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/releases/tag/v0.4.0
[0.3.0]: https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/releases/tag/v0.3.0
[0.2.0]: https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/releases/tag/v0.2.0
[0.1.0]: https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing/releases/tag/v0.1.0
