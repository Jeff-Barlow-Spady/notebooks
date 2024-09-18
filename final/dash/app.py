# Import required libraries
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a Dash application with a Bootstrap theme for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create an app layout
app.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.H1(
                    "SpaceX Launch Records Dashboard",
                    style={"textAlign": "center", "color": "#003366"},
                    className="mb-4",
                ),
                width=12,
            )
        ),
        # Launch Site Dropdown
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
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
                            searchable=True,
                            placeholder="Select a Launch Site",
                            style={"margin-bottom": "20px"},
                        ),
                    ]
                ),
                width=6,
            )
        ),
        # Success Pie Chart
        dbc.Row(dbc.Col(dcc.Graph(id="success-pie-chart"), width=10)),
        # Payload Slider
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
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
                                i: str(i)
                                for i in range(
                                    int(min_payload), int(max_payload) + 1, 1000
                                )
                            },
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ]
                ),
                width=10,
            )
        ),
        # Success-Payload Scatter Chart
        dbc.Row(dbc.Col(dcc.Graph(id="success-payload-scatter-chart"), width=10)),
    ],
    fluid=True,
)


# Callback for updating success pie chart
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
            legend="Outcome",
        )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
    return fig


# Callback for updating success-payload scatter chart
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
        template="plotly_white",
    )

    # Enhancing the layout for a more polished look
    fig.update_layout(
        title_font_size=20,
        xaxis_title="Payload Mass (kg)",
        yaxis_title="Launch Outcome",
        legend_title="Launch Sites",
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="closest",
    )

    fig.update_traces(marker=dict(size=10, line=dict(width=2, color="DarkSlateGrey")))

    return fig


# Start the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
