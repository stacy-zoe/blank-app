import streamlit as st
import pandas as pd

st.title("Lifora - Blood Intelligence Demo")
if "donor" not in st.session_state:
    st.session_state.donor = pd.DataFrame(columns=[
        "Name", "Blood Group", "Last Donated", "Next Eligible", "Phone", "Address"
    ])
st.header("Add Donor")
name = st.text_input("Donor Name")
blood_group = st.selectbox("Blood Group", ["A+", "B+", "O+", "O-", "AB+"])
last_donated = st.date_input("Last Donated")
phone = st.text_input("Phone Number")
address = st.text_area("Address")
if st.button("Add Donor"):
    last_donated_ts = pd.Timestamp(last_donated)
    next_eligible = last_donated_ts + pd.Timedelta(days=90)
    new_row = {
        "Name": name,
        "Blood Group": blood_group,
        "Last Donated": last_donated_ts,
        "Next Eligible": next_eligible,
        "Phone": phone,
        "Address": address
    }
    st.session_state.donor = pd.concat(
        [st.session_state.donor, pd.DataFrame([new_row])],
        ignore_index=True
    )
    st.success("Donor Added Successfully!")
st.header("Dashboard")
st.session_state.donor["Next Eligible"] = pd.to_datetime(
    st.session_state.donor["Next Eligible"]
)
today = pd.Timestamp.today().normalize()
total_donors = len(st.session_state.donor)
eligible_today = len(
    st.session_state.donor[
        st.session_state.donor["Next Eligible"] <= today
    ]
)
st.write("Total Donors:", total_donors)
st.write("Eligible Today:", eligible_today)
st.dataframe(st.session_state.donor)

st.header("Emergency Request")
required_group = st.selectbox(
    "Required Blood Group",
    ["A+", "B+", "O+", "O-", "AB+"],
    key="emergency_group"
)
if st.button("Search Matching Donors"):
    matches = st.session_state.donor[
        (st.session_state.donor["Blood Group"] == required_group) &
        (st.session_state.donor["Next Eligible"] <= today)
    ]
    if len(matches) > 0:
        st.success("Matching Eligible Donors Found:")
        st.dataframe(matches)
    else:
        st.error("No Eligible Donors Found!")
st.header("Predictive Alert")
blood_counts = st.session_state.donor["Blood Group"].value_counts()
low_groups = []
threshold = 2
for group in ["A+", "B+", "O+", "O-", "AB+"]:
    count = blood_counts.get(group, 0)
    if count < threshold:
        low_groups.append(group)
if low_groups:
    st.warning(f"Low stock predicted for: {', '.join(low_groups)}")
else:
    st.success("All blood groups are sufficiently stocked.")