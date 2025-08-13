
import streamlit as st
import pandas as pd

# Load data
inventory = pd.read_csv("enhanced_inventory_data.csv")
layout = pd.read_csv("enhanced_warehouse_layout.csv")

st.title("Smart Space Management: AI-Driven Warehouse Optimization")

# KPIs
st.header("📊 Key Performance Indicators")
total_items = len(inventory)
slow_moving_count = inventory[inventory['Slow_Moving_SKU'] == 'Yes'].shape[0]
abc_counts = inventory['ABC_Class'].value_counts()
consolidation_index = inventory['Location'].nunique() / total_items
slotting_accuracy = round((inventory['Access_Frequency'] > 50).mean() * 100, 2)

st.metric("Total Items", total_items)
st.metric("Slow-Moving SKUs", slow_moving_count)
st.metric("Inventory Consolidation Index", round(consolidation_index, 2))
st.metric("Slotting Accuracy (%)", slotting_accuracy)

# ABC Zone Efficiency
st.header("📦 ABC Classification Efficiency")
st.bar_chart(abc_counts)

# Inventory Consolidation
st.header("📍 Inventory Consolidation Opportunities")
duplicate_items = inventory.groupby('ItemID')['Location'].nunique()
fragmented_items = duplicate_items[duplicate_items > 1]
st.write("Items stored in multiple locations:")
st.dataframe(fragmented_items)

# Long Tail SKU Identification
st.header("🐢 Long-Tail SKU Identification")
long_tail = inventory[inventory['Slow_Moving_SKU'] == 'Yes']
st.write("Slow-moving items:")
st.dataframe(long_tail[['ItemID', 'Access_Frequency', 'Location']])

# Chat Interface Simulation
st.header("🗣️ Ask the AI Agent")
query = st.text_input("Type your question here:")

def respond_to_query(q):
    q = q.lower()
    if "underutilized zone" in q:
        zone_usage = inventory['Location'].apply(lambda x: x.split('-')[0]).value_counts()
        least_used = zone_usage.idxmin()
        return f"The most underutilized zone is {least_used}."
    elif "frequently accessed items" in q:
        top_items = inventory.sort_values(by='Access_Frequency', ascending=False).head(5)
        return "Top 5 frequently accessed items:\n" + "\n".join(top_items['ItemID'].values)
    elif "total space used" in q:
        return "This demo does not include physical space dimensions. Please consult a human expert."
    else:
        return "I'm sorry, I didn't understand that. Routing to a human expert..."

if query:
    response = respond_to_query(query)
    st.write("**Agent Response:**")
    st.write(response)
