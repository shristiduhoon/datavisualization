from dash import Dash, html, dcc, Input, Output
import plotly.express as px

df = px.data.iris()

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Iris Flower Analysis Dashboard"),

    html.Label("Select Flower Species"),

    dcc.Dropdown(
        id="species_dropdown",
        options=[
            {"label": "Setosa", "value": "setosa"},
            {"label": "Versicolor", "value": "versicolor"},
            {"label": "Virginica", "value": "virginica"}
        ],
        value="setosa",
        clearable=False
    ),

    dcc.Graph(id="species_graph")
])

@app.callback(
    Output("species_graph", "figure"),
    Input("species_dropdown", "value")
)
def update_graph(selected_species):
    filtered_df = df[df["species"] == selected_species]

    fig = px.scatter(
        filtered_df,
        x="sepal_width",
        y="sepal_length",
        color="species",
        title="Iris Flower Analysis"
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)