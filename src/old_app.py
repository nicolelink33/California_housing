import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shiny.express import input, render, ui
from scipy.stats import norm

# Page configuration
ui.page_opts(title="California Housing", fillable=True)

# --- SIDEBAR FILTERS ---
with ui.sidebar(width=300):
    ui.markdown("### Filter:")
    
    # Matching the specific sliders in your design
    ui.input_slider("house_val", "Median house value:", 0, 500000, [150000, 350000])
    ui.input_slider("lat", "Latitude:", 30, 45, [34, 42])
    ui.input_slider("long", "Longitude:", -124, -114, [-122, -117])
    ui.input_slider("income", "Median income:", 0, 15000, [2000, 10000])
    ui.input_slider("age", "House age:", 1, 52, [10, 30])
    ui.input_slider("rooms", "Total rooms:", 1, 40000, [5000, 20000])
    ui.input_slider("beds", "Total bedrooms:", 1, 6000, [1000, 4000])
    ui.input_slider("pop", "Population:", 1, 40000, [1000, 15000])
    ui.input_slider("households", "Households:", 1, 6000, [500, 3000])
    
    ui.input_radio_buttons(
        "ocean", "Ocean Proximity:", 
        ["<1hr Ocean", "Inland", "Near Ocean", "Near Bay", "Island"]
    )

# --- MAIN CONTENT ---
with ui.layout_columns(col_widths=[7, 5]):

    with ui.layout_columns(col_widths=12, row_heights=["150px", "1fr"]):
        # Top Row: KPI Value Boxes
        with ui.layout_column_wrap(width=1/2):
            with ui.value_box(theme="light", max_height="150px"):
                "Median house value"
                "$12,000"
                "▲ 12% from state median"
            
            with ui.value_box(theme="light", max_height="150px"):
                "Median income value"
                "$2,000"
                "▲ 5% from state median"
    
        # Left Column: The Map
        with ui.card(full_screen=True):
            @render.plot
            def house_map():
                # Placeholder for the scatter plot map
                fig, ax = plt.subplots(figsize=(8, 8))
                # Simulated data points
                x = np.random.uniform(-124, -114, 2000)
                y = np.random.uniform(33, 42, 2000)
                colors = np.random.randint(100000, 500000, 2000)
                
                sc = ax.scatter(x, y, c=colors, s=2, cmap='viridis', alpha=0.6)
                plt.colorbar(sc, label='median_house_value', ax=ax, shrink=0.6)
                ax.set_xlabel("Longitude")
                ax.set_ylabel("Latitude")
                ax.grid(True, alpha=0.3)
                return fig

    # Right Column: Statistics & Distributions
    with ui.layout_column_wrap(width=1):
        
        with ui.card():
            ui.card_header(
                ui.div(
                    "Distribution:", 
                    ui.input_select("dist_type", None, ["Median House Value", "Income"], width="200px"),
                    class_="d-flex justify-content-between align-items-center"
                )
            )
            @render.plot
            def distribution_plot():
                # FIX: Plot both on ONE axis
                fig, ax = plt.subplots(figsize=(5, 3))
                x = np.linspace(-4, 10, 100)
                
                # "Selected" (Greenish/Orange)
                y1 = norm.pdf(x, 2, 1.5)
                ax.fill_between(x, y1, color="#A8D695", alpha=0.7, label="Selected")
                
                # "State" (Purple)
                y2 = norm.pdf(x, 5, 2)
                ax.fill_between(x, y2, color="#B39DDB", alpha=0.6, label="State")
                
                # Adding the floating text labels like in the image
                ax.text(8, 0.15, "Selected", color="green", fontweight='bold')
                ax.text(8, 0.12, "State", color="purple", fontweight='bold')
                return fig

        # Distribution Plots
        with ui.card():
            ui.card_header("Comparison: Median Income")
            @render.plot
            def comparison_scatter():
                fig, ax = plt.subplots(figsize=(5, 3))
                x = np.random.uniform(0, 16, 1000)
                y = x * 30000 + np.random.normal(0, 50000, 1000)
                ax.scatter(x, y, s=1, alpha=0.5)
                ax.set_title("median_house_value vs median_income", fontsize=10)
                ax.set_xlabel("median_income")
                ax.set_ylabel("median_house_value")
                return fig

        with ui.card():
            ui.card_header("Median House Value by Ocean Proximity")
            @render.plot
            def boxplot_proximity():
                fig, ax = plt.subplots(figsize=(5, 2))
                data = [np.random.normal(i, 1, 100) for i in range(4)]
                bplot = ax.boxplot(data, patch_artist=True)
                colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
                for patch, color in zip(bplot['boxes'], colors):
                    patch.set_facecolor(color)
                return fig