import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

url = "https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/Monterrey/airbnb.csv"

df = pd.read_csv(url)

print("Dataset loaded successfully")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Required columns
required_columns = ['latitude', 'longitude', 'price', 'minimum_nights']

missing = [c for c in required_columns if c not in df.columns]

if missing:
    raise ValueError(f"Missing columns in dataset: {missing}")

# Data cleaning
for col in required_columns:
    if col == 'price':
        df[col] = pd.to_numeric(
            df[col].astype(str).replace(r'[^\d.]', '', regex=True),
            errors='coerce'
        )
    else:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove missing values
df = df.dropna(subset=required_columns)

# Validate latitude and longitude
df = df[
    df['latitude'].between(-90, 90) &
    df['longitude'].between(-180, 180)
]

print("Clean dataset:", df.shape)
print(df.head())

if df.empty:
    raise ValueError("No valid records found in dataset.")

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Airbnb Listings - Monterrey",
        style={'textAlign': 'center'}
    ),

    html.H3("Select Minimum Nights"),

    dcc.Slider(
        id='night-slider',
        min=1,
        max=30,
        step=1,
        value=3,
        marks={i: str(i) for i in range(1, 31, 5)}
    ),

    html.Br(),

    html.H3("Select Price Range"),

    dcc.RangeSlider(
        id='price-slider',
        min=0,
        max=max(1000, int(df['price'].max())),
        value=[
            0,
            min(2500, max(1000, int(df['price'].max())))
        ],
        step=100,
        tooltip={
            'placement': 'bottom',
            'always_visible': True
        }
    ),

    html.Br(),

    html.Div(id='count'),

    dcc.Graph(
        id='airbnb-map',
        style={'height': '700px'}
    )
], style={'padding': '30px'})


# Callback
@app.callback(
    Output('airbnb-map', 'figure'),
    Output('count', 'children'),
    Input('night-slider', 'value'),
    Input('price-slider', 'value')
)
def update_graph(nights, price_range):

    dff = df[
        (df['minimum_nights'] >= nights) &
        (df['price'] >= price_range[0]) &
        (df['price'] <= price_range[1])
    ]

    print("Filtered rows:", len(dff))
    if dff.empty:
        fig = px.scatter_geo(
            title="No listings found. Change the filters."
        )
        fig.update_layout(height=700)
        return fig, "No records found"

    fig = px.scatter_geo(
        dff,
        lat='latitude',
        lon='longitude',
        color='price',
        hover_name='name' if 'name' in dff.columns else None,
        hover_data=['minimum_nights', 'room_type']
        if 'room_type' in dff.columns
        else ['minimum_nights'],
        color_continuous_scale='Sunset',
        projection='mercator',
        title='Airbnb Property Locations',
        height=700
    )

    fig.update_geos(
        fitbounds='locations',
        visible=True,
        showland=True
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10)
    )

    return fig, f"Total listings found: {len(dff)}"


# Run app
if __name__ == '__main__':
    app.run(debug=True,port=8006)
