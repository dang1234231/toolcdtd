import streamlit as st
from collections import defaultdict

CHARACTERS = [
    "Bậc Thầy Tấn Công",
    "Quyền Sát",
    "Thợ Lặn Sâu",
    "Cơn Lốc Sân Cỏ",
    "Hiệp Sĩ Phi Nhanh",
    "Vua Home Run"
]

def get_chain_lengths(history):
    chains = defaultdict(int)
    if not history:
        return chains
    current = history[0]
    count = 1
    for i in range(1, len(history)):
        if history[i] == current:
            count += 1
        else:
            chains[current] = max(chains[current], count)
            current = history[i]
            count = 1
    chains[current] = max(chains[current], count)
    return chains

def detect_recent_winners(recent_winners, how_many=3):
    return set(recent_winners[-how_many:])

def detect_top_winners(win_stats):
    if not win_stats:
        return set()
    max_win = max(win_stats.values())
    return {char for char, win in win_stats.items() if win == max_win}

def analyze_characters(recent_winners, win_stats):
    chains = get_chain_lengths(recent_winners)
    recent_set = detect_recent_winners(recent_winners, 3)
    top_winners = detect_top_winners(win_stats)

    exclude = set()
    reasons_dict = {}
    for char in CHARACTERS:
        reasons = []
        if char in recent_set:
            reasons.append("vừa thắng gần đây")
        if chains.get(char, 0) >= 2:
            reasons.append(f"đang chuỗi thắng {chains[char]}")
        if char in top_winners:
            reasons.append("thắng nhiều nhất")
        if reasons:
            exclude.add(char)
            reasons_dict[char] = reasons

    possible_choices = [char for char in CHARACTERS if char not in exclude]
    return possible_choices, reasons_dict

def recalculate_win_stats(recent_winners):
    stats = defaultdict(int)
    for name in recent_winners:
        stats[name] += 1
    return stats

# --- Giao diện chính ---
st.set_page_config(page_title="Dự Đoán Không Phải Quán Quân", layout="centered")
st.title("🏆 Tool Dự Đoán: Ai Không Phải Là Quán Quân")

st.header("📝 Nhập 10 nhân vật thắng gần nhất:")
recent_winners = []
for i in range(10):
    val = st.selectbox(f"Ván {i+1}", CHARACTERS, key=f"recent_{i}")
    recent_winners.append(val)

st.header("📊 Nhập số lần thắng trong 100 ván gần nhất:")
stats_100 = {}
for char in CHARACTERS:
    stats_100[char] = st.number_input(f"{char}", min_value=0, max_value=100, step=1)

total = sum(stats_100.values())
if total != 100:
    st.error(f"❌ Tổng số ván phải là 100! Hiện tại là {total}.")
else:
    full_history = []
    for name in CHARACTERS:
        full_history.extend([name] * stats_100[name])
    win_stats = recalculate_win_stats(full_history)
    possible, reasons = analyze_characters(recent_winners, win_stats)

    st.success("✅ Nhân vật CÓ THỂ CHỌN (ít khả năng thắng):")
    if possible:
        for char in possible:
            st.write(f" - {char}")
    else:
        st.warning("⚠️ Không còn ai để chọn. Tất cả đều là quán quân gần đây.")

    st.subheader("🔍 Nhân vật bị loại trừ vì:")
    for char, reason in reasons.items():
        st.write(f" - {char}: {', '.join(reason)}")

    st.subheader("📈 Các nhân vật thắng dưới 5 lần trong 100 ván gần nhất:")
    for char in CHARACTERS:
        count = win_stats.get(char, 0)
        if count < 5:
            st.write(f" - {char} ({count} lần thắng)")
