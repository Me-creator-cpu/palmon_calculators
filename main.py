import streamlit as st
import pandas as pd
import locale

cols_exp = ['Level from', 'Level to', 'Cost']
cols_comp = ['Level from', 'Cost']
cols_mut = ['Level', 'Step', 'Substep', 'Cost level']
cols_mut_full = ['Cost type', 'Cost']
cols_stars = ['Stars level', 'Unit Cost', 'Total']
cols_boss = ['Stars level', 'Unit Cost', 'Total']
cols_equip = ['Level', 'Opus pearls']
cols_equip_nov = ['Step', 'Name', 'Stars', 'Cost']

df_costs_exp=None
df_costs_comp=None
df_costs_mut=None
df_costs_mut_full=None
df_costs_stars=None
df_costs_boss=None
df_equip_data=None
df_equip_nov=None

data_values={
    "Value":["Energy","Crystals","Pieces","Level300"],
    "Icon":["🟢",     "💎",     "🧩",    "🔝"],
}
option_values=data_values['Icon']
map_values={"Energy":"🟢Energy",
            "Crystals":"💎Crystals",
            "Pieces":"🧩Pieces",
            "Level300":"🔝Level300" }

col_stars=st.column_config.NumberColumn(
        min_value=0,
        max_value=5,
        format="%d ⭐"
    )

def write_js_menu(bln=False): 
    # ---- HIDE STREAMLIT STYLE ----
    #class="stToolbarActionButton" data-testid="stToolbarActionButton"
    #
    hide_st_style = """
                <style>
                MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                stSidebar {visibility: display;}
                [data-testid="stSidebar"] {display: inline-block;}
                </style>
                """
    if bln:
        st.markdown(hide_st_style, unsafe_allow_html=True)    

def write_no_streamlit_link():
    #st.toast("Style applyed")
    hide_st_style = """
                    <style>
                    ._container_gzau3_1 _viewerBadge_nim44_23 {display:none;visibility: hidden;}
                    ._profileContainer_gzau3_53 {display:none;visibility: hidden;}
                    ._link_gzau3_10 {display:none;visibility: hidden;}
                    footer {visibility: hidden;}
                    [data-testid="appCreatorAvatar"] {display:none;visibility: hidden;}
                    [data-testid="stToolbarActionButtonLabel"] {display:none;visibility: hidden;}
                    [data-testid="stToolbarActionButtonIcon"] {display:none;visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def large_num_format(value):
    locale.setlocale(locale.LC_ALL, "fr_FR")
    try:
        return locale.format_string("%.0f", int(value), grouping=True)
    except:
        return None
        
def percent_format(value):
    try:
        ret=value*100
        return f"{ret:.2f}%"  # "12.34%"
    except:
        return empty()

def format_stars(x): #⭐
    try:
        return ("⭐" * int(x))[0:int(x)]
    except:
        return x

def str2number(val):
    try:
        t=str(val).replace(' ','')
        return int(t)
    except:
        return int(0)
        
def del_session_variable(var_key):
    try:
        del st.session_state[var_key]
    except:
        return None

def add_session_variable(var_key,var_value):
    del_session_variable(var_key)
    st.session_state[var_key]=var_value

def get_session_variable(var_key):
    try:
        return st.session_state[var_key]
    except:
        return None

def read_csv(file):
    try:
        df = pd.read_csv(file)
    except:
        df = None
    return df

def calcul_upgrade_costs(from_lvl=1,to_lvl=300):
    global df_costs_exp
    df=df_costs_exp.copy(deep=True)
    if df is not None:
        val_cost=df.loc[(df["Level from"] >= from_lvl) & (df["Level from"] <= to_lvl)]["Cost"].sum()
        return val_cost
    else:
        return None

def calcul_upgrade_comp_costs(from_lvl=1,to_lvl=30,formated=True):
    global df_costs_exp
    if df_costs_exp is not None:
        val_cost=get_upgrade_comp_costs(from_lvl,to_lvl)
        if formated:
            return large_num_format(val_cost)
        else:
            return val_cost
    else:
        return None

def get_upgrade_comp_costs(from_lvl=1,to_lvl=30):
    global df_costs_comp
    df=df_costs_comp.copy(deep=True)
    if df is not None:
        val_cost=df.loc[(df["Level from"] >= from_lvl) & (df["Level from"] <= to_lvl)]["Cost"].sum()
        return int(val_cost)
    else:
        return None

def obj_row(nb_cells=2,with_border=False):
    return st.columns(nb_cells,border=with_border, width="stretch")

def obj_multiselect(df,column):
    return st.multiselect(f"Filter values for {column}:", 
                          df[column].unique(), 
                          default=list(df[column].unique()))    
    
def build_chart_bar(df_chart,xField,yField,sLabel,selMin=1,selMax=30,with_slider=True, with_switch=False):
    if df_chart is not None:
        switch_axis = False
        try:
            if with_switch:
                switch_axis = st.toggle('Switch axis')
        except:
            switch_axis = False
        x_Field = xField
        y_Field = yField
        if switch_axis:
            x_Field = yField
            y_Field = xField            

        if with_slider==True:
            sel_min=selMin
            sel_max=selMax
            range_level_min, range_level_max= st.slider(
                label=sLabel,
                min_value=sel_min,
                max_value=sel_max,
                value=(sel_min,sel_max),
                step=1
            )
            df2=df_chart[[xField,yField]]
            df2['Selection']=df2.apply(lambda row: row[yField] if range_level_min <= row[xField] <= range_level_max else 0, axis=1)
            
            st.bar_chart(df2, x=x_Field, y=[y_Field,'Selection'], color=["#0068c9", "#ff4b4b"], stack=False)            
            df = df_chart.loc[(df_chart[x_Field] >= int(range_level_min)) & (df_chart[x_Field] <= int(range_level_max))]
            total_txt='Total Energy cost'
            to_txt='to'
            total_col = f"{total_txt} {range_level_min} {to_txt} {range_level_max}"
            try:
                st.markdown(f":orange-badge[{total_col} : {large_num_format(int(df[y_Field].sum()))}]")
            except:
                st.markdown(f":orange-badge[{total_col} : {int(df[y_Field].sum())}]")
            excel_loaded=True
            return range_level_min, range_level_max
        else:
            st.bar_chart(df_chart, x=x_Field, y=y_Field, stack=False)
            df = df_chart.loc[(df_chart[xField] >= int(selMin)) & (df_chart[xField] <= int(selMax))]
            total_txt='Total Crystals cost'
            to_txt='to'
            total_col = f"{total_txt} {selMin} {to_txt} {selMax}"
            st.markdown(f":orange-badge[{total_col} : {int(df[yField].sum())}]")
            return selMin,selMax

def build_table_any(df):
    st.dataframe(
        df,
        column_config={
            "Cost": st.column_config.NumberColumn(
                "Costs",
                min_value=0,
                max_value=10000000,
                step=1,
                format="compact",
            ),
            "Unit cost": st.column_config.NumberColumn(format="compact"),
            "Total": st.column_config.NumberColumn(format="compact"),
        },
        hide_index=True,
     )

def build_table_full_costs(df_src):
    df=df_src.copy()
    df['Type']=df['Type'].apply(lambda b: option_values[data_values['Value'].index(b)]+' '+b)
    st.dataframe(
            df,
            column_config={
                "Cost type": st.column_config.TextColumn(
                    "Cost type",
                ),                
                "Cost": st.column_config.NumberColumn(
                    "Costs",
                    min_value=0,
                    max_value=10000000,
                    step=1,
                    format="compact",
                ),
            },
            hide_index=True,
         ) 

def pg_home():
    st.title(f"{app_title}")
    
def pg_total_costs():
    global df_costs_mut_full,df_stars
    rowval = st.columns(2,border=False, width="stretch")
    with rowval[0]:
        st.subheader('Val') 
        build_table_full_costs(df_costs_mut_full)
    with rowval[1]:
        st.subheader('Stars')
        df_stars=df_costs_stars.copy(deep=True)
        #df_stars = df_stars[:-1]
        df_stars['Stars']=df_stars['Stars'].apply(lambda b: format_stars(b) )
        df_stars.at['Total','Unit cost']=df_stars['Unit cost'].mean()
        df_stars.at['Total','Total']=df_stars['Total'].sum()
        df_stars.at['Total','Stars']='Average / Total'
        build_table_any(df_stars) 
        
def pg_comp():
    global df_costs_comp
    st.subheader('Compétences')
    df = df_costs_comp
    range_level_min, range_level_max = build_chart_bar(df,'Level from','Cost','Coûts depuis le niveau:',int(1),int(30))
    
    with st.container(horizontal_alignment="center", 
                      vertical_alignment="center", 
                      border=True):
        nb_pal=st.slider('Nb Palmons', min_value=1, max_value=7, value=1, step=1)
        cost_unit=calcul_upgrade_comp_costs(from_lvl=range_level_min,to_lvl=range_level_max,formated=False)
        #st.write(cost_unit)
        # 200 / 80 / 40
        even_ratio=st.selectbox("Points ratio", [200,80,40])
        event_points=int(cost_unit)*int(even_ratio)
        cost_nb=int(cost_unit)*int(nb_pal)
        event_points_nb=int(cost_nb)*int(even_ratio)
        row1 = st.columns(3,border=False, width="stretch")
        row2 = st.columns(3,border=False, width="stretch")
        row3 = st.columns(3,border=False, width="stretch")
        with row1[0]:
            st.write(f"Coût évolution pour {nb_pal}:")
        with row1[1]:
            st.write(large_num_format(cost_nb))
        with row2[0]:
            st.write(f"Points événement:")
        with row2[1]:    
            st.write(large_num_format(event_points))
        with row3[0]:
            st.write(f"Points événement pour {nb_pal}:")
        with row3[1]:
            st.write(large_num_format(event_points_nb))

    with st.expander('Données du graphique', expanded=False, width="stretch"):
        build_table_any(df.loc[(df['Level from'] >= range_level_min) & (df['Level from'] <= range_level_max)])

def pg_costs():
    global df_costs_comp, df_costs_exp
    df = df_costs_exp
    df_pal=df_costs_exp
    df_pal
    st.subheader('Evolution')
    min_upg=df_pal.loc[(df_pal["Level from"] >= 1)]["Level"].min()
    max_upg=df.loc[(df["Cost"] >= 1)]["Level to"].max()
    range_level_min, range_level_max = build_chart_bar(df,'Level from','Cost','Coût depuis le niveau:',int(min_upg),int(max_upg))
    with st.container(horizontal_alignment="center", 
                      vertical_alignment="center", 
                      border=True):
        nb_pal=st.slider('Nb palmons', min_value=1, max_value=7, value=1, step=1)
        cost_unit=calcul_upgrade_costs(from_lvl=range_level_min,to_lvl=range_level_max)
        event_points=int(cost_unit)/int(2000)
        cost_nb=int(cost_unit)*int(nb_pal)
        event_points_nb=int(cost_nb)/int(2000)
        row1 = st.columns(3,border=False, width="stretch")
        row2 = st.columns(3,border=False, width="stretch")
        row3 = st.columns(3,border=False, width="stretch")
        with row1[0]:
            st.write(f"Coût évolution pour {nb_pal} UR:")
        with row1[1]:
            st.write(large_num_format(cost_nb))
        with row2[0]:
            st.write(f"Points événement:")
        with row2[1]:    
            if event_points>=int(15000):
                st.markdown(f':green[{large_num_format(event_points)}]')
            else:
                st.write(large_num_format(event_points))
        with row3[0]:
            st.write(f"Points événement pour {nb_pal} UR:")
        with row3[1]:
            if event_points_nb>=int(15000):
                st.markdown(f':green[{large_num_format(event_points_nb)}]')
            else:
                st.write(large_num_format(event_points_nb))
        
    with st.expander('Données du graphique', expanded=False, width="stretch"):
        build_table_any(df.loc[(df['Level from'] >= range_level_min) & (df['Level to'] <= range_level_max)])    

def pg_mut():
    global df_costs_mut
    st.header('Mutation') 
    df = df_costs_mut
    df_energy=df_costs_mut[(df['Step'] != 0)]
    df_energy=df_energy.groupby(['Level']).sum()
    df_energy.reset_index(level=0, inplace=True)
    df_crystal=df.loc[(df['Step'] == 0)]  
    st.subheader("🟢Energy")
    range_level_min, range_level_max = build_chart_bar(df_energy,'Level','Cost level','Coût mutation entre:',int(df_energy['Level'].min()),int(df_energy['Level'].max()))
    st.subheader("💎Crystals")
    df_crystal=df_crystal.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)]
    build_chart_bar(df_crystal,'Level','Cost level','Coût mutation entre:',int(df_crystal['Level'].min()),int(df_crystal['Level'].max()),False)
    with st.expander('Données du graphique', expanded=False, width="stretch"):
        st.subheader("🟢Energy", divider="green")
        build_table_any(df_energy.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)])
        st.subheader("💎Crystals", divider="blue")
        build_table_any(df_crystal.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)])        

def pg_equip():
    global df_equip_data
    st.header("✨ Equipement") 
    df = df_equip_data
    range_level_min, range_level_max = build_chart_bar(df,'Level','Opus pearls','Costs from level:',int(df['Level'].min()),int(df['Level'].max()),with_slider=True, with_switch=False)
    with st.expander('Données du graphique', expanded=False, width="stretch"):
        build_table_any(df.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)])

def pg_equip_nov():
    global df_equip_nov
    st.header("✨ Equipement Novice") 
    df = df_equip_nov
    
    lambda_steps = lambda x: str(x['Step']) + '.' + str(x['Stars'])
    lambda_name_ver = lambda x: (str(x['Name']).split(" ", 1)[0],str(str(x['Name'])+" ").split(" ", 1)[1])
    df['Steps'] = df.apply(lambda_steps, axis=1)
    df[['Category','Stage']]=df.apply(lambda_name_ver,axis=1, result_type='expand')    
    opt_cat = obj_multiselect(df,'Category')
    df_g=df[['Step','Cost']].set_index('Step').groupby("Step").sum()
    df_g.index.name = 'Idx'
    df_g['Step']=df_g.apply(lambda x: x.index)
    range_level_min, range_level_max = build_chart_bar(df_g,'Step','Cost','Costs from level:',int(df['Step'].min()),int(df['Step'].max()),with_slider=True, with_switch=False)
    with st.expander('Données du graphique', expanded=False, width="stretch"):
        df_filter=df.loc[(df['Step'] >= range_level_min) & (df['Step'] <= range_level_max) & (df["Category"].isin(opt_cat))]
        build_table_any(df_filter[['Step','Name','Stars','Cost']])

def pg_boss():
    global df_costs_boss
    rowval = st.columns(2,border=False, width="stretch")
    with rowval[0]:
        df=df_costs_boss
        st.subheader('Boss') 
        df_boss=df.copy(deep=True)
        df_boss['Stars']=df_boss['Stars'].apply(lambda b: format_stars(b) )
        df_boss['Total']=df_boss['Unit cost'].apply(lambda b: int(b)*int(5) )
        build_table_any(df_boss)


app_title='Calculateur Palmons'

st.set_page_config(
    page_title=app_title,
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Evolutions
df_costs_exp = read_csv('data/ps_pal_costs.csv')

#Compétences
df_costs_comp = read_csv('data/ps_pal_comp_costs.csv')

#Mutation
df_costs_mut = read_csv('data/ps_pal_mut_steps_costs.csv')

#Boss
df_costs_boss = read_csv('data/ps_boss_costs.csv')

#Equipement
df_equip_data = read_csv('data/ps_equip_costs.csv')
df_equip_nov = read_csv('data/ps_equip_nov_costs.csv')

# Coûts totaux
df_costs_mut_full = read_csv('data/ps_pal_mut_costs.csv')
df_costs_stars = read_csv('data/ps_pal_stars_costs.csv')

#pg_total_costs()

if 1 == 2:
    df_costs_exp
    df_costs_comp
    df_costs_mut
    df_costs_mut_full
    df_costs_stars
    df_costs_boss
    df_equip_data
    df_equip_nov

pages = {
    'Home':[ 
        st.Page(pg_home, title='Home', icon="🏠"),
    ],
    'Calculateurs':[ 
        st.Page(pg_costs, title='Evolution',icon="🗂️"),
        st.Page(pg_comp, title='Compétences',icon="📊"),
        st.Page(pg_mut, title='Mutation',icon="📊"),
    ],
    'Données':[ 
        st.Page(pg_equip, title='Equipement',icon="🗂️"),
        st.Page(pg_equip_nov, title='Equipement novice',icon="🗂️"),
        st.Page(pg_boss, title='Boss',icon="🗂️"),
        st.Page(pg_total_costs, title='Coûts totaux', icon="🔐"),
    ],
}
with st.sidebar:
    top_nav = 'Top menu'
    nav_sections = 'Menu avec rubriques'
    
pg = st.navigation(
    pages if nav_sections else [page for section in pages.values() for page in section],
    position="top" if top_nav else "sidebar"
)
pg.run() 
