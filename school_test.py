import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------- Constants ----------
HEADERS = [
    "Name", "Class", "Father's Name", "Father's Occupation", "Mother's Name",
    "Mother's Occupation", "DOB", "Contact No", "Address",
    "Admission Fee", "Van Fee", "Monthly Fee",
    "Van Fee Months Paid", "Monthly Fee Months Paid",
    "Total Paid", "Payment Details", "Payment DateTime"
]

# ---------- Helper Functions ----------
def get_filename(class_name):
    return f"class_{class_name}.xlsx"

def get_class_data(class_name):
    filename = get_filename(class_name)
    if not os.path.exists(filename):
        return pd.DataFrame(columns=HEADERS)
    df = pd.read_excel(filename)
    for col in HEADERS:
        if col not in df.columns:
            df[col] = "" if col in ["Payment Details", "Payment DateTime", "Van Fee Months Paid", "Monthly Fee Months Paid"] else 0
    df = df[HEADERS]
    df.to_excel(filename, index=False)
    return df

def save_class_data(class_name, df):
    filename = get_filename(class_name)
    df.to_excel(filename, index=False)

# ---------- Streamlit App ----------
st.set_page_config(page_title="School Management System", layout="wide")
st.title("🏫 School Management System")

menu = st.sidebar.radio("Choose an option:", ("Add Student", "View Class Data", "Update Payment"))

# ---------- Add Student ----------
if menu == "Add Student":
    st.header("➕ Add New Student")

    with st.form("add_student_form"):
        name = st.text_input("Name", key="name_input")
        class_name = st.text_input("Class", key="class_input")
        father_name = st.text_input("Father's Name", key="father_name_input")
        father_occ = st.text_input("Father's Occupation", key="father_occ_input")
        mother_name = st.text_input("Mother's Name", key="mother_name_input")
        mother_occ = st.text_input("Mother's Occupation", key="mother_occ_input")
        dob = st.date_input("Date of Birth", key="dob_input")
        contact = st.text_input("Contact No", key="contact_input")
        address = st.text_area("Address", key="address_input")
        admission_fee = st.number_input("Admission Fee", 0, 100000, key="admission_fee_input")
        van_fee = st.number_input("Van Fee", 0, 5000, key="van_fee_input")
        monthly_fee = st.number_input("Monthly Fee", 0, 10000, key="monthly_fee_input")

        submitted = st.form_submit_button("Add Student")

    if submitted:
        if name and class_name and contact:
            data = {
                "Name": name,
                "Class": class_name,
                "Father's Name": father_name,
                "Father's Occupation": father_occ,
                "Mother's Name": mother_name,
                "Mother's Occupation": mother_occ,
                "DOB": dob,
                "Contact No": contact,
                "Address": address,
                "Admission Fee": admission_fee,
                "Van Fee": van_fee,
                "Monthly Fee": monthly_fee,
                "Van Fee Months Paid": "",
                "Monthly Fee Months Paid": "",
                "Total Paid": 0,
                "Payment Details": "",
                "Payment DateTime": ""
            }

            df = get_class_data(class_name)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            save_class_data(class_name, df)

            st.success(f"✅ Student {name} added to Class {class_name}!")
        else:
            st.warning("⚠️ Please fill at least Name, Class, and Contact No fields.")

# ---------- View Class Data ----------
elif menu == "View Class Data":
    st.header("📚 View Class Data")
    class_name = st.text_input("Enter Class to View Data", key="view_class_input")
    if st.button("View Data"):
        df = get_class_data(class_name)
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("⚠️ No data found for this class.")

# ---------- Update Payment ----------
elif menu == "Update Payment":
    st.header("💰 Update Payment for Student")
    class_name = st.text_input("Class Name", key="update_class_input")
    student_name = st.text_input("Student Name", key="update_student_input")
    admission_fee = st.number_input("Admission Fee Paid", 0, 100000, key="admission_fee_paid_input")
    van_fee = st.number_input("Van Fee Paid", 0, 5000, key="van_fee_paid_input")
    monthly_fee = st.number_input("Monthly Fee Paid", 0, 10000, key="monthly_fee_paid_input")

    van_months = st.text_input("Van Fee Months (comma separated)", key="van_months_input")
    monthly_months = st.text_input("Monthly Fee Months (comma separated)", key="monthly_months_input")

    payment_details = st.text_area("Payment Details", key="payment_details_input")

    if st.button("Update Payment"):
        df = get_class_data(class_name)
        if df.empty:
            st.warning("⚠️ No student data found for this class.")
        else:
            idx = df.index[df["Name"] == student_name].tolist()
            if idx:
                idx = idx[0]
                df.at[idx, "Admission Fee"] += admission_fee
                df.at[idx, "Van Fee"] += van_fee
                df.at[idx, "Monthly Fee"] += monthly_fee

                # Convert safely to avoid AttributeError
                existing_van_months = str(df.at[idx, "Van Fee Months Paid"]) if pd.notna(df.at[idx, "Van Fee Months Paid"]) else ""
                existing_monthly_months = str(df.at[idx, "Monthly Fee Months Paid"]) if pd.notna(df.at[idx, "Monthly Fee Months Paid"]) else ""

                new_van_months = [m.strip() for m in van_months.split(",") if m.strip()]
                new_monthly_months = [m.strip() for m in monthly_months.split(",") if m.strip()]

                combined_van_months = set(existing_van_months.split(",")).union(new_van_months)
                combined_monthly_months = set(existing_monthly_months.split(",")).union(new_monthly_months)

                df.at[idx, "Van Fee Months Paid"] = ", ".join(sorted(combined_van_months))
                df.at[idx, "Monthly Fee Months Paid"] = ", ".join(sorted(combined_monthly_months))

                total_paid = df.at[idx, "Admission Fee"] + df.at[idx, "Van Fee"] + df.at[idx, "Monthly Fee"]
                df.at[idx, "Total Paid"] = total_paid
                df.at[idx, "Payment Details"] = payment_details
                df.at[idx, "Payment DateTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                save_class_data(class_name, df)
                st.success(f"💰 Payment updated for {student_name}!")
            else:
                st.warning("⚠️ Student not found in this class.")
