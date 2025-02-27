from dash import dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash_loading_spinners import Hash

from pages.constantes import LIMA

from ..data import DATA

Fallos = dbc.Row(dbc.Col(Hash(html.Div(id='fallos-judiciales', className="navbar-nav-scroll", ), color=LIMA), class_name="mt-5"))

@callback(
        Output('fallos-judiciales','children'),
        [
            Input("select-voces-tematicas",'value'),
            Input("select-provincia",'value'),
            Input("select-tipo-fallo",'value'),
        ]
)
def update_fallos(voces, provincia, tipo):
    df = DATA['contenido'].copy()
    cards = []

    if voces and not "Todas" in voces:
        df = df[df['Voces temáticas']==voces]
    if provincia and not "Todos" in provincia:
        df = df[df['Provincia']==provincia]
    if tipo and not "Todos" in tipo:
        df = df[df['Tipo de fallo']==tipo]


    if len(df) == 0:
        cards.append(dbc.Card(dbc.CardBody(
            html.Div([
                html.P("No hay resultados para los filtros aplicados"),
            ], className="poppins text-center small mx-2")
        ), className="mx-3 p-3 card-jurisprudencia"))
    else:
        for _, row in df.iterrows():
            cards.append(dbc.Card(dbc.CardBody(
                html.Div([
                    html.Div([
                        html.Span([html.B('AÑO: '), f"{row['Año']}"], className="mx-2"),
                        html.Span([html.B('PROVINCIA: '), f"{row['Provincia']}"], className="mx-2"),
                        html.Span([html.B('CIUDAD: '), f"{row['Ciudad']}"], className="mx-2"),
                    ], className="text-end juris-encabezado"),
                    html.Hr(),
                    html.P([html.B("VOCES TEMÁTICAS: "), row['Voces temáticas']]),
                    html.P([html.B("JURISDICCIÓN TERRITORIAL: "), row['Jurisdicción territorial']]),
                    html.P([html.B("ORGANISMO: "), row['Organismo judicial o administrativo']]),
                    html.P([html.B("AUTOS: "), row['Autos']]),
                    html.Hr(),
                    html.P([html.B("TIPO DE FALLO: "), row['Tipo de fallo']]),
                    html.P([html.B("SÍNTESIS DE FALLO: "), html.U(f"Página: {row['Página']}")]),
                    html.P(row['Sintesis del fallo']),
                    html.A("Ver fallo completo", href=f"https://drive.google.com/file/d/17qtstKAxwjIn3aqND3kISzkPJjO7l3aF/view#page={row['Página']}", target="_blank", className="btn btn-primary text-dark")
                ], className="poppins small mx-2")
            ), className="mb-4 mx-3 p-3 card-jurisprudencia"))
                
    return cards