import datetime as dt
import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
from dateutil.relativedelta import relativedelta


st.title("🎈 Filter com")
st.write(
    "Filter commands."
)

# if not hasattr(st.session_state,"longRun") :
#     st.session_state.longRun=True
#     'Starting a long computation...'

#     # Add a placeholder
#     latest_iteration = st.empty()
#     bar = st.progress(0)

#     for i in range(10):
#         # Update the progress bar with each iteration.
#         latest_iteration.text(f'Iteration {i+1}')
#         bar.progress(i + 1)
#         time.sleep(0.1)

#     '...and now we\'re done!'


# x=-1
# if x<0 : x=0
# if not hasattr(st.session_state,"slider"): toto=0 
# else: toto=st.session_state.slider
# map_data = pd.DataFrame(
#     np.random.randn(100, 2) / [50, 50] + [49,toto],
#     columns=['lat', 'lon'])

# st.map(map_data)

# x = st.sidebar.slider('x',key="slider")  # 👈 this is a widget
# st.write(x, 'squared is', x * x)

# if st.sidebar.checkbox('Show dataframe'):
#     chart_data = pd.DataFrame(
#        np.random.randn(20, 3),
#        columns=['a', 'b', 'c'])

#     chart_data

# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
#     })

# option = st.sidebar.selectbox(
#     'Which number do you like best?',
#      df['first column'])

# 'You selected: ', option

# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")

# if "df" not in st.session_state:
#     st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

# st.header("Choose a datapoint color")
# color = st.color_picker("Color", "#FF0000")
# st.divider()
# st.scatter_chart(st.session_state.df, x="x", y="y", color=color)

## Range selector
# cols1,_ = st.sidebar.columns((1,2)) # To make it narrower
format = 'MMM DD, YYYY'  # format output
start_date = dt.date(year=2007,month=1,day=1)-relativedelta(years=0)  #  I need some range in the past
end_date = dt.datetime.now().date()-relativedelta(years=0)
max_days = end_date-start_date
d =  dt.datetime.now().date()-relativedelta(years=1)
# slider = st.sidebar.slider('Years', min_value=start_date, value=end_date ,max_value=end_date, format=format)        
years = st.sidebar.slider('Years', start_date, end_date ,(d,end_date), format=format)
## Sanity check
# st.table(pd.DataFrame([[start_date, slider, end_date]],
#                       columns=['start',
#                                'selected',
#                                'end'],
#                       index=['date']))

# Show a slider widget with the years using `st.slider`.
# years = st.sidebar.slider("Years", 2007, 2024, (2023, 2024))
#combo client
data = requests.get("http://gaston.caps-tech.com:3023/api/v1/client").json()
df = pd.DataFrame(data)
df_splitted = df['groups'].str.split('-',n=1, expand=True)[1]

@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    return df

if not st.sidebar.checkbox('Tous les clients'):
    #'You selected: ', comboClient.split('-')[0]
    allClient = False
else:
    allClient=True

comboClient = st.sidebar.selectbox(
    'Which client?',
     df, disabled=allClient,key="combo")

df = load_data(st.secrets["COM_URL"])

# Show a multiselect widget with the genres using `st.multiselect`.
status = st.sidebar.multiselect(
    "status",
    df.com_status_id.unique(),
    [5],
)

# Show a multiselect widget with the genres using `st.multiselect`.
centilisations = st.sidebar.multiselect(
    "centilisations",
    df.com_centilisation.unique(),
    [75,300],
)
# Show a multiselect widget with the genres using `st.multiselect`.
typeTimbre = st.sidebar.multiselect(
    "type timbre",
    df.com_type_timbre.unique(),
    ["VERT_CHAMPAGNE"],
)
def highlight_vc(s):
    if s.com_type_timbre=="VERT_CHAMPAGNE" :  return ['background-color: green']*len(s)

def highlight_vc_color(s):
    return ['color: white']*len(s) if s.com_type_timbre=="VERT_CHAMPAGNE" else ['color: black']*len(s)
def highlight_ldv(s):
    if s.com_type_timbre=="LIE_DE_VIN" :  return ['background-color: #641835']*len(s) 
    if s.com_type_timbre=="VERT_CHAMPAGNE" :  return ['background-color: green']*len(s)
    if s.com_type_timbre=="VERT" :  return ['background-color: #90EE90']*len(s)
    if s.com_type_timbre=="BLEU" :  return ['background-color: blue']*len(s)
    if s.com_type_timbre=="BLANC_VAT_18%" :  return ['background-color: beige']*len(s)
    if s.com_type_timbre=="BLANC_VAT_40%" :  return ['background-color: beige']*len(s)
    if s.com_type_timbre=="GRIS" :  return ['background-color: #EEEEEE']*len(s)
    if s.com_type_timbre=="EXPORT" :  return ['background-color: #EDC9F9']*len(s)
    else:
        return ['background-color: white']*len(s)

def highlight_ldv_color(s):
    return ['color: white']*len(s) if s.com_type_timbre=="LIE_DE_VIN" else ['color: black']*len(s)


#df_filtered = df[(df["com_date_livraison"].between(years[0]+"-01-01", years[1]+"01-01"))]

df_date = df["com_date_livraison"].str.split('T',n=1,expand=True)[0]
df.com_date_livraison = df_date
df['com_date_livraison'] = pd.to_datetime(df['com_date_livraison'], format='%Y-%m-%d')
if allClient : 
    filtered_df = df.loc[(df['com_date_livraison'] >= f'{years[0]}')
                        & (df['com_date_livraison'] <f'{years[1]}')
                        & df["com_status_id"].isin(status)
                        & df["com_centilisation"].isin(centilisations)
                        & df["com_type_timbre"].isin(typeTimbre)
                        ]
else:
    filtered_df = df.loc[(df['com_date_livraison'] >= f'{years[0]}')
                     & (df['com_date_livraison'] <f'{years[1]}')
                     &  (df['com_client_id'] == int(comboClient.split('-')[0]))
                     & (df['com_date_livraison'] <f'{years[1]}')
                     & df["com_status_id"].isin(status)
                     & df["com_centilisation"].isin(centilisations)
                     & df["com_type_timbre"].isin(typeTimbre)   
                     ]

styled_df = filtered_df.style.apply(highlight_ldv,axis=1).apply(highlight_ldv_color,axis=1)

# Display the data as a table using `st.dataframe`.
st.dataframe(
    styled_df,
    use_container_width=True,
    column_config={"": st.column_config.TextColumn("Id"),
                   "com_id": st.column_config.TextColumn("ordre"),
                   "com_client_id": st.column_config.TextColumn("client"),
                   "com_client_site": st.column_config.TextColumn("site"),
                   "com_quantite": st.column_config.TextColumn("quantité"),
                   "com_prix_au_mille_ht": st.column_config.NumberColumn(
                        "Prix",
                        help="The price of the product in euros",
                        step=0.01,
                        format="€ %.2d",
                    ),
                    "com_unite":None,
                    "com_type":None,
                    "com_transformation":None,
                    "com_stock_alloue":None,
                    "com_stock_commande":None,
                    "com_stockfourn_num_commande":None,
                    "com_date_modif":None,
                    "com_facture_num" :st.column_config.NumberColumn(
                        "Facture",
                        help="Numéo de facture",
                        step=1,
                        min_value=1,
                        format="F %d",
                    ),
                   # "com_date_livraison": st.column_config.TextColumn("date"),
                   
                    "com_date_livraison": st.column_config.DatetimeColumn(
                        "date",
                        #min_value=datetime(2023, 6, 1),
                        #max_value=datetime(2025, 1, 1),
                        format="YYYY-MM-DD",
                    ),}

)





