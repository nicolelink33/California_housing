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
import sys
from pathlib import Path

import folium
from folium.plugins import MarkerCluster
import ibis
from ibis import _, literal
import duckdb

# Set up utils path to work both locally and on Posit Connect
src_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from utils import apply_filters

load_dotenv(Path(__file__).parent / ".env")

# Import dataset and convert to parquet - for filtering
con = ibis.duckdb.connect() 
parquet = con.read_parquet("data/processed/housing_with_county.parquet", table_name="housing")

# Load whole dataset to use in querychat: 
state_df = parquet.execute()
#processed_data = pd.read_csv("data/processed/housing_with_county.csv")

# Compute state medians
state_median_house_value = parquet.median_house_value.median().to_pandas()
state_median_income = parquet.median_income_usd.median().to_pandas()

# Compute dataset min and maxes to use as filter inputs
House_min = int(parquet.median_house_value.min().to_pandas())
House_max = int(parquet.median_house_value.max().to_pandas())

Age_min = int(parquet.housing_median_age.min().to_pandas())
Age_max = int(parquet.housing_median_age.max().to_pandas())

Rooms_min = int(parquet.total_rooms.min().to_pandas())
Rooms_max = int(parquet.total_rooms.max().to_pandas())

Beds_min = int(parquet.total_bedrooms.min().to_pandas())
Beds_max = int(parquet.total_bedrooms.max().to_pandas())

county_list = (
    parquet
    .filter(parquet.county.notnull())  # 1. Filter nulls
    .select("county")                  # 2. Keep it as a Table object
    .distinct()                        # 3. Now distinct works on the Table
    .order_by("county")                 # 4. Use sort_by for Table objects
    .to_pandas()                       # 5. Convert to Pandas
    ["county"]                         # 6. Grab the column from the resulting DF
    .tolist()                          # 7. Final List
)

Income_min = int(parquet.median_income_usd.min().to_pandas())
Income_75q = int(parquet.median_income_usd.quantile(0.75).to_pandas())
Income_max = int(parquet.median_income_usd.max().to_pandas())

Pop_min = int(parquet.population.min().to_pandas())
Pop_max = int(parquet.population.max().to_pandas())

Households_min = int(parquet.households.min().to_pandas())
Households_max = int(parquet.households.max().to_pandas())


# Convert median_income from 10k USD to USD
#processed_data["median_income_usd"] = processed_data["median_income"] * 10000
#processed_data = processed_data.mutate(median_income_usd = processed_data.median_income * 10000)

# Load california counties geojson
with open("data/raw/cal_counties.geojson") as f:
    counties_geojson = json.load(f)

# Set up querychat
qc = querychat.QueryChat(
    state_df,
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

def create_median_house_value_box(df):
    if df is None or df.empty or "median_house_value" not in df.columns:
        return ui.value_box("Median house value", "N/A", "No data available")

    filt_value = round(df.median_house_value.median(), 1)

    diff = round(((filt_value - state_median_house_value) / state_median_house_value) * 100, 1)
    if diff > 0:
        arrow = "↑"
    elif diff < 0:
        arrow = "↓"
    else: 
        arrow = ""

    content = ui.div(
        ui.div(
            f"${int(filt_value):,}",
        ),
        ui.div(
            f"{arrow} {abs(diff)}% from state median" if arrow else f"{diff}% from state median house value",
            style="font-size:0.8rem;"
        )
    )

    return ui.value_box(
        "Median house value",
        content,
    )

# Median Income Value
def create_median_income_box(df):
    if df is None or df.empty or "median_income_usd" not in df.columns:
        return ui.value_box("Median income", "N/A", "No data available")

    filt_value = round(df.median_income_usd.median(), 1)

    diff = round(((filt_value - state_median_income) / state_median_income) * 100, 1)
    if diff > 0:
        arrow = "↑"
    elif diff < 0:
        arrow = "↓"
    else: 
        arrow = ""
    
    content = ui.div(
        ui.div(
            f"${int(filt_value):,}",
        ),
        ui.div(
            f"{arrow} {abs(diff)}% from state median" if arrow else f"{diff}% from state median income",
            style="font-size:0.8rem;"
        )
    )

    return ui.value_box(
        "Median income",
        content,
    )

def create_distribution_plot(df, metric, state_data=state_df):
    fig, ax = plt.subplots(figsize=(5.0, 2.6))
    ax.ticklabel_format(axis='y', style='plain')

    pretty_names = {
        "median_house_value": "Median House Value",
        "median_income": "Median Income",
        "housing_median_age": "House Age",
        "total_rooms": "Total Rooms",
        "total_bedrooms": "Total Bedrooms",
        "population": "Population",
        "households": "Households",
    }

    metric_to_use = "median_income_usd" if metric == "median_income" else metric

    selected_vals = df[metric_to_use].dropna()
    state_vals = state_data[metric_to_use].dropna()

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

    ax.set_xlabel(pretty_names.get(metric_to_use, metric_to_use))
    ax.set_ylabel("Density", labelpad=4)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x/1000:,.0f}k"))
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.2)
    ax.yaxis.offsetText.set_visible(False)
    ax.tick_params(axis="both", labelsize=8)
    fig.subplots_adjust(left=0.22, right=0.98, top=0.95, bottom=0.22)
    return fig

def create_geo_cluster_plot(df):
    if df.empty:
        return None

    m = folium.Map(location=[36.7, -119.4], zoom_start=6, tiles=None)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite",
        overlay=False,
        control=True,
    ).add_to(m)

    folium.TileLayer("OpenStreetMap", name="Street Map").add_to(m)

    folium.GeoJson(
        counties_geojson,
        name="Counties",
        style_function=lambda feature: {
            "fillColor": "#f0f0f0",
            "color": "#444444",
            "weight": 1.2,
            "fillOpacity": 0.15,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["county"],
            aliases=["County:"],
            sticky=False,
        ),
    ).add_to(m)

    marker_cluster = MarkerCluster(name="Housing blocks").add_to(m)

    for _, row in df.iterrows():
        color = house_value_color(row["median_house_value"]) 
        popup_html = (
            f"<b>County:</b> {row['county']}<br>"
            f"<b>Median House Value:</b> ${row['median_house_value']:,}<br>"
            f"<b>Median Income:</b> ${row['median_income_usd']:,.0f}"
        )
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            color=color,  
            fill=True,
            fill_color=color,   
            fill_opacity=0.75,
            popup=folium.Popup(popup_html, max_width=220),
        ).add_to(marker_cluster)

    sw = [df["latitude"].min(), df["longitude"].min()]
    ne = [df["latitude"].max(), df["longitude"].max()]
    m.fit_bounds([sw, ne], max_zoom=12)

    legend_html = """
        <div style="
            position: fixed; bottom: 30px; left: 30px; z-index: 1000;
            background: white; padding: 10px 14px; border-radius: 8px;
            border: 1px solid #ccc; font-size: 12px; line-height: 1.8;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.2);">
        <b>Median House Value</b><br>
        <span style="color:#2166ac;">&#9632;</span> &lt; $100k<br>
        <span style="color:#74add1;">&#9632;</span> $100k – $150k<br>
        <span style="color:#fee090;">&#9632;</span> $150k – $200k<br>
        <span style="color:#f46d43;">&#9632;</span> $200k – $300k<br>
        <span style="color:#d73027;">&#9632;</span> &gt; $300k
        </div>
        """
    m.get_root().html.add_child(folium.Element(legend_html))

    folium.LayerControl().add_to(m)

    map_html = m._repr_html_()
    map_html = map_html.replace(
        '<div style="width:100%;">',
        '<div class="map-container-outer" style="width:100%;height:100%;">',
        1,
    )
    map_html = map_html.replace(
        'div style="position:relative;width:100%;height:0;padding-bottom:60%;"',
        'div class="map-container-inner" style="position:relative;width:100%;height:100%;min-height:300px;"',
        1,
    )
    return map_html

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
        .querychat-sidebar {
            height: 1000px;
            overflow-y: auto !important; /* Enable vertical scrolling */
        }
        .map-card-full {
            padding: 0 !important;
            margin: 0 !important;
            overflow: hidden;
        }
        .map-card-full .bslib-card-body,
        .map-card-full .card-body {
            padding: 0 !important;
            margin: 0 !important;
            height: 100%;
        }
        .map-card-full > div,
        .map-card-full .shiny-html-output,
        .map-card-full .html-fill-container,
        .map-card-full .html-fill-item,
        .map-card-full [class*="card-body"],
        .map-card-full [class*="html-fill"] {
            height: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        .map-container-outer {
            width: 100% !important;
            height: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        .map-container-inner {
            position: relative !important;
            width: 100% !important;
            height: 100% !important;
            min-height: 300px !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        .map-container-inner iframe {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
        }
        .map-container-inner > span {
            display: none !important;
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
            padding: 2px 0;
            margin: 0;
            line-height: 1.2;
        }
        .footer p {
            margin: 0;
        }
    """
    ),
    ui.panel_title(
        ui.div(
            ui.h1("California Housing Dashboard"),
            ui.p("Explore how proximity to the ocean and household income related to housing prices across California in 1990 using census block-level housing data.",
            style="font-size:0.95rem; color:#555; margin-bottom:20px;"
            )
        )
    ),

    ui.navset_pill(

        # ── Tab 1: Traditional Dashboard ─────────────────────────────────────────
        ui.nav_panel("Dashboard", 

            ui.layout_sidebar(
                # Sidebar inputs
                ui.sidebar(

                    ui.input_action_button("reset_button", "Reset All Filters"),

                    ui.accordion(
                        ui.accordion_panel(
                            ui.HTML("""
                                House Properties
                                <span style="
                                    cursor:default; margin-left:6px;
                                    display:inline-flex; align-items:center; justify-content:center;
                                    width:14px; height:14px; border-radius:50%;
                                    border:1.5px solid #888; color:#888;
                                    font-size:10px; font-weight:bold;
                                    line-height:1; vertical-align:middle;"
                                    title="All measures are aggregated at the census block level.">
                                    i
                                </span>
                            """),
                            
                            ui.input_slider(
                                id="house_val_slider",
                                label="Median house value:",
                                min=House_min,
                                max=House_max,
                                value=[House_min, House_max],
                            ),
                            ui.input_slider(
                                id="age_slider",
                                label="House age:",
                                min=Age_min,
                                max=Age_max,
                                value=[Age_min, Age_max],
                                step=1,
                            ),
                            ui.input_slider(
                                id="rooms_slider",
                                label="Total rooms:",
                                min=Rooms_min,
                                max=Rooms_max,
                                value=[Rooms_min, Rooms_max],
                                step=1,
                            ),
                            ui.input_slider(
                                id="beds_slider",
                                label="Total bedrooms:",
                                min=Beds_min,
                                max=Beds_max,
                                value=[Beds_min, Beds_max],
                                step=1,
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
                                label="County:",
                                choices=county_list,
                                selected=[],
                                multiple=True
                            ),
                            value="house_properties",
                        ),
                        ui.accordion_panel(

                            ui.HTML("""
                                Socio-economic Properties
                                <span style="
                                    cursor:default; margin-left:6px;
                                    display:inline-flex; align-items:center; justify-content:center;
                                    width:14px; height:14px; border-radius:50%;
                                    border:1.5px solid #888; color:#888;
                                    font-size:10px; font-weight:bold;
                                    line-height:1; vertical-align:middle;"
                                    title="All measures are aggregated at the census block level.">
                                    i
                                </span>
                            """),
                            
                            ui.input_slider(
                                id="income_slider",
                                label="Median income:",
                                min=Income_min,
                                max=Income_max,
                                value=[Income_75q, Income_max],
                                step=0.01,
                            ),
                            ui.input_slider(
                                id="pop_slider",
                                label="Population:",
                                min=Pop_min,
                                max=Pop_max,
                                value=[Pop_min, Pop_max],
                                step=1,
                            ),
                            ui.input_slider(
                                id="households_slider",
                                label="Households:",
                                min=Households_min,
                                max=Households_max,
                                value=[Households_min, Households_max],
                                step=1,
                            ),

                            value="socio_economic"
                        ),
                        id="filters_accordion",
                        open=True,
                        multiple=True,
                    ),
                    width=300
                ),
                
                # Page configuration

                ui.layout_columns(
                    # County banner — full width above all columns
                    ui.card(
                        ui.output_ui("county_banner"),
                        class_="p-2",
                        max_height="50px",
                    ),
                    col_widths=12,
                ),

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
                            ui.div(
                                ui.output_ui("geo_cluster_plot"),
                                ui.div(
                                    ui.input_action_button("reset_map_btn", "Reset View", class_="btn-sm"),
                                    style="position:absolute;top:90px;left:10px;z-index:1000;",
                                ),
                                style="position:relative;height:100%;width:100%;min-height:400px;",
                            ),
                            full_screen=True,
                            height="100%",
                            fill=True,
                            class_="map-card-full p-0",
                        ),
                        col_widths=12,
                        row_heights=["200px", "1fr"],
                        class_="dashboard-panel",
                    ),
                    # Column 2
                    ui.layout_column_wrap(
                        
                        # Distribution Plots
                        ui.card(
                            ui.card_header("State vs Selected Data Distribution:"),
                            ui.input_select(
                                id="distribution_var",
                                label=None,
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
                            max_height="350px",
                            class_="plot-card",
                        ),

                        # Comparison Scatterplot
                        ui.card(
                            ui.card_header("Median House Value versus:"),
                            ui.input_select(
                                id="comparison_var",
                                label=None,
                                choices={
                                    "median_income": "Median Income",
                                    #"housing_median_age": "House Age",
                                    "total_rooms": "Total Rooms",
                                    #"total_bedrooms": "Total Bedrooms",
                                    #"population": "Population",
                                    "households": "Households",
                                },
                                selected="median_income",
                            ),
                            ui.output_plot("comparison_scatter"),
                            max_height="350px",
                            class_="plot-card",
                        ),

                        # Ocean Proximity Boxplots
                        ui.card(
                            ui.card_header("Median House Value by Ocean Proximity:"),
                            ui.output_plot("boxplot_proximity"),
                            max_height="350px",
                            class_="plot-card",
                        ),
                        width=1,
                        class_="dashboard-panel",
                    ),
                    col_widths=[8, 4]
                ),
                style="display:flex; flex-direction:column; gap:0;",
                
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
            ui.page_sidebar(
                qc.sidebar(),

                ui.card(
                    ui.card_header(ui.output_text("chat_title")),
                    ui.output_data_frame("chat_table"),
                    ui.output_ui("download_button_ui"),
                    height="400px",
                ),
                ui.layout_columns(
                    ui.card(
                        ui.output_ui("querychat_geo_cluster_plot"),
                        full_screen=True,
                    ),

                    ui.div(
                        # Top part of right column
                        ui.card(
                            ui.output_ui("querychat_median_house"),
                            ui.output_ui("querychat_median_income"),
                            height="280px", # Fixed height to ensure split
                        ),
                        # Bottom part of right column
                        ui.card(
                            ui.input_select(
                                id="querychat_distribution_var",
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
                            ui.output_plot("querychat_distribution_plot"),
                            height="320px",
                            class_="plot-card",
                        ),
                        class_="d-flex flex-column gap-3" # Bootstrap classes for vertical spacing
                    ),
                    col_widths=(8, 4), # This sets the 2/3 and 1/3 ratio
                    height="600px",
                ),
            ),
        ),

        id="tab",
    ),

)
# Helper function to assign colors based on house value ranges
def house_value_color(value):
    if value < 100_000:
        return "#2166ac"   # cheapest
    elif value < 150_000:
        return "#74add1" 
    elif value < 200_000:
        return "#fee090"  
    elif value < 300_000:
        return "#f46d43"  
    else:
        return "#d73027"   # most expensive

def server(input, output, session):

    # ── Tab 1: reactive calcs ─────────────────────────────────────────────────
    
    # Reactive value to hold counties selected via map clicks.
    # Plain click - replace selection with that county.
    # Shift+click - toggle that county in/out of the current selection.
    selected_counties_rv = reactive.value([])

    @reactive.effect
    @reactive.event(input.reset_button)
    def _():
        # Reset Sliders
        ui.update_slider("house_val_slider", value=[House_min, House_max])
        ui.update_slider("income_slider", value=[Income_75q, Income_max])
        ui.update_slider("age_slider", value=[Age_min, Age_max])
        ui.update_slider("rooms_slider", value=[Rooms_min, Rooms_max])
        ui.update_slider("beds_slider", value=[Beds_min, Beds_max])
        ui.update_slider("pop_slider", value=[Pop_min, Pop_max])
        ui.update_slider("households_slider", value=[Households_min, Households_max])
        
        # Reset Checkbox Group
        ui.update_checkbox_group("ocean_checkbox", selected=["<1H OCEAN", "NEAR OCEAN", "NEAR BAY"])
        
        # Reset Selectize (County)
        ui.update_selectize("county_select", selected=[])

        # Clear map-click county selection on reset
        selected_counties_rv.set([])

    # Handle county click events fired from the Folium map
    @reactive.effect
    @reactive.event(input.map_county_click)
    def _handle_map_county_click():
        event = input.map_county_click()
        if not event or "county" not in event:
            return
        clicked = event["county"]
        shift_held = event.get("shift", False)
        current = list(selected_counties_rv())
        if shift_held:
            # Shift+click: toggle the clicked county in/out of the selection
            if clicked in current:
                current.remove(clicked)
            else:
                current.append(clicked)
            selected_counties_rv.set(current)
        else:
            # Plain click: if the county is already the sole selection, deselect it;
            # otherwise replace the selection with just this county
            if current == [clicked]:
                selected_counties_rv.set([])
            else:
                selected_counties_rv.set([clicked])
        # Keep the county_select dropdown in sync with the map selection
        ui.update_selectize("county_select", selected=selected_counties_rv())

    # Filter dataset
    @reactive.calc
    def filtered_expr():
        return apply_filters(
            parquet,
            house_val_range=input.house_val_slider(),
            income_range=input.income_slider(),
            age_range=input.age_slider(),
            rooms_range=input.rooms_slider(),
            beds_range=input.beds_slider(),
            pop_range=input.pop_slider(),
            households_range=input.households_slider(),
            ocean_proximity=input.ocean_checkbox(),
            county_select=list(input.county_select() or []),
        )
        idx_households = processed_data.households.between(
            left=input.households_slider()[0], right=input.households_slider()[1], inclusive="both"
        )
        idx_ocean = processed_data.ocean_proximity.isin(input.ocean_checkbox())

        #Merge counties from the dropdown and from map clicks (union).
        # If neither source has any selection, no county filter is applied.
        dropdown_counties = list(input.county_select() or [])
        map_counties = list(selected_counties_rv() or [])
        selected_counties = list(set(
            [c.strip() for c in dropdown_counties] + [c.strip() for c in map_counties]
        ))

        idx_county = (
            processed_data.county.isin(selected_counties)
            if selected_counties else pd.Series(True, index=processed_data.index)
            )

        return processed_data[idx_house_val & idx_income & idx_age & idx_rooms & idx_beds & idx_pop & idx_households & idx_ocean & idx_county]

    # County Banner
    @render.ui
    def county_banner():
        dropdown_counties = list(input.county_select() or [])
        map_counties = list(selected_counties_rv() or [])
        counties = list(dict.fromkeys(dropdown_counties + map_counties))

        if not counties:
            text = "Currently showing: All counties in California"
        else:
            if len(counties) <= 3:
                text = "Currently showing: " + ", ".join(counties)
            else:
                others = len(counties) - 3
                text = f"Currently showing: {', '.join(counties[:3])} and {others} other{'s' if others > 1 else ''}"  

        return ui.div(
            ui.p(text, style="font-size:0.9rem; margin:0;"),
            style="display:flex; align-items:center; height:100%;",
        )
    
    @reactive.calc
    def filtered_data():
        return filtered_expr().to_pandas()

    # Median House Value
    @render.ui
    def median_house():
        df = filtered_data()

        if df is None or df.empty or "median_house_value" not in df.columns:
            return ui.value_box("Median house value", "N/A", "No data available")

        filt_value = round(df.median_house_value.median(), 1)
        state_value = state_median_house_value

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
        df = filtered_data()
        if df is None or df.empty or "median_income_usd" not in df.columns:
            return ui.value_box("Median income", "N/A", "No data available")

        filt_value = round(df.median_income_usd.median(), 1)
        state_value = state_median_income

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
    
    @render.ui
    def geo_cluster_plot():
        df = filtered_data()

        if df.empty:
            return ui.div("No data matches the current filters.", style="padding:1rem;color:#888;")

        m = folium.Map(location=[36.7, -119.4], zoom_start=6, tiles=None)

        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri",
            name="Satellite",
            overlay=False,
            control=True,
        ).add_to(m)

        folium.TileLayer("OpenStreetMap", name="Street Map").add_to(m)

        # Read currently selected counties to drive highlight styling
        active_counties = set(selected_counties_rv())

        def county_style(feature):
            """Style GeoJson counties; highlight map-click selected ones."""
            name = feature.get("properties", {}).get("county", "")
            if name in active_counties:
                # Selected county: solid teal fill
                return {"fillColor": "#2ca25f", "color": "#006d2c", "weight": 2.0, "fillOpacity": 0.45}
            return {"fillColor": "#f0f0f0", "color": "#444444", "weight": 1.2, "fillOpacity": 0.15}
        
        folium.GeoJson(
            counties_geojson,
            name="Counties",
            style_function=county_style,
            tooltip=folium.GeoJsonTooltip(
                fields=["county"],
                aliases=["County:"],
                sticky=False,
            ),
        ).add_to(m)

        marker_cluster = MarkerCluster(name="Housing blocks").add_to(m)

        for _, row in df.iterrows():
            color = house_value_color(row["median_house_value"]) 
            popup_html = (
                f"<b>County:</b> {row['county']}<br>"
                f"<b>Median House Value:</b> ${row['median_house_value']:,}<br>"
                f"<b>Median Income:</b> ${row['median_income_usd']:,.0f}"
            )
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=4,
                color=color,  
                fill=True,
                fill_color=color,   
                fill_opacity=0.75,
                popup=folium.Popup(popup_html, max_width=220),
            ).add_to(marker_cluster)
            
        _ = input.reset_map_btn()
        selected_counties_active = list(selected_counties_rv()) or list(input.county_select() or [])
        if selected_counties_active:
            # Collect all coordinates from the matching county polygons in the GeoJSON
            county_lats, county_lons = [], []
            for feature in counties_geojson.get("features", []):
                if feature.get("properties", {}).get("county") in selected_counties_active:
                    geom = feature.get("geometry", {})
                    coords = geom.get("coordinates", [])
                    geom_type = geom.get("type", "")
                    # Flatten Polygon / MultiPolygon coordinate rings
                    rings = coords if geom_type == "MultiPolygon" else [coords]
                    for poly in rings:
                        for ring in poly:
                            for lon, lat in ring:
                                county_lats.append(lat)
                                county_lons.append(lon)
            if county_lats:
                sw = [min(county_lats), min(county_lons)]
                ne = [max(county_lats), max(county_lons)]
                m.fit_bounds([sw, ne])  # No max_zoom — let Leaflet pick the right level
            else:
                # Fallback: use data point bounds if GeoJSON lookup found nothing
                sw = [df["latitude"].min(), df["longitude"].min()]
                ne = [df["latitude"].max(), df["longitude"].max()]
                m.fit_bounds([sw, ne])
        else:
            # No county filter — fit to all visible data points with a sensible max zoom
            sw = [df["latitude"].min(), df["longitude"].min()]
            ne = [df["latitude"].max(), df["longitude"].max()]
            m.fit_bounds([sw, ne], max_zoom=12)

        legend_html = """
            <div style="
                position: fixed; bottom: 30px; left: 30px; z-index: 1000;
                background: white; padding: 10px 14px; border-radius: 8px;
                border: 1px solid #ccc; font-size: 12px; line-height: 1.8;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.2);">
            <b>Median House Value</b><br>
            <span style="color:#2166ac;">&#9632;</span> &lt; $100k<br>
            <span style="color:#74add1;">&#9632;</span> $100k – $150k<br>
            <span style="color:#fee090;">&#9632;</span> $150k – $200k<br>
            <span style="color:#f46d43;">&#9632;</span> $200k – $300k<br>
            <span style="color:#d73027;">&#9632;</span> &gt; $300k
            </div>

            <div style="
                    position: fixed; bottom: 30px; right: 30px; z-index: 1000;">
                <div style="position: relative; display: inline-block;">
                    <div style="
                        width: 26px; height: 26px; border-radius: 50%;
                        background: white; border: 1px solid #ccc;
                        box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
                        display: flex; align-items: center; justify-content: center;
                        font-size: 14px; cursor: default; user-select: none;"
                    onmouseenter="document.getElementById('map-tip').style.display='block'"
                    onmouseleave="document.getElementById('map-tip').style.display='none'">
                    ℹ️
                    </div>
                    <div id="map-tip" style="
                        display: none; position: absolute;
                        bottom: 32px; right: 0;
                        background: white; border: 1px solid #ccc; border-radius: 8px;
                        padding: 8px 12px; font-size: 12px; white-space: nowrap;
                        box-shadow: 2px 2px 6px rgba(0,0,0,0.2); color: #333;">
                    🖱️ <b>Click</b> a county to filter<br>
                    ⇧ <b>Shift+click</b> to select multiple
                    </div>
                </div>
            </div>   
            """
        m.get_root().html.add_child(folium.Element(legend_html))

        # Inject a JavaScript listener that fires a Shiny input event
        # whenever the user clicks a county polygon on the map.
        county_click_js = """
        <script>
        (function() {
            function attachCountyClick(map) {
                map.eachLayer(function(layer) {
                    if (layer.eachLayer) {
                        layer.eachLayer(function(subLayer) {
                            if (subLayer.feature && subLayer.feature.properties && subLayer.feature.properties.county) {
                                subLayer.on('click', function(e) {
                                    var countyName = subLayer.feature.properties.county;
                                    var shiftHeld = e.originalEvent && e.originalEvent.shiftKey;
                                    // Use window.parent.Shiny -- Shiny lives on the parent page,
                                    // not inside this Folium iframe
                                    var shiny = window.parent && window.parent.Shiny;
                                    if (shiny) {
                                        shiny.setInputValue('map_county_click', {
                                            county: countyName,
                                            shift: shiftHeld
                                        }, {priority: 'event'});
                                    }
                                    L.DomEvent.stopPropagation(e);
                                });
                            }
                        });
                    }
                });
            }

            // The Leaflet map lives in this iframe's window -- search here, not window.parent
            var tries = 0;
            var interval = setInterval(function() {
                tries++;
                var maps = Object.values(window).filter(function(v) {
                    return v && v._container && v.eachLayer;
                });
                if (maps.length > 0) {
                    maps.forEach(attachCountyClick);
                    clearInterval(interval);
                } else if (tries > 40) {
                    clearInterval(interval);
                }
            }, 250);
        })();
        </script>
        """
        m.get_root().html.add_child(folium.Element(county_click_js))

        folium.LayerControl().add_to(m)

        map_html = m._repr_html_()
        map_html = map_html.replace('div style="position:relative;width:100%;height:0;padding-bottom:60%;"',
                    'div style="width:100%;height:100%;padding-bottom:60%;"')  # Ensure the map fills the container
        return ui.HTML(f'{map_html}')

    
    # Distribution Plots
    @render.plot
    def distribution_plot():
        df = filtered_data()
        metric = input.distribution_var()
        fig, ax = plt.subplots(figsize=(5.0, 2.6))
        ax.ticklabel_format(axis='y', style='plain')

        pretty_names = {
            "median_house_value": "Median House Value",
            "median_income": "Median Income",
            "housing_median_age": "House Age",
            "total_rooms": "Total Rooms",
            "total_bedrooms": "Total Bedrooms",
            "population": "Population",
            "households": "Households",
        }

        metric_to_use = "median_income_usd" if metric == "median_income" else metric

        selected_vals = df[metric_to_use].dropna()
        state_vals = state_df[metric_to_use].dropna()

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

        ax.set_xlabel(pretty_names.get(metric_to_use, metric_to_use))
        ax.set_ylabel("Density", labelpad=4)
        if metric in ("median_house_value", "median_income"):
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x/1000:,.0f}k"))
        elif metric in ("housing_median_age"):
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))
        else:  # population, households, total_rooms, total_bedrooms
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:.0f}K" if x >= 1000 else f"{int(x):,}"))
        ax.legend(frameon=False, fontsize=8)
        ax.grid(alpha=0.2)
        ax.yaxis.offsetText.set_visible(False)
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
            "median_income_usd": "Median Income",
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

        x_col_to_use = "median_income_usd" if x_col == "median_income" else x_col
        ax.scatter(
            plot_df[x_col_to_use],
            plot_df["median_house_value"],
            s=8,
            alpha=0.25,
            color="#4e79a7",
            edgecolors="none",
        )
        ax.set_xlabel(pretty_names.get(x_col_to_use, x_col_to_use))
        ax.set_ylabel("Median House Value", labelpad=4)
        if x_col_to_use == "median_income_usd":
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x/1000:,.0f}K"))
        elif x_col_to_use in ("total_rooms", "households"):
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:.0f}K" if x >= 1000 else f"{int(x):,}"))
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
    def _ai_df():
        """Get querychat filtered dataframe as pandas DataFrame."""
        df = qc_vals.df()
        if df is None:
            return state_df
        if hasattr(df, "to_pandas"):
            return df.to_pandas()
        if hasattr(df, "to_native"):
            return df.to_native()
        return df if isinstance(df, pd.DataFrame) else pd.DataFrame(df)

    @render.ui
    def querychat_geo_cluster_plot():
        df = _ai_df()
    
        # 1. Check if the dataframe is empty
        if df.empty:
            return ui.div("No data matches the current filters.", style="padding:1rem;color:#888;")

        # 2. Check for required columns
        if "longitude" not in df.columns or "latitude" not in df.columns:
            return ui.div("Coordinates are missing in the data, so the map is not going to be shown.", style="padding:1rem;color:#888;")
        
        map_html = create_geo_cluster_plot(df)
        if map_html is None:
            return ui.div("No data matches the current filters.", style="padding:1rem;color:#888;")
        map_html = map_html.replace(
            '<div style="width:100%;">',
            '<div class="map-container-outer" style="width:100%;height:100%;">',
            1,
        )
        map_html = map_html.replace(
            'div style="position:relative;width:100%;height:0;padding-bottom:60%;"',
            'div class="map-container-inner" style="position:relative;width:100%;height:100%;min-height:300px;"',
            1,
        )
        return ui.HTML(map_html)

    @render.ui
    def querychat_median_house():
        df = _ai_df()
        
        # Check if the required column exists
        if "median_house_value" not in df.columns:
            return ui.div("'median_house_value' column is missing in the data, so this box is not going to be shown.", style="padding:1rem;color:#888;")
        return create_median_house_value_box(df)

    # Median Income Value
    @render.ui
    def querychat_median_income():
        df = _ai_df()
        
        # Check if the required column exists
        if "median_income_usd" not in df.columns:
            return ui.div("'median_income_usd' column is missing in the data, so this box is not going to be shown.", style="padding:1rem;color:#888;")
        return create_median_income_box(df)
    
    @render.plot
    def querychat_distribution_plot():
        df = _ai_df()
        metric = input.querychat_distribution_var()
        col_to_check = "median_income_usd" if metric == "median_income" else metric

        if df.empty or col_to_check not in df.columns:
            fig, ax = plt.subplots(figsize=(5.0, 2.6))
            msg = "No data matches the current filters." if df.empty else f"Column '{col_to_check}' is missing in the data, so this graph is not going to be shown."
            ax.text(0.5, 0.5, msg, ha="center", va="center")
            ax.set_axis_off()
            return fig

        return create_distribution_plot(df, input.querychat_distribution_var(), state_df)
    
    @render.ui
    def download_button_ui():
        df = _ai_df()

        if df is None or df.empty:
            return None
        return ui.download_button(
            id="download_querychat_filtered_df",
            label="Download Filtered Data (CSV)"
        )

    @render.download(filename="california_housing_filtered.csv")
    def download_querychat_filtered_df():
        df = _ai_df()
        if df is None or df.empty:
            return None
        yield df.to_csv(index=False)

    @render.text
    def chat_title():
        return qc_vals.title() or "Chatbot Data View"

    @render.data_frame
    def chat_table():
        df = _ai_df()
        if df is None or df.empty:
            return render.DataGrid(pd.DataFrame())  # Empty grid
        return render.DataGrid(
            df,
            filters=True,           # Column filters
            editable=False         # Set True if you want editing
        )


app = App(app_ui, server)
