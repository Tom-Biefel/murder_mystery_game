import streamlit as st
from mysterium.game import Game
from mysterium.utils import validate_name

st.set_page_config(page_title="Mysterium", page_icon="🔍", layout="centered")

if "game" not in st.session_state:
    st.session_state.game    = None
if "log" not in st.session_state:
    st.session_state.log     = []
if "started" not in st.session_state:
    st.session_state.started = False

def log(msg):
    st.session_state.log.append(msg)

if not st.session_state.started:
    st.title("🔍 Mysterium")
    st.subheader("A murder has occurred at Blackwood Manor.")
    st.write("You are the detective. Explore 9 rooms, collect clues, and solve the case.")
    st.divider()
    name = st.text_input("Your detective name:", placeholder="e.g. Maria")
    difficulty = st.selectbox("Difficulty:", ["easy", "medium", "hard"])
    if st.button("Start Investigation", type="primary"):
        if not name.strip():
            st.error("Please enter your name.")
        else:
            try:
                validate_name(name)
                st.session_state.game    = Game(player_name=name, difficulty=difficulty)
                st.session_state.started = True
                st.session_state.log     = [f"🕵️ {name} begins the investigation..."]
                st.rerun()
            except ValueError as e:
                st.error(str(e))
else:
    game   = st.session_state.game
    player = game.player

    st.title("🔍 Mysterium")
    col1, col2, col3 = st.columns(3)
    col1.metric("Detective",   player.name)
    col2.metric("Room",        player.current_room)
    col3.metric("Clues Found", player.total_clues_found)
    st.divider()

    if game.game_over:
        st.success("🎉 Case closed! Well done, detective.")
        if st.button("Play again"):
            st.session_state.started = False
            st.session_state.game    = None
            st.session_state.log     = []
            st.rerun()
        st.stop()

    left, right = st.columns([1, 1])

    with left:
        st.subheader("🚶 Move")
        exits = game.rooms[player.current_room].neighbours
        chosen_room = st.selectbox("Go to:", exits, key="move_select")
        if st.button("Move", key="move_btn"):
            success = game.move(chosen_room)
            log(f"➡️  Moved to **{chosen_room}**" if success else f"❌ Cannot reach {chosen_room}")
            st.rerun()

        st.divider()

        st.subheader("🔎 Search Room")
        if st.button("Search this room", key="search_btn"):
            found = game.search()
            if found:
                for clue in found:
                    log(f"🔍 Found: *{clue.description}* → **{clue.points_to}**")
            else:
                log(f"💤 Nothing new in the {player.current_room}.")
            st.rerun()

    with right:
        st.subheader("📋 Evidence Board")
        evidence = player.evidence_summary()
        if evidence:
            for name_ev, score in sorted(evidence.items(), key=lambda x: x[1], reverse=True):
                st.progress(int(score), text=f"{name_ev}: {score}%")
        else:
            st.caption("No evidence collected yet.")

        st.divider()

        st.subheader("⚖️ Make Accusation")
        from mysterium.models.suspect import ALL_SUSPECTS
        from mysterium.models.weapon  import ALL_WEAPONS
        suspects = [s.name for s in ALL_SUSPECTS]
        weapons  = [w.name for w in ALL_WEAPONS]
        rooms    = list(game.rooms.keys())
        acc_suspect = st.selectbox("Suspect:", suspects, key="acc_s")
        acc_weapon  = st.selectbox("Weapon:",  weapons,  key="acc_w")
        acc_room    = st.selectbox("Room:",    rooms,    key="acc_r")
        if st.button("🔴 Accuse!", type="primary", key="accuse_btn"):
            result = game.accuse(acc_suspect, acc_weapon, acc_room)
            log(f"✅ {result['message']}" if result["correct"] else f"❌ {result['message']}")
            st.rerun()

    st.divider()
    st.subheader("📜 Investigation Log")
    for entry in reversed(st.session_state.log):
        st.markdown(entry)
