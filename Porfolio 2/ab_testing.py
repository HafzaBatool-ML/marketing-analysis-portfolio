import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import statsmodels.stats.proportion as sp

# Load Dataset
df = pd.read_csv("C:\\Users\\pc\\Desktop\\Porfolio 2\\digital_marketing_campaign_dataset.csv")


print("--- A/B Testing & Statistical Analysis ---")

# 1. Chi-Square Test: Kya channels ke beech conversion mein koi farq hai?
# Null Hypothesis ($H_0$): Sab channels ka performance barabar hai.
contingency_table = pd.crosstab(df['CampaignChannel'], df['Conversion'])
chi2, p_val_chi, dof, ex = chi2_contingency(contingency_table)

print(f"Chi-Square Statistic: {chi2:.4f}")
print(f"P-Value: {p_val_chi:.4f}")

if p_val_chi < 0.05:
    print("Result: Statistically Significant (Channels perform differently)")
else:
    print("Result: Not Significant (Differences are likely due to random chance)")

# 2. Pairwise Z-Test: Referral vs Social Media
# Referral (Highest Rate) vs Social Media (Lowest Rate)
ref_conv = df[df['CampaignChannel'] == 'Referral']['Conversion']
soc_conv = df[df['CampaignChannel'] == 'Social Media']['Conversion']

count = [ref_conv.sum(), soc_conv.sum()]
nobs = [len(ref_conv), len(soc_conv)]

z_stat, p_val_z = sp.proportions_ztest(count, nobs)

print("\n--- Pairwise Z-Test (Referral vs Social Media) ---")
print(f"Z-Statistic: {z_stat:.4f}")
print(f"P-Value: {p_val_z:.4f}")

if p_val_z < 0.05:
    print("Result: Referral is significantly better than Social Media.")
else:
    print("Result: No significant difference between these two channels.")