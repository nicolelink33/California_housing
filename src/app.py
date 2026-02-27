import hashlib
import numpy as np
import pandas as pd
import json
from shiny import App, ui, reactive, render
from shinywidgets import output_widget, render_widget
from ipyleaflet import Map, TileLayer, CircleMarker, Popup, GeoJSON
from ipywidgets import HTML

# Import dataset
processed_data = pd.read_csv("data/processed/housing_with_county.csv")

# Load california counties geojson
with open("data/raw/cal_counties.geojson") as f:
    counties_geojson = json.load(f)

# Page configuration
app_ui = ui.page_fillable(
    ui.panel_title("California Housing"),


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
                    ui.column(6, ui.value_box("Median house value", ui.output_text("median_house"))),
                    ui.column(6, ui.value_box("Median income", ui.output_text("median_income"))),
                ),

                # Map Visualization
                output_widget("map_output")
                
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
    @render.text
    def median_house():
        median_value = round(filtered_data().median_house_value.median(), 1)
        return f"${int(median_value):,}"

    # Median Income Value
    @render.text
    def median_income():
        median_inc = round(filtered_data().median_income.median()*10000, 1)
        return f"${int(median_inc):,}"
    
    # Layered Map
    @render_widget
    def map_output():
        df = filtered_data()
        m = Map(center=(37, -119), zoom=6)

        # Satellite layer (ESRI World Imagery)
        m.add_layer(TileLayer(
            url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attribution='Esri World Imagery'
        ))

        # Selected counties from dashboard
        selected_counties = list(input.county_select() or [])
        selected_counties = [c.strip() for c in selected_counties]

        print("Selected:", selected_counties)
        print("GeoJSON sample:", counties_geojson["features"][0]["properties"]["county"])
        print("DF sample:", df["county"].iloc[0] if not df.empty else "DF EMPTY")


        # Color-blind-friendly palette (Okabe-Ito)
        color_palette = [
            "#E69F00", "#56B4E9", "#009E73", "#F0E442",
            "#0072B2", "#D55E00", "#CC79A7", "#999999"
        ]

        # Map county names to colors
        def get_color(county_name):
            idx = int(hashlib.md5(county_name.encode()).hexdigest(), 16)
            return color_palette[idx % len(color_palette)]
        

        # GeoJSON layer with dynamic fill based on selection
        geo_layer = GeoJSON(
            data=counties_geojson,
            style_function=lambda feature: {
                "color": "white",
                "fillColor": (
                    get_color(feature["properties"]["county"])
                    if len(selected_counties) == 0 or
                    feature["properties"]["county"].strip() in selected_counties
                    else "lightgray"
                ),
                "fillOpacity": (
                    0.6
                    if len(selected_counties) == 0 or
                    feature["properties"]["county"].strip() in selected_counties
                    else 0.1
                ),
                "weight": 1,
            }
        )

        m.add_layer(geo_layer)

        # Add sampled points
        if not df.empty:
            df_sample = df.sample(min(500, len(df)), random_state=42)
            for _, row in df_sample.iterrows():
                circle = CircleMarker(
                    location=(row.latitude, row.longitude),
                    radius=5,
                    color='blue',
                    fill_color='blue',
                    fill_opacity=0.5
                )
                circle.popup = Popup(
                    location=(row.latitude, row.longitude),
                    child=HTML(value=f"County: {row.county}<br>"
                                    f"Median House Value: ${int(row.median_house_value):,}<br>"
                                    f"Median Income: ${int(row.median_income*10000):,}"),
                    close_button=True
                )
                m.add(circle)

        return m
    
        

    
    # Distribution Plots


    # Comparison Scatterplot


    # Ocean Proximity Boxplot




app = App(app_ui, server)