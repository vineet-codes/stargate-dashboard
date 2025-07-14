import streamlit as st
import pandas as pd
from stargate import fetch_nft_mint_counts
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Stargate NFT Dashboard",
    page_icon="🚀",
    layout="wide"
)

# Title and description
st.title("🚀 Stargate NFT Holders Dashboard")
st.markdown("Real-time data from VeChain mainnet showing NFT holder counts by level")

# Add some styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Main content
try:
    with st.spinner("Fetching latest data from VeChain mainnet..."):
        result, total_holders, vet_staked, nfts_remaining = fetch_nft_mint_counts()
    
    # Display total in a prominent metric
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total NFT Holders",
            value=f"{total_holders:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Number of Levels",
            value=len(result),
            delta=None
        )
    
    with col3:
        # Calculate total VET staked
        total_vet_staked = sum(vet_staked.values())
        st.metric(
            label="Total VET Staked",
            value=f"{total_vet_staked:,}",
            delta=None
        )
    
    with col4:
        # Find the level with most holders
        max_level = max(result, key=result.get)
        max_count = result[max_level]
        st.metric(
            label="Most Popular Level",
            value=f"{max_level} ({max_count:,})",
            delta=None
        )
    
    st.markdown("---")
    
    # Create DataFrame for better display
    df = pd.DataFrame([
        {
            'Level': level,
            'Holders': count,
            'Remaining': nfts_remaining[level],
            'VET Staked': vet_staked[level]
        }
        for level, count in result.items()
    ])
    df = df.sort_values('Holders', ascending=False)
    
    # Display table
    st.subheader("📊 NFT Holders by Level")
    
    # Create a styled table
    st.dataframe(
        df.style.format({
            'Holders': '{:,}',
            'Remaining': '{:,}',
            'VET Staked': '{:,}'
        }).background_gradient(subset=['Holders'], cmap='Blues'),
        use_container_width=True,
        hide_index=True
    )
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Holders Distribution")
        fig_bar = px.bar(
            df, 
            x='Level', 
            y='Holders',
            title="NFT Holders by Level",
            color='Holders',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(
            xaxis_title="Level",
            yaxis_title="Number of Holders",
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Holders Percentage")
        fig_pie = px.pie(
            df, 
            values='Holders', 
            names='Level',
            title="Distribution of NFT Holders"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Raw data section
    with st.expander("🔍 Raw Data"):
        st.json(result)
    
    # Add timestamp
    st.markdown("---")
    st.caption(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

except Exception as e:
    st.error(f"Error fetching data: {str(e)}")
    st.info("Please check your internet connection and try again.") 