import streamlit as st
import plotly.graph_objects as go
import landscapes
import base64
import json
import numpy as np

def get_base64_image(image_path):
    """Reads a local image file and converts it to a base64 string for CSS insertion."""
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    except FileNotFoundError:
        return ""

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

# Initialize Session State variables to manage active screen routing and trajectory data
if "app_screen" not in st.session_state:
    st.session_state.app_screen = "WELCOME"
if "selected_algo" not in st.session_state:
    st.session_state.selected_algo = None
if "selected_scenario" not in st.session_state:
    st.session_state.selected_scenario = None
if "simulation_path" not in st.session_state:
    st.session_state.simulation_path = None

# Core runtime hooks for conversational memory and pacing matrices
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "unlocked_math_symbols" not in st.session_state:
    st.session_state.unlocked_math_symbols = []
if "hud_stage" not in st.session_state:
    st.session_state.hud_stage = "STORY_START"  # STAGES: STORY_START -> SIMULATION_ACTIVE
if "ready_for_plot" not in st.session_state:
    st.session_state.ready_for_plot = False
if "current_hyperparameters" not in st.session_state:
    st.session_state.current_hyperparameters = {}


def consult_mission_ai_chat(user_directive, current_algo, current_scenario):
    """
    Interfaces with Gemini using the modern google-genai SDK and a persistent 
    chat session to provide dynamic narrative-driven gamified orchestration.
    """
    from google import genai
    from google.genai import types

    # Safe system default structures if the pipe drops out
    fallback_response = {
        "radio_transmission": "Communication array fluctuating. Manual overrides authorized.",
        "unlock_symbols": [],
        "ready_to_simulate": False,
        "learning_rate": 0.15 if "Adam" in current_algo else 0.0015,
        "momentum_beta": 0.9,
        "exploration_noise": 0.2
    }

    # System prompt hard-coding behavioral expectations
    system_prompt = (
        "You are the immersive, sci-fi tactical Mission Guidance AI for OPTIMA_VISUALIZED, "
        "a 3D optimization simulator designed to teach complex algorithms through physical analogies.\n\n"
        f"CURRENT ENVIRONMENT: {current_scenario}\n"
        f"ACTIVE OPTIMIZER SYSTEM: {current_algo}\n\n"
        "YOUR ROLE & NARRATIVE FLOW:\n"
        "1. If the user input is 'INITIALIZE_ENVIRONMENT', paint a simple, high-stakes emergency picture. "
        "End by asking the operator a direct, simple question on how they would physically handle the landscape hurdle.\n"
        "2. If the user responds with a strategy or question, analyze it. Connect their physical idea to a mathematical symbol "
        "and unlock it. Then, IMMEDIATELY tell them what hurdle is left to solve before the system is stable. "
        "For example: 'Excellent, our torch shows us the steepness—that is the Gradient. But we are still shaking and losing speed! "
        "How can we build up smooth forward speed so we don't get stuck on flat areas?'\n"
        "3. Keep the user engaged by only asking for ONE physical fix at a time. Once they have addressed the core concepts "
        "(e.g., slope/gradient AND momentum/velocity), unlock the remaining symbols, explain the final master formula, "
        "and explicitly tell them: 'System synchronized! You are clear to hit the ENGAGE LIVE PLOT button below!' Then set 'ready_to_simulate' to true.\n\n"
        "MATH UNMASKING DESIGNATIONS:\n"
        "- For Momentum: ['w_t', 'grad_w', 'v_t', 'beta']\n"
        "- For Adam: ['m_t', 'v_t', 'm_hat', 'v_hat']\n"
        "- For Grey Wolf: ['alpha_pos', 'A', 'D', 'a_factor']\n\n"
        "STRICT COMPLIANCE STRUCTURE: You must output your reply ONLY as a valid JSON object matching this schema layout:\n"
        "{\n"
        '  "radio_transmission": "Your tactical, responsive, narrative-driven text here.",\n'
        '  "unlock_symbols": ["symbol_id_1", "symbol_id_2"],\n'
        '  "ready_to_simulate": boolean,\n'
        '  "learning_rate": float,\n'
        '  "momentum_beta": float,\n'
        '  "exploration_noise": float\n'
        "}"
    )

    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key_val = st.secrets["GOOGLE_API_KEY"]
        else:
            return fallback_response
            
        # 1. Initialize the Client inside State so it NEVER closes between page reruns
        if "ai_client" not in st.session_state or st.session_state.ai_client is None:
            st.session_state.ai_client = genai.Client(api_key=api_key_val)
            
        # 2. Initialize the Chat Session using the persistent state client
        if st.session_state.chat_session is None:
            st.session_state.chat_session = st.session_state.ai_client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json"
                )
            )
        
        message_to_send = user_directive if user_directive.strip() else "INITIALIZE_ENVIRONMENT"
        
        # 3. Fire message through the open channel
        response = st.session_state.chat_session.send_message(message_to_send)
        
        parsed_output = json.loads(response.text)
        return parsed_output
        
        message_to_send = user_directive if user_directive.strip() else "INITIALIZE_ENVIRONMENT"
        
        # Fire message through modern sync multi-turn session channels
        response = st.session_state.chat_session.send_message(message_to_send)
        
        parsed_output = json.loads(response.text)
        return parsed_output
        
    except Exception as e:
        # If any parsing errors happen, print them directly to the console for easier debug checking
        print(f"[DEBUG LOG AI EXCEPTION]: {str(e)}")
        return fallback_response


# =====================================================================
# SCREEN 1: THE INITIALIZATION DECK (WELCOME SCREEN)
# =====================================================================
if st.session_state.app_screen == "WELCOME":
    st.markdown("<h1 class='game-title'>OPTIMA_VISUALIZED</h1>", unsafe_allow_html=True)
    st.markdown("<p class='game-subtitle'>INTERACTIVE 3D LOSS LANDSCAPE EXPEDITION ENGINE</p>", unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 1.6, 1])
    with center_col:
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
            
        if st.button("INITIALIZE MISSION DESCENT"):
            st.session_state.selected_algo = algo_choice
            st.session_state.selected_scenario = scenario_choice
            st.session_state.simulation_path = None  
            st.session_state.app_screen = "HUD"
            st.session_state.hud_stage = "STORY_START"
            st.session_state.unlocked_math_symbols = []
            st.session_state.chat_session = None
            st.session_state.ready_for_plot = False
            if "mission_override_log" in st.session_state:
                del st.session_state.mission_override_log
            st.rerun()

# =====================================================================
# SCREEN 2: THE FULL-SCREEN TACTICAL HUD (IMMERSIVE MULTIMODAL MODE)
# =====================================================================
elif st.session_state.app_screen == "HUD":
    hud_cols = st.columns([3, 1])
    with hud_cols[0]:
        short_algo = st.session_state.selected_algo.split('(')[0].strip()
        short_scenario = st.session_state.selected_scenario.split('(')[0].strip()
        st.markdown(f"### 🛰️ OPTIMA_VISUALIZED // {short_algo.upper()} // {short_scenario.upper()}")
    with hud_cols[1]:
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        if st.button("← Go Back"):
            st.session_state.app_screen = "WELCOME"
            st.session_state.simulation_path = None  
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
    st.write("---")
    
    scenario = st.session_state.selected_scenario
    
    # Environment Skinning & Background Association Logic
    if "Ocean" in scenario:
        X, Y, Z = landscapes.get_trench_escape_data()
        terrain_colorscale = [[0, '#010b1a'], [0.4, '#0a2c5c'], [0.8, '#1e71cc'], [1, '#ffffff']]
        radar_line_color = "#00ffff"
        bg_image_url = get_base64_image("assets/ocean.jpg")
        mission_log = "🌌 **MISSION BRIEFING:** We are navigating a narrow deep-sea chasm. The floor is almost completely flat. Without momentum, your tracker will run out of speed and get stuck halfway through the escape trench."
        f_eval = landscapes.rosenbrock_fitness if hasattr(landscapes, 'rosenbrock_fitness') else lambda x, y: (1-x)**2 + 100*(y-x**2)**2
    elif "Cyberpunk" in scenario:
        X, Y, Z = landscapes.get_cyberpunk_matrix_data()
        terrain_colorscale = [[0, '#05010a'], [0.3, '#32045c'], [0.7, '#88069e'], [1, '#ff007f']]
        radar_line_color = "#ff007f"
        bg_image_url = get_base64_image("assets/cyberCity.jpg")
        mission_log = "⚡ **MISSION BRIEFING:** We are intercepting an encrypted corporate broadcast. The terrain drops into violent, unpredictable cliffs. Static step updates will overshoot completely; we need an adaptive learning speed."
        f_eval = landscapes.ackley_fitness if hasattr(landscapes, 'ackley_fitness') else lambda x, y: -20*np.exp(-0.2*np.sqrt(0.5*(x**2+y**2)))
    else:
        X, Y, Z = landscapes.get_desert_swarm_data()
        terrain_colorscale = [[0, '#1a0600'], [0.4, '#5c1903'], [0.8, '#c74416'], [1, '#ffa473']]
        radar_line_color = "#ff4500"
        bg_image_url = get_base64_image("assets/desert.jpg")
        mission_log = "🏜️ **MISSION BRIEFING:** A sandstorm scattered our sensor array into hundreds of identical sand dunes. Isolated trackers are highly vulnerable to localized trap dunes."
        f_eval = landscapes.rastrigin_fitness if hasattr(landscapes, 'rastrigin_fitness') else lambda x, y: x**2 + y**2 - 10*np.cos(2*np.pi*x) - 10*np.cos(2*np.pi*y) + 20

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

    fig = go.Figure(data=[go.Surface(
        z=Z, x=X, y=Y, 
        colorscale=terrain_colorscale, 
        showscale=False,
        opacity=0.8,
        contours_z=dict(show=True, usecolormap=False, highlightcolor=radar_line_color, project_z=True, color=radar_line_color)
    )])

    # --- PLOTLY TRAJECTORY ENGINE ---
    if st.session_state.simulation_path is not None:
        path_data = st.session_state.simulation_path
        
        if len(path_data.shape) == 2:  # Descents
            fig.add_trace(go.Scatter3d(
                x=[path_data[0, 0]], y=[path_data[0, 1]], z=[f_eval(path_data[0, 0], path_data[0, 1])],
                mode='lines+markers',
                marker=dict(size=6, color='#00ffcc' if "Momentum" in st.session_state.selected_algo else '#ff007f'),
                line=dict(color='#00ffcc' if "Momentum" in st.session_state.selected_algo else '#ff007f', width=5),
                name='Active Trajectory'
            ))
            
            frames = []
            slider_steps = []
            for idx in range(1, len(path_data) + 1):
                sub_path = path_data[:idx]
                frame_name = f'step_{idx}'
                
                frames.append(go.Frame(
                    data=[go.Scatter3d(
                        x=sub_path[:, 0], y=sub_path[:, 1],
                        z=[f_eval(p[0], p[1]) for p in sub_path]
                    )],
                    name=frame_name,
                    traces=[1]
                ))
                
                slider_steps.append(dict(
                    args=[[frame_name], dict(mode="immediate", transition=dict(duration=0), frame=dict(duration=0, redraw=False))],
                    label=str(idx),
                    method="animate"
                ))
                
        elif len(path_data.shape) == 3:  # Swarms
            fig.add_trace(go.Scatter3d(
                x=path_data[0, :, 0], y=path_data[0, :, 1], z=[f_eval(w[0], w[1]) for w in path_data[0]],
                mode='markers',
                marker=dict(size=6, color='#ffaa00', symbol='x'),
                name='AGWO Swarm'
            ))
            
            frames = []
            slider_steps = []
            for idx in range(len(path_data)):
                swarm_pos = path_data[idx]
                frame_name = f'step_{idx}'
                
                frames.append(go.Frame(
                    data=[go.Scatter3d(
                        x=swarm_pos[:, 0], y=swarm_pos[:, 1],
                        z=[f_eval(w[0], w[1]) for w in swarm_pos]
                    )],
                    name=frame_name,
                    traces=[1]
                ))
                
                slider_steps.append(dict(
                    args=[[frame_name], dict(mode="immediate", transition=dict(duration=0), frame=dict(duration=0, redraw=False))],
                    label=str(idx + 1),
                    method="animate"
                ))

        fig.frames = frames
        
        fig.update_layout(
            updatemenus=[dict(
                type="buttons", direction="left", x=0.05, y=-0.05, xanchor="right", yanchor="top",
                pad=dict(t=10, r=10), showactive=False,
                buttons=[
                    dict(
                        label="▶ PLAY DESCENT", method="animate",
                        args=[None, dict(frame=dict(duration=60, redraw=True), fromcurrent=True, mode="immediate", transition=dict(duration=0))]
                    ),
                    dict(
                        label="⏸ PAUSE", method="animate",
                        args=[[None], dict(frame=dict(duration=0, redraw=True), mode="immediate", transition=dict(duration=0))]
                    )
                ]
            )],
            sliders=[dict(
                active=0, currentvalue=dict(prefix="Mission Iteration Sequence: ", font=dict(color="#00ffcc", size=14)),
                pad=dict(t=5), x=0.08, y=-0.05, len=0.92, steps=slider_steps
            )]
        )
    else:
        fig.add_trace(go.Scatter3d(x=[None], y=[None], z=[None], mode='markers', showlegend=False))

    fig.update_layout(
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)", showbackground=True, title="X Axis"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)", showbackground=True, title="Y Axis"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)", showbackground=True, title="Loss"),
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, b=40, t=0), height=600, uirevision='constant_view_angle'
    )

    st.plotly_chart(fig, use_container_width=True)
    
    st.write("---")
    
    # 4. Lower multimodal workspace layout
    log_col, control_col = st.columns([1.2, 1])
    with log_col:
        st.markdown("#### 💬 Mission Guidance AI")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
        
        # Trigger initialization call if the user just spawned into the landscape
        if "mission_override_log" not in st.session_state:
            with st.spinner("Establishing secure neural link to tactical guidance satellite..."):
                ai_payload = consult_mission_ai_chat("INITIALIZE_ENVIRONMENT", st.session_state.selected_algo, st.session_state.selected_scenario)
                st.session_state.mission_override_log = ai_payload["radio_transmission"]
                st.session_state.unlocked_math_symbols = ai_payload.get("unlock_symbols", [])
                st.session_state.ready_for_plot = ai_payload.get("ready_to_simulate", False)
                st.session_state.current_hyperparameters = {
                    "lr": ai_payload.get("learning_rate", 0.01),
                    "beta": ai_payload.get("momentum_beta", 0.9),
                    "noise": ai_payload.get("exploration_noise", 0.2)
                }
                st.rerun()

        st.info(st.session_state.mission_override_log)
            
        st.write("---")
        
        # --- THE MATH UNMASKING HUD CANVAS ---
        st.markdown("#### 📐 Recovered Telemetry Formulas")
        
        unlocked = st.session_state.unlocked_math_symbols
        metric_cols = st.columns(4)
        
        if "Momentum" in st.session_state.selected_algo:
            with metric_cols[0]: st.metric("Position Vector", "$w_t$" if "w_t" in unlocked else "🔒 LOCKED")
            with metric_cols[1]: st.metric("Gradient", r"$\nabla f(w_t)$" if "grad_w" in unlocked else "🔒 LOCKED")
            with metric_cols[2]: st.metric("Velocity Force", "$v_t$" if "v_t" in unlocked else "🔒 LOCKED")
            with metric_cols[3]: st.metric("Friction Lag", r"$\beta$" if "beta" in unlocked else "🔒 LOCKED")
            
            if all(sym in unlocked for sym in ["w_t", "grad_w", "v_t", "beta"]):
                st.success("🎯 **HYPERPARAMETER SYSTEM COMPLETE: MATH SYNCHRONIZED**")
                st.latex(r"v_t = \beta v_{t-1} + \eta \nabla f(w_t)")
                st.latex(r"w_{t+1} = w_t - v_t")
                
        elif "Adam" in st.session_state.selected_algo:
            with metric_cols[0]: st.metric("1st Moment (Mean)", "$m_t$" if "m_t" in unlocked else "🔒 LOCKED")
            with metric_cols[1]: st.metric("2nd Moment (Variance)", "$v_t$" if "v_t" in unlocked else "🔒 LOCKED")
            with metric_cols[2]: st.metric("Bias Corr Mean", r"$\hat{m}_t$" if "m_hat" in unlocked else "🔒 LOCKED")
            with metric_cols[3]: st.metric("Bias Corr Var", r"$\hat{v}_t$" if "v_hat" in unlocked else "🔒 LOCKED")
            
            if all(sym in unlocked for sym in ["m_t", "v_t", "m_hat", "v_hat"]):
                st.success("🎯 **HYPERPARAMETER SYSTEM COMPLETE: MATH SYNCHRONIZED**")
                st.latex(r"w_{t+1} = w_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t")
                
        elif "Grey Wolf" in st.session_state.selected_algo:
            with metric_cols[0]: st.metric("Alpha Leader Vector", r"$\vec{X}_\alpha$" if "alpha_pos" in unlocked else "🔒 LOCKED")
            with metric_cols[1]: st.metric("Encircle Step", r"$\vec{A}$" if "A" in unlocked else "🔒 LOCKED")
            with metric_cols[2]: st.metric("Distance Variance", r"$\vec{D}$" if "D" in unlocked else "🔒 LOCKED")
            with metric_cols[3]: st.metric("Convergence Factor", "$a$" if "a_factor" in unlocked else "🔒 LOCKED")
            
            if all(sym in unlocked for sym in ["alpha_pos", "A", "D", "a_factor"]):
                st.success("🎯 **HYPERPARAMETER SYSTEM COMPLETE: MATH SYNCHRONIZED**")
                st.latex(r"\vec{D} = |\vec{C} \cdot \vec{X}_{\text{leader}} - \vec{X}|")
                st.latex(r"\vec{X}_{(t+1)} = \frac{\vec{X}_1 + \vec{X}_2 + \vec{X}_3}{3}")


    with control_col:
        st.markdown("#### 🛰️ Command Terminal")
        
        if st.session_state.hud_stage == "STORY_START":
            st.markdown("💡 *Communicate with your Mission AI. Ask clarifying questions or propose your physical strategies.*")
            
            user_input = st.text_input(
                "Transmit strategy or inquiry query package:", 
                placeholder="Type your strategic ideas or concept questions here...",
                key="terminal_text_input"
            )
            
            st.caption("🎙️ Voice link hardware layer placeholder overrides:")
            st.button("🔴 TAP TO TRANSMIT VOICE OVERRIDE", key="voice_override_btn")
            st.write("\n")
            
            if st.button("🚀 TRANSMIT COMMUNICATIONS SIGNAL", key="submit_directive_btn"):
                if not user_input.strip():
                    st.warning("Please type a question or strategy update string before broadcasting.")
                else:
                    with st.spinner("Decoding telemetry payload..."):
                        ai_payload = consult_mission_ai_chat(user_input, st.session_state.selected_algo, st.session_state.selected_scenario)
                        
                        st.session_state.mission_override_log = ai_payload["radio_transmission"]
                        new_symbols = ai_payload.get("unlock_symbols", [])
                        st.session_state.unlocked_math_symbols = list(set(st.session_state.unlocked_math_symbols + new_symbols))
                        
                        # Dynamically bind status flag and hyperparameters passed back from Gemini
                        st.session_state.ready_for_plot = ai_payload.get("ready_to_simulate", False)
                        st.session_state.current_hyperparameters = {
                            "lr": ai_payload.get("learning_rate", 0.01),
                            "beta": ai_payload.get("momentum_beta", 0.9),
                            "noise": ai_payload.get("exploration_noise", 0.2)
                        }
                        st.rerun()
            
            # Show the unlock button conditionally if Gemini flipped the boolean gate to true
            if st.session_state.ready_for_plot:
                st.success("🎯 **PROPULSION MATRICES ALIGNED:** Conceptual bridge confirmed by AI.")
                if st.button("🔥 UNLOCK & ENGAGE LIVESTREAM TRAJECTORY SIMULATION", key="transition_stage_btn"):
                    st.session_state.hud_stage = "SIMULATION_ACTIVE"
                    st.rerun()

        elif st.session_state.hud_stage == "SIMULATION_ACTIVE":
            st.success("🛰️ **PROPULSION STAGE RUNNING:** Plotly tracking arrays calculating physics updates.")
            
            # Check if simulation path needs initial processing computation run
            if st.session_state.simulation_path is None:
                import optimizers
                start_x, start_y = 2.0, 2.0
                params = st.session_state.current_hyperparameters
                
                if "Ocean" in scenario:
                    raw_grad = landscapes.rosenbrock_gradient if hasattr(landscapes, 'rosenbrock_gradient') else lambda x, y: (2*(x-1) - 400*x*(y-x**2), 200*(y-x**2))
                    grad_func = lambda x, y: tuple(np.clip(raw_grad(x, y), -50.0, 50.0))
                elif "Cyberpunk" in scenario:
                    raw_grad = landscapes.ackley_gradient if hasattr(landscapes, 'ackley_gradient') else lambda x, y: (x*0.1, y*0.1)
                    grad_func = lambda x, y: tuple(np.clip(raw_grad(x, y), -50.0, 50.0))
                else:
                    raw_grad = landscapes.rastrigin_gradient if hasattr(landscapes, 'rastrigin_gradient') else lambda x, y: (2*x + 20*np.pi*np.sin(2*np.pi*x), 2*y + 20*np.pi*np.sin(2*np.pi*y))
                    grad_func = lambda x, y: tuple(np.clip(raw_grad(x, y), -50.0, 50.0))

                if "Momentum" in st.session_state.selected_algo:
                    st.session_state.simulation_path = optimizers.simulate_momentum(
                        start_x, start_y, grad_func, steps=40, lr=params["lr"], beta=params["beta"]
                    )
                elif "Adam" in st.session_state.selected_algo:
                    st.session_state.simulation_path = optimizers.simulate_adam(
                        start_x, start_y, grad_func, steps=40, lr=params["lr"], beta1=params["beta"]
                    )
                elif "Grey Wolf" in st.session_state.selected_algo:
                    st.session_state.simulation_path = np.array(optimizers.simulate_agwo(
                        start_x, start_y, f_eval, steps=35, num_wolves=10
                    ))
                st.rerun()

            live_tweak = st.text_input("Send mid-flight steering optimization directive:", placeholder="e.g., We are bouncing too much, stabilize!")
            if st.button("⚡ TRANSMIT STEERING OVERRIDE", key="live_tweak_btn"):
                with st.spinner("Processing corrective adjustments mid-flight..."):
                    ai_payload = consult_mission_ai_chat(f"MID_FLIGHT_ADJUSTMENT: {live_tweak}", st.session_state.selected_algo, st.session_state.selected_scenario)
                    st.session_state.mission_override_log = ai_payload["radio_transmission"]
                    st.session_state.current_hyperparameters = {
                        "lr": ai_payload.get("learning_rate", 0.01),
                        "beta": ai_payload.get("momentum_beta", 0.9),
                        "noise": ai_payload.get("exploration_noise", 0.2)
                    }
                    # Clear path data to force recomputation on next cycle step run
                    st.session_state.simulation_path = None
                    st.rerun()
                
            st.write("---")
            if st.button("🔄 Reset Mission Scenario & Clear Memory", key="reset_mission_btn"):
                st.session_state.hud_stage = "STORY_START"
                st.session_state.unlocked_math_symbols = []
                st.session_state.chat_session = None
                st.session_state.ai_client = None # Reset client channel here
                st.session_state.ready_for_plot = False
                if "mission_override_log" in st.session_state:
                    del st.session_state.mission_override_log
                if "simulation_path" in st.session_state:
                    st.session_state.simulation_path = None
                st.rerun()