
import streamlit as st
ss = st.session_state
from flightplotting import plotsec
import plotly.express as px

def write():
    manid = st.slider("select manoeuvre", 1, 17, 1)
    man = ss.intended[manid-1]


    aligned = man.get_data(ss.aligned)
    intended = man.get_data(ss.template)
    corrected = man.get_data(ss.corrected_template)

    results =  ss.definition[man.uid].mps.collect(man)

    intra_results = man.analyse(aligned,intended)

    interdg=results.downgrade()
    intradg = intra_results.downgrade()

    score = 10 - interdg - intradg

    st.write(f"downgrades: - {intra_results.downgrade_list()} (intra) - {interdg} (inter)")
    st.title(f"{man.uid}: {score}")


    st.plotly_chart(plotsec(aligned, nmodels=10, scale=5), use_container_width=True)

    with st.expander("Inter Element Downgrades"):
        st.dataframe(results.downgrade_df())

    with st.expander("Intra Element Downgrades"):

        elid = st.slider("select element", 1, len(man.elements.data), 1)
        el=man.elements[elid-1]

        st.write(f"Downgrades for element {el.uid}, {el.describe()}")

        flown = el.get_data(aligned)
        template = el.get_data(intended).relocate(flown.pos[0])
        flown_lc =  el.setup_analysis_state(flown, template)
        template_lc =  el.setup_analysis_state(template, template)

        fig = plotsec(flown_lc, nmodels=5, scale=2, color="red")
        fig = plotsec(template_lc, nmodels=5, scale=2, color="blue", fig=fig)
        st.plotly_chart(fig)

        mdf = el.intra_scoring.measuredf(el, flown_lc, template_lc)
        #res = el.intra_scoring.dgs(mdf)
        col = st.selectbox("plot criteria", mdf.columns)
        fig = px.scatter(mdf, y=col, width=600, height=300)
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(intra_results[el.uid].results.downgrade_df())