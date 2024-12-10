import streamlit as st
from headloop.designer import design
from Bio.SeqRecord import SeqRecord

st.set_page_config(
    page_title="Headloop Primer Designer",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Headloop Primer Designer")

st.markdown("""
This tool helps design headloop primers for suppression PCR to suppress amplification of a known haplotype.
Please provide the following information:
""")

# Input fields
col1, col2 = st.columns(2)

with col1:
    sense_oligo = st.text_input("Sense Primer (right primer)", placeholder="e.g., CTGGTCCAGTGCGTTATTGG")
    antisense_oligo = st.text_input("Antisense Primer (left primer)", placeholder="e.g., AGCCAAATGCTTCTTGCTCTTTT")

with col2:
    guide_context = st.text_input(
        "Guide Sequence with Context",
        placeholder="e.g., CTACAGGACGTACCTGCACCCGGATTCACCAGCGCCCG",
        help="Provide guide sequence and ≥ 15 bp forward context"
    )
    orientation = st.selectbox(
        "Guide Orientation",
        options=["sense", "antisense"],
        help="Is the guide in the same strand as the 'sense' primer or 'antisense' primer?"
    )

if st.button("Design Primers"):
    if all([sense_oligo, antisense_oligo, guide_context]):
        try:
            # Call the design function
            result = design(sense_oligo, antisense_oligo, guide_context, orientation)
            
            # Display results
            st.success("Primers designed successfully!")
            
            st.subheader("Results")
            for primer in result:
                if isinstance(primer, SeqRecord):
                    st.code(f"Sequence: {primer.seq}\nDescription: {primer.description}")
                else:
                    st.code(str(primer))
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please fill in all fields.") 