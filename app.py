import pandas as pd
import plotly.express as px
import geopandas as gpd

from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# =====================================================
# LOAD DATA
# =====================================================


df = pd.read_csv("data/Health.csv")
summary = pd.read_csv("data/summary.csv")
diseas = pd.read_csv("data/disease.csv")
gdf = gpd.read_file("data/Addis.geojson")
#print(summary.head())
# print(diseas.head())
# IMPORTANT:
# Convert CRS BEFORE merge
gdf = gdf.to_crs(epsg=4326)

# Merge shapefile with dataframe
merged = gdf.merge(
    df,
    left_on="Sub_City",
    right_on="Sub city",
    how="left"
)
merged = merged.fillna(0)
merged = merged[merged.geometry.notnull()]
# Subcity values
subcities = df["Sub city"].unique()

# Dashboard colors
colors = [
    "#4F46E5",
    "#06B6D4",
    "#10B981",
    "#F59E0B",
    "#EF4444"
]


# =====================================================
# APP
# =====================================================
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],

    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0"
        }
    ]
)


# =====================================================
# KPI CARD FUNCTION
# =====================================================
def create_card(title, card_id, color):

    return dbc.Card(

        dbc.CardBody([

            html.H6(
                title,
                className="text-muted fw-semibold"
            ),

            html.H3(
                id=card_id,
                className=f"text-{color} fw-bold"
            )

        ]),

        className="""
        shadow-sm
        border-0
        rounded-4
        h-100
        """
    )

server=app.server
# =====================================================
# LAYOUT
# =====================================================
app.layout = dbc.Container([

    # =================================================
    # HEADER
    # =================================================
    dbc.Row([

        dbc.Col([

            html.Div(
                html.Img(
                        src="/assets/logo.png",
                    height="100px"
                    ),
                className="""
                text-center
                fw-bold
                text-primary
                """
            )

        ],
            width=2,
            className="d-flex align-items-center justify-content-center"
        ),

        dbc.Col([

            html.H5(
                "Addis Ababa City Administration",

                className="""
                text-primary
                fw-bold
                text-center
                mb-2
                """
            ),
       html.H6(
                "LINDA Familia project Land Scope Review MCH Dashboard",

                className="""
                text-primary
                fw-bold
                text-center
                mb-2
                """
            ),
            html.H6(
                "የአዲስ አበባ ከተማ አስተዳደር የእናቶች እና ህፃናት ጤና የመረጃ ጥንቅር",

                className="""
                text-secondary
                text-center
                """
            )

        ],
            width=8,
            className="d-flex flex-column justify-content-center"
        ),

        dbc.Col([

            html.Div(
               # "HEALTH",
                className="""
                text-center
                fw-bold
                text-successdashboard
                """
            )

        ],
            width=2,
            className="d-flex align-items-center justify-content-center"
        )

    ],style={
        "position": "fixed",
        "top": "0",
        "left": "0",
        "right": "0",
        "zIndex": "999",
        "backgroundColor": "white",
        "padding": "10px",
    },
        className="""
        bg-white
        shadow-sm
        rounded-4
        p-3
        mb-4
        """
    ),
    html.Div(style={"height": "150px"}),
    # =================================================
    # DROPDOWNS
    # =================================================
    dbc.Row([

        dbc.Col([

            dcc.Dropdown(

                id="health_value",

                options=[

                    {
                        "label": "First Antenatal Care",
                        "value": "First ANC"
                    },

                    {
                        "label": "Second Antenatal Care",
                        "value": "Second ANC"
                    },

                    {
                        "label": "Total Antenatal Care",
                        "value": "ANC"
                    },

                    {
                        "label": "Total Delivery",
                        "value": "TD"
                    },

                    {
                        "label": "Breech Delivery",
                        "value": "BCG"
                    },

                    {
                        "label": "Spontaneous Vaginal Delivery",
                        "value": "SVD"
                    },

                    {
                        "label": "Still Birth",
                        "value": "SB"
                    },

                    {
                        "label": "Neonatal Death",
                        "value": "ND"
                    },

                    {
                        "label": "Maternal Death",
                        "value": "MD"
                    }

                ],

                value="ANC",
                clearable=False

            )

        ], lg=6),

        dbc.Col([

            dcc.Dropdown(

                id="subcity-dropdown",

                options=[
                    {
                        "label": city,
                        "value": city
                    }
                    for city in subcities
                ],

                value=subcities[0],
                clearable=False

            )

        ], lg=6)

    ],
        className="mb-4 g-3"
    ),

    # =================================================
    # MAP + KPI
    # =================================================
    dbc.Row([

        # MAP
         dbc.Col([

            dbc.Card([

                dbc.CardHeader(
                    html.H5(
                        "Addis Ababa MCH Map",
                        className="text-center"
                    )
                ),

                dbc.CardBody([

                    dcc.Graph(
                        id="Addis_map",
                        figure={}
                    )

                ])

            ], className="shadow")

        ], lg=5),

        # KPI CARDS
        dbc.Col([

            dbc.Row([

                dbc.Col([
                    create_card(
                        "Antenatal Care",
                        "anc-card",
                        "primary"
                    )
                ], md=6),

                dbc.Col([
                    create_card(
                        "Neonatal Death",
                        "ND-cart",
                        "danger"
                    )
                ], md=6),

                dbc.Col([
                    create_card(
                        "Breech Delivery",
                        "BD-cart",
                        "warning"
                    )
                ], md=6),

                dbc.Col([
                    create_card(
                        "SVD",
                        "SVD-cart",
                        "success"
                    )
                ], md=6),

                dbc.Col([
                    create_card(
                        "Total Delivery",
                        "delivery-cart",
                        "info"
                    )
                ], md=6),

                dbc.Col([
                    create_card(
                        "Still Birth",
                        "SB-cart",
                        "secondary"
                    )
                ], md=6)

            ],
                className="g-3"
            )

        ], lg=7)

    ],
        className="mb-4 g-3"
    ),

    # =================================================
    # BAR + PIE
    # =================================================
    dbc.Row([

        dbc.Col([

            dbc.Card([

                dbc.CardBody([

                    dcc.Graph(
                        id="Bar_graphe",
                        figure={}
                    )

                ])

            ],
                className="shadow-sm border-0 rounded-4"
            )

        ], lg=6),

        dbc.Col([

            dbc.Card([

                dbc.CardBody([

                    dcc.Graph(
                        id="Pie_graphe",
                        figure={}
                    )

                ])

            ],
                className="shadow-sm border-0 rounded-4"
            )

        ], lg=6)

    ],
        className="mb-4 g-3"
    ),

    # =================================================
    # Dropdown
    # =================================================
     dbc.Row([
         
        dbc.Col([

            dcc.Dropdown(

                id="summary_data",

                options=[

                    {
                        "label": "Total number of live births",
                        "value": "Total number of live births"
                    },

                    {
                        "label": "Neonatal death (Per 1000 live births)",
                        "value": "Neonatal death (Per 1000 live births)"
                    },

                    {
                        "label": "Maternal death (Per 100,000 births))",
                        "value": "Maternal death (Per 100,000 births))"
                    },

                  

                ],

                value="Total number of live births",
                multi=True,
                clearable=False

            )

        ], lg=6),

        dbc.Col([

            dcc.Dropdown(

                id="disease",

                options=[
                     {
                        "label": "Incidence of malaria cases per 1,000",
                        "value": "Incidence of all malaria cases per 1,000"
                    },
                     {
                        "label": "Prevalence, HIV",
                        "value": "Prevalence, HIV"
                    },
                     {
                        "label": "Prevalence, Sepsis/1,000",
                        "value": "Prevalence, Sepsis/1,000"
                    },
                     {
                        "label": "TB Incidence per 100,000 population",
                        "value": "TB Incidence per 100,000 population"
                    },
                ],

                value="TB Incidence per 100,000 population",
                multi=True,
                clearable=False

            )

        ], lg=6)

    ],
        className="mb-4 g-3"
    ),


    dbc.Row([
         
        dbc.Col([

            dbc.Card([
            html.H6("Maternal and child delivery outcomes in each region, 2022 to 2025 ", className="text-center"),
                dbc.CardBody([

                    dcc.Graph(
                        id="summary_graphe",
                        figure={}
                    )

                ])

            ],
                className="shadow-sm border-0 rounded-4"
            )

        ], lg=6),
        
    # =================================================
    # LINE CHART 
    # =================================================

        dbc.Col([

            dbc.Card([
            html.H6("prevalence some communicable  disease", className="text-center"),
                dbc.CardBody([

                    dcc.Graph(
                        id="Disease_chart",
                        figure={}
                    )

                ])

            ],
                className="shadow-sm border-0 rounded-4"
            )

        ], lg=6)

    ],
        className="mb-4 g-3"
    ),

    # =================================================
    # FOOTER
    # =================================================
    dbc.Container(

    dbc.Row(

        [

            # LEFT SIDE
            dbc.Col(
                [

                    html.H5(
                        "Addis Ababa MCH Dashboard",
                        className="fw-bold mb-2"
                    ),

                    html.P(
                        "Maternal and Child Health data visualization and monitoring dashboard.",
                        className="mb-1"
                    ),
                      html.P(
                        "Copyright ©2026 | EPHI",
                        className="mb-1"
                    ),



                ],

                xs=12,
                sm=12,
                md=6,
                lg=6,

                className="mb-3 text-center text-md-start"
            ),


            # RIGHT SIDE
            dbc.Col(
                [

                    html.P(
                        "Desing by: Weldemariam Bahre",
                        className="mb-1"
                    ),

                    html.P(
                        "Email: weldemariambahre@gmail.com",
                        className="mb-1"
                    ),

                    html.P(
                        "Phone: +251946674151",
                        className="mb-1"
                    ),

                ],

                xs=12,
                sm=12,
                md=6,
                lg=6,

                className="text-center text-md-end"
            ),

        ],

        className="align-items-center"

    ),

    fluid=True,

    style={
     "backgroundColor": "#0F4C5C",
    "color": "white",
    "padding": "15px 20px",
    "fontFamily": "Segoe UI, sans-serif",
    "fontSize": "14px",
    "borderTop": "2px solid white"
    }

)

],
    fluid=True,

    style={
        "backgroundColor": "#f4f6f9",
        "padding": "15px"
    }
)


# =====================================================
# UPDATE CHARTS
# =====================================================
@callback(

    Output("Bar_graphe", "figure"),
    Output("Pie_graphe", "figure"),
    Output("Addis_map", "figure"),

    Input("health_value", "value")

)
def update_charts(value):

    sorted_df = df.sort_values(
        by=value,
        ascending=False
    )

    # =================================================
    # BAR CHART
    # =================================================
    bar_fig = px.bar(

        sorted_df,

        x="Sub city",
        y=value,

        text=value,

        color="Sub city",

        color_discrete_sequence=colors,

        template="plotly_white"
    )

    bar_fig.update_traces(

        texttemplate='%{y:,}',
        textposition='outside',

        hovertemplate=
        "<b>%{x}</b><br>" +
        f"{value}: " +
        "%{y:,}<extra></extra>"
    )

    bar_fig.update_layout(

        title={
            "text": f"{value} by Sub City",
            "x": 0.5,
            "xanchor": "center"
        },

        height=500,

        paper_bgcolor="#f8f9fa",
        plot_bgcolor="#f8f9fa",

        showlegend=False,

        font=dict(
            family="Arial",
            size=14
        ),

        margin=dict(
            t=70,
            l=30,
            r=30,
            b=30
        ),

        transition={
            "duration": 1200,
            "easing": "cubic-in-out"
        }
    )

    # =================================================
    # PIE CHART
    # =================================================
    pie_fig = px.pie(

        sorted_df,

        names="Sub city",
        values=value,

        hole=0.55,

        color_discrete_sequence=
        px.colors.qualitative.Set3
    )

    pie_fig.update_traces(

        textposition='inside',

        textinfo='percent+label',

        hovertemplate=
        "<b>%{label}</b><br>" +
        "Value: %{value:,}<br>" +
        "Percent: %{percent}<extra></extra>"
    )

    pie_fig.update_layout(

        title={
            "text": f"{value} Distribution",
            "x": 0.5
        },

        height=500,

        paper_bgcolor="#f8f9fa",

        font=dict(
            family="Arial",
            size=14
        )
    )

    # =================================================
    # LINE CHART
    # =================================================
    
    # line_fig = px.line(

    #     sorted_df,

    #     x="Sub city",
    #     y=value,

    #     markers=True,

    #     template="plotly_white"
    # )

    # line_fig.update_traces(
    #     marker_line_width=3,
    #     marker_line_color="black",

    #     line=dict(
    #         width=5,
    #         shape="spline"
    #     ),

    #     marker=dict(
    #         size=12,
    #         line=dict(
    #             width=2,
    #             color="blue"
    #         )
    #     ),

    #     hovertemplate=
    #     "<b>%{x}</b><br>" +
    #     f"{value}: " +
    #     "%{y:,}<extra></extra>"
    # )

    # line_fig.update_layout(

    #     title={
    #         "text": f"{value} Trend by Sub City",
    #         "x": 0.5
    #     },

    #     height=500,

    #     hovermode="x unified",

    #     paper_bgcolor="#f8f9fa",
    #     plot_bgcolor="#f8f9fa",

    #     font=dict(
    #         family="Arial",
    #         size=14
    #     ),

    #     margin=dict(
    #         t=70,
    #         l=40,
    #         r=40,
    #         b=40
    #     ),

    #     transition={
    #         "duration": 1200,
    #         "easing": "cubic-in-out"
    #     }
    # )

    # line_fig.update_xaxes(
    #     showgrid=False
    # )

    # line_fig.update_yaxes(
    #     gridcolor="lightgray"
    # )


    # =================================================
    # MAP
    # =================================================
    fig_map = px.choropleth_map(
    merged,
    geojson=merged.geometry,
    locations=merged.index,
    color=value,
    hover_name="Sub city",
    center={"lat": 8.96, "lon": 38.80},
    zoom=10,
    opacity=0.7,
    #opacity=1,
    color_continuous_scale="Viridis"
    # [
    #     [0, "rgba(59, 151, 151,0.3)"],
    #     [1, "rgba(255,165,0,1)"]
    # ]
)
    fig_map.update_traces(
    marker_line_color="black",
    marker_line_width=1.5
)

    fig_map.update_layout(
    margin=dict(r=0, t=0, l=0, b=0),
    height=500
    )



    return (
        bar_fig,
        pie_fig,
        #line_fig,
        fig_map,
        #summary_line
    )


# =====================================================
# KPI CALLBACK
# =====================================================
@callback(

    Output("anc-card", "children"),
    Output("ND-cart", "children"),
    Output("BD-cart", "children"),
    Output("SVD-cart", "children"),
    Output("delivery-cart", "children"),
    Output("SB-cart", "children"),
    #Output("Addis_map", "figure"),

    Input("subcity-dropdown", "value")
)
def update_data(subcity):

    temp = df[df["Sub city"] == subcity]

    anc = temp["ANC"].iloc[0]
    nd = temp["ND"].iloc[0]
    bd = temp["BCG"].iloc[0]
    svd = temp["SVD"].iloc[0]
    delivery = temp["TD"].iloc[0]
    sb = temp["SB"].iloc[0]

    return (

        f"{anc:,}",
        f"{nd:,}",
        f"{bd:,}",
        f"{svd:,}",
        f"{delivery:,}",
        f"{sb:,}"
    )

@callback(
    Output("summary_graphe","figure"),
    Input("summary_data","value")
)
def summary_graphe(value):
    summary_line = px.line(
        summary,
        x="year",
        y=value,
        markers=True,
        template="plotly_white"
    )

    summary_line.update_layout(
        legend=dict(
            orientation="h",   # horizontal legend
            yanchor="bottom",
            y=-0.4,            # pushes legend below graph
            xanchor="center",
            x=0.5
        )
    )

    return summary_line
@callback(
    Output("Disease_chart","figure"),
    Input("disease","value")

)
def disease(value):
       diseas_line= px.line(diseas,x="Years",
                          y=value,
                          markers=True,
                         template="plotly_white"
                          )
       diseas_line.update_layout(
        legend=dict(
            orientation="h",   # horizontal legend
            yanchor="bottom",
            y=-0.4,            # pushes legend below graph
            xanchor="center",
            x=0.5
        )
       )
       return diseas_line
# =====================================================
# RUN APP
# =====================================================
if __name__ == "__main__":
    #app.run_server(host="0.0.0.0", port=8050, debug=False)
    app.run(debug=True)
    
# app = Dash(__name__)

# server = app.server