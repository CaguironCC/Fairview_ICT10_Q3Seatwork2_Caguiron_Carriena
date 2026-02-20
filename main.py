# Import necessary modules
from js import document
from pyodide.ffi import create_proxy


def check_eligibility(event):
    """
    Check if a student is eligible for Intramurals
    based on registration, medical clearance, and grade level.
    """
    
    # Get form values
    name = document.getElementById("name").value.strip()
    grade = document.getElementById("grade").value
    section = document.getElementById("sec").value.strip()
    
    # Get radio button values for registration
    registration = None
    if document.querySelector('input[name="registration"]:checked'):
        registration = document.querySelector('input[name="registration"]:checked').value
    
    # Get radio button values for medical clearance
    medical = None
    if document.querySelector('input[name="medical"]:checked'):
        medical = document.querySelector('input[name="medical"]:checked').value
    
    # Get result elements
    status_text = document.getElementById("status-text")
    team_text = document.getElementById("team-text")
    message_text = document.getElementById("message-text")
    result_div = document.getElementById("result")
    
    # Check if all elements exist
    if not all([status_text, team_text, message_text, result_div]):
        print("Error: Some result elements not found")
        return
    
    # Check if all fields are filled
    if not name or not grade or not section or not registration or not medical:
        status_text.innerHTML = "Status: NOT ELIGIBLE"
        team_text.innerHTML = "Team: Not Assigned"
        message_text.innerHTML = "Please fill all fields"
        status_text.className = "status not-eligible"
        result_div.style.display = "block"
        return
    
    # Check grade requirement (must be grades 7-10)
    if grade not in ["7", "8", "9", "10"]:
        status_text.innerHTML = "Status: NOT ELIGIBLE"
        team_text.innerHTML = "Team: Not Assigned"
        message_text.innerHTML = "Only grades 7-10 can participate"
        status_text.className = "status not-eligible"
        result_div.style.display = "block"
        return
    
    # Check eligibility conditions
    if registration == "yes" and medical == "yes":
        # Define teams dictionary
        teams = {
            "Emerald": "Blue Bears",
            "Topaz": "Red Bulldogs",
            "Sapphire": "Yellow Tigers",
            "Ruby": "Green Hornets"
        }
        
        # Check if section exists in teams
        if section in teams:
            team_name = teams[section]
            
            # Display eligible results
            status_text.innerHTML = "Status: ELIGIBLE"
            team_text.innerHTML = f"Team: {team_name}"
            message_text.innerHTML = f"Congratulations {name}! Welcome to Team {team_name}!"
            status_text.className = "status eligible"
        else:
            # Handle invalid section
            status_text.innerHTML = "Status: NOT ELIGIBLE"
            team_text.innerHTML = "Team: Not Assigned"
            message_text.innerHTML = f"Invalid section: {section}"
            status_text.className = "status not-eligible"
    else:
        # Display not eligible results
        status_text.innerHTML = "Status: NOT ELIGIBLE"
        team_text.innerHTML = "Team: Not Assigned"
        
        # Create list of reasons for ineligibility
        reasons = []
        if registration == "no":
            reasons.append("register online")
        if medical == "no":
            reasons.append("get medical clearance")
        
        # Create appropriate message
        if len(reasons) == 2:
            message = f"You need to: {reasons[0]} and {reasons[1]}"
        elif len(reasons) == 1:
            message = f"You need to: {reasons[0]}"
        else:
            message = "Please complete all requirements"
        
        message_text.innerHTML = message
        status_text.className = "status not-eligible"
    
    # Show result section
    result_div.style.display = "block"


def setup_event_listener():
    """
    Set up the event listener for the check button
    """
    check_btn = document.getElementById("check-btn")
    if check_btn:
        check_btn.addEventListener("click", create_proxy(check_eligibility))
    else:
        print("Error: Check button not found")

# Initialize the application when the page loads
setup_event_listener()
