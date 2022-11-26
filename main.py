from typing import TypeVar
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# dash é composto por duas partes
# layout e interação
HTML = TypeVar("HTML")

app = Dash(__name__, external_stylesheets=["assets/style.css", {"rel": "stylesheet", "type": "text/css"}])

colors = {
    'background': None,
    'text': '#111111'
}


def create_table(dataframe, max_rows=10) -> HTML:
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


# dataframe
df = pd.DataFrame({
    "Fruits": ["Oranges", "Apples", "Grapes", "Apples", "Grapes"],
    "Amount": [4, 4, 2, 4, 5],
    "City": ["Ouro Branco", "Ouro Preto", "Belo Horizonte", "Ouro Branco", "Ouro Preto"]
})

df2 = pd.read_csv("https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw"
                  "/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv")

fig = px.bar(df, x="Fruits", y="Amount", color="City", barmode="group")
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig2 = px.scatter(df2, x="gdp per capita", y="life expectancy", size="population", color="continent",
                  hover_name="country", log_x=True, size_max=60)

app.layout = html.Div(children=[
    html.H1("Fruits graph", style={"text-align": "center"}),
    html.Div(children="Amount about fruits", style={"text-align": "center", "margin-bottom": "10px"}),
    dcc.Graph(id="graph", figure=fig),
    html.H4(children="Table fruits", style={"textAlign": "left", "margin-left": "150px", "padding": "18px"}),
    html.Div([
        create_table(df),
        dcc.Graph(id="graph2", figure=fig2),
        html.Label("Multi-select dropdown"),
        dcc.Dropdown(["Brazil", "Montreal", "San Francisco"],
                     ["Montreal", "San Francisco"],
                     multi=True),
        html.Br(),
        html.Label("Slider"),
        dcc.Slider(min=0, max=10, marks={i: f"Label {i}" if i == 1 else str(i) for i in range(1, 7)}, value=5),
        html.Label('Checkboxes'),
        dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
                      ['Montréal', 'San Francisco']
                      )
    ])])

if __name__ == '__main__':
    app.run_server(debug=True)
