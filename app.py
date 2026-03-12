import streamlit as st
from mysterium.game import Game
from mysterium.models.suspect import all_suspects
from mysterium.models.weapon import all_weapons
from mysterium.models.room import all_rooms

# Page setup
st.set_page_config(page_title="Blackwood Manor", page_icon="🕯️", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: #1a1a2e; }
[data-testid="stSidebar"] * { color: #e0d7c6 !important; }
h1, h2, h3 { color: #c9a84c; }
</style>
""", unsafe_allow_html=True)

suspects = [s.name() for s in all_suspects]
weapons = [w.name() for w in all_weapons]
rooms = [r.name for r in all_rooms]


# Small helper functions
def init_state():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "game" not in st.session_state:
        st.session_state.game = None
    if "clue_log" not in st.session_state:
        st.session_state.clue_log = []
    if "message" not in st.session_state:
        st.session_state.message = ""
    if "result" not in st.session_state:
        st.session_state.result = None


def start_new_game(name: str, difficulty: str):
    st.session_state.game = Game(name, difficulty)
    st.session_state.clue_log = []
    st.session_state.message = ""
    st.session_state.result = None
    st.session_state.started = True
    st.session_state["notes"] = ""


def log_found_clues(found_descriptions, current_room):
    """Add newly found clue descriptions to the log (simple version)."""
    for desc in found_descriptions:
        st.session_state.clue_log.append({"room": current_room, "description": desc})


init_state()


# Start screen
if not st.session_state.started:
    st.title("🕯️ Blackwood Manor")
    st.caption("A murder mystery. Search rooms, collect clues, and make an accusation.")

    name = st.text_input("Detective name")
    difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], index=1)

    if st.button("Begin Investigation"):
        if not name.strip():
            st.warning("Please enter a name.")
        else:
            try:
                start_new_game(name.strip(), difficulty)
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    st.stop()


# Result screen
if st.session_state.result:
    st.title("🕯️ Blackwood Manor")
    if st.session_state.result["correct"]:
        st.success(st.session_state.result["message"])
    else:
        st.error(st.session_state.result["message"])

    if st.button("Play again"):
        st.session_state.started = False
        st.rerun()

    st.stop()


# Main game screen
game: Game = st.session_state.game
status = game.status()
current_room = status["room"]
room_obj = game.rooms[current_room]

st.title("🕯️ Blackwood Manor")

if st.session_state.message:
    st.info(st.session_state.message)

# Sidebar
with st.sidebar:
    st.header("📓 Detective Notebook")

    st.caption(f"Detective: {status['player']}")
    st.metric("Clues found", status['clues_found'])

    if status["move_history"]:
        history = [str(r[0]) if isinstance(r, tuple) else str(r) for r in status["move_history"][-5:]]
        st.caption("🗺️ " + " → ".join(history))

    st.markdown("---")

    # Notebook text area
    notes = st.text_area(
        "Your Notes",
        value=st.session_state.get("notes", ""),
        height=300,
        placeholder="Write your notes here..."
    )

    st.session_state["notes"] = notes

    st.markdown("---")

    if st.button("New game"):
        st.session_state.game = None
        st.session_state.started = False
        st.session_state.notes = ""
        st.session_state.clue_log = []
        st.rerun()

# Layout
col_evidence, col_room, col_accuse = st.columns([2, 2, 1.3])

# Evidence log
with col_evidence:
    st.subheader("Evidence Log")
    with st.container(border=True):
        if st.session_state.clue_log:
            for entry in reversed(st.session_state.clue_log):
                st.write(f"📍 **{entry['room']}**: {entry['description']}")
        else:
            st.caption("No clues yet. Search a room!")

# Room + movement
with col_room:
    st.subheader("Current Location")
    with st.container(border=True):
        st.write(f"### {current_room}")
        st.caption(room_obj.description)

    if not room_obj.clues:
        st.caption("✓ This room has been fully searched.")

    if st.button("Search room"):
        found = game.search()
        if found:
            log_found_clues(found, current_room)
            st.session_state.message = "You found something!"
        else:
            st.session_state.message = "Nothing more to find here."
        st.rerun()

    st.markdown("**Move to:**")
    for nb in room_obj.neighbours:
        if st.button(nb, key=f"move_{nb}"):
            ok = game.move(nb)
            st.session_state.message = f"You moved to the {nb}." if ok else "You can't go there from here."
            st.rerun()

    if hasattr(room_obj, "leads_to"):
        if st.button(f"Use secret passage → {room_obj.leads_to}"):
            dest = game.use_passage()
            st.session_state.message = f"You slip into the {dest}."
            st.rerun()

# Accusation
with col_accuse:
    with st.expander("⚖️ Make Accusation"):
        suspect_choice = st.selectbox("Suspect", suspects)
        weapon_choice = st.selectbox("Weapon", weapons)
        room_choice = st.selectbox("Room", rooms)

        if st.button("Accuse"):
            st.session_state.result = game.accuse(suspect_choice, weapon_choice, room_choice)
            st.rerun()
