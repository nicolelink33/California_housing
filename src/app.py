import altair as alt
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.ticker import FuncFormatter
from shiny import App, ui, reactive, render
from shinywidgets import output_widget, render_widget
import querychat
from chatlas import ChatGithub
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

# Import dataset
processed_data = pd.read_csv("data/processed/housing_with_county.csv")

# Load california counties geojson
with open("data/raw/cal_counties.geojson") as f:
    counties_geojson = json.load(f)

# Set up querychat
qc = querychat.QueryChat(
    processed_data.copy(),
    "housing",
    greeting="""👋 Ask me anything about California housing prices in 1990.

* <span class="suggestion">Show only houses in San Francisco</span>
* <span class="suggestion">Filter to houses near the ocean</span>
* <span class="suggestion">What was the most expensive house in 1990?</span>
* <span class="suggestion">Which county has the highest median house value?</span>
""",
    data_description="""
California housing values in 1990 (aggregated to approximately 20,000 California housing blocks).
- longitude: longitude in decimal degrees
- latitude: latitude in decimal degrees
- ocean_proximity: "<1H ocean", "Near ocean", "Near bay", "Island", or "Inland"
- housing_median_age: median house age in years
- total_rooms: total number of rooms on the block
- total_bedrooms: total number of bedrooms on the block
- population: total population on the block
- households: total number of households on the block
- median_income: median income of the block
- median_house_value: median house value of the block
- county: name of the block's county
""",
    client=ChatGithub(model="gpt-4.1-mini"),
)


# Page configuration
app_ui = ui.page_fluid(
    ui.tags.style(
        """
        .dashboard-panel {
            padding-left: 0.1rem;
            padding-right: 0.1rem;
        }
        .plot-card {
            padding: 0.1rem;
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            background: #ffffff;
            margin-bottom: 0.1rem;
        }
        @media (max-width: 1200px) {
            .plot-card .shiny-plot-output {
                height: 300px !important;
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


    ui.tags.style("""
        .footer {
            font-size: 0.75rem;
            color: #6c757d;
            text-align: center;
            padding: 4px 0;
            margin: 0;
        }
    """
    ),
    ui.panel_title(
        ui.div(
            ui.h1("California Housing Dashboard"),
            ui.p("Explore how proximity to the ocean and household income related to housing prices across California in 1990.",
            style="font-size:0.95rem; color:#555; margin-bottom:20px;"
            )
        )
    ),

    ui.navset_pill(

        # ── Tab 1: Traditional Dashboard ─────────────────────────────────────────
        ui.nav_panel("Manual Filtering", 

            ui.layout_sidebar(
                # Sidebar inputs
                ui.sidebar(
                    ui.input_action_button("reset_button", "Reset All Filters"),

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
                        value=[round(processed_data.median_income.quantile(0.75),2), round(processed_data.median_income.max(), 2)],
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
                        selected=["<1H OCEAN", "NEAR OCEAN", "NEAR BAY"],
                    ),

                    ui.input_selectize(
                        id="county_select",
                        label="Select County:",
                        choices=sorted(processed_data["county"].dropna().unique()),
                        selected=[],
                        multiple=True
                    ),

                    width=300
                ),
                
                # Page configuration
                ui.layout_columns(
                    # Column 1
                    ui.layout_columns(
                            
                        # Value Boxes
                        ui.layout_column_wrap(
                            ui.output_ui("median_house"),
                            ui.output_ui("median_income"),
                            width=1/2,
                            heights_equal="all",
                            fill=True
                        ),

                        # Map Visualization
                        ui.card(
                            ui.card_header("Geographic Distribution"),
                            ui.output_ui("geo_cluster_container", fill=True),
                            output_widget("geo_cluster_plot"),
                            full_screen=True, # Allows users to expand the map
                            min_height="720px",
                            #fill=True,
                        ),
                        col_widths=12,
                        # row_heights=["150px", "1fr"],
                        class_="dashboard-panel",
                    ),
                    # Column 2
                    ui.layout_column_wrap(
                        
                        # Distribution Plots
                        ui.card(
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
                            ui.output_plot("distribution_plot"),
                            min_height="200px",
                            class_="plot-card",
                        ),

                        # Comparison Scatterplot
                        ui.card(
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
                            ui.output_plot("comparison_scatter"),
                            min_height="200px",
                            class_="plot-card",
                        ),

                        # Ocean Proximity Boxplots
                        ui.card(
                            ui.output_plot("boxplot_proximity"),
                            min_height="200px",
                            class_="plot-card",
                        ),
                        width=1,
                        #min_height="900px",
                        class_="dashboard-panel",
                    ),
                    col_widths=[8, 4]
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
        ),

        # ── Tab 2: LLM Chat ───────────────────────────────────────────────────────
        ui.nav_panel(
            "AI Chatbot",
            ui.layout_sidebar(
                qc.sidebar(),
                ui.card(
                    ui.card_header(ui.output_text("chat_title")),
                    ui.output_data_frame("chat_table"),
                    ui.output_ui("download_button_ui"),
                    fill=True,
                ),
                fillable=True,
            ),


        ),

        id="tab",
        
        #ui.nav_menu(
        #    
        #)
    ),

)


def server(input, output, session):
    # ── Tab 1: reactive calcs ─────────────────────────────────────────────────
    @reactive.effect
    @reactive.event(input.reset_button)
    def _():
        # Reset Sliders
        ui.update_slider("house_val_slider", value=[processed_data.median_house_value.min(), processed_data.median_house_value.max()])
        ui.update_slider("income_slider", value=[processed_data.median_income.min(), processed_data.median_income.max()])
        ui.update_slider("age_slider", value=[processed_data.housing_median_age.min(), processed_data.housing_median_age.max()])
        ui.update_slider("rooms_slider", value=[processed_data.total_rooms.min(), processed_data.total_rooms.max()])
        ui.update_slider("beds_slider", value=[processed_data.total_bedrooms.min(), processed_data.total_bedrooms.max()])
        ui.update_slider("pop_slider", value=[processed_data.population.min(), processed_data.population.max()])
        ui.update_slider("households_slider", value=[processed_data.households.min(), processed_data.households.max()])
        
        # Reset Checkbox Group
        ui.update_checkbox_group("ocean_checkbox", selected=["<1H OCEAN", "NEAR OCEAN", "NEAR BAY", "ISLAND", "INLAND"])
        
        # Reset Selectize (County)
        ui.update_selectize("county_select", selected=[])

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

        x_min = min(state_vals.min(), selected_vals.min())
        x_max = max(state_vals.max(), selected_vals.max())
        if x_min == x_max:
            x_max = x_min + 1.0
        x_grid = np.linspace(x_min, x_max, 256)

        # Use KDE when variance exists; otherwise fall back to a reference line.
        if state_vals.nunique() > 1:
            state_kde = gaussian_kde(state_vals)
            ax.plot(x_grid, state_kde(x_grid), color="#8e6bbd", linewidth=2, label="State")
            ax.fill_between(x_grid, state_kde(x_grid), color="#8e6bbd", alpha=0.20)
        else:
            ax.axvline(state_vals.iloc[0], color="#8e6bbd", linewidth=2, label="State")

        if selected_vals.nunique() > 1:
            selected_kde = gaussian_kde(selected_vals)
            ax.plot(x_grid, selected_kde(x_grid), color="#9acb5b", linewidth=2, label="Selected")
            ax.fill_between(x_grid, selected_kde(x_grid), color="#9acb5b", alpha=0.20)
        else:
            ax.axvline(selected_vals.iloc[0], color="#9acb5b", linewidth=2, label="Selected")

        ax.set_xlabel(pretty_names[metric])
        ax.set_ylabel("Density", labelpad=4)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x/1000:,.0f}k"))
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


    # ── Tab 2: querychat ──────────────────────────────────────────────────────
    qc_vals = qc.server()

    @reactive.calc
    def querychat_filtered_df():
        return processed_data.head(10) # placeholder for reactive querychat filtered df 
    
    @render.ui
    def download_button_ui():
        df = querychat_filtered_df()

        if df is None or df.empty:
            return None  # hide button if no data

        return ui.download_button(
            id="download_querychat_filtered_df",
            label="Download Filtered Data (CSV)"
        )

    @render.download(filename="california_housing_filtered.csv")
    def download_querychat_filtered_df():
        df = querychat_filtered_df()

        if df is None or df.empty:
            return None

        yield df.to_csv(index=False)

    @render.text
    def chat_title():
        return "placeholder text"

    @render.data_frame
    def chat_table():
        return "placeholder dataframe"


app = App(app_ui, server)
