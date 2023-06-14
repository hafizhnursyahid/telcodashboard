from lib import *
from Home import df


st.sidebar.header("Select Data:")
Contract = st.sidebar.multiselect(
    "Select the Contract Type:",
    options=df["Contract"].unique()
)

Churn = st.sidebar.multiselect(
    "Select the Churn Type:",
    options=df["Churn"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["gender"].unique()
)

df_selection = df.query(
    "Contract == @Contract & Churn == @Churn & gender == @gender"
)

st.write(df_selection)
st.title("Dashboard")
st.markdown("##")


total_sales = float(df_selection["TotalCharges"].sum())
average_sale_by_transaction = round(df_selection["TotalCharges"].mean(), 2)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Charges Values:")
    st.subheader(f"US $ {total_sales:,.2f}")

with right_column:
    st.subheader("Average Charges:")
    st.subheader(f"US $ {average_sale_by_transaction:,.2f}")

st.markdown("""---""")


profit_by_PM = (
    df_selection.groupby(by=["PaymentMethod"]).sum()[["TotalCharges"]].sort_values(by="TotalCharges")
)
fig_product_sales = px.bar(
    profit_by_PM,
    x="TotalCharges",
    y=profit_by_PM.index,
    orientation="h",
    title="<b>Sales by Payment Method</b>",
    color_discrete_sequence=["#0083B8"] * len(profit_by_PM),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

profit_by_PB = (
    df_selection.groupby(by=["OnlineSecurity"]).sum()[["TotalCharges"]].sort_values(by="TotalCharges")
)
fig_PB_sales = px.bar(
    profit_by_PB,
    x=profit_by_PB.index,
    y="TotalCharges",
    orientation="v",
    title="<b>Sales by Online Security Type</b>",
    color_discrete_sequence=["#0083B8"] * len(profit_by_PB),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


left_column2, right_column2 = st.columns(2)
left_column2.plotly_chart(fig_PB_sales, use_container_width=True)
right_column2.plotly_chart(fig_product_sales, use_container_width=True)


logButton = st.checkbox(label="Logharitmic Scale")


df_new = df_selection.groupby(by=["Contract", "tenure"]).size().reset_index(name='Count of Contract')
df_mtm = df_new[df_new['Contract'] == 'Month-to-month']
df_1y = df_new[df_new['Contract'] == 'One year']
df_2y = df_new[df_new['Contract'] == 'Two year']

mypalette = Spectral11[0:3]
p = bpl.figure(plot_width=400, plot_height=400, y_axis_type="log" if logButton else None)

p.line(df_mtm['tenure'], df_mtm['Count of Contract'], line_color=mypalette[0], legend_label='Month-to-month')
p.line(df_1y['tenure'], df_1y['Count of Contract'], line_color=mypalette[1], legend_label='One year')
p.line(df_2y['tenure'], df_2y['Count of Contract'], line_color=mypalette[2], legend_label='Two year')

if logButton:
    p.yaxis[0].formatter = NumeralTickFormatter(format="0")

p.legend.title = "Contract Types"
p.legend.location = "top_right"

st.bokeh_chart(p, use_container_width=True)

left_column3, middle_column3, right_column3 = st.columns(3)
left_column3.write("Month to Month")
middle_column3.write("One Year")
right_column3.write("Two Year")


left_column4, middle_column4, right_column4 = st.columns(3)
left_column4.write(df_mtm.drop(columns=["Contract"]))
middle_column4.write(df_1y.drop(columns=["Contract"]))
right_column4.write(df_2y.drop(columns=["Contract"]))


col1, col2 = st.columns(2)
opsi = df.drop(columns=["Churn","gender","SeniorCitizen","Partner","Dependents","PhoneService","MultipleLines","InternetService",
                        "OnlineSecurity","OnlineBackup","DeviceProtection","TechSupport","StreamingTV","StreamingMovies","Contract",
                        "PaperlessBilling","PaymentMethod"]).columns

with col1:
    pil1 = st.selectbox(label="X-Axis", options=opsi, index=0)
with col2:
    pil2 = st.selectbox(label="Y-axis", options=opsi, index=2)

color_encode = st.checkbox(label = "Churn Type")

scatter_fig = df.plot_bokeh.scatter(x=pil1, y=pil2, category="Churn" if color_encode else None,
                                         xlabel=pil1.capitalize(), ylabel=pil2.capitalize(),
                                         title="{} vs {}".format(pil1.capitalize(), pil2.capitalize()),
                                         figsize=(650,500), show_figure=False)

st.bokeh_chart(scatter_fig, use_container_width=True)


st.markdown("""---""")