import altair as alt
import numpy as np
import pandas as pd
import json
from shiny import App, ui, reactive, render
from shinywidgets import output_widget, render_widget

# Import dataset
processed_data = pd.read_csv("data/processed/housing_with_county.csv")

# Load california counties geojson
with open("data/raw/cal_counties.geojson") as f:
    counties_geojson = json.load(f)

# Page configuration
app_ui = ui.page_fillable(
    ui.panel_title("California Housing"),

    # CSS styling
    ui.tags.style("""
        html, body {
            height: 100%;
            margin: 0;
        }

        .fillable {
            padding-bottom: 0 !important;
        }

        .footer {
            font-size: 0.75rem;
            color: #6c757d;
            text-align: center;
            padding: 4px 0;
            margin: 0;
        }
    """),

    ui.layout_sidebar(
        # Sidebar inputs
        ui.sidebar(
            ui.input_slider(
                id="house_val_slider",
                label="Median house value:",
                min=processed_data.median_house_value.min(),
                max=processed_data.median_house_value.max(),
                value=[processed_data.median_house_value.min(), processed_data.median_house_value.max()],
            ),

            ui.input_slider(
                id="income_slider",
                label="Median income:",
                min=processed_data.median_income.min(),
                max=processed_data.median_income.max(),
                value=[processed_data.median_income.min(), processed_data.median_income.max()],
            ),
            ui.input_slider(
                id="age_slider",
                label="House age:",
                min=processed_data.housing_median_age.min(),
                max=processed_data.housing_median_age.max(),
                value=[processed_data.housing_median_age.min(), processed_data.housing_median_age.max()],
            ),
            ui.input_slider(
                id="rooms_slider",
                label="Total rooms:",
                min=processed_data.total_rooms.min(),
                max=processed_data.total_rooms.max(),
                value=[processed_data.total_rooms.min(), processed_data.total_rooms.max()],
            ),
            ui.input_slider(
                id="beds_slider",
                label="Total bedrooms:",
                min=processed_data.total_bedrooms.min(),
                max=processed_data.total_bedrooms.max(),
                value=[processed_data.total_bedrooms.min(), processed_data.total_bedrooms.max()],
            ),
            ui.input_slider(
                id="pop_slider",
                label="Population:",
                min=processed_data.population.min(),
                max=processed_data.population.max(),
                value=[processed_data.population.min(), processed_data.population.max()],
            ),
            ui.input_slider(
                id="households_slider",
                label="Households:",
                min=processed_data.households.min(),
                max=processed_data.households.max(),
                value=[processed_data.households.min(), processed_data.households.max()],
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
            ),

            ui.input_selectize(
                id="county_select",
                label="Select County:",
                choices=sorted(processed_data["county"].dropna().unique()),
                selected=[],
                multiple=True
            )
        ),
        
        # Page configuration
        ui.layout_columns(
            # Column 1
            ui.column(10,
                      
                # Value Boxes
                ui.row(
                    ui.column(6, ui.output_ui("median_house")),
                    ui.column(6, ui.output_ui("median_income")),
                ),

                # Map Visualization
                output_widget("geo_cluster_plot")
                
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
        
    ),

    ui.div(
            "California Housing: A dashboard that facilitates investigation of California housing prices in 1990.  |  ", 
            "Authors: Ali Boloor Foroosh, Fu Hung (Teem) Kwong, Nicole Link, Shrabanti Bala Joya  |  ", 
            ui.a("GitHub Repository",
                href="https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing",
                target="_blank"),
            "  |  Last updated: Feb 28, 2026",
            class_="footer"
            )

)


def server(input, output, session):
    # Filter dataset
    @reactive.calc
    def filtered_data():
        idx_house_val = processed_data.median_house_value.between(
            left=input.house_val_slider()[0], right=input.house_val_slider()[1], inclusive="both"
        )
        idx_income = processed_data.median_income.between(
            left=input.income_slider()[0], right=input.income_slider()[1], inclusive="both"
        )
        idx_age = processed_data.housing_median_age.between(
            left=input.age_slider()[0], right=input.age_slider()[1], inclusive="both"
        )
        idx_rooms = processed_data.total_rooms.between(
            left=input.rooms_slider()[0], right=input.rooms_slider()[1], inclusive="both"
        )
        idx_beds = processed_data.total_bedrooms.between(
            left=input.beds_slider()[0], right=input.beds_slider()[1], inclusive="both"
        )
        idx_pop = processed_data.population.between(
            left=input.pop_slider()[0], right=input.pop_slider()[1], inclusive="both"
        )
        idx_households = processed_data.households.between(
            left=input.households_slider()[0], right=input.households_slider()[1], inclusive="both"
        )
        idx_ocean = processed_data.ocean_proximity.isin(input.ocean_checkbox())

        # Selected counties from dashboard
        selected_counties = list(input.county_select() or [])
        selected_counties = [c.strip() for c in selected_counties] 

        idx_county = (
            processed_data.county.isin(selected_counties)
            if selected_counties else pd.Series(True, index=processed_data.index)
            )

        return processed_data[idx_house_val & idx_income & idx_age & idx_rooms & idx_beds & idx_pop & idx_households & idx_ocean & idx_county]

    # Median House Value
    @render.ui
    def median_house():
        filt_value = round(filtered_data().median_house_value.median(), 1)
        state_value = round(processed_data.median_house_value.median(), 1)

        diff = round(((filt_value - state_value) / state_value) * 100, 1)
        if diff > 0:
            arrow = "↑"
        elif diff < 0:
            arrow = "↓"
        else: 
            arrow = ""
        
        percent_text = ui.span(
            f"{arrow} {abs(diff)}% from state median" if arrow else f"{diff}% from state median house value",
            style="font-size:0.85rem;"
        )

        return ui.value_box(
            "Median house value",
            f"${int(filt_value):,}",
            percent_text
        )

    # Median Income Value
    @render.ui
    def median_income():
        filt_value = round(filtered_data().median_income.median() * 10000, 1)
        state_value = round(processed_data.median_income.median() * 10000, 1)

        diff = round(((filt_value - state_value) / state_value) * 100, 1)
        if diff > 0:
            arrow = "↑"
        elif diff < 0:
            arrow = "↓"
        else: 
            arrow = ""
        
        percent_text = ui.span(
            f"{arrow} {abs(diff)}% from state median" if arrow else f"{diff}% from state median income",
            style="font-size:0.85rem;"
        )

        return ui.value_box(
            "Median income",
            f"${int(filt_value):,}",
            percent_text
        )
    
    @render_widget
    def geo_cluster_plot():
        df = filtered_data()

        if df.empty:
            return None

        df_sample = df.sample(min(5000, len(df)), random_state=42)

        df_sample = df_sample.replace([np.inf, -np.inf], np.nan)
        df_sample = df_sample.fillna(0)

        # County background layer
        counties = alt.Chart(
            alt.Data(values=counties_geojson["features"])
        ).mark_geoshape(
            fill="lightgray",
            stroke="white",
            strokeWidth=0.5
        ).encode(
            tooltip=alt.value(None)
        )
        
        # brush = alt.selection_interval()
        
        # Housing points layer
        points = (
            alt.Chart(df_sample)
            .mark_circle(opacity=0.35)
            .encode(
                longitude="longitude:Q",
                latitude="latitude:Q",
                color=alt.Color(
                    "median_house_value:Q",
                    scale=alt.Scale(scheme="viridis"),
                    title="Median House Value"
                ),
                tooltip=[
                    alt.Tooltip("county:N", title="County"),
                    alt.Tooltip("median_house_value:Q", title="Median House Value", format=",.0f"),
                    alt.Tooltip("median_income:Q", title="Median Income (10k USD)", format=",.2f")
                ]
            )
            #.add_params(brush)
        )

        # Combined

        chart = (
            (counties + points)
            .project(type="mercator")
            .properties(
                width=700,
                height=500,
                title="Geographic Distribution of Housing Values"
            )
            .interactive()
            
            # .add_selection(zoom)
        )

        return chart


    
    # Distribution Plots


    # Comparison Scatterplot


    # Ocean Proximity Boxplot




app = App(app_ui, server)