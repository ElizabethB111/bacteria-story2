import altair as alt
import pandas as pd
import numpy as np
import streamlit as st

# --- Data ---
data = [
    {"Bacteria": "Aerobacter aerogenes", "Penicillin": 870, "Streptomycin": 1, "Neomycin": 1.6},
    {"Bacteria": "Bacillus anthracis", "Penicillin": 0.001, "Streptomycin": 0.01, "Neomycin": 0.007},
    {"Bacteria": "Brucella abortus", "Penicillin": 1, "Streptomycin": 2, "Neomycin": 0.02},
    {"Bacteria": "Diplococcus pneumoniae", "Penicillin": 0.005, "Streptomycin": 11, "Neomycin": 10},
    {"Bacteria": "Escherichia coli", "Penicillin": 100, "Streptomycin": 0.4, "Neomycin": 0.1},
    {"Bacteria": "Klebsiella pneumoniae", "Penicillin": 850, "Streptomycin": 1.2, "Neomycin": 1},
    {"Bacteria": "Mycobacterium tuberculosis", "Penicillin": 800, "Streptomycin": 5, "Neomycin": 2},
    {"Bacteria": "Proteus vulgaris", "Penicillin": 3, "Streptomycin": 0.1, "Neomycin": 0.1},
    {"Bacteria": "Pseudomonas aeruginosa", "Penicillin": 850, "Streptomycin": 2, "Neomycin": 0.4},
    {"Bacteria": "Salmonella (Eberthella) typhosa", "Penicillin": 1, "Streptomycin": 0.4, "Neomycin": 0.008},
    {"Bacteria": "Salmonella schottmuelleri", "Penicillin": 10, "Streptomycin": 0.8, "Neomycin": 0.09},
    {"Bacteria": "Staphylococcus albus", "Penicillin": 0.007, "Streptomycin": 0.1, "Neomycin": 0.001},
    {"Bacteria": "Staphylococcus aureus", "Penicillin": 0.03, "Streptomycin": 0.03, "Neomycin": 0.001},
    {"Bacteria": "Streptococcus fecalis", "Penicillin": 1, "Streptomycin": 1, "Neomycin": 0.1},
    {"Bacteria": "Streptococcus hemolyticus", "Penicillin": 0.001, "Streptomycin": 14, "Neomycin": 10},
    {"Bacteria": "Streptococcus viridans", "Penicillin": 0.005, "Streptomycin": 10, "Neomycin": 40}
]

df = pd.DataFrame(data)

# Melt for plotting
df_melt = df.melt(id_vars="Bacteria", var_name="Antibiotic", value_name="MIC")
df_melt["log_MIC"] = np.log10(df_melt["MIC"])

# Mark resistant bacteria
resistant_set = ["Aerobacter aerogenes", "Klebsiella pneumoniae", "Pseudomonas aeruginosa"]
df_melt["Resistant"] = df_melt["Bacteria"].apply(lambda x: "Multidrug-Resistant" if x in resistant_set else "Other")
df_melt["Bacteria_Label"] = df_melt.apply(
    lambda row: "⚠️ " + row["Bacteria"] if row["Resistant"] == "Multidrug-Resistant" else row["Bacteria"], axis=1
)

# --- Streamlit content ---
st.set_page_config(layout="wide")
st.title("Multidrug-Resistant Bacteria: When No Antibiotic Works")

st.markdown("""
### 🧪 Antibiotic Resistance is a Global Health Threat
This chart shows the **Minimum Inhibitory Concentration (MIC)** (the lowest concentration of an antibiotic that stops bacterial growth) for three common antibiotics.

Bacteria with ⚠️ are **multidrug-resistant (MDR)**: resistant to **all three antibiotics**. These bacteria may be untreatable with commonly-available medications.

A log scale is used here to visualize MIC values: higher values mean **stronger resistance**.
""")

# --- Base Chart ---
base = alt.Chart(df_melt).encode(
    x=alt.X("log_MIC:Q", title="log₁₀(MIC)", scale=alt.Scale(zero=False)),
    y=alt.Y("Bacteria_Label:N", sort="-x", title="Bacterial Species"),
    color=alt.Color(
    "Antibiotic:N",
    title="Antibiotic",
    scale=alt.Scale(
        domain=["Penicillin", "Streptomycin", "Neomycin"],
        range=["#1f77b4", "#ff7f0e", "#2ca02c"]  # blue, orange, green
    )
),

    opacity=alt.condition(
        alt.datum.Resistant == "Multidrug-Resistant",
        alt.value(1),
        alt.value(0.3)
    ),
    tooltip=["Bacteria", "Antibiotic", "MIC"]
)

bars = base.mark_bar()

# --- Annotations for MDR cases ---
annotations_df = pd.DataFrame({
    "log_MIC": [np.log10(870), np.log10(850), np.log10(850)],
    "Bacteria_Label": ["⚠️ Aerobacter aerogenes", "⚠️ Klebsiella pneumoniae", "⚠️ Pseudomonas aeruginosa"],
    "Note": ["Very high resistance", "Near max resistance", "Resistant to all"]
})

annotations = alt.Chart(annotations_df).mark_text(
    align='left',
    baseline='middle',
    dx=8,
    fontSize=12,
    color='black'
).encode(
    x='log_MIC:Q',
    y='Bacteria_Label:N',
    text='Note:N'
)

chart = (bars + annotations).properties(
    width=750,
    height=550,
    title="Resistance Profile of Bacteria Across Three Antibiotics"
)

# --- Display in Streamlit ---
st.altair_chart(chart, use_container_width=True)

st.markdown("""
### Note:
- **Aerobacter aerogenes**, **Klebsiella pneumoniae**, and **Pseudomonas aeruginosa** show **high MICs** for all three antibiotics.
- These bacteria possess severe antimicrobial resistance and therefore need different treatments.
""")

