import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm
from shiny import App, reactive, render, ui

# Import dataset
raw_data = pd.read_csv("data/raw/housing.csv")

# Page configuration
app_ui = ui.page_fillable(
    ui.panel_title("California Housing"),
    
    ui.layout_sidebar(
        # Sidebar inputs
        ui.sidebar(
            ui.input_slider(
                id="house_val_slider",
                label="Median house value:",
                min=raw_data.median_house_value.min(),
                max=raw_data.median_house_value.max(),
                value=[raw_data.median_house_value.min(), raw_data.median_house_value.max()],
            ),
            ui.input_slider(
                id="lat_slider",
                label="Latitude:",
                min=raw_data.latitude.min(),
                max=raw_data.latitude.max(),
                value=[raw_data.latitude.min(), raw_data.latitude.max()],
            ),
            ui.input_slider(
                id="long_slider",
                label="Longitude:",
                min=raw_data.longitude.min(),
                max=raw_data.longitude.max(),
                value=[raw_data.longitude.min(), raw_data.longitude.max()],
            ),
            ui.input_slider(
                id="income_slider",
                label="Median income:",
                min=raw_data.median_income.min(),
                max=raw_data.median_income.max(),
                value=[raw_data.median_income.min(), raw_data.median_income.max()],
            ),
            ui.input_slider(
                id="age_slider",
                label="House age:",
                min=raw_data.housing_median_age.min(),
                max=raw_data.housing_median_age.max(),
                value=[raw_data.housing_median_age.min(), raw_data.housing_median_age.max()],
            ),
            ui.input_slider(
                id="rooms_slider",
                label="Total rooms:",
                min=raw_data.total_rooms.min(),
                max=raw_data.total_rooms.max(),
                value=[raw_data.total_rooms.min(), raw_data.total_rooms.max()],
            ),
            ui.input_slider(
                id="beds_slider",
                label="Total bedrooms:",
                min=raw_data.total_bedrooms.min(),
                max=raw_data.total_bedrooms.max(),
                value=[raw_data.total_bedrooms.min(), raw_data.total_bedrooms.max()],
            ),
            ui.input_slider(
                id="pop_slider",
                label="Population:",
                min=raw_data.population.min(),
                max=raw_data.population.max(),
                value=[raw_data.population.min(), raw_data.population.max()],
            ),
            ui.input_slider(
                id="households_slider",
                label="Households:",
                min=raw_data.households.min(),
                max=raw_data.households.max(),
                value=[raw_data.households.min(), raw_data.households.max()],
            ),

            ui.input_checkbox_group(
                id="ocean_checkbox",
                label="Ocean Proximity:",
                choices={
                    "<1H OCEAN": "<1hr Ocean",
                    "NEAR OCEAN": "Near Ocean",
                    "NEAR BAY": "Near Bay",
                    "ISLAND": "Island",
                    "INLAND": "Inland"
                },
                selected=["<1H OCEAN", "NEAR OCEAN", "NEAR BAY", "ISLAND", "INLAND"],
            )
        ),
        
        # Page configuration
        ui.layout_columns(
            # Column 1
            ui.column(10,
                      
                # Value Boxes
                ui.row(
                    ui.column(6, ui.value_box("Median house value", ui.output_text("median_house"))),
                    ui.column(6, ui.value_box("Median income", ui.output_text("median_income"))),
                ),

                # Map Visualization
                ui.output_ui("map_output")
                
            ),
            # Column 2
            ui.column(4,
                
                # Distribution Plots
                ui.row(ui.output_plot("distribution_plot")),

                # Comparison Scatterplot
                ui.row(ui.output_plot("comparison_scatter")),

                # Ocean Proximity Boxplots
                ui.row(ui.output_plot("boxplot_proximity")),
            ),
        ),
    )
)


def server(input, output, session):
    # Filter dataset
    @reactive.calc
    def filtered_data():
        idx_house_val = raw_data.median_house_value.between(
            left=input.house_val_slider()[0], right=input.house_val_slider()[1], inclusive="both"
        )
        idx_lat = raw_data.latitude.between(
            left=input.lat_slider()[0], right=input.lat_slider()[1], inclusive="both"
        )
        idx_long = raw_data.longitude.between(
            left=input.long_slider()[0], right=input.long_slider()[1], inclusive="both"
        )
        idx_income = raw_data.median_income.between(
            left=input.income_slider()[0], right=input.income_slider()[1], inclusive="both"
        )
        idx_age = raw_data.housing_median_age.between(
            left=input.age_slider()[0], right=input.age_slider()[1], inclusive="both"
        )
        idx_rooms = raw_data.total_rooms.between(
            left=input.rooms_slider()[0], right=input.rooms_slider()[1], inclusive="both"
        )
        idx_beds = raw_data.total_bedrooms.between(
            left=input.beds_slider()[0], right=input.beds_slider()[1], inclusive="both"
        )
        idx_pop = raw_data.population.between(
            left=input.pop_slider()[0], right=input.pop_slider()[1], inclusive="both"
        )
        idx_households = raw_data.households.between(
            left=input.households_slider()[0], right=input.households_slider()[1], inclusive="both"
        )
        idx_ocean = raw_data.ocean_proximity.isin(input.ocean_checkbox())

        return raw_data[idx_house_val & idx_lat & idx_long & idx_income & idx_age & idx_rooms & idx_beds & idx_pop & idx_ocean]

    # Median House Value
    @render.text
    def median_house():
        median_value = round(filtered_data().median_house_value.median(), 1)
        return f"${int(median_value):,}"

    # Median Income Value
    @render.text
    def median_income():
        median_inc = round(filtered_data().median_income.median()*10000, 1)
        return f"${int(median_inc):,}"
    
    # Distribution Plots


    # Comparison Scatterplot


    # Ocean Proximity Boxplot




app = App(app_ui, server)