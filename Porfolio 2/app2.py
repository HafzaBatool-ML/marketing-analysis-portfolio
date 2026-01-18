import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.stats.proportion as sp
from scipy.stats import chi2_contingency

# Dashboard Configuration
st.set_page_config(page_title="Marketing Analytics", layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv('Data files\digital_marketing_campaign_dataset.csv')
    return data

df = load_data()

st.title("Marketing Campaign Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("Filters")
selected_channel = st.sidebar.multiselect("Select Channel", options=df['CampaignChannel'].unique(), default=df['CampaignChannel'].unique())
df_filtered = df[df['CampaignChannel'].isin(selected_channel)]

# --- Key Metrics (KPIs) ---
total_spend = df_filtered['AdSpend'].sum()
total_conv = df_filtered['Conversion'].sum()
total_leads = df_filtered[df_filtered['WebsiteVisits'] > 0].shape[0]
total_visits = df_filtered[df_filtered['WebsiteVisits'] > 0].shape[0]
# CAC = Total Spend / Conversions
cac = total_spend / total_conv if total_conv > 0 else 0
# CAL (Cost per Lead/Visit) = Total Spend / Total Visitors
cal = total_spend / total_visits if total_visits > 0 else 0
total = len(df_filtered)
#avg_conv_rate = (total_conv / len(df_filtered)) * 100
# Display Top Metrics
col1, col2, col3, col4,col5,col6 = st.columns(6)
col1.metric("Total Targeted", f"{total:,.0f}")
col2.metric("Total Leads", f"{total_leads:,.0f}")
col3.metric("Total Conversions", f"{total_conv:,}")
col4.metric("Total Ad Spend", f"${total_spend:,.0f}")
col5.metric("CAC (Per Customer)", f"${cac:.2f}")
col6.metric("CAL (Per Lead)", f"${cal:.2f}")

st.divider()

st.header(" Data")
data = pd.read_csv("Data files\marketing_performance_summary.csv")
st.dataframe(data)
st.divider()
# --- 3. Performance Visuals ---
st.subheader("Channel-wise CAL & CAC Comparison")

# Metrics by Channel
metrics_df = df.groupby('CampaignChannel').agg({
    'AdSpend': 'sum',
    'Conversion': 'sum',
    'WebsiteVisits': lambda x: (x > 0).sum()
}).reset_index()

metrics_df['CAC'] = metrics_df['AdSpend'] / metrics_df['Conversion']
metrics_df['CAL'] = metrics_df['AdSpend'] / metrics_df['WebsiteVisits']

fig_metrics = px.bar(metrics_df, x='CampaignChannel', y=['CAC', 'CAL'], 
                     barmode='group')
st.plotly_chart(fig_metrics, use_container_width=True)
st.divider()
# Funnel Chart
st.subheader(" Conversion Funnel")
funnel_data = pd.DataFrame({
    "Stage": ["Targeted", "Leads (Visitors)", "Conversions"],
    "Count": [(len(df_filtered)/len(df_filtered))*100, (total_visits/len(df_filtered))*100 , (total_conv/len(df_filtered))*100]
})
fig_funnel = px.funnel(funnel_data, x='Count', y='Stage')
st.plotly_chart(fig_funnel, use_container_width=True)

st.divider()
# --- 2. Interactive A/B Testing Section ---
st.header("Hypothesis Testing Tool")
st.write("statistical Difference of conversion rate of Two channels")

test_col1, test_col2 = st.columns(2)

with test_col1:
    channel_a = st.selectbox("Select Channel A (Control)", options=df['CampaignChannel'].unique(), index=0)

with test_col2:
    channel_b = st.selectbox("Select Channel B (Variant)", options=df['CampaignChannel'].unique(), index=1)

if channel_a == channel_b:
    st.warning("Please select two different channels to compare.")
else:
    # Get data for selected channels
    data_a = df[df['CampaignChannel'] == channel_a]['Conversion']
    data_b = df[df['CampaignChannel'] == channel_b]['Conversion']
    
    # Calculate stats
    count = [data_a.sum(), data_b.sum()]
    nobs = [len(data_a), len(data_b)]
    rate_a = (data_a.sum() / len(data_a)) * 100
    rate_b = (data_b.sum() / len(data_b)) * 100
    
    # Run Z-test
    z_stat, p_val = sp.proportions_ztest(count, nobs)
    
    # Display Results
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.write(f"**{channel_a}** Conv. Rate: `{rate_a:.2f}%`")
    res_col2.write(f"**{channel_b}** Conv. Rate: `{rate_b:.2f}%`")
    
    if p_val < 0.05:
        res_col3.success(f"**Significant Difference!** (P-value: {p_val:.4f})")
        st.info(f"Insight: {channel_a if rate_a > rate_b else channel_b} is performing statistically better.")
    else:
        res_col3.error(f"**Not Significant** (P-value: {p_val:.4f})")
        st.info("Dono channels ke beech ka farq sirf random chance ho sakta hai.")

st.divider()

# --- CPC vs. Organic Visits Comparison ---
st.subheader("CPC vs. Organic Visits Comparison")

# Filter for CPC and Organic channels
cpc_organic_df = df_filtered[df_filtered['CampaignChannel'].isin(['PPC', 'Social Media', 'Display Ads', 'Search', 'Email'])]

# Group by channel and calculate metrics
channel_comparison = cpc_organic_df.groupby('CampaignChannel').agg({
    'WebsiteVisits': 'sum',
    'Conversion': 'sum',
    'AdSpend': 'sum'
}).reset_index()

channel_comparison['CPC'] = channel_comparison['AdSpend'] / channel_comparison['WebsiteVisits']
channel_comparison['Conversion_Rate'] = (channel_comparison['Conversion'] / channel_comparison['WebsiteVisits']) * 100

# Create dual-axis chart
col_cpc1, col_cpc2 = st.columns(2)

with col_cpc1:
    # CPC Comparison
    fig_cpc = px.bar(channel_comparison, x='CampaignChannel', y='CPC',
                     title='Cost Per Click by Channel',
                     color='CPC',
                     color_continuous_scale='Reds',
                     labels={'CPC': 'Cost Per Click ($)'})
    st.plotly_chart(fig_cpc, use_container_width=True)

with col_cpc2:
    # Website Visits Comparison
    fig_visits = px.bar(channel_comparison, x='CampaignChannel', y='WebsiteVisits',
                        title='Total Website Visits by Channel',
                        color='WebsiteVisits',
                        color_continuous_scale='Blues',
                        labels={'WebsiteVisits': 'Website Visits'})
    st.plotly_chart(fig_visits, use_container_width=True)

# Combined comparison chart
st.markdown("#### Combined Analysis: CPC vs Website Visits")
fig_combined = px.scatter(channel_comparison, x='CPC', y='WebsiteVisits',
                          size='Conversion', color='CampaignChannel',
                          hover_data=['Conversion_Rate', 'AdSpend'],
                          title='CPC vs Organic Visits (Bubble size = Conversions)',
                          labels={'CPC': 'Cost Per Click ($)', 'WebsiteVisits': 'Website Visits'})
st.plotly_chart(fig_combined, use_container_width=True)

st.divider()

# --- Deep Dive Story: Correlation ---
st.subheader("What Drives Conversions?")
corr_cols = ['AdSpend', "Age","Income","SocialShares", "WebsiteVisits",'TimeOnSite', 'EmailClicks', 'PagesPerVisit', 'Conversion']
corr = df_filtered[corr_cols].corr()[['Conversion']].sort_values(by='Conversion', ascending=False)
fig_corr = px.imshow(corr.T, text_auto=True, color_continuous_scale='RdBu_r', aspect="auto")
st.plotly_chart(fig_corr, use_container_width=True)
st.divider()

# --- Age and Income Group Analysis ---
st.header("Demographic Analysis")

# Create bins for Age and Income
df_filtered['AgeGroup'] = pd.cut(df_filtered['Age'], bins=[18, 30, 45, 60, 70], labels=['18-30', '31-45', '46-60', '60+'])
df_filtered['IncomeGroup'] = pd.qcut(df_filtered['Income'], q=4, labels=['Low', 'Medium', 'High', 'Very High'])

# Create two columns for side-by-side charts
col_age, col_income = st.columns(2)

with col_age:
    st.subheader("Conversion Rate by Age Group")
    # Aggregate data for Age Group
    age_conv = df_filtered.groupby(['AgeGroup', 'CampaignChannel'])['Conversion'].mean().reset_index()
    
    fig_age = px.bar(age_conv, x='AgeGroup', y='Conversion', 
                     color='CampaignChannel',
                     barmode='group',
                     title='Conversion Rate by Age Group & Channel',
                     labels={'Conversion': 'Conversion Rate'})
    st.plotly_chart(fig_age, use_container_width=True)

with col_income:
    st.subheader("Conversion Rate by Income Group")
    # Aggregate data for Income Group
    income_conv = df_filtered.groupby(['IncomeGroup', 'CampaignChannel'])['Conversion'].mean().reset_index()
    
    fig_income = px.bar(income_conv, x='IncomeGroup', y='Conversion', 
                        color='CampaignChannel',
                        barmode='group',
                        title='Conversion Rate by Income Group & Channel',
                        labels={'Conversion': 'Conversion Rate'})
    st.plotly_chart(fig_income, use_container_width=True)

st.divider()

# --- Campaign Type Analysis ---
st.subheader("Conversion Rate: Campaign Type vs. Channel")
campaign_conv = df_filtered.groupby(['CampaignType', 'CampaignChannel'])['Conversion'].mean().reset_index()

fig_campaign = px.bar(campaign_conv, x='CampaignType', y='Conversion', 
                      color='CampaignChannel',
                      barmode='group',
                      title='Conversion Rate by Campaign Type & Channel',
                      labels={'Conversion': 'Conversion Rate'},
                      height=500)
st.plotly_chart(fig_campaign, use_container_width=True)

st.divider()
