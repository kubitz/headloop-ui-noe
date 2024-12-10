import streamlit as st
from headloop.designer import design
from Bio.SeqRecord import SeqRecord

st.set_page_config(
    page_title="FishWeb Designer",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Headloop Primer Designer")

st.markdown("""
This tool helps design headloop primers for suppression PCR to suppress amplification of a known haplotype.
Please provide the following information, or test with example data:
""")

# Example data
example_data = {
    "sense_oligo": "CTGGTCCAGTGCGTTATTGG",
    "antisense_oligo": "AGCCAAATGCTTCTTGCTCTTTT",
    "guide_context": "CTACAGGACGTACCTGCACCCGGATTCACCAGCGCCCG",
}

# Checkbox for using example data
use_example = st.checkbox("Use example data")

# Input fields
col1, col2 = st.columns(2)

if use_example:
    sense_oligo = col1.text_input("Sense Fish Primer (right primer)", value=example_data["sense_oligo"])
    antisense_oligo = col1.text_input("Antisense Primer (left primer)", value=example_data["antisense_oligo"])
    guide_context = col2.text_input("Guide Sequence with Context", value=example_data["guide_context"])
else:
    sense_oligo = col1.text_input("Sense Fish Primer (right primer)", placeholder="e.g., CTGGTCCAGTGCGTTATTGG")
    antisense_oligo = col1.text_input("Antisense Primer (left primer)", placeholder="e.g., AGCCAAATGCTTCTTGCTCTTTT")
    guide_context = col2.text_input(
        "Guide Sequence with Context",
        placeholder="e.g., CTACAGGACGTACCTGCACCCGGATTCACCAGCGCCCG",
        help="Provide guide sequence and ≥ 15 bp forward context"
    )

orientation = col2.multiselect(
    "Guide Orientation(s)",
    options=["sense", "antisense"],
    default=["sense"],
    help="Select guide orientation(s) for designing primers."
)

if st.button("Design Primers"):
    if all([sense_oligo, antisense_oligo, guide_context]):
        try:
            # Iterate through selected orientations and display results
            st.subheader("Results")
            for orient in orientation:
                st.markdown(f"### Orientation: {orient.capitalize()}")
                try:
                    result = design(sense_oligo, antisense_oligo, guide_context, orient)
                    if result:
                        for primer in result:
                            if isinstance(primer, SeqRecord):
                                st.code(f"Sequence: {primer.seq}\nDescription: {primer.description}")
                            else:
                                st.code(str(primer))
                    else:
                        st.warning(f"No primers found for {orient} orientation.")
                except Exception as sub_error:
                    st.error(f"An error occurred while processing {orient} orientation: {str(sub_error)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please fill in all fields.")
