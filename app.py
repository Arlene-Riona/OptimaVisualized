import streamlit as st
import plotly.graph_objects as go
import landscapes

import streamlit as st
import plotly.graph_objects as go
import landscapes
import base64  # <-- Add this built-in library

def get_base64_image(image_path):
    """Reads a local image file and converts it to a base64 string for CSS insertion."""
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"

# 1. System Config & Complete Synthwave Dark Purple Gradient Injection
st.set_page_config(layout="wide", page_title="OptimaVisualized", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Premium Deep Dark Purple Gradient Background */
    .stApp { 
        background: linear-gradient(135deg, #06020f 0%, #120524 50%, #03010a 100%);
        color: #cbd5e1; 
        font-family: 'Courier New', monospace; 
    }
    
    /* Gamified Stylized Headings */
    .game-title {
        text-align: center; 
        font-size: 4rem; 
        font-weight: 900;
        letter-spacing: 5px;
        color: #00ffcc !important; 
        text-shadow: 0 0 20px rgba(0, 255, 204, 0.6), 0 0 40px rgba(0, 255, 204, 0.2);
        margin-bottom: 0px;
        margin-top: 50px;
    }
    
    .game-subtitle {
        text-align: center; 
        color: #6d5887; 
        letter-spacing: 3px;
        font-size: 1rem;
        margin-top: 5px;
        margin-bottom: 60px;
    }
    
    .center-label {
        text-align: center;
        font-size: 1.3rem;
        color: #f8fafc;
        margin-top: 35px;
        margin-bottom: 15px;
        font-weight: 600;
    }
    
    /* Strict CSS Target to Center the Streamlit Button Container */
    div.stButton {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 40px;
    }
    
    /* Interactive Neon Arcade Button Styling */
    .stButton>button { 
        background: linear-gradient(135deg, #0e051c 0%, #1c0b36 100%);
        color: #00ffcc; 
        border: 2px solid #00ffcc; 
        padding: 16px 45px;
        font-size: 1.1rem;
        font-weight: bold;
        letter-spacing: 2px;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background: #00ffcc; 
        color: #06020f; 
        box-shadow: 0 0 25px #00ffcc, 0 0 50px rgba(0,255,204,0.4);
        border: 2px solid #00ffcc;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State variables to manage active screen routing
if "app_screen" not in st.session_state:
    st.session_state.app_screen = "WELCOME"
if "selected_algo" not in st.session_state:
    st.session_state.selected_algo = None
if "selected_scenario" not in st.session_state:
    st.session_state.selected_scenario = None

# =====================================================================
# SCREEN 1: THE INITIALIZATION DECK (WELCOME SCREEN)
# =====================================================================
if st.session_state.app_screen == "WELCOME":
    st.markdown("<h1 class='game-title'>OPTIMA_VISUALIZED</h1>", unsafe_allow_html=True)
    st.markdown("<p class='game-subtitle'>INTERACTIVE 3D LOSS LANDSCAPE EXPEDITION ENGINE</p>", unsafe_allow_html=True)
    
    # Clean centered column structure
    _, center_col, _ = st.columns([1, 1.6, 1])
    
    with center_col:
        # 1. Algorithm Selection
        st.markdown("<p class='center-label'>⚡ Select the optimization algorithm to explore</p>", unsafe_allow_html=True)
        algo_choice = st.selectbox(
            "LABEL_HIDDEN",
            [
                "Gradient Descent with Momentum (Vector Acceleration)",
                "Adam (Adaptive Step Size Estimation)",
                "Adaptive Grey Wolf Optimizer (Cooperative Swarm)"
            ],
            label_visibility="collapsed"
        )
        
        # 2. Scenario Selection
        st.markdown("<p class='center-label'>🗺️ Select an expedition scenario</p>", unsafe_allow_html=True)
        scenario_choice = st.selectbox(
            "LABEL_HIDDEN_2",
            [
                "1. Deep Ocean Trench Escape (The Rosenbrock Chasm)",
                "2. Cyberpunk Signal Jam (The Adaptive Matrix)",
                "3. Sonoran Desert Swarm Rescue (The Rastrigin Dunes)"
            ],
            label_visibility="collapsed"
        )
            
        # 3. Action Button
        if st.button("INITIALIZE MISSION DESCENT"):
            st.session_state.selected_algo = algo_choice
            st.session_state.selected_scenario = scenario_choice
            st.session_state.app_screen = "HUD"
            st.rerun()

# =====================================================================
# SCREEN 2: THE FULL-SCREEN TACTICAL HUD (IMMERSIVE MULTIMODAL MODE)
# =====================================================================
elif st.session_state.app_screen == "HUD":
    
    # Top navigation line
    hud_cols = st.columns([3, 1])
    with hud_cols[0]:
        short_algo = st.session_state.selected_algo.split('(')[0].strip()
        short_scenario = st.session_state.selected_scenario.split('(')[0].strip()
        st.markdown(f"### 🛰️ OPTIMA_VISUALIZED // {short_algo.upper()} // {short_scenario.upper()}")
    with hud_cols[1]:
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        if st.button("← Go Back"):
            st.session_state.app_screen = "WELCOME"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
    st.write("---")
    
    # Environment Skinning & Background Association Logic
    # Environment Skinning & Background Association Logic
    scenario = st.session_state.selected_scenario
    if "Ocean" in scenario:
        X, Y, Z = landscapes.get_trench_escape_data()
        terrain_colorscale = [[0, '#010b1a'], [0.4, '#0a2c5c'], [0.8, '#1e71cc'], [1, '#ffffff']]
        radar_line_color = "#00ffff"
        # Convert local ocean image to base64
        bg_image_url = get_base64_image("assets/ocean.jpg")
        mission_log = "🌌 **MISSION BRIEFING:** We are navigating a narrow deep-sea chasm. The floor is almost completely flat. Without momentum, your tracker will run out of speed and get stuck halfway through the escape trench."
    elif "Cyberpunk" in scenario:
        X, Y, Z = landscapes.get_cyberpunk_matrix_data()
        terrain_colorscale = [[0, '#05010a'], [0.3, '#32045c'], [0.7, '#88069e'], [1, '#ff007f']]
        radar_line_color = "#ff007f"
        # Convert local cyberpunk image to base64
        bg_image_url = get_base64_image("assets/cyberCity.jpg")
        mission_log = "⚡ **MISSION BRIEFING:** We are intercepting an encrypted corporate broadcast. The terrain drops into violent, unpredictable cliffs. Static step updates will overshoot completely; we need an adaptive learning speed."
    else:
        X, Y, Z = landscapes.get_desert_swarm_data()
        terrain_colorscale = [[0, '#1a0600'], [0.4, '#5c1903'], [0.8, '#c74416'], [1, '#ffa473']]
        radar_line_color = "#ff4500"
        # Convert local desert image to base64
        bg_image_url = get_base64_image("assets/desert.jpg")
        mission_log = "🏜️ **MISSION BRIEFING:** A sandstorm scattered our sensor array into hundreds of identical sand dunes. Isolated trackers are highly vulnerable to localized trap dunes."

    # 1. Build the 3D surface plot with a completely transparent paper/plot profile
    fig = go.Figure(data=[go.Surface(
        z=Z, x=X, y=Y, 
        colorscale=terrain_colorscale, 
        showscale=False,
        opacity=0.8,
        contours_z=dict(show=True, usecolormap=False, highlightcolor=radar_line_color, project_z=True, color=radar_line_color)
    )])
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)", showbackground=True, title="X Axis"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)", showbackground=True, title="Y Axis"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)", showbackground=True, title="Loss"),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, b=0, t=0),
        height=550  
    )

    # 2. INJECT BACKGROUND IMAGE CSS
    st.markdown(f"""
        <style>
        [data-testid="stPlotlyChart"] {{
            background-image: linear-gradient(to bottom, rgba(6, 2, 15, 0.3), rgba(6, 2, 15, 0.6)), url('{bg_image_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            border-radius: 12px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0px 8px 32px rgba(0, 0, 0, 0.6);
        }}
        .js-plotly-plot .plotly .main-svg {{
            background: transparent !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # 3. RENDER THE PLOT
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("---")
    
    # 4. Lower multimodal workspace layout
    log_col, control_col = st.columns([1.2, 1])
    with log_col:
        st.markdown("#### 💬 Mission Guidance AI")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
        st.info(mission_log)
        
    with control_col:
        st.markdown("#### 🛰️ Command Terminal")
        user_input = st.text_input("Transmit flight directives via text:", placeholder="e.g., Tell the trackers to accelerate over flat regions...")
        st.caption("🎙️ Or tap to record tactical voice override instruction sequence:")
        st.button("🔴 TAP TO TRANSMIT VOICE OVERRIDE")
        st.write("\n")
        if st.button("Run Simulation"):
            st.success("Calculating trajectory vectors...")