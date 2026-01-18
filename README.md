# Marketing Campaign Performance Analysis

## Project Overview
This project analyzes multi-channel digital marketing campaign data to identify which marketing strategies drive conversions most efficiently. The analysis combines exploratory data analysis (EDA), statistical testing, and an interactive Streamlit dashboard to support data-driven marketing decisions.

The focus is on **cost efficiency, engagement quality, and conversion performance** across channels, campaign types, and demographics.

---

## Dataset
The dataset contains campaign-level marketing data including:

- CampaignChannel (PPC, Email, Social Media, Referral, SEO, etc.)
- CampaignType (Awareness, Conversion, Retention)
- AdSpend
- WebsiteVisits
- Conversion (binary)
- Engagement metrics (TimeOnSite, EmailClicks, PagesPerVisit, SocialShares)
- Demographics (Age, Income)

---

## Methodology
The analysis was conducted in three layers:

### 1. Exploratory Data Analysis (EDA)
- Channel-wise spend, visits, and conversions
- Cost metrics:
  - **CAC (Cost per Acquisition)**
  - **CAL / CPL (Cost per Lead / Visit)**
- Funnel analysis from targeting → visits → conversions
- Correlation analysis to identify conversion drivers

### 2. Statistical Testing
- **Chi-Square Test** to check whether conversion performance differs significantly across channels
- **Pairwise Z-tests** to compare conversion rates between selected channels
- Results show that while some channels appear stronger, overall performance is statistically stable across platforms

### 3. Interactive Dashboard (Streamlit)
- Channel filtering
- KPI summary (Spend, Leads, Conversions, CAC, CAL)
- CAC vs CAL comparison
- Conversion funnel visualization
- A/B testing tool for channel comparison
- Demographic analysis (Age & Income groups)
- Campaign type performance analysis

---

## Key Insights

### 1. Cost Efficiency (CAC & CPL)
- **PPC has the lowest CAC**, making it the most cost-efficient channel for scaling.
- Email marketing has the **highest CAC**, making it expensive per converted customer.

### 2. The Email Paradox
- Despite high CAC, **Email Clicks are one of the strongest predictors of conversion**.
- Email traffic is expensive but high-intent and closer to purchase.

### 3. Engagement Quality > Traffic Volume
- Time on Site and Email Clicks correlate more strongly with conversions than Social Shares.
- Increasing **engagement depth** is more effective than increasing raw visits.
- Recommendation: optimize landing page quality rather than relying on clickbait traffic.

### 4. Demographic Neutrality
- Age and Income show **near-zero correlation** with conversion.
- The product performs consistently across demographic segments.
- This supports a **broad-market scaling strategy** rather than niche targeting.

### 5. Campaign Type Matters Most
- **Conversion-focused campaigns outperform Awareness campaigns across all channels**.
- Budget allocation should prioritize high-intent conversion campaigns regardless of channel.

---

