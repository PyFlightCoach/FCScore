import streamlit as st 
ss = st.session_state

from flightplotting import plotdtw


def write():

    manid = st.slider("select manoeuvre", 1, 17, 1)
    man = ss.p23[manid-1]
    st.write(man.uid)
    fig=plotdtw(man.get_data(ss.aligned), man.all_elements.to_list())
    st.plotly_chart(fig, use_container_width=True)

    if st.button("Confirm Aligment"):
        ss.stage+=1
        st.experimental_rerun()