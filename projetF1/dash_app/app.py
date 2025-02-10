import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
from pymongo import MongoClient
import time
from flask_caching import Cache
import re
import numpy as np

MONGO_URI = "mongodb://mongodb:27017"
for i in range(10):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        if 'f1_data' not in client.list_database_names():
            raise Exception("La base de données 'f1_data' n'existe pas.")
        db = client['f1_data']
        if 'race_results' not in db.list_collection_names():
            raise Exception("La collection 'race_results' n'existe pas.")
        print("Connexion à MongoDB réussie et base trouvée !")
        break
    except Exception as e:
        print(f"Tentative {i+1} : {e}, nouvelle tentative dans 5s...")
        time.sleep(5)

# Accès à la base de données
collection = db['race_results']

#Mise en cache pour améliorer les performances
app = dash.Dash(__name__)
server = app.server
cache = Cache(server, config={'CACHE_TYPE': 'simple'})

@cache.memoize(timeout=600)
def get_data():
    return list(collection.find({}, {'_id': 0}))

data = get_data()
df = pd.DataFrame(data)

#Filtrage des entrées sans "Nom"
df = df[df["Nom"].notna()]

#Dictionnaire de correspondance entre les stats brutes et lisibles
stat_mapping = {
    "Stat_1": "Engagements",
    "Stat_2": "Grands Prix",
    "Stat_3": "Non participations",
    "Stat_6": "Coéquipiers",
    "Stat_7": "Saisons",
    "Stat_8": "Constructeurs",
    "Stat_9": "Motoristes",
    "Stat_10": "Modèles",
    "Stat_11": "Victoires",
    "Stat_12": "Pole Positions",
    "Stat_13": "Meilleurs Tours",
    "Stat_14": "Podiums",
    "Stat_15": "Hat Tricks",
    "Stat_16": "Grands Chelems",
    "Stat_17": "Abandons",
    "Stat_18": "Points",
    "Stat_19": "Tours en tête"
}

df = df.rename(columns={k: v for k, v in stat_mapping.items() if k in df.columns})

#Extraction et validation des valeurs numériques
def extract_number(value):
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        match = re.search(r"(\d+\.\d+|\d+)", value.replace(",", "."))
        if match:
            try:
                return float(match.group())
            except ValueError:
                return np.nan
    return np.nan

for col in stat_mapping.values():
    if col in df.columns:
        df[col] = df[col].apply(extract_number)

df.fillna(np.nan, inplace=True)  # Remplace les valeurs manquantes par np.nan

#Correction des valeurs manquantes logiques
if "Grands Prix" in df.columns and "Engagements" in df.columns:
    df["Grands Prix"] = df["Grands Prix"].fillna(df["Engagements"])

#Pré-calcul des moyennes pour optimiser les performances
moyennes_globales = df[stat_mapping.values()].mean()

#Graphique du nombre de Grands Prix par pilote
df_sorted = df.sort_values(by='Grands Prix', ascending=False)
default_fig_grands_prix = go.Figure()
default_fig_grands_prix.add_trace(go.Bar(
    x=df_sorted['Nom'],
    y=df_sorted['Grands Prix'],
    marker_color='purple'
))
default_fig_grands_prix.update_layout(
    title="Nombre de Grands Prix par pilote",
    xaxis_title="Pilotes",
    yaxis_title="Nombre de Grands Prix",
    xaxis={'categoryorder': 'total descending'},
    height=600
)

#Layout Dash
app.layout = html.Div([
    html.H1("Comparaison des Pilotes de F1"),
    dcc.Dropdown(
        id='pilote-selector',
        options=[{'label': nom, 'value': nom} for nom in df['Nom']],
        placeholder="Sélectionnez un pilote"
    ),
    html.Div(id='info-pilote'),
    dcc.Graph(id='graphique-stats'),
    dcc.Graph(id='graphique-grands-prix', figure=default_fig_grands_prix)
])

@app.callback(
    [Output('info-pilote', 'children'),
     Output('graphique-stats', 'figure')],
    [Input('pilote-selector', 'value')]
)
def update_graph(pilote_selectionne):
    if not pilote_selectionne or pilote_selectionne not in df['Nom'].values:
        return html.P("Sélectionnez un pilote valide."), go.Figure()

    pilote_info = df[df['Nom'] == pilote_selectionne]
    if pilote_info.empty:
        return html.P("Données indisponibles pour ce pilote."), go.Figure()

    pilote_info = pilote_info.iloc[0]

    fig_stats = go.Figure()
    fig_stats.add_trace(go.Bar(
        x=list(stat_mapping.values()),
        y=[pilote_info.get(col, 0) if pd.notna(pilote_info.get(col)) else None for col in stat_mapping.values()],
        name=f"{pilote_selectionne}",
        marker_color='blue'
    ))
    fig_stats.add_trace(go.Bar(
        x=list(stat_mapping.values()),
        y=[moyennes_globales[col] if pd.notna(moyennes_globales[col]) else None for col in stat_mapping.values()],
        name="Moyenne des pilotes",
        marker_color='red'
    ))

    fig_stats.update_layout(
        title=f"Statistiques de {pilote_selectionne} comparées à la moyenne",
        xaxis_title="Statistiques",
        yaxis_title="Valeurs (échelle logarithmique)",
        barmode='group',
        yaxis_type="log"
    )

    info_pilote = html.Table([
        html.Tr([html.Th("Statistique"), html.Th("Valeur")])
    ] + [
        html.Tr([html.Td(col), html.Td(pilote_info.get(col, "N/A"))]) for col in stat_mapping.values()
    ], style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'})

    return info_pilote, fig_stats

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)
