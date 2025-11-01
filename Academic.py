import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="AV Accident Dashboard", layout="wide")

# ---- Load dataset ----
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

csv_url = "https://raw.githubusercontent.com/nhusna01/EA2025/main/processed_av_accident_data.csv"
df = load_data(csv_url)

# ---- Initialize session_state ----
if "page" not in st.session_state:
    st.session_state.page = "Menu"

# ---- Function to change pages ----
def go_to(page_name):
    st.session_state.page = page_name

# ---- MENU PAGE ----
if st.session_state.page == "Menu":
    st.title("Menu Page")
    st.write("Welcome to the AV Accident Data Dashboard!")

    st.subheader("Dataset Preview")
    st.dataframe(df)

    st.subheader("Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Accidents", len(df))
    col2.metric(
        "Total Fatalities",
        df["Number_of_Casualties"].sum() if "Number_of_Casualties" in df.columns else "N/A"
    )
    col3.metric(
        "Average Vehicles",
        f"{df['Number_of_Vehicles'].mean():.2f}" if "Number_of_Vehicles" in df.columns else "N/A"
    )
    col4.metric(
        "Average Speed Limit",
        f"{df['Speed_Limit'].mean():.2f}" if "Speed_Limit" in df.columns else "N/A"
    )

    st.subheader("Select the Visualizations")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Visualization 1"):
            go_to("Visualization 1")
    with col2: 
        if st.button("Visualization 2"): 
            go_to("Visualization 2") 
    with col3: 
        if st.button("Visualization 3"): 
            go_to("Visualization 3")

# ---- Visualization 1 ----
elif st.session_state.page == "Visualization 1":
    st.title("Visualization 1: AV Accident Analysis")

    ## --- 1.1 Box Plot: Pre-crash Speed vs Severity ---
    st.subheader("1.1 Pre-crash Speed vs Severity")
    if "Severity" in df.columns and "SV Precrash Speed (MPH)" in df.columns:
        fig1 = px.box(
            df,
            x="Severity",
            y="SV Precrash Speed (MPH)",
            color="Severity",
            title="Pre-crash Speed vs Severity",
            color_discrete_sequence=[
                '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
            ]
        )
        fig1.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=1)
        fig1.update_layout(title_font=dict(size=20, color='black', family="Arial Black"), plot_bgcolor='white')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(
            "**Interpretation:** Higher pre-crash speeds are associated with greater accident severity."
        )
    else:
        st.warning("Columns 'Severity' or 'SV Precrash Speed (MPH)' not found.")

    ## --- 1.2 Grouped Bar: Severity by Lighting ---
    st.subheader("1.2 Severity by Lighting Conditions")
    if "Severity" in df.columns and "Lighting" in df.columns:
        counts = df.groupby(['Severity', 'Lighting']).size().reset_index(name='Count')
        fig2 = px.bar(
            counts,
            x='Severity',
            y='Count',
            color='Lighting',
            barmode='group',
            title='Severity by Lighting',
            color_discrete_sequence=['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#FF00FF']
        )
        fig2.update_traces(text=counts['Count'], textposition='outside')
        fig2.update_layout(
            plot_bgcolor='white',
            title_font=dict(size=18, color='black', family="Arial Black"),
            xaxis_title='Severity',
            yaxis_title='Count of Incidents',
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray')
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            "**Interpretation:** Lighting conditions affect accident severity. Bar labels show counts clearly."
        )
    else:
        st.warning("Columns 'Severity' or 'Lighting' not found.")

    ## --- 1.3 Correlation Heatmap ---
    st.subheader("1.3 Correlation Heatmap")
    required_cols = ['Mileage', 'Posted Speed Limit (MPH)', 'SV Precrash Speed (MPH)']
    if all(col in df.columns for col in required_cols):
        corr_vars = df[required_cols].apply(pd.to_numeric, errors='coerce').dropna()
        corr_matrix = corr_vars.corr(method='pearson')
        fig3 = px.imshow(
            corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            color_continuous_scale=['#FFFF00', '#FF7F00', '#FF0000'],
            text_auto=".2f",
            aspect="auto",
            title="Correlation Heatmap"
        )
        fig3.update_layout(title_font=dict(size=18, color='black', family="Arial Black"), plot_bgcolor='white')
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown(
            "**Interpretation:** Brighter warm colors indicate stronger positive correlations."
        )
    else:
        st.warning("Required numeric columns not found.")

    # --- Back to Menu Button ---
    if st.button("⬅ Back to Menu"):
        go_to("Menu")




# ---- Visualization 2 ----
elif st.session_state.page == "Visualization 2":
    st.title("Visualization 2: AV Accident Distribution")


# ----------------- 2.1 Box Plot: Pre-crash Speed vs Severity -----------------
    st.subheader("2.1 Pre-crash Speed vs Severity (Box Plot)")
    if "Severity" in df.columns and "SV Precrash Speed (MPH)" in df.columns:
        fig1 = px.box(
            df,
            x="Severity",
            y="SV Precrash Speed (MPH)",
            color="Severity",
            title="Pre-crash Speed vs Severity",
            color_discrete_sequence=['#FF0000','#FF7F00','#FFD700','#32CD32','#00FFFF','#0000FF','#FF00FF']
        )
        fig1.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=1)
        fig1.update_layout(title_font=dict(size=20, color='black', family="Arial Black"), plot_bgcolor='white')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(
            "**Interpretation:** Higher pre-crash speeds are associated with greater accident severity. Bold colors highlight differences between severity levels."
        )
    else:
        st.warning("Required columns for Box Plot not found.")

    # ----------------- 2.2 Histogram / Stacked Bar: Accident Distribution by Model Year -----------------
    st.subheader("2.2 Accident Distribution by Model Year and Severity (Stacked Bar)")
    if "Model Year" in df.columns and "Severity" in df.columns:
        df_counts = df.groupby(['Model Year', 'Severity']).size().reset_index(name='Count')
        df_counts['Model Year'] = df_counts['Model Year'].astype(str)
        df_counts = df_counts.sort_values('Model Year')
        
        fig2 = px.bar(
            df_counts,
            x='Model Year',
            y='Count',
            color='Severity',
            barmode='relative',
            color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF'],
            title='Accident Distribution by Model Year and Severity'
        )
        fig2.update_layout(
            xaxis_title='Model Year',
            yaxis_title='Number of Incidents',
            plot_bgcolor='white',
            title_font=dict(size=20, color='black', family='Arial Black')
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            "**Interpretation:** This stacked bar chart shows how accident severity varies across vehicle model years. It highlights which model years have higher counts and severe incidents."
        )
    else:
        st.warning("Required columns for Stacked Bar not found.")

    # ----------------- 2.3 Violin / Density Plot: Severity by Air Bag Deployment -----------------
    st.subheader("2.3 Severity Distribution by Air Bag Deployment (Violin Plot)")
    if "Air_Bag" in df.columns and "Severity" in df.columns:
        fig3 = px.violin(
            df,
            x='Air_Bag',
            y='Severity',
            color='Air_Bag',
            color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF'],
            box=True,
            points='all',
            title='Severity Distribution by Air Bag Deployment'
        )
        fig3.update_traces(opacity=0.8, line=dict(width=1.5), marker=dict(size=4, opacity=0.6))
        fig3.update_layout(
            xaxis_title='Air Bag Deployment Status',
            yaxis_title='Severity',
            plot_bgcolor='white',
            title_font=dict(size=22, family='Arial Black', color='black'),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            showlegend=True,
            legend_title_text='Air Bag Status'
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown(
            "**Interpretation:** This violin plot shows severity distribution for vehicles with and without airbags. Wider areas indicate higher concentration of incidents for each severity level."
        )
    else:
        st.warning("Required columns for Violin Plot not found.")

    # ----------------- Back to Menu -----------------
    st.button("⬅ Back to Menu", on_click=lambda: go_to("Menu"))




# ---- Visualization 3 ----
elif st.session_state.page == "Visualization 3":
    st.title("Visualization 3: Environmental and Collision Analysis")

    # ----------------- 3.1 Violin Plot: Speed Distribution by Weather -----------------
    st.subheader("3.2 Violin Plot: Speed Distribution by Weather")
    if "Weather" in df.columns and "SV Precrash Speed (MPH)" in df.columns:
        fig = px.violin(
            df,
            x='Weather',
            y='SV Precrash Speed (MPH)',
            color='Weather',
            box=True,
            points='all',
            color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF'],
            title='Speed Distribution Across Different Weather Conditions'
        )
        fig.update_layout(
            xaxis_title='Weather',
            yaxis_title='Precrash Speed (MPH)',
            title_font=dict(size=22, family='Arial Black', color='black'),
            plot_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "**Interpretation:** The violin plot shows how pre-crash speeds differ across weather conditions. Wider areas indicate higher data concentration, revealing risky speed patterns under adverse weather."
        )
    else:
        st.warning("Required columns for Violin Plot not found.")

    # ----------------- 3.2 Pie Chart: Accident Severity by Collision Type -----------------
    st.subheader("3.3 Pie Chart: Accident Severity by Collision Type")
    if "Crash_With" in df.columns and "Severity" in df.columns:
        crash_severity_counts = df.groupby(['Crash_With', 'Severity']).size().reset_index(name='Count')
        fig = px.pie(
            crash_severity_counts,
            names='Crash_With',
            values='Count',
            color='Crash_With',
            color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF'],
            title='Distribution of Accident Severity by Collision Type'
        )
        fig.update_layout(
            title_font=dict(size=22, family='Arial Black', color='black'),
            legend_title_text='Collision Type',
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "**Interpretation:** The pie chart shows the proportion of incidents by collision type. Larger segments indicate more frequent collision categories, revealing key accident risk sources."
        )
    else:
        st.warning("Required columns for Pie Chart not found.")



st.title("3.3 Radar Chart: Environmental Factors by Weather")

# ---- Check required columns exist ----
required_cols = ['Weather', 'Roadway_Type', 'Roadway_Surface', 'Lighting']
if all(col in df.columns for col in required_cols):

    # Aggregate data
    radar_data = df.groupby(required_cols).size().reset_index(name='Incident_Count')

    # Take top 3 weather conditions by total incidents
    top_weather = radar_data.groupby('Weather')['Incident_Count'].sum().nlargest(3).index
    radar_data = radar_data[radar_data['Weather'].isin(top_weather)]

    axes = ['Roadway_Type', 'Roadway_Surface', 'Lighting']
    weather_categories = radar_data['Weather'].unique()
    rainbow_colors = ['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF']

    traces = []
    for i, weather in enumerate(weather_categories):
        subset = radar_data[radar_data['Weather'] == weather]
        values = []
        for axis in axes:
            grouped = subset.groupby(axis)['Incident_Count'].sum()
            val = grouped.max() if not grouped.empty else 0
            values.append(val)
        values.append(values[0])  # close the loop
        traces.append(
            go.Scatterpolar(
                r=values,
                theta=axes + [axes[0]],
                fill='toself',
                name=weather,
                line=dict(color=rainbow_colors[i % len(rainbow_colors)], width=2),
                opacity=0.7
            )
        )

    # Create figure
    fig = go.Figure(data=traces)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showgrid=True, gridcolor='darkgray'),
            angularaxis=dict(showgrid=True)
        ),
        title='Radar Chart: Incident Distribution Across Environmental Factors by Weather',
        title_font=dict(size=22, family='Arial Black', color='black'),
        showlegend=True,
        legend_title_text='Weather Condition',
        plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "**Interpretation:** This radar chart compares how road type, surface, and lighting influence accident occurrences under different weather conditions. Larger areas indicate higher incident counts."
    )

else:
    st.warning(f"Required columns {required_cols} not found in the dataset.")
    
    
    # --- Back to Menu ---
    st.button("⬅ Back to Menu", on_click=lambda: go_to("Menu"))
