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

# Melt to long format
df_melt = df.melt(id_vars="Bacteria", var_name="Antibiotic", value_name="MIC")
df_melt["log_MIC"] = np.log10(df_melt["MIC"])

# Label multidrug-resistant bacteria
resistant_bacteria = ["Aerobacter aerogenes", "Klebsiella pneumoniae", "Pseudomonas aeruginosa"]
df_melt["Resistant"] = df_melt["Bacteria"].apply(lambda x: "Multidrug-Resistant" if x in resistant_bacteria else "Other")

# Tooltip notes
df_melt["Note"] = df_melt["Resistant"].apply(lambda r: "⚠️ Likely ineffective" if r == "Multidrug-Resistant" else "")

# Base bar chart
bar = alt.Chart(df_melt).mark_bar().encode(
    x=alt.X("log_MIC:Q", title="log₁₀(MIC)"),
    y=alt.Y("Bacteria:N", sort="-x"),
    color=alt.Color("Antibiotic:N"),
    opacity=alt.condition(
        alt.datum.Resistant == "Multidrug-Resistant",
        alt.value(1),
        alt.value(0.3)
    ),
    tooltip=["Bacteria", "Antibiotic", "MIC", "Resistant", "Note"]
)

# Highlight background for resistant bacteria
highlight_bg = alt.Chart(df_melt[df_melt["Resistant"] == "Multidrug-Resistant"]).mark_rect(
    opacity=0.08,
    color='crimson'
).encode(
    y=alt.Y('Bacteria:N', sort='-x')
)

# Inline annotation text
highlight_text = alt.Chart(df_melt[df_melt["Resistant"] == "Multidrug-Resistant"]).mark_text(
    align='left',
    dx=3,
    color='crimson',
    fontWeight='bold',
    fontSize=11
).encode(
    x="log_MIC:Q",
    y="Bacteria:N",
    text=alt.value("High Resistance")
)

# Reference rule (log MIC = 1 → MIC = 10)
threshold_line = alt.Chart(pd.DataFrame({'x': [np.log10(10)]})).mark_rule(
    strokeDash=[4, 3],
    color='black'
).encode(
    x='x:Q'
)

# Combine all layers
final_chart = alt.layer(
    highlight_bg,
    bar,
    threshold_line,
    highlight_text
).properties(
    width=750,
    height=550,
    title="🔬 Multidrug Resistance Across Three Antibiotics"
)

# Streamlit title + chart
st.title("🧬 The Resistant Few: When No Antibiotic Works")
st.altair_chart(final_chart, use_container_width=True)
