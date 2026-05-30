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
    dbc.Row(

    [

        dbc.Col([

            html.Div(
                html.Img(
                    src="/assets/logo.png",
                    style={
                        "height": "70px",
                        "maxWidth": "100%"
                    }
                ),
                className="text-center logo-img"
            )

        ],
            xs=3, md=2,
            className="d-flex align-items-center justify-content-center"
        ),

        dbc.Col([

            html.H5(
                "Addis Ababa City Administration",
                className="header-title text-primary fw-bold text-center mb-1",
            ),

            html.H6(
                "LINDA Familia project Landscape review MCH Dashboard",
                className="header-subtitle text-primary text-center mb-0",
            ),

        ],
            xs=6, md=8,
            className="d-flex flex-column justify-content-center"
        ),

        dbc.Col([
            html.Div(
                className="text-center fw-bold text-success"
            )
        ],
            xs=3, md=2,
            className="d-flex align-items-center justify-content-center"
        )

    ],

    style={
        "position": "fixed",
        "top": "0",
        "left": "0",
        "right": "0",
        "zIndex": "999",
        "backgroundColor": "white",
        "padding": "4px 8px",
    },

    className="""
    shadow-sm
    rounded-3
    mb-1
    """
),

# space below fixed header
html.Div(style={"height": "110px"}),
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
                        "የአዲስ እበባ ከተማ አስተዳደር ካርታ Addis Ababa MCH Map",
                        className="text-center"
                    )
                ),

                dbc.CardBody([

                    dcc.Graph(
                        id="Addis_map",
                        figure={},
                        config={"responsive": True},
                        style={"width": "100%", "height": "100%"}
                    )

                ])

            ], className="shadow")

        ], lg=5),

        # KPI CARDS
        dbc.Col([
                dbc.Alert(

    [

        html.H6(
            "የዳሽቦርድ አጠቃላይ መግለጫ (Dashboard Overview)",
            className="fw-bold text-center mb-2"
        ),

        html.P(
            "ይህ ዳሽቦርድ በሊንዳ ፋሚሊያ ፕሮጀክት ስር በአዲስ አበባ ከተማ አስተዳደር የእናቶችና የህፃናት ጤና መረጃዎችን ለመከታተል እና ለመተንተን የተዘጋጀ ነው።",
            className="mb-2 text-left"
        ),

        html.P(
            "This dashboard provides interactive visualization and monitoring of Maternal and Child Health (MCH) indicators across Addis Ababa Addministration under the LINDA Familia Project.",
            className="mb-0 text-left"
        )

    ],

    color="light",
    className="shadow-sm rounded-4 border-0 mb-3"
),
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
                ], md=6),

             ],
                className="g-3"
            ),
            
            dbc.Col([
                 html.P("")
            ])

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
                        id="Bar_graphe",figure={},
                        config={
                         "responsive": True,
                          "displayModeBar": False
                          },
                         style={
                          "width": "100%",
                         "height": "450px"
                            }
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
                        id="Pie_graphe",figure={},
                        config={
                         "responsive": True,
                         "displayModeBar": False
                          },
                          style={
                         "width": "100%",
                         "height": "400px"
                         }
                    )

                ])

            ],
                className="shadow-sm border-0 rounded-4"
            )

        ],          xs=12,
         sm=12,
         md=6,
         lg=6,
         xl=6)

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
                        "developed by: Weldemariam Bahre",
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
        y="Sub city",
        x=value,
        text=value,
        orientation="h",
        color="Sub city",
        color_discrete_sequence=colors,
        template="plotly_white"
    )
    bar_fig.update_traces(
        texttemplate='%{x:,}',
        textposition='outside',
        cliponaxis=False,
        hovertemplate=
        "<b>%{x}</b><br>" +
        f"{value}: " +
        "%{y:,}<extra></extra>"
    )

    bar_fig.update_layout(

        title={
            "text": f"{value} by Sub City",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 16}
        },

       # height=500,

        paper_bgcolor="#f8f9fa",
        plot_bgcolor="#f8f9fa",

        showlegend=False,
        autosize=True,

        font=dict(
            family="Arial",
            size=14
        ),

        margin=dict(
            t=90,
            l=20,
            r=60,
            b=30
        ),
        xaxis=dict(
        title="",
        tickfont=dict(size=10)
    ),

    yaxis=dict(
        title="",
        tickfont=dict(size=10)
    ),

        transition={
            "duration": 800,
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

        textinfo='percent',#+label',

        hovertemplate=
        "<b>%{label}</b><br>" +
        "Value: %{value:,}<br>" +
        "Percent: %{percent}<extra></extra>"
    )

    pie_fig.update_layout(

        title={
            "text": f"{value} Distribution",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 16}
        },

         paper_bgcolor="#f8f9fa",
         plot_bgcolor="#f8f9fa",
         autosize=True,
         margin=dict(
        l=10,
        r=10,
        t=50,
        b=60
    ),
        font=dict(
            family="Arial",
            size=14
        ),
        legend=dict(
        orientation="h",
        y=-0.15,
        x=0.5,
        xanchor="center",
        yanchor="top",
        font=dict(size=10)
    )
    )

    
    # =================================================
    # MAP
    # =================================================
    fig_map = px.choropleth_mapbox(
    merged,
    geojson=merged.__geo_interface__,
    locations=merged.index,
    color=value,
    hover_name="Sub city",
    center={"lat": 8.94, "lon": 38.78},
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
    marker_line_width=1
),

    fig_map.update_layout(
    #height =320,
    autosize=True,
    margin=dict(r=0, t=0, l=0, b=0),
    height=450,
    mapbox_style="open-street-map",  # IMPORTANT (no token needed)
    uirevision="constant",  # prevents reset on resize
    coloraxis_colorbar=dict(
        title=""
    )
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
#-----------------------
#--- Line graphe 
#-------------------------
def summary_graphe(value):
    summary_line = px.line(
        summary,
        x="year",
        y=value,
        markers=True,
        template="plotly_white",
        line_shape="spline"   # smooth professional curve
    )

    summary_line.update_traces(
        fill="tozeroy",
        fillcolor="rgba(0,123,255,0.08)",
        orientation="h",
        line=dict(width=3),
        marker=dict(size=7),
        hovertemplate=
        "<b>Year:</b> %{x}<br>" +
        f"<b>{value}:</b> %{{y:,}}<extra></extra>"
        
    ),
    summary_line.update_layout(
    legend=dict(
        orientation="h",
        x=0.5,
        xanchor="center",
        y=-0.25,   # 👈 BELOW graph
        yanchor="top",
        font=dict(size=10)
    ),

    margin=dict(
        t=60,
        l=40,
        r=20,
        b=90   # 👈 IMPORTANT space for legend
    )
)

    return summary_line
@callback(
    Output("Disease_chart","figure"),
    Input("disease","value")

)
# for the prevalnce 
def disease(value):
       diseas_line= px.line(diseas,x="Years",
                          y=value,
                          markers=True,
                         template="plotly_white",
                         #template="plotly_white",
                         line_shape="spline"
                          )
       
       diseas_line.update_layout(
        legend=dict(
            orientation="h",   # horizontal legend
            yanchor="bottom",
            y=-0.64,            # pushes legend below graph
            xanchor="center",
            x=0.5
        )
       ),
       diseas_line.update_traces(
        fill="tozeroy",
        fillcolor="rgba(0,123,255,0.08)",
        orientation="h",
        line=dict(width=3),
        marker=dict(size=7),
        hovertemplate=
        "<b>Year:</b> %{x}<br>" +
        f"<b>{value}:</b> %{{y:,}}<extra></extra>"
        
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