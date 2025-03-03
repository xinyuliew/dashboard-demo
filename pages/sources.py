import dash
import dash_mantine_components as dmc
from dash import html
import dash_bootstrap_components as dbc
from utils import create_notification
# Initialize Dash app
dash.register_page(__name__, path='/sources')

def sources_layout():
    layout = html.Div([
        dbc.Row([
                    dbc.Col([
                         create_notification("This page provides information about all the detailed methodology used in this project.")
                    ])
                ]),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    children=[
                        dbc.CardBody(
                            dmc.Accordion(
                                value=["datasets"],  # Default open item (can be changed)
                                children=[
                                    dmc.AccordionItem(
                                        [
                                            dmc.AccordionControl("Datasets"),
                                            dmc.AccordionPanel([
                                                html.P([
                                                    "Brambilla, Marco; Kharmale, Kalyani, 2022, ",
                                                    html.I("COVID-19 Vaccine Discussions on Reddit with Sentiment, Stance, Topics, and Timing"),
                                                    ", ",
                                                    html.A(
                                                        "https://doi.org/10.7910/DVN/XJTBQM",
                                                        href="https://doi.org/10.7910/DVN/XJTBQM",
                                                        target="_blank"
                                                    ),
                                                    ", Harvard Dataverse, V1, UNF:6:A7rRHB0MLPukoDLRzdIIgQ== [fileUNF]"
                                                ])
                                            ]),
                                        ],
                                        value="datasets",
                                    ),
                                    dmc.AccordionItem(
                                        [
                                            dmc.AccordionControl("Models"),
                                            dmc.AccordionPanel([
                                                html.P([
                                                    "Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). ",
                                                    html.I("BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"),
                                                    ". ",
                                                    "In Proceedings of NAACL-HLT 2019 (pp. 4171–4186). ",
                                                    html.A(
                                                        "https://doi.org/10.48550/arXiv.1810.04805",
                                                        href="https://doi.org/10.48550/arXiv.1810.04805",
                                                        target="_blank"
                                                    )
                                                ])
                                            ]),
                                        ],
                                        value="models",
                                    ),
                                    dmc.AccordionItem(
                                        [
                                            dmc.AccordionControl("Tools"),
                                            dmc.AccordionPanel([
                                                html.P([
                                                    "Dash, Plotly, Pandas, Scikit-learn, Hugging Face..."
                                                ])
                                            ]),
                                        ],
                                        value="tools",
                                    ),
                                    dmc.AccordionItem(
                                        [
                                            dmc.AccordionControl("Methodology"),
                                            dmc.AccordionPanel([
                                                html.P([
                                                    "In the future, we will provide more information about additional data sources and the methodology used to collect and analyse the data in supporting the improved analysis."
                                                   ])
                                            ]),
                                        ],
                                        value="methodology",
                                    ),
                                ],
                            )
                        ),
                    ],
                ),
            ])
        ]),
    ])

    return layout

layout = sources_layout()