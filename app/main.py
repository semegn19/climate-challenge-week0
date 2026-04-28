import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, filter_data, aggregate_monthly, calculate_summary_stats, get_variable_label, get_variable_unit

# Page configuration
st.set_page_config(
    page_title="Africa Climate Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #475569;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f9ff;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🌍 Africa Climate Monitor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Dashboard for Climate Analysis Across Five African Nations (2015-2026)</div>', unsafe_allow_html=True)

# Load data
with st.spinner("Loading climate data..."):
    df = load_data()

if df.empty:
    st.error("No data files found. Please ensure CSV files are in the 'data/' directory.")
    st.stop()

# Sidebar filters
st.sidebar.header("🔧 Filter Controls")

# Country multi-select
all_countries = sorted(df['Country'].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=all_countries,
    default=all_countries,
    help="Choose one or more countries to compare"
)

# Year range slider
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

# Variable selector
variables = ['T2M', 'T2M_MAX', 'T2M_MIN', 'PRECTOTCORR', 'RH2M', 'WS2M', 'QV2M']
selected_variable = st.sidebar.selectbox(
    "Select Variable",
    options=variables,
    format_func=lambda x: get_variable_label(x),
    help="Choose which climate variable to analyze"
)

# Filter data based on selections
filtered_df = filter_data(df, selected_countries, year_range)

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selections.")
    st.stop()

# Display basic info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Data Overview")
st.sidebar.metric("Total Records", f"{len(filtered_df):,}")
st.sidebar.metric("Selected Countries", len(selected_countries))
st.sidebar.metric("Years Covered", f"{year_range[0]} - {year_range[1]}")

# Color palette for countries
colors = {
    'Ethiopia': '#e41a1c',
    'Kenya': '#377eb8',
    'Nigeria': '#4daf4a',
    'Sudan': '#ff7f00',
    'Tanzania': '#984ea3'
}

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📈 Temperature Trends", "💧 Precipitation Analysis", "📊 Summary Statistics", "🔬 Statistical Insights"])

# Tab 1: Temperature Trends
with tab1:
    st.header(f"{get_variable_label(selected_variable)} Trends Over Time")
    
    if selected_variable in ['T2M', 'T2M_MAX', 'T2M_MIN']:
        # Monthly aggregation for line chart
        monthly_data = aggregate_monthly(filtered_df, selected_variable)
        monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()
        
        # Create interactive Plotly line chart with improved hover
        fig = go.Figure()
        
        for country in selected_countries:
            country_data = monthly_data[monthly_data['Country'] == country]
            if not country_data.empty:
                fig.add_trace(go.Scatter(
                    x=country_data['Date'],
                    y=country_data[selected_variable],
                    mode='lines+markers',
                    name=country,
                    line=dict(width=2, color=colors.get(country, '#666666')),
                    marker=dict(size=4, symbol='circle'),
                    hovertemplate=f'<b>{country}</b><br>' +
                                  'Date: %{x|%b %Y}<br>' +
                                  f'{get_variable_label(selected_variable)}: %{{y:.1f}} {get_variable_unit(selected_variable)}<br>' +
                                  '<extra></extra>'
                ))
        
        # Update layout with improved hover behavior
        fig.update_layout(
            title=f"{get_variable_label(selected_variable)} Trends ({year_range[0]}-{year_range[1]})",
            xaxis_title="Date",
            yaxis_title=f"{get_variable_label(selected_variable)} ({get_variable_unit(selected_variable)})",
            hovermode='closest',  # Only shows hover for the x-coordinate, not all lines at once
            legend_title="Country",
            template='plotly_white',
            height=500,
            width=None
        )
        
        # Set x-axis range
        fig.update_xaxes(
            range=[pd.Timestamp(f'{year_range[0]}-01-01'), pd.Timestamp(f'{year_range[1]}-12-31')]
        )
        
        st.plotly_chart(fig, width='stretch')
        
        # Add seasonal pattern subplot
        st.subheader("Seasonal Patterns (Monthly Climatology)")
        
        # Calculate monthly averages
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['Month'] = filtered_df_copy['Date'].dt.month
        monthly_clim = filtered_df_copy.groupby(['Country', 'Month'])[selected_variable].mean().reset_index()
        
        fig2 = go.Figure()
        
        for country in selected_countries:
            country_data = monthly_clim[monthly_clim['Country'] == country]
            if not country_data.empty:
                fig2.add_trace(go.Scatter(
                    x=country_data['Month'],
                    y=country_data[selected_variable],
                    mode='lines+markers',
                    name=country,
                    line=dict(width=2, color=colors.get(country, '#666666')),
                    marker=dict(size=8, symbol='circle'),
                    hovertemplate=f'<b>{country}</b><br>' +
                                  'Month: %{x}<br>' +
                                  f'{get_variable_label(selected_variable)}: %{{y:.1f}} {get_variable_unit(selected_variable)}<br>' +
                                  '<extra></extra>'
                ))
        
        fig2.update_layout(
            title="Annual Temperature Cycle (Average by Month)",
            xaxis_title="Month",
            yaxis_title=f"{get_variable_label(selected_variable)} ({get_variable_unit(selected_variable)})",
            hovermode='closest',
            legend_title="Country",
            template='plotly_white',
            height=500,
            width=None
        )
        
        fig2.update_xaxes(tickvals=list(range(1, 13)), ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        
        st.plotly_chart(fig2, width='stretch')
        
    else:
        st.info(f"Please select a temperature variable (T2M, T2M_MAX, or T2M_MIN) to view trends. Currently selected: {get_variable_label(selected_variable)}")

# Tab 2: Precipitation Analysis
with tab2:
    st.header("Precipitation Variability Analysis")
    
    if selected_variable == 'PRECTOTCORR' or 'PRECTOTCORR' in filtered_df.columns:
        
        # Create interactive boxplot using Plotly (fixed deprecated palette warning)
        fig = px.box(
            filtered_df, 
            x='Country', 
            y='PRECTOTCORR',
            color='Country',
            color_discrete_map=colors,
            points='outliers',
            title=f'Precipitation Distribution by Country ({year_range[0]}-{year_range[1]})'
        )
        
        fig.update_layout(
            yaxis_title="Daily Precipitation (mm)",
            xaxis_title="Country",
            template='plotly_white',
            height=500,
            width=None,
            showlegend=False
        )
        
        # Cap y-axis at 95th percentile for better visibility
        y_max = filtered_df['PRECTOTCORR'].quantile(0.95)
        fig.update_yaxes(range=[0, y_max])
        
        st.plotly_chart(fig, width='stretch')
        
        # Precipitation summary table
        st.subheader("Precipitation Summary Statistics")
        precip_stats = filtered_df.groupby('Country')['PRECTOTCORR'].agg([
            ('Mean (mm/day)', 'mean'),
            ('Median (mm/day)', 'median'),
            ('Std Dev', 'std'),
            ('Max (mm/day)', 'max'),
            ('Dry Days (%)', lambda x: (x < 1).sum() / len(x) * 100)
        ]).round(2).sort_values('Mean (mm/day)', ascending=False)
        
        st.dataframe(precip_stats, width='stretch')
        
        # Extreme events
        st.subheader("Extreme Precipitation Events")
        
        col1, col2 = st.columns(2)
        
        with col1:
            extreme_threshold = st.slider("Extreme Rain Threshold (mm/day)", 
                                         min_value=5, max_value=50, value=20, step=5)
        
        with col2:
            show_yearly = st.checkbox("Show Yearly Trends", value=False)
        
        extreme_stats = filtered_df.groupby('Country').apply(
            lambda x: (x['PRECTOTCORR'] > extreme_threshold).sum(), 
            include_groups=False
        ).reset_index(name='extreme_events')
        
        if show_yearly:
            yearly_extreme = filtered_df[filtered_df['PRECTOTCORR'] > extreme_threshold].groupby(
                ['Country', 'Year']).size().reset_index(name='count')
            
            fig2 = go.Figure()
            
            for country in selected_countries:
                country_data = yearly_extreme[yearly_extreme['Country'] == country]
                if not country_data.empty:
                    fig2.add_trace(go.Scatter(
                        x=country_data['Year'],
                        y=country_data['count'],
                        mode='lines+markers',
                        name=country,
                        line=dict(width=2, color=colors.get(country, '#666666')),
                        marker=dict(size=8),
                        hovertemplate=f'<b>{country}</b><br>' +
                                      'Year: %{x|%Y}<br>' +
                                      f'Days > {extreme_threshold}mm: %{{y}}<br>' +
                                      '<extra></extra>'
                    ))
            
            fig2.update_layout(
                title=f'Extreme Precipitation Events Over Time (>{extreme_threshold}mm/day)',
                xaxis_title="Year",
                yaxis_title=f'Number of Days',
                hovermode='closest',
                legend_title="Country",
                template='plotly_white',
                height=500,
                width=None
            )
            
            st.plotly_chart(fig2, width='stretch')
        else:
            st.dataframe(extreme_stats, width='stretch')
            
            # Add a bar chart for extreme events
            fig3 = px.bar(
                extreme_stats,
                x='Country',
                y='extreme_events',
                color='Country',
                color_discrete_map=colors,
                title=f'Total Extreme Events (>{extreme_threshold}mm/day) by Country'
            )
            fig3.update_layout(
                yaxis_title=f'Number of Days > {extreme_threshold}mm',
                xaxis_title="Country",
                template='plotly_white',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig3, width='stretch')
            
    else:
        st.info("Select 'PRECTOTCORR' from the variable dropdown to view precipitation analysis")

# Tab 3: Summary Statistics
with tab3:
    st.header(f"Summary Statistics: {get_variable_label(selected_variable)}")
    
    # Create summary statistics table
    summary_stats = calculate_summary_stats(filtered_df, selected_variable)
    summary_stats = summary_stats.sort_values('Mean', ascending=False)
    
    # Display as a styled dataframe
    st.dataframe(summary_stats, width='stretch')
    
    # Add an interactive bar chart for means comparison
    st.subheader("Mean Values Comparison")
    
    means = summary_stats['Mean'].reset_index()
    means.columns = ['Country', 'Mean']
    
    fig = px.bar(
        means,
        x='Mean',
        y='Country',
        orientation='h',
        color='Country',
        color_discrete_map=colors,
        title=f'Mean {get_variable_label(selected_variable)} by Country',
        text='Mean'
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>' +
                      f'{get_variable_label(selected_variable)}: %{{x:.1f}} {get_variable_unit(selected_variable)}<br>' +
                      '<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_title=f"{get_variable_label(selected_variable)} ({get_variable_unit(selected_variable)})",
        yaxis_title="Country",
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, width='stretch')
    
    # Download option
    csv = summary_stats.to_csv()
    st.download_button(
        label="📥 Download Summary Statistics (CSV)",
        data=csv,
        file_name=f"climate_summary_{selected_variable}_{year_range[0]}_{year_range[1]}.csv",
        mime="text/csv"
    )

# Tab 4: Statistical Insights
with tab4:
    st.header("Statistical Insights")
    
    st.markdown("""
    ### Key Statistical Findings
    
    Based on the Kruskal-Wallis test performed on temperature data across all five countries:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("H-Statistic", "15,393.0", help="Kruskal-Wallis test statistic")
    
    with col2:
        st.metric("P-value", "p < 0.001", help="Highly significant difference", delta="Significant")
    
    with col3:
        st.metric("Countries Compared", "5", help="Ethiopia, Kenya, Nigeria, Sudan, Tanzania")
    
    st.markdown("---")
    
    st.markdown("""
    ### Interpretation
    
    > **The Kruskal-Wallis test confirms statistically significant temperature differences across the five African nations (p < 0.001).**
    
    #### Key Implications:
    
    - **Country-specific adaptation strategies** are necessary rather than a continental approach
    - **Ethiopia** exhibits the most distinct temperature profile (normally distributed)
    - **Sudan and Nigeria** show higher temperature variability
    - **Statistical significance** validates the need for localized climate policies
    
    #### Climate Vulnerability Note:
    
    The significant differences in temperature regimes indicate that each country faces
    unique climate challenges requiring tailored adaptation and mitigation strategies.
    """)
    
    # Correlation insights
    st.subheader("Variable Correlations")
    st.markdown("""
    Strongest correlations observed in the combined dataset:
    
    | Variables | Correlation | Interpretation |
    |-----------|-------------|----------------|
    | DOY ↔ Month | 0.997 | Temporal relationship (expected) |
    | WS2M ↔ WS2M_MAX | 0.941 | Wind speed coupling |
    | RH2M ↔ QV2M | 0.905 | Moisture coupling |
    | T2M_RANGE ↔ QV2M | -0.892 | Dry conditions increase temperature range |
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
    🌍 Africa Climate Monitor | Data: 2015-2026 | Powered by Streamlit | 💡 Hover over any data point to see exact values
    </div>
    """, 
    unsafe_allow_html=True
)