import altair as alt
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
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
    ui.tags.style(
        """
        .dashboard-panel {
            padding-left: 0.1rem;
            padding-right: 0.1rem;
        }
        .plot-card {
            padding: 0.75rem;
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            background: #ffffff;
            margin-bottom: 0.75rem;
        }
        @media (max-width: 1200px) {
            .plot-card .shiny-plot-output {
                height: 230px !important;
            }
        }
        @media (max-width: 992px) {
            .dashboard-panel {
                padding-left: 0.2rem;
                padding-right: 0.2rem;
                width: 100% !important;
                flex: 0 0 100% !important;
                max-width: 100% !important;
            }
        }
        """
    ),


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
            ui.column(8,
                      
                # Value Boxes
                ui.row(
                    ui.column(
                        6,
                        ui.value_box(
                            "Median house value",
                            ui.output_text("median_house"),
                            style="min-height: 150px; padding: 0.75rem; font-size: 0.9rem; line-height: 1.2;",
                        ),
                        style="padding-left: 0.3rem; padding-right: 0.3rem;",
                    ),
                    ui.column(
                        6,
                        ui.value_box(
                            "Median income",
                            ui.output_text("median_income"),
                            style="min-height: 150px; padding: 0.75rem; font-size: 0.9rem; line-height: 1.2;",
                        ),
                        style="padding-left: 0.3rem; padding-right: 0.3rem;",
                    ),
                    style="margin-left: 0; margin-right: 0;",
                ),

                # Map Visualization
                output_widget("geo_cluster_plot"),
                
                class_="dashboard-panel",
            ),
            # Column 2
            ui.column(4,
                
                # Distribution Plots
                ui.div(
                    ui.input_select(
                        id="distribution_var",
                        label="Distribution:",
                        choices={
                            "median_house_value": "Median House Value",
                            "median_income": "Median Income",
                            "housing_median_age": "House Age",
                            "total_rooms": "Total Rooms",
                            "total_bedrooms": "Total Bedrooms",
                            "population": "Population",
                            "households": "Households",
                        },
                        selected="median_house_value",
                    ),
                    ui.output_plot("distribution_plot", width="100%", height="260px"),
                    class_="plot-card",
                ),

                # Comparison Scatterplot
                ui.div(
                    ui.input_select(
                        id="comparison_var",
                        label="Comparison:",
                        choices={
                            "median_income": "Median Income",
                            "housing_median_age": "House Age",
                            "total_rooms": "Total Rooms",
                            "total_bedrooms": "Total Bedrooms",
                            "population": "Population",
                            "households": "Households",
                        },
                        selected="median_income",
                    ),
                    ui.output_plot("comparison_scatter", width="100%", height="260px"),
                    class_="plot-card",
                ),

                # Ocean Proximity Boxplots
                ui.div(
                    ui.output_plot("boxplot_proximity", width="100%", height="260px"),
                    class_="plot-card",
                ),
                class_="dashboard-panel",
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
                width="container",
                height=420,
                title="Geographic Distribution of Housing Values"
            )
            .interactive()
            
            # .add_selection(zoom)
        )

        return chart


    
    # Distribution Plots
    @render.plot
    def distribution_plot():
        df = filtered_data()
        metric = input.distribution_var()
        fig, ax = plt.subplots(figsize=(5.0, 2.6))

        pretty_names = {
            "median_house_value": "Median House Value",
            "median_income": "Median Income",
            "housing_median_age": "House Age",
            "total_rooms": "Total Rooms",
            "total_bedrooms": "Total Bedrooms",
            "population": "Population",
            "households": "Households",
        }

        selected_vals = df[metric].dropna()
        state_vals = processed_data[metric].dropna()

        if selected_vals.empty:
            ax.text(0.5, 0.5, "No data for current filters", ha="center", va="center")
            ax.set_axis_off()
            return fig

        ax.hist(state_vals, bins=35, density=True, alpha=0.45, color="#8e6bbd", label="State")
        ax.hist(selected_vals, bins=35, density=True, alpha=0.45, color="#9acb5b", label="Selected")
        ax.set_xlabel(pretty_names[metric])
        ax.set_ylabel("Density", labelpad=4)
        ax.legend(frameon=False, fontsize=8)
        ax.grid(alpha=0.2)
        ax.tick_params(axis="both", labelsize=8)
        fig.subplots_adjust(left=0.22, right=0.98, top=0.95, bottom=0.22)
        return fig

    # Comparison Scatterplot
    @render.plot
    def comparison_scatter():
        df = filtered_data()
        x_col = input.comparison_var()
        fig, ax = plt.subplots(figsize=(5.0, 2.6))

        pretty_names = {
            "median_income": "Median Income",
            "housing_median_age": "House Age",
            "total_rooms": "Total Rooms",
            "total_bedrooms": "Total Bedrooms",
            "population": "Population",
            "households": "Households",
        }

        if df.empty:
            ax.text(0.5, 0.5, "No data for current filters", ha="center", va="center")
            ax.set_axis_off()
            return fig

        plot_df = df.sample(min(5000, len(df)), random_state=42)
        ax.scatter(
            plot_df[x_col],
            plot_df["median_house_value"],
            s=8,
            alpha=0.25,
            color="#4e79a7",
            edgecolors="none",
        )
        ax.set_xlabel(pretty_names[x_col])
        ax.set_ylabel("Median House Value", labelpad=4)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x/1000:,.0f}k"))
        ax.grid(alpha=0.2)
        ax.tick_params(axis="both", labelsize=8)
        fig.subplots_adjust(left=0.22, right=0.98, top=0.95, bottom=0.22)
        return fig

    # Ocean Proximity Boxplot
    @render.plot
    def boxplot_proximity():
        df = filtered_data()
        fig, ax = plt.subplots(figsize=(5.0, 2.6))

        if df.empty:
            ax.text(0.5, 0.5, "No data for current filters", ha="center", va="center")
            ax.set_axis_off()
            return fig

        order = ["<1H OCEAN", "INLAND", "NEAR OCEAN", "NEAR BAY", "ISLAND"]
        present = [c for c in order if c in df["ocean_proximity"].dropna().unique()]
        data = [df.loc[df["ocean_proximity"] == c, "median_house_value"].dropna() for c in present]

        if not present or all(series.empty for series in data):
            ax.text(0.5, 0.5, "No data for current filters", ha="center", va="center")
            ax.set_axis_off()
            return fig

        label_map = {
            "<1H OCEAN": "<1H Ocean",
            "INLAND": "Inland",
            "NEAR OCEAN": "Near Ocean",
            "NEAR BAY": "Near Bay",
            "ISLAND": "Island",
        }
        display_labels = [label_map[c] for c in present]

        bp = ax.boxplot(
            data,
            labels=display_labels,
            patch_artist=True,
            showfliers=False,
            medianprops={"color": "#222222", "linewidth": 1.5},
            whiskerprops={"linewidth": 1.1},
            capprops={"linewidth": 1.1},
        )
        colors = ["#f4a259", "#4e79a7", "#59a14f", "#9c6ade", "#e15759"]
        for patch, color in zip(bp["boxes"], colors[: len(present)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
            patch.set_edgecolor("#4a4a4a")
            patch.set_linewidth(0.9)

        ax.set_xlabel("Ocean Proximity")
        ax.set_ylabel("Median House Value", labelpad=4)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x/1000:,.0f}k"))
        ax.grid(alpha=0.2, axis="y")
        ax.tick_params(axis="x", labelsize=8, rotation=90)
        for tick in ax.get_xticklabels():
            tick.set_horizontalalignment("center")
            tick.set_verticalalignment("top")
        ax.tick_params(axis="y", labelsize=8)
        fig.subplots_adjust(left=0.22, right=0.98, top=0.95, bottom=0.30)
        return fig




app = App(app_ui, server)
