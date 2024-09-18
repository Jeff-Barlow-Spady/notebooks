# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

# Define a stylesheet for the app

# Create an app layout
app.layout = html.Div(
    children=[
        # Header
        html.Div(
            children=[
                html.H1(
                    "SpaceX Launch Records Dashboard",
                    style={
                        "textAlign": "center",
                        "color": "#003366",  # Dark Blue
                        "font-size": "40px",
                        "margin-bottom": "20px",
                        "font-family": "Arial, sans-serif",
                    },
                )
            ],
            className="header",
        ),
        # Body
        html.Div(
            children=[
                # Section: Launch Site Selection
                html.Div(
                    children=[
                        html.Label(
                            "Select Launch Site:", style={"font-weight": "bold"}
                        ),
                        dcc.Dropdown(
                            id="site-dropdown",
                            options=[
                                {"label": "All Sites", "value": "ALL"},
                                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
                            ],
                            value="ALL",
                            placeholder="Select a Launch Site",
                            style={
                                "width": "100%",
                                "padding": "3px",
                                "border-radius": "4px",
                                "background-color": "#f7f7f7",  # Light Grey
                            },
                        ),
                    ],
                    style={
                        "width": "50%",
                        "margin": "20px auto",
                        "padding": "20px",
                        "background-color": "#e6e6e6",  # Very Light Grey
                        "border-radius": "10px",
                        "box-shadow": "2px 2px 5px #999999",  # Soft shadow
                    },
                ),
                # Section: Success Pie Chart
                html.Div(
                    children=[dcc.Graph(id="success-pie-chart")],
                    style={
                        "width": "80%",
                        "margin": "20px auto",
                        "padding": "20px",
                        "background-color": "#e6e6e6",
                        "border-radius": "10px",
                        "box-shadow": "2px 2px 5px #999999",
                    },
                ),
                # Section: Payload Range Selector
                html.Div(
                    children=[
                        html.Label(
                            "Payload Range (Kg):", style={"font-weight": "bold"}
                        ),
                        dcc.RangeSlider(
                            id="payload-slider",
                            min=min_payload,
                            max=max_payload,
                            step=1000,
                            value=[min_payload, max_payload],
                            marks={
                                i: f"{i}"
                                for i in range(
                                    int(min_payload), int(max_payload) + 1, 1000
                                )
                            },
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    style={
                        "width": "80%",
                        "margin": "20px auto",
                        "padding": "20px",
                        "background-color": "#e6e6e6",
                        "border-radius": "10px",
                        # Scatter Plot Section
                        "box-shadow": "2px 2px 5px #999999",
                    },
                ),
                # Section: Success-Payload Scatter Chart
                html.Div(
                    children=[dcc.Graph(id="success-payload-scatter-chart")],
                    style={
                        "width": "80%",
                        "margin": "20px auto",
                        "padding": "20px",
                        "background-color": "#e6e6e6",
                        "border-radius": "10px",
                        "box-shadow": "2px 2px 5px #999999",
                    },
                ),
            ],
            style={
                "font-family": "Arial, sans-serif",
                "background-color": "#f4f4f9",
                "padding": "20px",
            },
        ),
    ],
    className="container",
)

# Styling Improvements in Callbacks


# Update Success Pie Chart Callback
@app.callback(Output("success-pie-chart", "figure"), [Input("site-dropdown", "value")])
def update_success_pie_chart(selected_site):
    if selected_site == "ALL":
        fig = px.pie(
            spacex_df,
            names="Launch Site",
            title="Total Successful Launches by Site",
            legend_title="Launch Sites",
        )
    else:
        site_df = spacex_df[spacex_df["Launch Site"] == selected_site]
        fig = px.pie(
            site_df,
            names="class",
            title=f"Successful Launches for {selected_site}",
            legend_title="Outcome",
        )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
    return fig


# Update Success-Payload Scatter Chart Callback
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"), Input("payload-slider", "value")],
)
def update_success_payload_scatter_chart(selected_site, payload_range):
    if selected_site == "ALL":
        site_df = spacex_df
    else:
        site_df = spacex_df[spacex_df["Launch Site"] == selected_site]

    filtered_df = site_df[
        (site_df["Payload Mass (kg)"] >= payload_range[0])
        & (site_df["Payload Mass (kg)"] <= payload_range[1])
    ]

    fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Launch Site",
        symbol="class",
        title="Payload vs. Launch Outcome",
        labels={"class": "Launch Outcome"},
        hover_data=["Booster Version"],
    )
    fig.update_layout(legend=dict(x=0, y=1), margin=dict(t=0, b=0, l=0, r=0))
    fig.update_traces(marker=dict(size=10, line=dict(width=2, color="DarkSlateGrey")))

    return fig


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
