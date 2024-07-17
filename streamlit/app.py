
import streamlit as st

import streamlit.web.cli as stcli

import requests
import json



def main():
    st.title("Application for Classifying Candidates as Hired or Not Hired")
    # Inputs from user in sidebar
    st.sidebar.header("User Inputs")

    cities = [
        "Valencia", "Madrid", "New York", "Chicago", "Los Angeles", "Miami", 
        "Lyon", "Las Vegas", "Paris", "Nancy", "Barcelona", 
        "San Francisco", "Seville", "Marseille", "Washington"
    ]
    
    eye_colors = ["Blue", "Hazel", "Brown", "Green"]
    jobs = ["Data Scientist", "Data Analyst", "Data Engineer", "Data Steward"]

    city_of_origin = st.sidebar.selectbox("City of Origin", cities)
    eye_color = st.sidebar.selectbox("Eye Color", eye_colors)
    test_score = st.sidebar.slider("Technical Test Score (between 0 and 100)", 0, 100)
    age = st.sidebar.number_input("Age", min_value=16, max_value=100)
    gender = st.sidebar.selectbox("Gender", ["M", "F"])
    degree = st.sidebar.selectbox("Degree", ["Bachelor's", "High School", "Doctorate", "Master's"])
    job = st.sidebar.selectbox("Job", jobs)
    experience = st.sidebar.number_input("Years of Experience", min_value=0, max_value=50)
    availability = st.sidebar.selectbox("Availability", ["yes", "no"])
    salary = st.sidebar.number_input("Salary (in euros)", min_value=0, step=1000)


    # Button to submit
    if st.sidebar.button("Submit"):
        data = {
            'ville_d_origine': city_of_origin,
            'couleur_des_yeux': eye_color,
            'note': test_score,
            'age': age,
            'sexe': gender,
            'diplome': degree,
            'métier': job,
            'experience': experience,
            'dispo': availability,
            'salaire': salary
        }
        # Generate and display the concatenated text
        text = concatenate_text(data)
        st.write(text)
        classification,Explication=result_api(text)
        if classification == 'hired':
            classification_colored = f"<span style='color: green;'>{classification}</span>"
        else:
            classification_colored = f"<span style='color: red;'>{classification}</span>"
        
        st.markdown(f"### Classification: {classification_colored}", unsafe_allow_html=True)
        
        st.header('Explanation:')
        st.write(Explication)
      

def result_api(text):
    url = "https://p3syxy7mh9.execute-api.us-east-1.amazonaws.com/class/" #change me

    payload = json.dumps({
    "text": text
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res=response.text
    result = json.loads(json.loads(res))
    # Accéder aux valeurs du dictionnaire
    print(result)
    classification = result['Class']
    explanation = result['Explanation']
    return classification , explanation


def concatenate_text(x):
    if x['sexe'] == 'M':
        sexe = 'man'
        pronoun = 'he'
        possessive_pronoun = 'his'
    else:
        sexe = 'woman'
        pronoun = 'she'
        possessive_pronoun = 'her'

    if x['dispo'] == 'no':
        availability = "is not available"
    else:
        availability = "is available"

    full_text = (
        f"The candidate is a {int(x['age'])}-year-old {sexe} ",
        f"from {x['ville_d_origine']} with {x['couleur_des_yeux'].lower()} eyes. ",
        f"{pronoun.capitalize()} has {int(x['experience'])} years of experience as a {x['métier']} and holds a {x['diplome']}'s degree. ",
        f"Currently, {pronoun} {availability} and {possessive_pronoun} salary is {x['salaire']} euros. ",
        f"{pronoun.capitalize()} scored {x['note']} in the technical test."
    )
    return ''.join(full_text)

if __name__=='__main__':
    main()

