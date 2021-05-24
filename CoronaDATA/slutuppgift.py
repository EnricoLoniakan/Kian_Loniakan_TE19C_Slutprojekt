#importerar biblitek som best passar projektet

from dash_html_components.Div import Div
import pandas as pd                             # Panda biblioteket för att kunna läsa in datan med "pd.read_csv"
import matplotlib.pyplot as plt                #Vid behov av matplotlib
import plotly.express as px                   #Plotly biblitoket för att rita upp graferna 
from plotly.subplots import make_subplots  #Vid behov av subplot
import plotly.graph_objects as go         
import dash                                #Dash biblioteket för att kunna få fram en dashboard för graferna
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc            # Dash_bootsrap_components hjälper dashboardens utseende med bootstrap biblioteket

#All data som programmet behöver läsa in

Regional_Total_Data = pd.read_csv("Regional_Totals_Data.csv")  # varsin variabel för att enkelt förstå vart de tillhör

Gender_Data = pd.read_csv("Gender_Data.csv")

Regional_Daily_Cases = pd.read_csv("Regional_Daily_Cases.csv")



app = dash.Dash(__name__) 

#Variabler för de olika graferna

# px.'namn på typ av graf'(datan, x="xvärde", y="yvärde")...

Regional_cases_Scatter = px.scatter(Regional_Total_Data, x="Total_Deaths", y="Total_Cases", color="Region", size="Total_Cases",labels=dict(Total_Cases="Totala fall", Total_Deaths="Totala döda"),title='Corona regionalt (scatter)')

Gender_Data_Piechart_Cases = px.pie(Gender_Data, values="Total_Cases", names="Gender",title='Antal fall')

Gender_Data_Piechart_Deaths = px.pie(Gender_Data, values="Total_Deaths", names="Gender",title=' Antal döda')

Regional_Daily_Cases_lines = px.line(Regional_Daily_Cases, x="Date", y="Sweden_Total_Daily_Cases", hover_data={"Date": "|%B %d, %Y"},labels=dict(Sweden_Total_Daily_Cases="Totala fall", Date="Datum"))

# app.layout alltså själva dash layouten som byggs som html, allt inom diven är sånt som kommer upp på dashboarden

app.layout = html.Div(children=[
    html.H1("Kians Corona Grafer", className="h1"),  # html h1 till dashboarden 


dbc.Row( # dbc.Row med hjälp av bootstrap lägger allt inom på en rad på dashboarden vilket med width kan välja olika storlekar, dbc.Row funkar ungeför som Div

    [

    dbc.Col(dcc.Dropdown(      #dbc.Col hjälper dropdownen bli bootstrap anpassad
            id='total',
            options=[
                {'label': 'Totala fall', 'value': 'Total_Cases'},   #val på dropdownen , label='namn', value='vad som skall visas'
                {'label': 'Totala döda', 'value': 'Total_Deaths'},
    ],
            value='Total_Cases'    #standard värde då hemsidan startas
        ),
        
        width={'size': 3, "offset": 0, 'order': 3}, # size hur mycket av en rad den ska ta upp (max: 12), offset är hur långt ifrån start den skall börja

        ),

    ]),

dbc.Row(

    [
        
        dbc.Col(dcc.Graph(id='Stapel'),
        width=6, md={'size': 6, "offset": 0, 'order': 'first'}, # då width och size delas upp så bestämmer width antal rad upptagelse och size storlek på grafen

        ),     # order hjälper programmet veta vilken av graferna som skall komma först


    dbc.Col(dcc.Graph(
        
        id='Scatter',      #identity

        figure=Regional_cases_Scatter),                   # figure eller fig får fram grafen som skriven 
        width=6, md={'size': 6, "offset": 0, 'order': 'last'},
                
         ),

    


]),

dbc.Row(

[

dbc.Row(dbc.Col(html.H1(children = "Totala fall samt döda inom kön"),
                width={'size': 6, 'offset': 3},

),

),

]),


dbc.Row(

[
    
    dbc.Col(dcc.Graph(
        
        id='Piechart1',

        figure=Gender_Data_Piechart_Cases),

         width=6, md={'size': 6, "offset": 0, 'order': 'first'},


    ),

    dbc.Col(dcc.Graph(
        
        id='Piechart2',

        figure=Gender_Data_Piechart_Deaths),

         width=6, md={'size': 6, "offset": 0, 'order': 'last'}

    )


]),


html.Div(children=[                                               #testar o lägga upp en graf med en div istället för bootsrap
    html.H1(children = "Sveriges totala fall under en period"),  
    dcc.Graph(
        
        id='Linechart',

        figure=Regional_Daily_Cases_lines
                
         )

])

])


@app.callback(
    Output("Stapel", "figure"),   # output beskriver vad som skall ges ut vilket i detta fall är barcharten
    [Input("total", "value")]          #input beskriver vad som skall tas in 
    
)

def update_figure(value):  #med hjälp av "def update_figure() så kan jag få fram en graf på ett annorlunda sätt en tidigare"


        fig = px.bar(Regional_Total_Data, y=value, x="Region",title='Corona regionalt')             #ritar upp graf på ett annorlunda sätt.
        fig.update_layout(transition_duration=500,xaxis_title="Totala döda",yaxis_title="Totala fall", 
                
        )

        

        return fig


if __name__ == "__main__":              #startar servern
    app.run_server(debug = True)

    
