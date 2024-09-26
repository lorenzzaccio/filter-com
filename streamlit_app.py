import datetime as dt
import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
from dateutil.relativedelta import relativedelta

st.set_page_config(
   page_title="Ex-stream-ly Cool App",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

percentage_width_main = 100
# Inject custom CSS to set the width of the sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 500px !important; # Set the width to your desired value
        }
   
        .appview-container .main .block-container{{
            max-width: {percentage_width_main}%;
            padding-top: {1}rem;
            padding-right: {1}rem;
            padding-left: {1}rem;
            padding-bottom: {1}rem;
              }}
        .uploadedFile {{display: none}}
        footer {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("🎈 Filter com")
st.write(
    "Filter commands."
)

format = 'MMM DD, YYYY'  # format output
start_date = dt.date(year=2007,month=1,day=1)-relativedelta(years=0)  #  I need some range in the past
end_date = dt.datetime.now().date()-relativedelta(years=0)
max_days = end_date-start_date
d =  dt.datetime.now().date()-relativedelta(days=100)     
years = st.sidebar.slider('Years', start_date, end_date ,(d,end_date), format=format)


@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    return df

# #combo client
df = load_data(st.secrets["CLIENT_URL"])
df_splitted = df['groups'].str.split('-',n=1, expand=True)[1]
if not st.sidebar.checkbox('Tous les status'):
    allStatus = False
else:
    allStatus=True

if not st.sidebar.checkbox('Tous les timbres'):
    allTimbre = False
else:
    allTimbre=True

if not st.sidebar.checkbox('Toutes les centilisations'):
    allCentili = False
else:
    allCentili=True

if not st.sidebar.checkbox('Tous les clients'):
    allClient = False
else:
    allClient=True

comboClient = st.sidebar.selectbox(
    'Which client?',
     df, disabled=allClient,key="combo")

df = load_data(st.secrets["COM_URL"])

# Show a multiselect widget with the genres using `st.multiselect`.
liste_status =  sorted(df.com_status_id.unique()) if allStatus else  [5]
status = st.sidebar.multiselect(
    "status",
    sorted(df.com_status_id.unique()),
    liste_status,
)

# Show a multiselect widget with the genres using `st.multiselect`.
liste_centili =  sorted(df.com_centilisation.unique()) if allCentili else [75,300]

centilisations = st.sidebar.multiselect(
    "centilisations",
    sorted(df.com_centilisation.unique()),
    liste_centili,
)
# Show a multiselect widget with the genres using `st.multiselect`.
liste_timbre =  df.com_type_timbre.unique() if allTimbre else["VERT_CHAMPAGNE"]
typeTimbre = st.sidebar.multiselect(
    "type timbre",
    df.com_type_timbre.unique(),
   liste_timbre,
)
def highlight_status(s):
    if s.com_status_id==1 :  return ['background-color: #641835']*len(s) 
    if s.com_status_id==2 :  return ['background-color: green']*len(s)
    if s.com_status_id==3 :  return ['background-color: #90EE90']*len(s)
    if s.com_status_id==4 :  return ['background-color: blue']*len(s)
    if s.com_status_id==5 :  return ['background-color: beige']*len(s)
    if s.com_status_id==6 :  return ['background-color: beige']*len(s)
    if s.com_status_id==7 :  return ['background-color: #EEEEEE']*len(s)
    if s.com_status_id==8 :  return ['background-color: #EDC9F9']*len(s)
    else:
        return ['background-color: white']*len(s)
    
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

df_date = df["com_date_livraison"].str.split('T',n=1,expand=True)[0]
df.com_date_livraison = df_date

names = {"VERT_CHAMPAGNE": ('🟩'),"VERT": ('🟩'),"BLEU": ('🟦'),"BLEU_BFAV": ('🟦'),  "BLANC_VAT_18": ('⬜'),"BLANC_VAT_18%": ('⬜'),"BLANC_VAT_40": ('⬜'),"BLANC_VAT_40%": ('⬜'),"LIE_DE_VIN": ('🟧'),"EXPORT":'⬜'," ":'🟡',"":'🟡',"GRIS":'⬛️' }
centi = {18: ('🐜'),18.75: ('🐜'),18.7: ('🐜'),20: ('🐝'),37.5: ('🐞'),50: ('🐠'),70: ('🐡'), 75: ('🐕'), 0: ('🐨'),100: ('🐬'),150: ('🐭'),300: ('🐯'),450: ('🐰'),600:'🐪',900:'🐫',1200:'🐵',1500:'🐴',15000:'🐳' }

df['sitecli_texteFiscal'] += " " + df['com_type_timbre'].map(lambda x: names[x][0]) +  df['com_centilisation'].map(lambda x: centi[x][0])

df = df.reindex(columns=['com_date_livraison', 'sitecli_addr1', 'com_quantite','com_ref_article_client','sitecli_texteFiscal', 'com_centilisation','com_client_id','com_status_id','com_type_timbre'])


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

filtered_df["com_centilisation"] = filtered_df["com_centilisation"].astype(str).apply(lambda x: x.replace('.0',''))
styled_df = filtered_df.style.apply(highlight_status,axis=1).apply(highlight_ldv_color,axis=1)
#rearrangecolumns order
# styled_df = styled_df[['com_date_livraison', 'sitecli_addr1', 'com_quantite','com_ref_article_client' 'sitecli_texteFiscal', 'com_centilisation']]

# Display the data as a table using `st.dataframe`.
st.dataframe(
    styled_df,
    use_container_width=True,
    column_config={
                  "com_date_livraison": st.column_config.DateColumn(
                        "date",
                        format="YYYY-MM-DD",
                    ),
                  "sitecli_texteFiscal": st.column_config.TextColumn("texte",width='small'),
                  "sitecli_addr1": st.column_config.TextColumn("client",width='small'),
                  "com_ref_article_client": st.column_config.TextColumn("ref",width='large'),
                   "com_quantite": st.column_config.TextColumn("quantité",width='small'),
                   "com_prix_au_mille_ht": st.column_config.NumberColumn(
                        "Prix",
                        help="The price of the product in euros",
                        step=0.01,
                        format="€ %.2d",
                        width='small'
                    ),
                    "":None,
                     "com_centilisation":None,
                    "com_num_com":None,
                    "com_id":None,
                    "offrecom_offrenum":None,
                    "com_ref_article_client_fact":None,
                    "com_prix_au_mille_ht_achat":None,
                    "liv_num_daa":None,
                    "offrecom_id":None,
                    "com_prix_au_mille_ht":None,
                    "com_desc_ordre":None,
                    "com_prefix":None,
                    "com_article_id":None,
                    "com_ref_article_client_etiq":None,
                    "com_client_site":None,
                    "com_unite":None,
                    "com_type":None,
                    "com_transformation":None,
                    "com_stock_alloue":None,
                    "com_stock_commande":None,
                    "com_stockfourn_num_commande":None,
                    "com_date_modif":None,
                    "com_facture_num":None,
                    "com_status_id":None,
                    "com_type_timbre":None,
                    "com_client_id":None,
                    }

)





