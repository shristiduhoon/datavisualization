from dash import Dash,html

#Step1-Create dash application
app = Dash(__name__)
#step2-define dashboard layout
app.layout=html.Div([
    html.H1("Welcome to Python Dash"),
    html.P("My First Interactive Dashboard"),
    html.H2("Learning dashboard Framework")
])
#step3-Run application
if(__name__=="__main__"):
    app.run(debug=True)
