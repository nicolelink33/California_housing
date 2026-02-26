# Milestone 2 App Specification

## Section 1: Job Stories
| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | I want to analyze the relationship between median income and median house value so I can determine whether higher income areas were associated with higher property prices in 1990. | ⏳ Pending |                               |
| 2   | I want to compare median house values across ocean proximity categories in order to assess whether coastal access was associated with higher property values in 1990. | ⏳ Pending     |       |
| 3   | I want to visualize the geographic distribution of house values across California to identify spatial clusters of high and low value regions.| ⏳ Pending  |                               |


## Section 2: Component Inventory
| ID            | Type          | Shiny widget / renderer   | Depends on                   | Job story  |
| ------------- | ------------- | -----------------------   | ---------------------------- | ---------- |
| `house_val_slider`   | Input         | `ui.house_val()`          | —                            | #1, #2, #3     |
| `lat_slider`         | Input         | `ui.lat()`                | —                            | #1, #2, #3     |
| `long_slider`        | Input         | `ui.long()`               | —                            | #1, #2, #3     |
| `income_slider`      | Input         | `ui.income()`             | —                            | #1, #2, #3     |
| `age_slider`         | Input         | `ui.age()`                | —                            | #1, #2, #3     |
| `rooms_slider`       | Input         | `ui.rooms()`              | —                            | #1, #2, #3     |
| `beds_slider`        | Input         | `ui.beds()`               | —                            | #1, #2, #3     |
| `pop_slider`         | Input         | `ui.pop()`                | —                            | #1, #2, #3     |
| `households_slider`  | Input         | `ui.households()`         | —                            | #1, #2, #3     |
| `ocean_checkbox`       | Input         | `ui.ocean()`              | —                            | #1, #2, #3     |
| `dist_type`   | Input         | `ui.dist_type()`          | —                            | #1, #2         |
| `filtered_df` | Reactive calc | `@reactive.calc`        | `house_val`,`lat`,`long`,`income`,`age`,`rooms`,`beds`,`pop`,`households`,`ocean`,`dist_type` | #1, #2, #3 |
| `median_house`        | Output        | `ui.value_box`          | `filtered_df`                | #1, #2         |
| `median_income`       | Output        | `ui.value_box`          | `filtered_df`                | #1, #2         |
| `house_map`           | Output        | `@render.plot`          | `filtered_df`                | #3             |
| `distribution_plot`   | Output        | `@render.plot`          | `filtered_df`,`dist_type`    | #1, #2         |
| `comparison_scatter`  | Output        | `@render.plot`          | `filtered_df`                | #1, #2         |
| `boxplot_proximity`   | Output        | `@render.plot`          | `filtered_df`                | #1, #2         |


## Section 3: Reactivity Diagram
````markdown
```mermaid
flowchart TD
  A[/house_val/] --> K{{filtered_df}}
  B[/lat/] --> K
  C[/long/] --> K
  D[/income/] --> K
  E[/age/] --> K
  F[/rooms/] --> K
  G[/beds/] --> K
  H[/pop/] --> K
  I[/households/] --> K
  J[/ocean/] --> K
  K --> P1([value_box])
  K --> P2([value_box])
  K --> P3([house_map])
  K --> P5([comparison_scatter])
  K --> P6([boxplot_proximity])
  L[/dist_type/] --> P4([distribution_plot])
  K --> P4
```
````
![Reactivity Diagram](../img/reactivity.png)


## Section 4: Calculation Details
Dataset Filtering: 
The `@reactive.calc` `filtered_df` depends on the inputs:
- `house_val_slider` minimum and maximum - aka Median house value
- `lat_slider` minimum and maximum - Latitude
- `long_slider` minimum and maximum - Longitude
- `income_slider` minimum and maximum - Median income
- `age_slider` minimum and maximum - House age
- `rooms_slider` minimum and maximum - Total number of rooms
- `beds_slider` minimum and maximum - Total number of bedrooms
- `pop_slider` minimum and maximum - Population
- `households_slider` minimum and maximum - Number of households
- `ocean_checkbox` - selected categorical value(s) for ocean proximity
This calculation filters the rows of the raw dataframe to all selected input values.
It is consumed by the map visualization, the two value boxes for median house value and median income value, and the three plots: the distribution plot, the comparison scatter plot, and the ocean proximity box plot. 