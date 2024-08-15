import streamlit as st
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(
    page_icon='🎳',
    page_title='Nobody is Perfect',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Load the board image
board_image = Image.open("nobody.jpg")

# Convert image to base64 to embed it in HTML
buffered = BytesIO()
board_image.save(buffered, format="JPEG")  # Use "PNG" if your image is in PNG format
img_str = base64.b64encode(buffered.getvalue()).decode()

# Coordinates for each field (example values, you'll need to adjust these)
field_coordinates = [
    (19, 8), (12, 17), (11, 24.5), (8, 32), (9, 39), (7, 46), (9, 53), (8, 60.5), (8, 67.5), (9, 74), (9.5, 81.5),
    (12, 89),  # Top row
    (23, 91), (33.5, 89.5), (44, 90.5), (54, 90), (64, 91.5), (76, 94),  # Right column
    (86, 91.5), (89, 84.5), (87.5, 77.5), (89.5, 70), (88, 63), (91, 55.5), (89, 48.5), (90, 41.5), (88, 34), (87.5, 27),
    (88, 20.5), (87, 12.5), (86, 5),  # Bottom row
    (75, 4), (65, 5), (55, 6), (44, 4.5), (34, 5.5),  # Left column
]

# Function to reset player positions
def reset_positions():
    for i in range(num_players):
        st.session_state[f'marker_position_{i}'] = 0  # Reset markers to the first field

# Sidebar for player settings
with st.sidebar:
    st.title("Game Settings")
    num_players = st.selectbox("Number of Players", range(2, 9), index=5)
    st.divider()

    emoji_options = [
        # Blue
        "🔵",  # Blue Circle
        "🐟",  # Fish
        "💧",  # Droplet

        # Orange
        "🟠",  # Orange Circle
        "🐅",  # Tiger
        "🎃",  # Jack-O-Lantern

        # Green
        "🟢",  # Green Circle
        "🐢",  # Turtle
        "🍀",  # Four Leaf Clover

        # White
        "⚪",  # White Circle
        "🐇",  # Rabbit
        "❄️",  # Snowflake

        # Pink (assuming it refers to light pink)
        "💗",  # Pink Heart
        "🐷",  # Pig
        "🌸",  # Cherry Blossom

        # Turquoise (assuming this is meant to be aqua)
        "🩵",  # Light Blue Heart
        "🐬",  # Dolphin
        "💎",  # Gem Stone

        # Rosa (assuming it refers to rose or deep pink)
        "💖",  # Sparkling Heart
        "🦩",  # Flamingo
        "🌹",  # Rose

        # Yellow
        "🟡",  # Yellow Circle
        "🐥",  # Chick
        "🌟",  # Star

        # Red
        "🔴",  # Red Circle
        "🦊",  # Fox
        "🍎",  # Apple

        # Black
        "⚫",  # Black Circle
        "🐈‍⬛",  # Black Cat
        "🖤",  # Black Heart

        # Lila (assuming this is purple)
        "🟣",  # Purple Circle
        "🐙",  # Octopus
        "🍇",  # Grapes

        # Original emojis added back to the list
        "🚀", "🎈", "🔥", "🎯", "🎲", "🏀", "⚽", "🎸"
    ]
    player_emojis = []
    for i in range(num_players):
        emoji = st.selectbox(f"Player {i + 1} Icon", emoji_options, key=f"player_emoji_{i}")
        player_emojis.append(emoji)
    st.divider()

    icon_size = st.slider("Icon Size (px)", min_value=10, max_value=100, value=30)
    st.divider()

    # Slider to adjust the size of the right column
    col2_width_ratio = st.slider("Right Column Width Ratio", min_value=1, max_value=12, value=1)
    col1_width_ratio = 13 - col2_width_ratio  # Ensuring the total ratio sums to 6

    # Add reset button
    if st.button("Reset Player Positions"):
        reset_positions()
        st.experimental_rerun()

# Initialize session state for marker positions
for i in range(num_players):
    if f'marker_position_{i}' not in st.session_state:
        st.session_state[f'marker_position_{i}'] = 0  # Start with markers for the players at the first field

# Function to move marker to the next field
def move_marker(player_index, steps):
    st.session_state[f'marker_position_{player_index}'] = (st.session_state[f'marker_position_{player_index}'] + steps) % len(field_coordinates)

# Create a layout with two columns: one for the image and one for the move panels
col1, col2 = st.columns([col1_width_ratio, col2_width_ratio])

with col1:
    # Generate HTML for overlays
    overlays_html = ""
    field_occupancy = {i: [] for i in range(len(field_coordinates))}

    # Track which players are on which fields
    for i in range(num_players):
        position = st.session_state[f'marker_position_{i}']
        field_occupancy[position].append(i)

    # Create HTML for each field with players
    for position, players in field_occupancy.items():
        top, left = field_coordinates[position]
        for offset, player_index in enumerate(players):
            row = offset // 3  # Number of players per row
            col = offset % 3   # Number of players per column
            top_offset = top + row * 3  # Adjust the multiplier for more spacing if needed
            left_offset = left + col * 2  # Adjust the multiplier for more spacing if needed
            overlays_html += f'<div class="overlay" style="top: {top_offset}%; left: {left_offset}%;"><b style="font-size:{icon_size}px;">{player_emojis[player_index]}</b></div>'

    # Display the board image with HTML overlays
    st.markdown(
        f"""
        <style>
        .board-container {{
            position: relative;
            text-align: center;
        }}
        .board-image {{
            width: 100%;
            height: auto;
        }}
        .overlay {{
            position: absolute;
            transform: translate(-50%, -50%);
        }}
        </style>
        <div class="board-container">
            <img src="data:image/jpeg;base64,{img_str}" class="board-image"/>
            {overlays_html}
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    # Display columns for the players
    for i in range(num_players):
        subcol1, subcol2 = col2.columns([3,1])
        player = f"{i + 1}: {player_emojis[i]}"
        # subcol1.markdown(f"<div style='text-align: center;'><b>{i + 1}: {player_emojis[i]}</b></div>", unsafe_allow_html=True)

        # steps_forward = subcol2.number_input('steps forward', min_value=-10, max_value=10, value=1, key=f'forward_{i}', label_visibility="hidden")
        steps_forward = subcol1.number_input(player, min_value=-10, max_value=10, value=1, key=f'forward_{i}')
        if subcol2.button(f'Move', key=f'move_forward_{i}', help=None):
            move_marker(i, steps_forward)
            st.experimental_rerun()

        # st.markdown(
        #     f"""
        #     <style>
        #     div[data-testid="stButton"] > button {{
        #         display: block;
        #         margin: 0 auto;
        #     }}
        #     </style>
        #     """,
        #     unsafe_allow_html=True
        # )