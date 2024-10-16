import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Basketball-Referece",
                   page_icon=":basketball",
                   layout="wide"
)

df = pd.read_excel(
    io="nba_team_stats.xlsx",
    sheet_name="NBA_TEAM"
)



# SIDEBAR

st.sidebar.header("League")

league = st.sidebar.multiselect(
    "Select the League:",
    options = df["League"].unique(),
    default = df["League"].unique()
)

# team = st.sidebar.multiselect(
#     "Select the Team:",
#     options = df["Team"].unique(),
#     default = df["Team"].unique()
# )

# season = st.sidebar.multiselect(
#     "Select the Season:",
#     options = df["Season"].unique(),
#     default = df["Season"].unique()
# )

df_selection = df.query(
    "League == @league"
)
df_team_selection = df_selection.sort_values(by=['Team'])

team = st.sidebar.multiselect(
    "Select the Team:",
    options = df_team_selection["Team"].unique(),
    default = df_team_selection["Team"].unique()
)

df_team_selection = df.query(
    "Team == @team"
)


#MAIN WINDOW
st.title("Why The NBA Sucks")
st.markdown("##")

#supporting metrics
max_season = df_team_selection["Season"].max()
df_team_max_season = df_team_selection.query(
    "Season == @max_season"
)

#KPI Cards
games_played = int(df_team_max_season["G"].sum())
three_pa_max_season = df_team_max_season["3PA"].sum()
fga_max_season = df_team_max_season["FGA"].sum()

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Games Played:")
    st.subheader(f"{games_played:,}")

with middle_column:
    st.subheader("3 Pt Attempts:")
    st.subheader(f"{three_pa_max_season:,}")

with right_column:
    st.subheader("FG Attempts:")
    st.subheader(f"{fga_max_season:,}")

st.markdown("---")

#3PA out of FGA Trend by League


df_team_selection = df_team_selection.groupby(['Season', 'League'], as_index=False)[["3PA", "FGA", "FG", "G", "3P"]].sum() 
df_team_selection["3PA Pct"] = (100*df_team_selection["3PA"] / df_team_selection["FGA"]).round(1)
df_team_selection["Missed 3FG per Game"] = ((df_team_selection["3PA"]-df_team_selection["3P"]) / df_team_selection["G"]).round(1)

fig_MFG_chart = px.bar(df_team_selection,
                        title="Missed 3-Pt Attempts per Game",
                         x="Season",
                         y="Missed 3FG per Game",
                         color="League",
                         text_auto=True,
                         text="Missed 3FG per Game"
                         )
fig_MFG_chart.update_layout(barmode='group',
                            uniformtext_minsize=18,
                            uniformtext_mode='show')
#fig_MFG_chart.update_traces(texttemplate="%{y}", textposition='top center')
fig_MFG_chart.update_yaxes(visible=False,
                           showgrid=False,
                           showticklabels=False
                           )
st.plotly_chart(fig_MFG_chart)


fig_3PA_chart = px.line(df_team_selection,
                        title="3-Pt Attempts vs FG Attempts",
                         x="Season",
                         y="3PA Pct",
                         color="League",
                         text="3PA Pct")

fig_3PA_chart.update_traces(texttemplate="%{y}", textposition='top center')
fig_3PA_chart.update_yaxes(visible=False,
                           showgrid=False,
                           showticklabels=False)

st.plotly_chart(fig_3PA_chart)

#st.dataframe(df_team_selection_grouped.sort_values(by=['Season'],ascending=False))