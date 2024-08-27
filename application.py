import streamlit as st
import requests

# Function to make a GET request to a REST API
def fetch_data_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
        return None

def post_data_to_api(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while posting data: {e}")
        return None

# Function for the Studio page
def studio():
    st.title("Studio Management")

    st.markdown("---")
    st.header("Create a New Studio")

    # Fetch the list of members to select from
    members = fetch_data_from_api("http://localhost:9090/api/v1/user")

    if members:
        member_options = {f"{member['firstName']} {member['lastName']}": member['_id'] for member in members}
        selected_members = st.multiselect(
            "Select Members for the Studio",
            options=list(member_options.keys())
        )
        selected_member_ids = [member_options[name] for name in selected_members]
    else:
        st.error("Unable to fetch members. Please try again later.")
        selected_member_ids = []

    # Form to create a new studio
    with st.form("create_studio"):
        name = st.text_input("Studio Name")
        description = st.text_area("Description (Optional)")
        location = st.text_input("Location")

        submit = st.form_submit_button("Create Studio")

        if submit:
            # Validation
            if not name:
                st.error("Studio Name is required.")
            elif not location:
                st.error("Location is required.")
            elif not selected_member_ids:
                st.error("At least one member must be selected.")
            else:
                # Prepare data
                studio_data = {
                    "name": name,
                    "description": description,
                    "location": location,
                    "memberIds": selected_member_ids
                }

                # Send data to the API
                response = post_data_to_api("http://localhost:9090/api/v1/studio", studio_data)

                if response:
                    st.success(f"Studio '{name}' created successfully!")
                    st.json(response)  # Display the response for debugging

    st.markdown("---")
    st.header("List of Studios")

    # Fetch the list of studios using the reusable function
    studios = fetch_data_from_api("http://localhost:9090/api/v1/studio")

    if studios:
        st.table(studios)  # Display the list of studios
    else:
        st.info("No studios found or an error occurred.")

# Function for the Healthplan page
def healthplan():
    st.title("Healthplan Management")

    st.markdown("---")
    st.header("Create a New Healthplan")

    # Fetch the list of members to select from
    members = fetch_data_from_api("http://localhost:9090/api/v1/user")

    if members:
        member_options = {f"{member['firstName']} {member['lastName']}": member['_id'] for member in members}
        selected_member = st.selectbox(
            "Select Member for the Healthplan",
            options=list(member_options.keys())
        )
        member_id = member_options[selected_member]
    else:
        st.error("Unable to fetch members. Please try again later.")
        member_id = None

    # Form to create a new healthplan
    with st.form("create_healthplan"):
        name = st.text_input("Healthplan Name")
        duration_weeks = st.number_input("Duration (in weeks)", min_value=1, step=1)
        goal = st.text_input("Goal (e.g., 'Weight Loss', 'Muscle Gain')")

        # Define the days and meals
        days = []
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            st.subheader(day)
            meals = []
            for i in range(1, 4):  # Assume 3 meals per day
                with st.expander(f"Meal {i}"):
                    meal_name = st.text_input(f"Meal {i} Name", key=f"{day}_meal_{i}_name")
                    meal_time = st.text_input(f"Meal {i} Time (e.g., 'Breakfast', 'Lunch')", key=f"{day}_meal_{i}_time")
                    calories = st.number_input(f"Calories for Meal {i}", min_value=0, key=f"{day}_meal_{i}_calories")
                    protein_g = st.number_input(f"Protein (g) for Meal {i}", min_value=0.0, step=0.1, key=f"{day}_meal_{i}_protein")
                    carbs_g = st.number_input(f"Carbs (g) for Meal {i}", min_value=0.0, step=0.1, key=f"{day}_meal_{i}_carbs")
                    fat_g = st.number_input(f"Fat (g) for Meal {i}", min_value=0.0, step=0.1, key=f"{day}_meal_{i}_fat")
                    ingredients = st.text_area(f"Ingredients for Meal {i} (comma separated)", key=f"{day}_meal_{i}_ingredients")
                    ingredient_list = [ingredient.strip() for ingredient in ingredients.split(",")]

                    meals.append({
                        "name": meal_name,
                        "time": meal_time,
                        "calories": calories,
                        "protein_g": protein_g,
                        "carbs_g": carbs_g,
                        "fat_g": fat_g,
                        "ingredients": ingredient_list,
                    })

            days.append({
                "day": day,
                "meals": meals
            })

        submit = st.form_submit_button("Create Healthplan")

        if submit:
            # Validation
            if not name:
                st.error("Healthplan Name is required.")
            elif not duration_weeks:
                st.error("Duration in weeks is required.")
            elif not goal:
                st.error("Goal is required.")
            elif not member_id:
                st.error("A member must be selected.")
            else:
                # Prepare data
                healthplan_data = {
                    "memberId": member_id,
                    "name": name,
                    "duration_weeks": duration_weeks,
                    "goal": goal,
                    "days": days,
                }

                # Send data to the API
                response = post_data_to_api("http://localhost:9090/api/v1/healthplan", healthplan_data)

                if response:
                    st.success(f"Healthplan '{name}' created successfully!")
                    st.json(response)  # Display the response for debugging

    st.markdown("---")
    st.header("List of Healthplans")

    # Fetch the list of healthplans using the reusable function
    healthplans = fetch_data_from_api("http://localhost:9090/api/v1/healthplan")

    if healthplans:
        st.table(healthplans)  # Display the list of healthplans
    else:
        st.info("No healthplans found or an error occurred.")

# Function for the Workoutplan page
def workoutplan():
    st.title("Workoutplan Management")

    st.markdown("---")
    st.header("Create a New Workoutplan")

    # Fetch the list of members to select from
    members = fetch_data_from_api("http://localhost:9090/api/v1/user")

    if members:
        member_options = {f"{member['firstName']} {member['lastName']}": member['_id'] for member in members}
        selected_member = st.selectbox(
            "Select Member for the Workoutplan",
            options=list(member_options.keys())
        )
        member_id = member_options[selected_member]
    else:
        st.error("Unable to fetch members. Please try again later.")
        member_id = None

    # Form to create a new workout plan
    with st.form("create_workoutplan"):
        name = st.text_input("Workoutplan Name")
        duration_weeks = st.number_input("Duration (in weeks)", min_value=1, step=1)
        frequency_per_week = st.number_input("Frequency per week", min_value=1, step=1)
        goal = st.text_input("Goal (e.g., 'Strength Building', 'Endurance')")

        # Define the days and exercises
        days = []
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            st.subheader(day)
            focus = st.text_input(f"Focus for {day} (e.g., 'Upper Body', 'Cardio')", key=f"{day}_focus")
            exercises = []
            for i in range(1, 4):  # Assume up to 3 exercises per day
                with st.expander(f"Exercise {i}"):
                    exercise_name = st.text_input(f"Exercise {i} Name", key=f"{day}_exercise_{i}_name")
                    exercise_type = st.text_input(f"Exercise {i} Type (e.g., 'Strength', 'Cardio')", key=f"{day}_exercise_{i}_type")
                    sets = st.number_input(f"Sets for Exercise {i}", min_value=1, step=1, key=f"{day}_exercise_{i}_sets")
                    reps = st.text_input(f"Reps for Exercise {i} (can be a number or a description like 'AMRAP')", key=f"{day}_exercise_{i}_reps")
                    rest_seconds = st.number_input(f"Rest (seconds) between sets for Exercise {i}", min_value=0, step=10, key=f"{day}_exercise_{i}_rest_seconds")
                    duration_seconds = st.number_input(f"Duration (seconds) for Exercise {i} (if applicable)", min_value=0, step=10, key=f"{day}_exercise_{i}_duration_seconds")

                    exercises.append({
                        "name": exercise_name,
                        "type": exercise_type,
                        "sets": sets,
                        "reps": reps,
                        "rest_seconds": rest_seconds,
                        "duration_seconds": duration_seconds,
                    })

            days.append({
                "day": day,
                "focus": focus,
                "exercises": exercises
            })

        submit = st.form_submit_button("Create Workoutplan")

        if submit:
            # Validation
            if not name:
                st.error("Workoutplan Name is required.")
            elif not duration_weeks:
                st.error("Duration in weeks is required.")
            elif not frequency_per_week:
                st.error("Frequency per week is required.")
            elif not goal:
                st.error("Goal is required.")
            elif not member_id:
                st.error("A member must be selected.")
            else:
                # Prepare data
                workoutplan_data = {
                    "memberId": member_id,
                    "name": name,
                    "duration_weeks": duration_weeks,
                    "frequency_per_week": frequency_per_week,
                    "goal": goal,
                    "days": days,
                }

                # Send data to the API
                response = post_data_to_api("http://localhost:9090/api/v1/workoutplan", workoutplan_data)

                if response:
                    st.success(f"Workoutplan '{name}' created successfully!")
                    st.json(response)  # Display the response for debugging

    st.markdown("---")
    st.header("List of Workoutplans")

    # Fetch the list of workoutplans using the reusable function
    workoutplans = fetch_data_from_api("http://localhost:9090/api/v1/workoutplan")

    if workoutplans:
        st.table(workoutplans)  # Display the list of workoutplans
    else:
        st.info("No workoutplans found or an error occurred.")

# Function for the Users page
def users():
    st.title("User Management")

    st.markdown("---")
    st.header("Create a New User")

    # Form to create a new user
    with st.form("create_user"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        submit = st.form_submit_button("Create User")

        if submit:
            st.success(f"User '{username}' with email '{email}' created successfully!")

    st.markdown("---")
    st.header("List of Users")

    # Fetch the list of users using the reusable function
    users = fetch_data_from_api("http://localhost:9090/api/v1/user")

    if users:
        st.table(users)  # Display the list of users
    else:
        st.info("No users found or an error occurred.")

# Dictionary of pages
pages = {
    "Studio": studio,
    "Healthplan": healthplan,
    "Workoutplan": workoutplan,
    "Users": users,
}

# Sidebar with page selection
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page
page = pages[selection]
page()