import random,time,streamlit as st
from questions import QUESTIONS
st.set_page_config(page_title="Sonic Search | AI Mission Sessions",page_icon="🎧",layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
.stApp{background:radial-gradient(ellipse at 15% 0%,#282043 0%,#0b0b13 45%,#090a10 100%);color:#f6f4ff;font-family:'Space Grotesk',sans-serif}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#171625,#101018);border-right:1px solid #302b46}
.block-container{max-width:1150px;padding-top:2rem}
.hero{padding:28px;border-radius:22px;border:1px solid #4c3c6c;background:linear-gradient(120deg,#ff4fa320,#4deeea12),#151522;box-shadow:0 0 35px #a78bfa14}
.kicker{font-family:'Space Mono',monospace;color:#4deeea;font-size:12px;letter-spacing:.16em}
.mission{background:linear-gradient(135deg,#191827,#11111b);border:1px solid #38314c;border-radius:18px;padding:18px;min-height:155px}
div.stButton>button{border-radius:12px;border:1px solid #5c4c79;min-height:43px;font-weight:700;background:#211d32;color:#f6f4ff}
div.stButton>button[kind="primary"]{background:linear-gradient(90deg,#ff4fa3,#a78bfa);color:#100b18;border:0}
div[data-testid="stProgressBar"]>div>div{background:linear-gradient(90deg,#ff4fa3,#4deeea)}
hr{border-color:#302b46}
</style>""",unsafe_allow_html=True)
defaults={"home":True,"quiz":[],"index":0,"answers":{},"hints":set(),"finished":False,"score":0,"player":"PLAYER","start":0}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k]=v
def launch(mode,player,focus,difficulty):
    pool=[q.copy() for q in QUESTIONS if q.get("difficulty")==difficulty and (not focus or q["topic"] in focus)]; random.shuffle(pool)
    st.session_state.quiz=pool[:10] if mode=="10-track sprint" else pool
    st.session_state.index=0; st.session_state.answers={}; st.session_state.hints=set()
    st.session_state.finished=False; st.session_state.home=False
    st.session_state.player=player.strip() or "PLAYER"; st.session_state.start=time.time()
with st.sidebar:
    st.markdown("## 🎧 SONIC // AI")
    st.caption("MISSION CONTROL · DSC401-6")
    st.markdown("---")
    st.markdown("### 🎚️ Operator profile")
    st.write(st.session_state.player if not st.session_state.home else "Awaiting operator")
    st.metric("Latest score",st.session_state.score)
    st.progress(min(st.session_state.score/50,1))
    st.markdown("---")
    st.markdown("### 📡 Objective")
    st.write("Navigate AI foundations, agent design, problem formulation and search.")
    st.info("Read the scenario. Choose a move. Learn from the debrief.")
    st.markdown("---")
    st.caption("OPTIONAL SOUNDTRACK")
    audio=st.file_uploader("Upload MP3/WAV",type=["mp3","wav"])
    if audio: st.audio(audio,loop=True)
st.markdown('<div class="hero"><div class="kicker">DSC401-6 · ARTIFICIAL INTELLIGENCE · UNITS I & II</div><h1 style="font-size:3rem;margin:0">🎧 SONIC SEARCH</h1><h3 style="color:#ff4fa3;margin-top:.2rem">The AI Mission Sessions</h3><p>Every state is a stage. Every decision changes the route. Clear the set.</p></div>',unsafe_allow_html=True)
st.write("")
if st.session_state.home:
    st.markdown("## 🛰️ Mission briefing")
    st.write("You are the search operator for a live AI system. Identify the right agent, read the environment, and route through search problems without confusing a good-looking path with the best one.")
    a,b,c=st.columns(3)
    with a: st.markdown('<div class="mission"><div class="kicker">01 / WARM-UP</div><h3>🎛️ Signal Check</h3><p>AI foundations, rationality, sensors and percepts.</p></div>',unsafe_allow_html=True)
    with b: st.markdown('<div class="mission"><div class="kicker">02 / SYSTEMS</div><h3>🥁 Agent Architecture</h3><p>Agent types, performance measures and environments.</p></div>',unsafe_allow_html=True)
    with c: st.markdown('<div class="mission"><div class="kicker">03 / HEADLINER</div><h3>🎹 Search Stage</h3><p>Problem formulation, BFS, DFS, UCS, heuristics and A*.</p></div>',unsafe_allow_html=True)
    st.markdown("---"); st.markdown("### 🎚️ Configure your set")
    player=st.text_input("Operator callsign",value="PLAYER")
    mode=st.radio("Mission type",["10-track sprint","Full album · all questions"],horizontal=True)
    difficulty=st.radio("Choose difficulty",["Easy","Medium","Hard"],horizontal=True,
                        format_func=lambda x: {"Easy":"🟢 Easy · Sound Check","Medium":"🟡 Medium · Studio Session","Hard":"🔴 Hard · Headliner Challenge"}[x])
    focus=st.multiselect("Focus topics (optional)",sorted(set(q["topic"] for q in QUESTIONS)))
    st.caption(f"Each difficulty has its own 50-question bank. Selected: {difficulty}. Questions are randomized at launch.")
    if st.button("🚀 Launch mission",type="primary",use_container_width=True):
        launch(mode,player,focus,difficulty); st.rerun()
    st.markdown("---")
    st.markdown("**Coverage:** AI approaches and applications · agents and environments · rationality · problem formulation · state spaces · uninformed/informed search · BFS/DFS/UCS · heuristics · greedy search · A* · means–ends analysis.")
elif st.session_state.finished:
    quiz=st.session_state.quiz
    score=0
    for q in quiz:
        answer=st.session_state.answers.get(q["id"])
        if q["type"]=="fill":
            score += int(str(answer or "").strip().lower()==q["answer_text"].lower())
        else:
            score += int(answer==q["answer"])
    pct=round(score/len(quiz)*100) if quiz else 0; st.session_state.score=score
    st.markdown("## 🏁 Mission debrief")
    st.markdown(f"### Good run, {st.session_state.player}. Here's your final mix.")
    a,b,c=st.columns(3); a.metric("Score",f"{score}/{len(quiz)}"); b.metric("Accuracy",f"{pct}%")
    elapsed=int(time.time()-st.session_state.start); c.metric("Run time",f"{elapsed//60}m {elapsed%60}s")
    st.progress(pct/100)
    st.success("HEADLINER CLEAR — strong conceptual control." if pct>=80 else "SOLID SET — review missed tracks." if pct>=60 else "REHEARSAL MODE — review each debrief and replay.")
    st.markdown("### 🔍 Track-by-track review")
    for q in quiz:
        ans=st.session_state.answers.get(q["id"]); correct=ans==q.get("answer") if q["type"]!="fill" else str(ans).strip().lower()==q["answer_text"].lower()
        right=q.get("answer_text") if q["type"]=="fill" else q["options"][q["answer"]]
        with st.expander(f"{'🟢' if correct else '🔴'} Track {q['id']} · {q['topic']}"):
            st.write(q["q"]); st.write("**Your response:**",ans if ans is not None else "Skipped")
            st.write("**Expected response:**",right); st.write("**Debrief:**",q["explanation"])
    if st.button("↻ Run another mission",type="primary",use_container_width=True):
        st.session_state.home=True; st.session_state.quiz=[]; st.session_state.finished=False; st.rerun()
else:
    quiz=st.session_state.quiz; i=st.session_state.index; q=quiz[i]
    st.progress((i+1)/len(quiz)); a,b,c=st.columns(3)
    a.caption(f"TRACK {i+1:02d}/{len(quiz):02d}"); b.caption("SECTOR · "+q["topic"].upper()); c.caption("LEVEL · "+q["difficulty"].upper())
    st.markdown("---"); st.markdown("## "+q["q"])
    if q["type"]=="fill":
        choice=st.text_input("Type your response",value=str(st.session_state.answers.get(q["id"],"")),key=f"fill_{q['id']}")
    else:
        opts=q["options"]; labels=[f"{chr(65+j)} · {v}" for j,v in enumerate(opts)]
        prev=st.session_state.answers.get(q["id"])
        choice=st.radio("Choose your response",range(len(opts)),format_func=lambda j:labels[j],index=prev if isinstance(prev,int) else None,key=f"pick_{q['id']}")
    if st.button("💡 Reveal hint"): st.session_state.hints.add(q["id"])
    if q["id"] in st.session_state.hints: st.info("HINT // "+q["hint"])
    if st.button("🎚️ Lock in answer",type="primary",use_container_width=True):
        st.session_state.answers[q["id"]]=choice
        correct=choice==q.get("answer") if q["type"]!="fill" else str(choice).strip().lower()==q["answer_text"].lower()
        expected=q.get("answer_text") if q["type"]=="fill" else q["options"][q["answer"]]
        if correct: st.success("ON BEAT ✓ "+q["explanation"])
        else: st.error("OFF BEAT — expected: "+expected); st.info(q["explanation"])
    st.markdown("---"); left,right=st.columns(2)
    with left:
        if st.button("← Previous track",disabled=i==0,use_container_width=True): st.session_state.index-=1; st.rerun()
    with right:
        if st.button("🏁 End session" if i==len(quiz)-1 else "Next track →",type="primary",use_container_width=True):
            if i==len(quiz)-1: st.session_state.finished=True
            else: st.session_state.index+=1
            st.rerun()
