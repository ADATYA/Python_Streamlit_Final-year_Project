import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# reading the data form excel file
try:
   df = pd.read_excel("Adidas.xlsx")
except:
    df = pd.DataFrame({'Data': [1, 2, 3]})
st.set_page_config(layout = "wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
image = Image.open('adidas.jpg')

col1, col2 = st.columns([0.15,0.85])
with col1:
    st.image(image, use_container_width=True)

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    background-color:red;
    }
    </style>
    <center><h1 class="title-test"><em>Adidas 2026 Interactive Sales Dashboard</em></h1></center>"""

with col2:
     st.markdown(html_title, unsafe_allow_html=True)

# Changing Last Update file...

col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")

# Bar and Graph chart are startin here..
with col4:
    fig = px.bar(df, x = "Retailer", y = "TotalSales", labels={"TotalSales" : "Total Sales {$}"},
                 title = "Total Sales by Retailer", hover_data=["TotalSales"],
                 template="gridon",height=500)
    st.plotly_chart(fig,use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Retailer wise Sales")
    data = df[["Retailer","TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)

# In case Download the file data...
with dwn1:
    st.download_button("Download Data", data = data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")

df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")
result = df.groupby(by = df["Month_Year"])["TotalSales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x = "Month_Year", y = "TotalSales", title="Total Sales Over Time",
                   template="gridon")
    st.plotly_chart(fig1,use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button("Download Data", data = result.to_csv().encode("utf-8"),
                       file_name="Monthly Sales.csv", mime="text/csv")
# Bar and Graph chartr end here..

st.divider()

result1 = df.groupby(by="State")[["TotalSales","UnitsSold"]].sum().reset_index()

# add the units sold as a line chart on a secondary y-axis
fig3 = go.Figure()
fig3.add_trace(go.Bar(x = result1["State"], y = result1["TotalSales"], name = "Total Sales"))
fig3.add_trace(go.Scatter(x=result1["State"], y = result1["UnitsSold"], mode = "lines",
                          name ="Units Sold", yaxis="y2"))
fig3.update_layout(
    title = "Total Sales and Units Sold by State",
    xaxis = dict(title="State"),
    yaxis = dict(title="Total Sales", showgrid = False),
    yaxis2 = dict(title="Units Sold", overlaying = "y", side = "right"),
    template = "gridon",
    legend = dict(x=1,y=1.1)
)
_, col6 = st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3,use_container_width=True)

_, view3, dwn3 = st.columns([0.5,0.45,0.45])
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)
with dwn3:
    st.download_button("Download Data", data = result1.to_csv().encode("utf-8"), 
                       file_name = "Sales_by_UnitsSold.csv", mime="text/csv")
st.divider()

_, col7 = st.columns([0.1,1])
treemap = df[["Region","City","TotalSales"]].groupby(by = ["Region","City"])["TotalSales"].sum().reset_index()

def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)

treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)

fig4 = px.treemap(treemap, path = ["Region","City"], values = "TotalSales",
                  hover_name = "TotalSales (Formatted)",
                  hover_data = ["TotalSales (Formatted)"],
                  color = "City", height = 700, width = 600)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4,use_container_width=True)

_, view4, dwn4 = st.columns([0.5,0.45,0.45])
with view4:
    result2 = df[["Region","City","TotalSales"]].groupby(by=["Region","City"])["TotalSales"].sum()
    expander = st.expander("View data for Total Sales by Region and City")
    expander.write(result2)
with dwn4:
    st.download_button("Need Data", data = result2.to_csv().encode("utf-8"),
                                        file_name="Sales_by_Region.csv", mime="text.csv")

_,view5, dwn5 = st.columns([0.5,0.45,0.45])
with view5:
    expander = st.expander("View Sales Raw Data")
    expander.write(df)
with dwn5:
    st.download_button("Download Raw DataFiles", data = df.to_csv().encode("utf-8"),
                       file_name = "SalesRawData.csv", mime="text/csv")
st.divider()
# 1. Key Metrics Section
import streamlit as st

# 1. Key Metrics Section
st.subheader("📊 Executive Summary")

# Data Calculation
total_sales = df["TotalSales"].sum() if "TotalSales" in df.columns else 0
total_units = (
    df["UnitsSold"].sum()
    if "UnitsSold" in df.columns
    else (df["Quantity"].sum() if "Quantity" in df.columns else 0)
)
avg_order = df["TotalSales"].mean() if "TotalSales" in df.columns else 0

# Custom CSS for Modern KPI Cards
st.markdown(
    """
    <style>
    .kpi-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    .kpi-title {
        font-size: 14px;
        font-weight: 600;
        color: #6c757d;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #1e293b;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Responsive Layout using Columns
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Total Revenue</div>
            <div class="kpi-value">৳ {total_sales/1_000_00:.2f} Lakh</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 Total Units Sold</div>
            <div class="kpi-value">{total_units:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🛒 Avg Sales / Order</div>
            <div class="kpi-value">৳ {avg_order:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# 2. Top 5 & Bottom 5 Cities
st.subheader("🌆 City Performance Overview")

col_top, col_bot = st.columns(2)

city_sales = df.groupby("City")["TotalSales"].sum().reset_index()

with col_top:
    top_5 = city_sales.nlargest(5, "TotalSales")
    fig_top = px.bar(top_5, x="TotalSales", y="City", orientation='h', 
                     title="Top 5 Performing Cities", text_auto='.2s',
                     color="TotalSales", color_continuous_scale="Greens")
    fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top, use_container_width=True)

with col_bot:
    bottom_5 = city_sales.nsmallest(5, "TotalSales")
    fig_bot = px.bar(bottom_5, x="TotalSales", y="City", orientation='h', 
                      title="Bottom 5 Performing Cities", text_auto='.2s',
                      color="TotalSales", color_continuous_scale="Reds")
    fig_bot.update_layout(yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_bot, use_container_width=True)

# 3. Monthly Trend Line Chart
if "Date" in df.columns or "Order Date" in df.columns:
    date_col = "Date" if "Date" in df.columns else "Order Date"
    df[date_col] = pd.to_datetime(df[date_col])
    
    monthly_sales = df.resample('M', on=date_col)["TotalSales"].sum().reset_index()
    
    st.subheader("📈 Monthly Sales Trend")
    fig_trend = px.line(monthly_sales, x=date_col, y="TotalSales", markers=True,
                        title="Sales Over Time", labels={date_col: "Date", "TotalSales": "Sales Amount"})
    fig_trend.update_traces(line_color="#29b5e8", line_width=3)
    st.plotly_chart(fig_trend, use_container_width=True)

# 4. Product-wise Sales Distribution
if "Product" in df.columns or "Category" in df.columns:
    prod_col = "Product" if "Product" in df.columns else "Category"
    
    st.subheader("👟 Sales by Product Category")
    prod_df = df.groupby(prod_col)["TotalSales"].sum().reset_index()
    
    fig_donut = px.pie(prod_df, values="TotalSales", names=prod_col, hole=0.4,
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_donut, use_container_width=True)

# ------------------------------------------------------------------


# 1. Clear Filter Callback Function
def clear_all_filters():
    st.session_state["region_val"] = []
    st.session_state["state_val"] = []
    st.session_state["city_val"] = []
    st.session_state["search_val"] = ""


# 2. Sidebar Filters (Region, State, City)
st.sidebar.header("Choose the filter option:")

# ⚠️ Pipeline Disclaimer Notice Box
st.sidebar.warning(
    "⚠️ **Notice:** This filter section is currently in the pipeline. "
    "It will be fully operational in near future."
)

# 🗑️ Clear All Filters Button
st.sidebar.button("🗑️ Clear All Filters", on_click=clear_all_filters)

# Region Filter
region_col = "Region" if "Region" in df.columns else None
region = st.sidebar.multiselect(
    "Pick the Region",
    df[region_col].unique() if region_col else [],
    key="region_val",
)
df2 = df[df[region_col].isin(region)] if (region and region_col) else df.copy()

# State Filter
state_col = "State" if "State" in df2.columns else None
state = st.sidebar.multiselect(
    "Pick the State",
    df2[state_col].unique() if state_col else [],
    key="state_val",
)
df3 = df2[df2[state_col].isin(state)] if (state and state_col) else df2.copy()

# City Filter
city_col = "City" if "City" in df3.columns else None
city = st.sidebar.multiselect(
    "Pick the City",
    df3[city_col].unique() if city_col else [],
    key="city_val",
)

# Apply all dynamic filters
filtered_df = df3.copy()
if city and city_col:
    filtered_df = filtered_df[filtered_df[city_col].isin(city)]

# Category column check for search
cat_col = (
    "Category"
    if "Category" in df.columns
    else ("Product" if "Product" in df.columns else None)
)

# ------------------------------------------------------------------
# 🔍 Search Box
# ------------------------------------------------------------------
st.sidebar.markdown("---")  # Divider line
search_term = st.sidebar.text_input(
    "🔍 Search City or Product", key="search_val"
)

if search_term:
    conditions = []
    if city_col:
        conditions.append(
            filtered_df[city_col]
            .astype(str)
            .str.contains(search_term, case=False, na=False)
        )
    if cat_col:
        conditions.append(
            filtered_df[cat_col]
            .astype(str)
            .str.contains(search_term, case=False, na=False)
        )

    if conditions:
        combined_condition = np.logical_or.reduce(conditions)
        filtered_df = filtered_df[combined_condition]