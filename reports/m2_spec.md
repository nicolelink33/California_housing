# Milestone 2 App Specification

## Section 1: Job Stories
| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | I want to analyze the relationship between median income and median house value so I can determine whether higher income areas were associated with higher property prices in 1990. | ⏳ Pending |                               |
| 2   | I want to compare median house values across ocean proximity categories in order to assess whether coastal access was associated with higher property values in 1990. | ⏳ Pending     |       |
| 3   | I want to visualize the geographic distribution of house values across California to identify spatial clusters of high and low value regions.| ⏳ Pending  |                               |


## Section 2: Component Inventory


## Section 3: Reactivity Diagram


## Section 4: Calculation Details
Dataset Filtering: 
This `@reactive.calc` depends on the inputs:
- `house_val` minimum and maximum - aka Median house value
- `lat` minimum and maximum - Latitude
- `lon` minimum and maximum - Longitude
- `income` minimum and maximum - Median income
- `age` minimum and maximum - House age
- `rooms` minimum and maximum - Total number of rooms
- `beds` minimum and maximum - Total number of bedrooms
- `pop` minimum and maximum - Population
- `households` minimum and maximum - Number of households
- `ocean` - selected categorical value(s) for ocean proximity
This calculation filters the rows to all selected input values.
It is consumed by the map visualization, the two KPI value boxes for medain house value and median income value, and the three plots: the distribution plot, the comparison scatter plot, and the ocean proximity box plot. 