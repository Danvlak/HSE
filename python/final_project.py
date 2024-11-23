import streamlit as st
import datetime

class Table:
    def __init__(self, name, seats):
        self.name = name
        self.seats = seats
        self.status_free = True

    def take(self):
        self.status_free = False

    def release(self):
        self.status_free = True

    def __str__(self):
        return f"{self.name} - {self.seats} seats"

    def __repr__(self):
        return self.__str__()

class Booking:
    def __init__(self, name, phone, booking_time, period, table):
        self.name = name
        self.phone = phone
        self.booking_time = booking_time
        self.period = period
        self.table = table

def add_table(name, seats):
    table = Table(name, seats)
    st.session_state.tables.append(table)

def add_booking(name, phone, booking_time, period, table):
    booking = Booking(name, phone, booking_time, period, table)
    st.session_state.bookings.append(booking)

# Session state initialization
if 'tables' not in st.session_state:
    st.session_state.tables = []
if 'bookings' not in st.session_state:
    st.session_state.bookings = []
if "selected_table" not in st.session_state:
    st.session_state.selected_table = None

# Page selection
page = st.sidebar.radio("Page", ["Tables", "Booking", "Status"])

if page == "Tables":
    st.header("Tables")

    # Select a table
    if st.session_state.tables:
        selected_table_value = st.selectbox(
            "Table",
            st.session_state.tables,
            format_func=lambda table: f"{table.name} - {table.seats}"
        )
        if selected_table_value:
            st.session_state.selected_table = selected_table_value
    else:
        st.write("No tables available")

    # Buttons to interact with tables
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.session_state.selected_table:
            if st.button("Take the table", key=f"take_table_{st.session_state.selected_table.name}"):
                table_to_take = None
                for table in st.session_state.tables:
                    if table.name == st.session_state.selected_table.name and table.seats == st.session_state.selected_table.seats:
                        table_to_take = table
                if table_to_take.status_free == True:                 
                    table_to_take.status_free = False
                    st.success(f"{table_to_take.name} has been taken.")
                else:
                    st.warning("Selected table not found in the list")
    with col2:
        if st.session_state.selected_table:
            if st.button("Release the table", key=f"release_table_{st.session_state.selected_table.name}"):
                table_to_release = None
                for table in st.session_state.tables:
                    if table.name == st.session_state.selected_table.name and table.seats == st.session_state.selected_table.seats:
                        table_to_release = table
                if table_to_release.status_free == False:                 
                    table_to_release.status_free = True
                    st.success(f"{table_to_release.name} has been released.")
                else:
                    st.warning("Selected table not found in the list")
    with col4:
        if st.session_state.selected_table:
            if st.button("Delete", key=f"delete_main_{st.session_state.selected_table.name}"):
                table_to_remove = None
                for table in st.session_state.tables:
                    if table.name == st.session_state.selected_table.name and table.seats == st.session_state.selected_table.seats:
                        table_to_remove = table
                        break
                if table_to_remove:
                    st.session_state.tables.remove(table_to_remove)
                    st.success(f"{table_to_remove.name} has been deleted.")
                    st.session_state.selected_table = None  # Reset the selected table
                else:
                    st.warning("Selected table not found in the list.")

    # Add new table
    new_table_name = st.text_input("Name of table")
    new_table_seats = st.number_input(
        label="Number of seats",
        min_value=1,
        max_value=8,
        step=1
    )
    if st.button("Add") and new_table_name and new_table_seats > 0:
        add_table(new_table_name, new_table_seats)
        st.success(f"{new_table_name} with {new_table_seats} seats was added to the list")

elif page == "Booking":
    st.header("Booking")

    # Create a booking
    input_name = st.text_input("Input name")
    input_phone = st.text_input("Input phone")

    # Time and period selection
    col1_input, col2_input = st.columns(2)
    booking_time = col1_input.time_input(
        "From",
        datetime.time(10, 0)
    )
    booking_period = col2_input.number_input(
        label="Period",
        min_value=0.5,
        max_value=3.0,
        step=0.5
    )

    # Select a table
    if st.session_state.tables:
        selected_table_value = st.selectbox(
            "Table",
            st.session_state.tables,
            format_func=lambda table: f"{table.name} - {table.seats}"
        )
        if selected_table_value:
            st.session_state.selected_table = selected_table_value
    else:
        st.write("No tables available")

    if st.session_state.selected_table:
        if st.button("Submit", key=f"submit_table_{st.session_state.selected_table.name}"):
            table_to_submit = None
            for table in st.session_state.tables:
                if table.name == st.session_state.selected_table.name and table.seats == st.session_state.selected_table.seats:
                    table_to_submit = table
            if table_to_submit:
                add_booking(input_name, input_phone, booking_time, booking_period, selected_table_value)
                st.success(f"Booking created for {input_name} at table {selected_table_value}.")
            else:
                st.warning("Error creating booking")

    # Display status of tables
    st.subheader("Tables' status")
    for table in st.session_state.tables:
        col1, col2, col3 = st.columns([3, 1, 1])
        st.session_state.selected_table = table
        status = "Free" if table.status_free else "Taken"
        with col1:
            st.write(f"{table.name} - {table.seats}")
        with col2:
            st.write(status)
        with col3:
            if st.button("Delete", key=f"delete_{id(table)}"):
                st.session_state.tables = [t for t in st.session_state.tables if t != table]
                st.rerun()
                

elif page == "Status":
    st.header("Status")

    # Count number of free tables and seats
    free_tables = sum(1 for table in st.session_state.tables if table.status_free)
    free_seats = sum(table.seats for table in st.session_state.tables if table.status_free)

    # Print a list of bookings
    for booking in st.session_state.bookings:
        st.write(f"{booking.name} - {booking.phone} booked {booking.table.name} at {booking.booking_time} for {booking.period} hours")

    # Print number of free tables and seats
    st.write(f"Number of free tables: {free_tables}")
    st.write(f"Number of free seats: {free_seats}")
