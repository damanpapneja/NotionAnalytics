import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import base64
import re

def patch_st_markdown():
    """Monkey-patch st.markdown to replace <div class="person-icon"></div> with inline base64 images."""
    original_markdown = st.markdown

    # Load and base64‑encode all 5 images into a list
    images_data = []
    for i in range(1, 6):
        with open(f'image{i}.png', 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
            images_data.append(b64)

    def new_markdown(html, *args, **kwargs):
        # Replace each <div class="person-icon"></div> with a random image
        def replacer(match):
            chosen = random.choice(images_data)
            return (
                f'<div class="person-icon" '
                f'style="background: url(\'data:image/png;base64,{chosen}\') '
                f'no-repeat center center; background-size: contain;"></div>'
            )

        # Run a regex that looks for exactly <div class="person-icon"></div>
        new_html = re.sub(
            r'<div\s+class="person-icon"\s*></div>',
            replacer,
            str(html)  # in case "html" is not already a string
        )
        return original_markdown(new_html, *args, **kwargs)

    # Override st.markdown with our patched version
    st.markdown = new_markdown

# Call the patch function so that st.markdown is replaced
patch_st_markdown()


# Set page configuration (sidebar is collapsed so it won't show)
st.set_page_config(
    page_title="Workspace Analytics", layout="wide", initial_sidebar_state="collapsed"
)

# Custom CSS for styling - Dark Mode with updated colors, icon alignment, and using 'Inter'
st.markdown(
    """
<style>
    /* Global styling */
    .stApp {
        font-family: sans-serif;
        background-color: #121212;
        color: #e0e0e0;
    }
    /* Remove the sidebar completely */
    [data-testid="stSidebar"] { dispalay: none; }

    /* Main content area styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Card styling for sections */
    .member-card {
        background-color: #262626;
        border-radius: 4px;
        padding: 10px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        color: #D4D4D4;
    }

    /* Dropdown styling for Last 90 Days */
    .dropdown {
        border: 1px solid #444444;
        border-radius: 4px;
        padding: 5px 10px;
        font-size: 0.9rem;
        background-color: #1B2028;
        color: #2483E2;
    }

    /* Icon placeholders */
    .person-icon {
        width: 20px;
        height: 20px;
        background-color: #555555;
        border-radius: 50%;
        margin-right: 10px;
        display: inline-block;
        vertical-align: middle;
    }
    .page-icon {
        width: 20px;
        height: 20px;
        background-color: #555555;
        border-radius: 5px;
        margin-right: 10px;
        display: inline-block;
        vertical-align: middle;
    }

    /* Align text with icons */
    .icon-text {
        display: inline-block;
        vertical-align: middle;
    }

    /* Responsive layout adjustments */
    @media (max-width: 1200px) {
        .stApp .block-container {
            padding: 1rem;
        }
    }
    @media (max-width: 992px) {
        .main .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)


# Top header (common across tabs)
st.markdown(
    '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">'
    "<h2>Workspace Analytics</h2>"
    '<button style="background-color: #2d2d2d; border: 1px solid #444444; border-radius: 4px; padding: 5px 10px; color: #e0e0e0;">Have feedback?</button>'
    "</div>",
    unsafe_allow_html=True,
)

# Create tabs for Engagement, Collaboration, and Discovery
engagement_tab, collaboration_tab, discovery_tab = st.tabs(["Engagement", "Collaboration", "Discovery"])

# -------------------------------
# ENGAGEMENT TAB CONTENT
# ------------------------------
with engagement_tab:
    # Header and dropdown for Member Engagement
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown("<h3>Member Engagement</h3>", unsafe_allow_html=True)
    with col2:
        st.markdown(
            '<div style="text-align: right;"><span class="dropdown">Last 90 Days <span style="font-size: 14px;">⌄</span></span></div>',
            unsafe_allow_html=True,
        )

    # Total Members card
    st.markdown(
        """
<div class="member-card" style="width: 100%;">
    <h2 style="margin: 0;">Total Members <span style="float: right;">98</span></h2>
    <p style="font-size: 0.9rem; color: #4caf50; margin-top: 1px;">&gt;↗ 118% more than previous 90 days</p>
</div>
""",
        unsafe_allow_html=True,
    )

    # -------------------------------
    # Three current activity sections
    # -------------------------------
    col1, col2, col3 = st.columns(3)

    # Current Active Members card
    with col1:
        st.markdown(
            """
        <div class="member-card">
            <h4 style="margin-bottom: 10px;">Active Members <span style="float: right;">32</span></h4>
            <div style="display: flex; align-items: center; font-weight: bold; margin-bottom: 10px;">
                <div style="flex: 1; text-align: left;">Name</div>
                <div style="flex: 1; text-align: left;"># Sessions</div>
                <div style="flex: 1; text-align: left;">Top Teamspace</div>
            </div>
            <!-- For the Name column, using person-icon to denote people's names -->
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Alice</span></div>
                <div style="flex: 1; text-align: left;">1010</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">General</span></div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Bob</span></div>
                <div style="flex: 1; text-align: left;">990</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Product</span></div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Charlie</span></div>
                <div style="flex: 1; text-align: left;">800</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Marketing</span></div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Dana</span></div>
                <div style="flex: 1; text-align: left;">500</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Finance</span></div>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Eve</span></div>
                <div style="flex: 1; text-align: left;">210</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Engineering</span></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Current Active Contributors card
    with col2:
        st.markdown(
            """
        <div class="member-card">
            <h4 style="margin-bottom: 10px;">Active Contributors <span style="float: right;">18</span></h4>
            <div style="display: flex; align-items: center; font-weight: bold; margin-bottom: 10px;">
                <div style="flex: 1; text-align: left;">Name</div>
                <div style="flex: 1; text-align: left;"># Edits</div>
                <div style="flex: 1; text-align: left;">Top Teamspace</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Zoe</span></div>
                <div style="flex: 1; text-align: left;">500</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Marketing</span></div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Rebecca</span></div>
                <div style="flex: 1; text-align: left;">565</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Analytics</span></div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Fig</span></div>
                <div style="flex: 1; text-align: left;">367</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Data</span></div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Nicole Wu</span></div>
                <div style="flex: 1; text-align: left;">278</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">HR</span></div>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Stephanie</span></div>
                <div style="flex: 1; text-align: left;">109</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Strategy</span></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Current Active Creators card
    with col3:
        st.markdown(
            """
        <div class="member-card">
            <h4 style="margin-bottom: 10px;">Active Creators <span style="float: right;">5</span></h4>
            <div style="display: flex; align-items: center; font-weight: bold; margin-bottom: 10px;">
                <div style="flex: 1; text-align: left;">Name</div>
                <div style="flex: 1; text-align: left;"># Additions</div>
                <div style="flex: 1; text-align: left;">Top Teamspace</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Rebecca</span></div>
                <div style="flex: 1; text-align: left;">50</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Engineering</span></div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Fig</span></div>
                <div style="flex: 1; text-align: left;">43</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Marketing</span></div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Zoe</span></div>
                <div style="flex: 1; text-align: left;">32</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Analytics</span></div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Sohrab A...</span></div>
                <div style="flex: 1; text-align: left;">16</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">Data</span></div>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="flex: 1; text-align: left;"><div class="person-icon"></div><span class="icon-text">Nicole Wu</span></div>
                <div style="flex: 1; text-align: left;">9</div>
                <div style="flex: 1; text-align: left;"><div class="page-icon"></div><span class="icon-text">HR</span></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # -------------------------------
    # Charts for each activity section
    # -------------------------------
    col1_chart, col2_chart, col3_chart = st.columns(3)

    # Common chart parameters
    chart_height = 1.5
    chart_width = 4
    font_size = 7

    # Chart for Current Active Members
    with col1_chart:
        fig, ax = plt.subplots(figsize=(chart_width, chart_height))
        fig.patch.set_facecolor("#262626")
        ax.set_facecolor("#262626")
        x = np.linspace(0, 9, 10)
        # Simulated upward data with fluctuations matching a max of 32
        y = np.array([9, 9, 7, 8, 10, 15, 17, 21, 26, 32])

        # Add title to match section header styling
        title_fontsize = 9  # Match h4 size from section above
        plt.figtext(
            0.05,  # X position - aligned with left edge of plot
            0.95,  # Y position - top of the figure
            "Active Members over time",
            fontsize=title_fontsize,
            color="#D4D4D4",
            fontweight="medium",
            ha="left",
        )

        ax.fill_between(x, y, color="#e0f0ff", alpha=0.5)
        ax.plot(x, y, color="#80bfff")
        ax.set_ylim(0, 32)
        ax.set_yticks(np.linspace(0, 32, 5))
        ax.set_xticks(np.linspace(x.min(), x.max(), 15))
        ax.set_xticklabels([])
        ax.tick_params(axis="y", colors="#D4D4D4", labelsize=font_size)
        ax.tick_params(axis="x", colors="#262626")
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Adjust plot margins to make room for the title
        plt.subplots_adjust(top=0.8)
        st.pyplot(fig)

    # Chart for Current Active Contributors
    with col2_chart:
        fig, ax = plt.subplots(figsize=(chart_width, chart_height))
        fig.patch.set_facecolor("#262626")
        ax.set_facecolor("#262626")
        x = np.linspace(0, 9, 10)
        y = np.array([8, 10, 11, 12, 15, 15, 15, 17, 17, 18])

        # Add title to match section header styling
        title_fontsize = 9  # Match h4 size from section above
        plt.figtext(
            0.05,  # X position - aligned with left edge of plot
            0.95,  # Y position - top of the figure
            "Active Contributors over time",
            fontsize=title_fontsize,
            color="#D4D4D4",
            fontweight="medium",
            ha="left",
        )

        ax.fill_between(x, y, color="#e0f0ff", alpha=0.5)
        ax.plot(x, y, color="#80bfff")
        ax.set_ylim(0, 18)
        ax.set_yticks(np.linspace(0, 18, 4))
        ax.set_xticks(np.linspace(x.min(), x.max(), 15))
        ax.set_xticklabels([])
        ax.tick_params(axis="y", colors="#D4D4D4", labelsize=font_size)
        ax.tick_params(axis="x", colors="#262626")
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Adjust plot margins to make room for the title
        plt.subplots_adjust(top=0.8)
        st.pyplot(fig)

    # Chart for Current Active Creators
    with col3_chart:
        fig, ax = plt.subplots(figsize=(chart_width, chart_height))
        fig.patch.set_facecolor("#262626")
        ax.set_facecolor("#262626")
        x = np.linspace(0, 9, 10)
        y = np.array([4, 4, 4, 4, 4, 5, 5, 4, 4, 5])

        # Add title to match section header styling
        title_fontsize = 9  # Match h4 size from section above
        plt.figtext(
            0.05,  # X position - aligned with left edge of plot
            0.95,  # Y position - top of the figure
            "Active Creators over time",
            fontsize=title_fontsize,
            color="#D4D4D4",
            fontweight="medium",
            ha="left",
        )

        ax.fill_between(x, y, color="#e0f0ff", alpha=0.5)
        ax.plot(x, y, color="#80bfff")
        ax.set_ylim(0, 5)
        ax.set_yticks(np.linspace(0, 5, 6))
        ax.set_xticks(np.linspace(x.min(), x.max(), 15))
        ax.set_xticklabels([])
        ax.tick_params(axis="y", colors="#D4D4D4", labelsize=font_size)
        ax.tick_params(axis="x", colors="#262626")
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Adjust plot margins to make room for the title
        plt.subplots_adjust(top=0.8)
        st.pyplot(fig)
    # -------------------------------
    # Content Engagement Section
    # -------------------------------
    st.markdown("<h3>Content Engagement</h3>", unsafe_allow_html=True)
    col1_ce, col2_ce = st.columns(2)
    with col1_ce:
        st.markdown(
            """
        <div class="member-card" style="width: 100%;">
            <h2 style="margin: 0;">Total Pages <span style="float: right;">12</span></h2>
            <p style="font-size: 0.9rem; color: #4caf50; margin-top: 1px;">> Active Pages: 6</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2_ce:
        st.markdown(
            """
        <div class="member-card" style="width: 100%;">
            <h2 style="margin: 0;">Total Sessions <span style="float: right;">126</span></h2>
            <p style="font-size: 0.9rem;color: #4caf50; margin-top: 1px;">> Active Sessions: 56</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Content Engagement Details Table
    pages = [
        "General", "Product", "Finance", "People", "Engineering", "Marketing",
        "Analytics", "Data", "HR", "Strategy", "Operations", "BizOps"
    ]
    top_members = ["Alice", "Bob", "Charlie", "Dana", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack"]
    top_contributors = ["Zoe", "Liam", "Emma", "Noah", "Olivia", "Ava", "William", "Sophia", "Mason", "Isabella"]

    table_html = """
<table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
  <tr style="text-align: left; border-bottom: 1px solid #444444;">
    <th style="padding: 8px;">Page Name</th>
    <th style="padding: 8px;">Top Member</th>
    <th style="padding: 8px;">Top Contributor</th>
    <th style="padding: 8px;">Avg Scroll Depth</th>
    <th style="padding: 8px;">Avg Time Spent (min)</th>
  </tr>
    """
    for page in pages:
        scroll_depth = random.randint(0, 100)
        avg_time = random.randint(1, 15)
        member = random.choice(top_members)
        contributor = random.choice(top_contributors)
        progress_html = f"""
    <div style="width: 100%; background-color: #555555; height: 10px; border-radius: 5px; margin-bottom: 2px;">
        <div style="width: {scroll_depth}%; background-color: #4caf50; height: 10px; border-radius: 5px;"></div>
    </div>
    <span style="font-size: 0.8rem;">{scroll_depth}%</span>
    """
        table_html += f"""
  <tr style="border-bottom: 1px solid #444444;">
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">{page}</span></td>
    <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">{member}</span></td>
    <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">{contributor}</span></td>
    <td style="padding: 8px;">{progress_html}</td>
    <td style="padding: 8px;">{avg_time} min</td>
  </tr>
  """
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)


# -------------------------------
# COLLABORATION TAB CONTENT
# -------------------------------
with collaboration_tab:
    # Header and dropdown for Team-specific view
    col1_col, col2_col = st.columns([1, 4])
    with col1_col:
        st.markdown("<h3>Team-Specific</h3>", unsafe_allow_html=True)
    with col2_col:
        st.markdown(
            '<div style="text-align: right;"><span class="dropdown">Last 90 Days <span style="font-size: 14px;">⌄</span></span></div>',
            unsafe_allow_html=True,
        )

    # Split the row into two columns: left for Active Team Interactions card, right for donut chart
    # Adjust the ratio so the left section is larger and the right chart is smaller
    col_left, col_right = st.columns([4.5, 2])

    # Left column: Active Team Interactions Card (increased min-height)
    with col_left:
        st.markdown(
            """
<div class="member-card" style="width: 100%; min-height: 240px;">
    <h2 style="margin: 0;">Active Team Interactions <span style="float: right;">1745</span></h2>
    <p style="font-size: 0.9rem; color: #4caf50; margin-top: 1px;">&gt;↗ 426% more than previous 90 days</p>
</div>
""",
            unsafe_allow_html=True,
        )

    # Right column: Donut Chart showing the interactions mix (smaller donut size and label size)
    with col_right:
        import matplotlib.pyplot as plt

        # Sample distribution of interactions (Edits has highest share)
        labels = [
            "Edits", "Comments", "Reactions", "Mentions",
            "Shares", "Kanbans", "Tasks", "Databases"
        ]
        sizes = [30, 20, 15, 10, 10, 9, 6, 5]  # Total 100
        # Darker-to-lighter pastel blues
        colors = [
            "#7DA7C7", "#8FBED6", "#9FD3E6", "#AADFF0",
            "#B3E5F2", "#BCE9F4", "#C6EDF6", "#D0F2F9"
        ]

        fig, ax = plt.subplots(figsize=(1.5, 1.1))  # Reduced size
        fig.patch.set_facecolor("none")
        ax.set_facecolor("none")

        # Create the donut chart without percentage labels, with smaller text
        wedges, texts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            startangle=140,
            textprops={"fontsize": 4, "color": "#e0e0e0"},  # Reduced font size
        )
        # Create the donut hole
        centre_circle = plt.Circle((0, 0), 0.70, fc="#121212")
        fig.gca().add_artist(centre_circle)

        ax.axis("equal")  # Ensures the pie is drawn as a circle
        st.pyplot(fig)

    
    # Collaboration-specific Analytics Table
    table_html = """
<table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
  <tr style="text-align: left; border-bottom: 1px solid #444444;">
    <th style="padding: 8px;">Current Team Page</th>
    <th style="padding: 8px;"># Unique Collaborators</th>
    <th style="padding: 8px;">Total Interactions</th>
    <th style="padding: 8px;">Interactions Trend</th>
    <th style="padding: 8px;">Top Collaborator</th>
  </tr>
  <tr style="border-bottom: 1px solid #444444;">
    <td style="padding: 8px;">
        <div class="page-icon"></div><span class="icon-text">Product Roadmap</span>
    </td>
    <td style="padding: 8px;">12</td>
    <td style="padding: 8px;">256</td>
    <td style="padding: 8px;"><span style="color: #4caf50;">+35%</span></td>
    <td style="padding: 8px;">
        <div class="person-icon"></div><span class="icon-text">Alice</span>
    </td>
  </tr>
  <tr style="border-bottom: 1px solid #444444;">
    <td style="padding: 8px;">
        <div class="page-icon"></div><span class="icon-text">Product Updates</span>
    </td>
    <td style="padding: 8px;">15</td>
    <td style="padding: 8px;">340</td>
    <td style="padding: 8px;"><span style="color: red;">-20%</span></td>
    <td style="padding: 8px;">
        <div class="person-icon"></div><span class="icon-text">Bob</span>
    </td>
  </tr>
  <tr style="border-bottom: 1px solid #444444;">
    <td style="padding: 8px;">
        <div class="page-icon"></div><span class="icon-text">Feature Releases</span>
    </td>
    <td style="padding: 8px;">17</td>
    <td style="padding: 8px;">512</td>
    <td style="padding: 8px;"><span style="color: #4caf50;">+45%</span></td>
    <td style="padding: 8px;">
        <div class="person-icon"></div><span class="icon-text">Charlie</span>
    </td>
  </tr>
  <tr style="border-bottom: 1px solid #444444;">
    <td style="padding: 8px;">
        <div class="page-icon"></div><span class="icon-text">Beta Testing</span>
    </td>
    <td style="padding: 8px;">11</td>
    <td style="padding: 8px;">478</td>
    <td style="padding: 8px;"><span style="color: red;">-10%</span></td>
    <td style="padding: 8px;">
        <div class="person-icon"></div><span class="icon-text">Dana</span>
    </td>
  </tr>
  <tr style="border-bottom: 1px solid #444444;">
    <td style="padding: 8px;">
        <div class="page-icon"></div><span class="icon-text">Product Design</span>
    </td>
    <td style="padding: 8px;">14</td>
    <td style="padding: 8px;">690</td>
    <td style="padding: 8px;"><span style="color: #4caf50;">+80%</span></td>
    <td style="padding: 8px;">
        <div class="person-icon"></div><span class="icon-text">Eve</span>
    </td>
  </tr>
  <tr style="border-bottom: 1px solid #444444;">
    <td style="padding: 8px;">
        <div class="page-icon"></div><span class="icon-text">User Feedback</span>
    </td>
    <td style="padding: 8px;">16</td>
    <td style="padding: 8px;">820</td>
    <td style="padding: 8px;"><span style="color: #4caf50;">+120%</span></td>
    <td style="padding: 8px;">
        <div class="person-icon"></div><span class="icon-text">Frank</span>
    </td>
  </tr>
  <tr style="border-bottom: 1px solid #444444;">
    <td style="padding: 8px;">
        <div class="page-icon"></div><span class="icon-text">Quality Assurance</span>
    </td>
    <td style="padding: 8px;">13</td>
    <td style="padding: 8px;">305</td>
    <td style="padding: 8px;"><span style="color: red;">-15%</span></td>
    <td style="padding: 8px;">
        <div class="person-icon"></div><span class="icon-text">Grace</span>
    </td>
  </tr>
  <tr style="border-bottom: 1px solid #444444;">
    <td style="padding: 8px;">
        <div class="page-icon"></div><span class="icon-text">Product Metrics</span>
    </td>
    <td style="padding: 8px;">18</td>
    <td style="padding: 8px;">765</td>
    <td style="padding: 8px;"><span style="color: #4caf50;">+60%</span></td>
    <td style="padding: 8px;">
        <div class="person-icon"></div><span class="icon-text">Hank</span>
    </td>
  </tr>
  <tr style="border-bottom: 1px solid #444444;">
    <td style="padding: 8px;">
        <div class="page-icon"></div><span class="icon-text">Innovation Lab</span>
    </td>
    <td style="padding: 8px;">10</td>
    <td style="padding: 8px;">410</td>
    <td style="padding: 8px;"><span style="color: red;">-25%</span></td>
    <td style="padding: 8px;">
        <div class="person-icon"></div><span class="icon-text">Ivy</span>
    </td>
  </tr>
  <tr>
    <td style="padding: 8px;">
        <div class="page-icon"></div><span class="icon-text">Product Strategy</span>
    </td>
    <td style="padding: 8px;">19</td>
    <td style="padding: 8px;">980</td>
    <td style="padding: 8px;"><span style="color: #4caf50;">+95%</span></td>
    <td style="padding: 8px;">
        <div class="person-icon"></div><span class="icon-text">Jack</span>
    </td>
  </tr>
</table>
"""
    st.markdown(table_html, unsafe_allow_html=True)
    # Header and dropdown for Team-specific view
    col1_col, col2_col = st.columns([1, 4])
    with col1_col:
        st.markdown("<h3>Cross-Team</h3>", unsafe_allow_html=True)
    with col2_col:
        st.markdown(
            '<div style="text-align: right;"><span class="dropdown">Last 90 Days <span style="font-size: 14px;">⌄</span></span></div>',
            unsafe_allow_html=True,
        )

    # Split the row into two columns: left for Active Team Interactions card, right for donut chart
    # Adjust the ratio so the left section is larger and the right chart is smaller
    col_left, col_right = st.columns([4.5, 2])

    # Left column: Active Team Interactions Card (increased min-height)
    with col_left:
        st.markdown(
            """
<div class="member-card" style="width: 100%; min-height: 240px;">
    <h2 style="margin: 0;">Cross Team Interactions <span style="float: right;">454</span></h2>
    <p style="font-size: 0.9rem; color: #4caf50; margin-top: 1px;">&gt;↗ 67% more than previous 90 days</p>
</div>
""",
            unsafe_allow_html=True,
        )

    # Right column: Donut Chart showing the interactions mix (smaller donut size and label size)
    with col_right:
        import matplotlib.pyplot as plt

        # Sample distribution of interactions (Edits has highest share)
        labels = [
            "Edits", "Comments", "Reactions", "Mentions",
            "Shares", "Kanbans", "Tasks", "Databases"
        ]
        sizes = [5, 25, 20, 20, 10, 5, 5, 10]  # Total 100
        # Darker-to-lighter pastel blues
        colors = [
            "#A8E6CF", "#B2F2D2", "#BBF8D7", "#C4FFD9", "#CCFFDF", 
            "#D5FFE3", "#DEFFE7", "#E7FFEB"
        ]

        fig, ax = plt.subplots(figsize=(1.5, 1.1))  # Reduced size
        fig.patch.set_facecolor("none")
        ax.set_facecolor("none")

        # Create the donut chart without percentage labels, with smaller text
        wedges, texts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            startangle=140,
            textprops={"fontsize": 4, "color": "#e0e0e0"},  # Reduced font size
        )
        # Create the donut hole
        centre_circle = plt.Circle((0, 0), 0.70, fc="#121212")
        fig.gca().add_artist(centre_circle)

        ax.axis("equal")  # Ensures the pie is drawn as a circle
        st.pyplot(fig)
    
        table_html = """
    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
    <tr style="text-align: left; border-bottom: 1px solid #444444;">
        <th style="padding: 8px;">Teamspace</th>
        <th style="padding: 8px;">Shared Content</th>
        <th style="padding: 8px;">Shared with</th>
        <th style="padding: 8px;">Top Collaborator</th>
        <th style="padding: 8px;">Interactions</th>
    </tr>
    <tr style="border-bottom: 1px solid #444444;">
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Product</span></td>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Product Roadmap</span></td>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Marketing</span></td>
        <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">Alice</span></td>
        <td style="padding: 8px;">980</td>
    </tr>
    <tr style="border-bottom: 1px solid #444444;">
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Engineering</span></td>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Sprint Overview</span></td>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Product</span></td>
        <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">Bob</span></td>
        <td style="padding: 8px;">865</td>
    </tr>
    <tr style="border-bottom: 1px solid #444444;">
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Finance</span></td>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Budget Report</span></td>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Operations</span></td>
        <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">Charlie</span></td>
        <td style="padding: 8px;">750</td>
    </tr>
    <tr style="border-bottom: 1px solid #444444;">
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">HR</span></td>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Employee Handbook</span></td>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">People</span></td>
        <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">Dana</span></td>
        <td style="padding: 8px;">620</td>
    </tr>
    <tr>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Analytics</span></td>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Data Insights</span></td>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Strategy</span></td>
        <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">Eve</span></td>
        <td style="padding: 8px;">510</td>
    </tr>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    # Header and dropdown for Team-specific view
    col1_col, col2_col = st.columns([1, 4])
    with col1_col:
        st.markdown("<h3>Cross-Product</h3>", unsafe_allow_html=True)
    with col2_col:
        st.markdown(
            '<div style="text-align: right;"><span class="dropdown">Last 90 Days <span style="font-size: 14px;">⌄</span></span></div>',
            unsafe_allow_html=True,
        )

    # Split the row into two columns: left for Active Team Interactions card, right for donut chart
    # Adjust the ratio so the left section is larger and the right chart is smaller
    col_left, col_right = st.columns([4.5, 2])

    # Left column: Active Team Interactions Card (increased min-height)
    with col_left:
        st.markdown(
            """
<div class="member-card" style="width: 100%; min-height: 240px;">
    <h2 style="margin: 0;">Cross Product Integrations <span style="float: right;">110</span></h2>
    <p style="font-size: 0.9rem; color: #4caf50; margin-top: 1px;">&gt;↗ 27% more than previous 90 days</p>
</div>
""",
            unsafe_allow_html=True,
        )

    # Right column: Donut Chart showing the interactions mix (smaller donut size and label size)
    with col_right:
        import matplotlib.pyplot as plt

        # Sample distribution of interactions (Edits has highest share)
        labels = [
            "Figma", "Slack", "Github"
        ]
        sizes = [60, 30, 10]  # Total 100
        # Darker-to-lighter pastel green
        colors = [
         "#FFF9C4", "#FFF59D", "#FFF176"
        ]

        fig, ax = plt.subplots(figsize=(1.5, 1.1))  # Reduced size
        fig.patch.set_facecolor("none")
        ax.set_facecolor("none")

        # Create the donut chart without percentage labels, with smaller text
        wedges, texts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            startangle=140,
            textprops={"fontsize": 4, "color": "#e0e0e0"},  # Reduced font size
        )
        # Create the donut hole
        centre_circle = plt.Circle((0, 0), 0.70, fc="#121212")
        fig.gca().add_artist(centre_circle)

        ax.axis("equal")  # Ensures the pie is drawn as a circle
        st.pyplot(fig)
        table_html = """
    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
    <tr style="text-align: left; border-bottom: 1px solid #444444;">
        <th style="padding: 8px;">Teamspace</th>
        <th style="padding: 8px;">Number of Integrations</th>
        <th style="padding: 8px;">Top Integration</th>
    </tr>
    <tr style="border-bottom: 1px solid #444444;">
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Engineering</span></td>
        <td style="padding: 8px;">25</td>
        <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">Github</span></td>
    </tr>
    <tr style="border-bottom: 1px solid #444444;">
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Product</span></td>
        <td style="padding: 8px;">22</td>
        <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">Figma</span></td>
    </tr>
    <tr style="border-bottom: 1px solid #444444;">
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Marketing</span></td>
        <td style="padding: 8px;">18</td>
        <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">Slack</span></td>
    </tr>
    <tr style="border-bottom: 1px solid #444444;">
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Finance</span></td>
        <td style="padding: 8px;">14</td>
        <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">Github</span></td>
    </tr>
    <tr>
        <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">General</span></td>
        <td style="padding: 8px;">10</td>
        <td style="padding: 8px;"><div class="person-icon"></div><span class="icon-text">Figma</span></td>
    </tr>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)


# -------------------------------
# DISCOVERY TAB CONTENT
# -------------------------------
with discovery_tab:
    # Top Header with Last 90 Days dropdown
    col1_dis, col2_dis = st.columns([1, 4])
    with col1_dis:
        st.markdown("<h3>Discovery</h3>", unsafe_allow_html=True)
    with col2_dis:
        st.markdown(
            '<div style="text-align: right;"><span class="dropdown">Last 90 Days <span style="font-size: 14px;">⌄</span></span></div>',
            unsafe_allow_html=True,
        )

    # Top Section: Total Searches Card
    st.markdown("""
<div class="member-card" style="width: 100%; min-height: 180px;">
    <h2 style="margin: 0;">Total Searches <span style="float: right;">148</span></h2>
    <p style="font-size: 0.9rem; color: #4caf50; margin-top: 1px;">&gt;↗ +5% more than previous 90 days</p>
</div>
""", unsafe_allow_html=True)

    # Section Heading: Searches by Teamspace
    st.markdown("<h4>Searches by Teamspace</h4>", unsafe_allow_html=True)
    st.markdown("""
<table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
  <tr style="text-align: left; border-bottom: 1px solid #444444; font-size: 12px;">
    <th style="padding: 8px;">Teamspace</th>
    <th style="padding: 8px;"># Searches</th>
    <th style="padding: 8px;">Search Trend</th>
    <th style="padding: 8px;">Top Searched Page</th>
    <th style="padding: 8px;">Top Searches</th>
  </tr>
  <tr style="border-bottom: 1px solid #444444; font-size: 12px;">
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">General</span></td>
    <td style="padding: 8px;">250</td>
    <td style="padding: 8px;"><span style="color: #4caf50;">+5%</span></td>
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Company Announcements</span></td>
    <td style="padding: 8px;">Latest updates</td>
  </tr>
  <tr style="border-bottom: 1px solid #444444; font-size: 12px;">
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Product</span></td>
    <td style="padding: 8px;">200</td>
    <td style="padding: 8px;"><span style="color: red;">-3%</span></td>
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Product Roadmap</span></td>
    <td style="padding: 8px;">New features</td>
  </tr>
  <tr style="border-bottom: 1px solid #444444; font-size: 12px;">
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Finance</span></td>
    <td style="padding: 8px;">180</td>
    <td style="padding: 8px;"><span style="color: #4caf50;">+2%</span></td>
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Budget Overview</span></td>
    <td style="padding: 8px;">Quarterly Report</td>
  </tr>
  <tr style="border-bottom: 1px solid #444444; font-size: 12px;">
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Engineering</span></td>
    <td style="padding: 8px;">150</td>
    <td style="padding: 8px;"><span style="color: red;">-1%</span></td>
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Sprint Planning</span></td>
    <td style="padding: 8px;">Tech Innovations</td>
  </tr>
  <tr style="font-size: 12px;">
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Marketing</span></td>
    <td style="padding: 8px;">120</td>
    <td style="padding: 8px;"><span style="color: #4caf50;">+7%</span></td>
    <td style="padding: 8px;"><div class="page-icon"></div><span class="icon-text">Campaign Metrics</span></td>
    <td style="padding: 8px;">Ad Performance</td>
  </tr>
</table>
""", unsafe_allow_html=True)

    # Section Heading: Searches by Content
    st.markdown("<h4>Searches by Content</h4>", unsafe_allow_html=True)
    st.markdown("""
<table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
  <tr style="text-align: left; border-bottom: 1px solid #444444; font-size: 12px;">
    <th style="padding: 8px;">Top Searches</th>
    <th style="padding: 8px;"># Searches</th>
    <th style="padding: 8px;">Click-through Rate</th>
  </tr>
  <tr style="border-bottom: 1px solid #444444; font-size: 12px;">
    <td style="padding: 8px;">Budget Forecast</td>
    <td style="padding: 8px;">300</td>
    <td style="padding: 8px;">25%</td>
  </tr>
  <tr style="border-bottom: 1px solid #444444; font-size: 12px;">
    <td style="padding: 8px;">Product Updates</td>
    <td style="padding: 8px;">280</td>
    <td style="padding: 8px;">0%</td>
  </tr>
  <tr style="border-bottom: 1px solid #444444; font-size: 12px;">
    <td style="padding: 8px;">Engineering Roadmap</td>
    <td style="padding: 8px;">260</td>
    <td style="padding: 8px;">15%</td>
  </tr>
  <tr style="border-bottom: 1px solid #444444; font-size: 12px;">
    <td style="padding: 8px;">Marketing Trends</td>
    <td style="padding: 8px;">240</td>
    <td style="padding: 8px;">10%</td>
  </tr>
  <tr style="font-size: 12px;">
    <td style="padding: 8px;">HR Policies</td>
    <td style="padding: 8px;">220</td>
    <td style="padding: 8px;">0%</td>
  </tr>
</table>
""", unsafe_allow_html=True)

        # Section Heading: Stale Content Watch
    st.markdown("<h4>Stale Content Watch</h4>", unsafe_allow_html=True)
    import matplotlib.pyplot as plt
    import numpy as np

    pages = ["Company Handbook", "Old Product Page", "Legacy Budget", "Archived Meeting", "Deprecated FAQ"]
    days_since_viewed = [50, 38, 32, 27, 20]

    # Increase figure height to give more room for labels
    fig, ax = plt.subplots(figsize=(5.5, 1))
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    y_pos = np.arange(len(pages))
    bar_colors = "#A8E6CF"  # Pastel green color
    bars = ax.barh(y_pos, days_since_viewed, height=0.3, color=bar_colors)

    ax.set_yticks(y_pos)
    # Left-align the labels; add more padding to avoid overlap
    ax.set_yticklabels(pages, fontsize=4, color="#666666", ha='left')
    ax.tick_params(axis='y', which='both', length=0, pad=60)  # Increase pad to move labels left

    ax.invert_yaxis()  # highest value on top
    ax.set_xlabel("Days Since Last Viewed", fontsize=4, color="#666666")

    # Remove tick marks from x-axis while keeping the numbers
    ax.tick_params(axis="x", which="both", length=0, labelsize=4, colors="#666666")

    # Remove spines (borders)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Optionally adjust subplot to ensure labels aren’t clipped
    plt.subplots_adjust(left=0.25, right=0.95)

    st.pyplot(fig)
