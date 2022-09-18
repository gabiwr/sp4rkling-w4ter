# importing libraries
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
# from st_aggrid import AgGrid
import random
import datetime
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype
)
# import pydeck as pdk

st.set_page_config(page_title='Restaurantes Rio de Janeiro',
                   layout='centered', initial_sidebar_state='auto')


RestaurantsDB = pd.read_excel('Rests-Rio.xlsx', sheet_name='DB')

RestaurantsDB.set_index('Nome', inplace=True)

abas = ['Geral', 'Preferidos', 'Novos', 'Aleatório', 'Mapa']

choice = st.sidebar.selectbox('Como será a sua escolha hoje?', abas)

st.title('Restaurantes Cariocas da Gabi')

if choice == 'Geral':

    GeralDF = RestaurantsDB
    del GeralDF['Ja fui?']
    del GeralDF['Preferido']

    # GeralDF.set_index('Nome', inplace=True)



    # for index,row in GeralDF.iterrows():
    #     Preco = range(int(row['PreçoMin']), int(row['PreçoMax'])+1)
    #     PrecoRange.append(Preco)
    #     Variacao.append(f'R${int(row.PreçoMin)} - R${int(row.PreçoMax)}')
    # GeralDF['Preço range'] = PrecoRange
    # GeralDF['Faixa de preço'] = Variacao


    # print(GeralDF['Faixa de preço'])

    # Filling null executive prices with their regular price
    GeralDF.PreçoE.fillna(GeralDF.Preço, inplace=True)
    GeralDF.PreçoEMin.fillna(GeralDF.PreçoMin, inplace=True)
    GeralDF.PreçoEMax.fillna(GeralDF.PreçoMax, inplace=True)

    # print(GeralDF)


    # ------------------------------------------------------------------------

    Geral = GeralDF.copy()

            # FILTERING :)

    # Select what category to filter

    executivo = st.checkbox("Almoço executivo?")

    if executivo:
        del Geral['PreçoMin']
        del Geral['PreçoMax']
        Geral['PreçoMin'] = Geral['PreçoEMin']
        Geral['PreçoMax'] = Geral['PreçoEMax']

    PrecoRange = []
    Variacao = []   
    for index,row in Geral.iterrows():
        Preco = range(int(row['PreçoMin']), int(row['PreçoMax'])+1)
        PrecoRange.append(Preco)
        Variacao.append(f'R${int(row.PreçoMin)} - R${int(row.PreçoMax)}')
    Geral['Preço range'] = PrecoRange
    Geral['Faixa de preço'] = Variacao

    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect("Filtrar opções por:", ['Ocasião','Localização', 'Faixa de preço', 'Culinária'])

        # Filter chosen category
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            if column in ['Ocasião','Localização', 'Culinária']:
                left, right = st.columns((1, 20))
                user_cat_input = right.multiselect(
                    f"Opções de {column}:",
                    Geral[column].unique(),
                    default=list(Geral[column].unique()),
                )
                Geral = Geral[Geral[column].isin(user_cat_input)]
            else:
                _min = float(Geral['PreçoMin'].min())
                _max = float(Geral['PreçoMax'].max())
                step = (_max - _min) / 40
                user_num_input = right.slider(
                    f"Para faixas de preço",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                Geral = Geral[((min(user_num_input) < Geral['PreçoMin'] )&(Geral['PreçoMin'] < max(user_num_input))) 
                | ((min(user_num_input) < Geral['PreçoMax'])&(Geral['PreçoMax'] < max(user_num_input))) 
                | ((Geral['PreçoMin'] < min(user_num_input))&(min(user_num_input) < Geral['PreçoMax']))]

    st.dataframe(Geral[['Culinária', 'Localização','Sub-Localização' , 'Faixa de preço', 'Ocasião']])

 # ------------------------------------------------------------------------

if choice == 'Preferidos':
    st.subheader('Quer ir pra algum dos seus preferidos?')

    PreferidosDF = RestaurantsDB[RestaurantsDB['Preferido'] == 'sim']
    PreferidosDF.PreçoEMin.fillna(PreferidosDF.PreçoMin, inplace=True)
    PreferidosDF.PreçoEMax.fillna(PreferidosDF.PreçoMax, inplace=True)

    Preferidos = PreferidosDF.copy()

    executivo = st.checkbox("Almoço executivo?")

    if executivo:
        del Preferidos['PreçoMin']
        del Preferidos['PreçoMax']
        Preferidos['PreçoMin'] = Preferidos['PreçoEMin']
        Preferidos['PreçoMax'] = Preferidos['PreçoEMax']


    Variacao = []   
    for index,row in Preferidos.iterrows():
        Variacao.append(f'R${int(row.PreçoMin)} - R${int(row.PreçoMax)}')
    Preferidos['Faixa de preço'] = Variacao


    # Filtering
    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect("Filtrar opções por:", ['Ocasião','Localização', 'Faixa de preço', 'Culinária'])

        # Filter chosen category
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            if column in ['Ocasião','Localização', 'Culinária']:
                left, right = st.columns((1, 20))
                user_cat_input = right.multiselect(
                    f"Opções de {column}:",
                    Preferidos[column].unique(),
                    default=list(Preferidos[column].unique()),
                )
                Preferidos = Preferidos[Preferidos[column].isin(user_cat_input)]
            else:
                _min = float(Preferidos['PreçoMin'].min())
                _max = float(Preferidos['PreçoMax'].max())
                step = (_max - _min) / 40
                user_num_input = right.slider(
                    f"Para faixas de preço",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                Preferidos = Preferidos[((min(user_num_input) < Preferidos['PreçoMin'] )&(Preferidos['PreçoMin'] < max(user_num_input))) 
                | ((min(user_num_input) < Preferidos['PreçoMax'])&(Preferidos['PreçoMax'] < max(user_num_input))) 
                | ((Preferidos['PreçoMin'] < min(user_num_input))&(min(user_num_input) < Preferidos['PreçoMax']))]
    st.dataframe(Preferidos[['Culinária', 'Localização','Sub-Localização' , 'Faixa de preço', 'Ocasião', 'Descrição']])

# ------------------------------------------------------------------------

if choice == 'Novos':
    NovosDF = RestaurantsDB[RestaurantsDB['Ja fui?'] != 'sim']
    NovosDF.PreçoEMin.fillna(NovosDF.PreçoMin, inplace=True)
    NovosDF.PreçoEMax.fillna(NovosDF.PreçoMax, inplace=True)

    Novos = NovosDF.copy()

    executivo = st.checkbox("Almoço executivo?")

    if executivo:
        del Novos['PreçoMin']
        del Novos['PreçoMax']
        Novos['PreçoMin'] = Novos['PreçoEMin']
        Novos['PreçoMax'] = Novos['PreçoEMax']


    Variacao = []   
    for index,row in Novos.iterrows():
        Variacao.append(f'R${int(row.PreçoMin)} - R${int(row.PreçoMax)}')
    Novos['Faixa de preço'] = Variacao


    # Filtering
    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect("Filtrar opções por:", ['Ocasião','Localização', 'Faixa de preço', 'Culinária'])

        # Filter chosen category
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            if column in ['Ocasião','Localização', 'Culinária']:
                left, right = st.columns((1, 20))
                user_cat_input = right.multiselect(
                    f"Opções de {column}:",
                    Novos[column].unique(),
                    default=list(Novos[column].unique()),
                )
                Novos = Novos[Novos[column].isin(user_cat_input)]
            else:
                _min = float(Novos['PreçoMin'].min())
                _max = float(Novos['PreçoMax'].max())
                step = (_max - _min) / 40
                user_num_input = right.slider(
                    f"Para faixas de preço",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                Novos = Novos[((min(user_num_input) < Novos['PreçoMin'] )&(Novos['PreçoMin'] < max(user_num_input))) 
                | ((min(user_num_input) < Novos['PreçoMax'])&(Novos['PreçoMax'] < max(user_num_input))) 
                | ((Novos['PreçoMin'] < min(user_num_input))&(min(user_num_input) < Novos['PreçoMax']))]
    st.dataframe(Novos[['Culinária', 'Localização','Sub-Localização' , 'Faixa de preço', 'Ocasião', 'Descrição']])


# ------------------------------------------------------------------------

if choice == 'Aleatório':
    
    AleatorioDF = RestaurantsDB.copy()
    AleatorioDF.PreçoEMin.fillna(AleatorioDF.PreçoMin, inplace=True)
    AleatorioDF.PreçoEMax.fillna(AleatorioDF.PreçoMax, inplace=True)

    Variacao = []   
    for index,row in AleatorioDF.iterrows():
        Variacao.append(f'R${int(row.PreçoMin)} - R${int(row.PreçoMax)}')
    AleatorioDF['Faixa de preço'] = Variacao

    Aleatorio = AleatorioDF[['Culinária', 'Localização','Sub-Localização' , 'Faixa de preço', 'Ocasião', 'Descrição']]
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        rand = st.button('Escolher restaurante aleatório')
    if rand:
        index = random.randint(-1, len(Aleatorio.index.to_list()))
        st.subheader(f'O restaurante escolhido foi {Aleatorio.index[index]}')
        st.dataframe(Aleatorio.iloc[index,:], width=500)

# ------------------------------------------------------------------------

if choice == 'Mapa':
    RestaurantsDB.reset_index(inplace=True)

    fig = px.scatter_mapbox(RestaurantsDB, lat="latitude", lon="longitude", hover_name="Nome", hover_data=["Ocasião", "Culinária"],
                        color_discrete_sequence=["maroon"], zoom=14, height = 700)
    fig.update_layout(mapbox_style="open-street-map")
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    left, right = st.columns((20,1))
    with left:
        st.plotly_chart(fig)