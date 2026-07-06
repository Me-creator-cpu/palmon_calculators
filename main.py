import streamlit
import pandas
import locale

cols_exp = ['Level from', 'Level to', 'Cost']
cols_comp = ['Level from', 'Cost']
cols_mut = ['Level', 'Step', 'Substep', 'Cost level']
cols_mut_full = ['Cost type', 'Cost']
cols_stars = ['Stars level', 'Unit Cost', 'Total']
cols_boss = ['Stars level', 'Unit Cost', 'Total']
cols_boss_data = ['Name','Type', 'Level', 'Stars','Comp 1','Comp 2','Comp 3','Comp 4','Comp 5','URL']
cols_equip = ['Level', 'Opus pearls']
cols_equip_nov = ['Step', 'Name', 'Stars', 'Cost']

df_costs_exp=None
df_costs_comp=None
df_costs_mut=None
df_costs_mut_full=None
df_costs_stars=None
df_costs_boss=None
df_boss_data=None
df_equip_data=None
df_equip_nov=None

data_values={
    "Value":["Energy","Crystals","Pieces","Level300"],
    "Icon":["🟢",     "💎",     "🧩",    "🔝"],
}
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
