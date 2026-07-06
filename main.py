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
        
def read_csv(file):
    try:
        df = pd.read_csv(file)
    except:
        df = None
    return df

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

def menu_tab_val():
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

df_costs_exp = read_csv('data/ps_pal_costs.csv')
df_costs_comp = read_csv('data/ps_pal_comp_costs.csv')
df_costs_mut = read_csv('data/ps_pal_mut_steps_costs.csv')
df_costs_mut_full = read_csv('data/ps_pal_mut_costs.csv')
df_costs_stars = read_csv('data/ps_pal_stars_costs.csv')
df_costs_boss = read_csv('data/ps_boss_costs.csv')
df_equip_data = read_csv('data/ps_equip_costs.csv')
df_equip_nov = read_csv('data/ps_equip_nov_costs.csv')

#menu_tab_val()

if 1 == 2:
    df_costs_exp
    df_costs_comp
    df_costs_mut
    df_costs_mut_full
    df_costs_stars
    df_costs_boss
    df_equip_data
    df_equip_nov

