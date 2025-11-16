import os
import json
import streamlit as st
import google.generativeai as genai

#Configuring api key
genai.configure(api_key="GEMINI_API_KEY")

#initializing a model
model = genai.GenerativeModel("gemini-2.5-flash")

#Given a dataset to give relation between skills and interests that user enters
career_dataset ={
    "web development": {
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "REST APIs", "Git"],
        "courses": ["freeCodeCamp Full Stack", "CS50 Web", "Coursera Front-End"],
        "internships": ["Frontend Intern", "Full-Stack Intern", "UI Developer Intern"]
    },

    "machine learning": {
        "skills": ["Python", "NumPy", "Pandas", "scikit-learn", "TensorFlow", "Model Training"],
        "courses": ["Google ML Crash Course", "DeepLearning.AI", "fast.ai"],
        "internships": ["ML Intern", "Data Science Intern", "AI Research Intern"]
    },

    "cloud computing": {
        "skills": ["AWS", "GCP", "Azure", "Docker", "Kubernetes", "Cloud Architecture"],
        "courses": ["AWS Educate", "Azure Fundamentals", "Google Cloud Essentials"],
        "internships": ["Cloud Engineer Intern", "DevOps Intern", "SRE Intern"]
    },

    "cybersecurity": {
        "skills": ["Linux", "Networking", "Ethical Hacking", "BurpSuite", "SIEM Tools"],
        "courses": ["TryHackMe", "HackTheBox", "CompTIA Security+"],
        "internships": ["Cybersecurity Intern", "SOC Analyst Intern", "Vulnerability Analyst Intern"]
    },

    "android development": {
        "skills": ["Kotlin", "Java", "Android Studio", "Jetpack Compose"],
        "courses": ["Android Basics by Google", "Udacity Kotlin Course"],
        "internships": ["Android Developer Intern", "Mobile App Developer Intern"]
    },

    "data analytics": {
        "skills": ["Excel", "SQL", "Power BI", "Tableau", "Python"],
        "courses": ["Google Data Analytics", "Udemy SQL Bootcamp"],
        "internships": ["Data Analyst Intern", "Business Analyst Intern"]
    },

    "data engineering": {
        "skills": ["SQL", "Apache Spark", "Airflow", "ETL Pipelines", "Python"],
        "courses": ["Data Engineering Zoomcamp", "Coursera DE specialization"],
        "internships": ["Data Engineer Intern", "ETL Developer Intern"]
    },

    "blockchain": {
        "skills": ["Solidity", "Web3.js", "Smart Contracts", "Ethereum"],
        "courses": ["CryptoZombies", "Blockchain Developer Udemy"],
        "internships": ["Blockchain Developer Intern", "Smart Contract Intern"]
    },

    "devops": {
        "skills": ["Linux", "GitHub Actions", "CI/CD", "Docker", "Kubernetes", "Jenkins"],
        "courses": ["KodeKloud DevOps", "AWS DevOps Basics"],
        "internships": ["DevOps Intern", "Automation Engineer Intern"]
    },

    "ui ux design": {
        "skills": ["Figma", "Wireframing", "Prototyping", "User Research"],
        "courses": ["Google UX Design", "DesignCourse UI Essentials"],
        "internships": ["UI/UX Intern", "Product Designer Intern"]
    },

    "game development": {
        "skills": ["Unity", "C#", "Game Physics", "Blender"],
        "courses": ["Unity Learn", "GameDev.tv Courses"],
        "internships": ["Game Developer Intern", "Unity Intern"]
    },

    "research & academia": {
        "skills": ["Paper Writing", "Python", "Experiment Design", "Statistics"],
        "courses": ["DeepLearning.AI Research", "Coursera Research Methods"],
        "internships": ["Research Intern", "AI Lab Intern"]
    }
}
#establishing relation 
def build_prompt(name, year, interests, skills,months):
    context = ""
    for key in career_dataset:
        if key.lower() in interests.lower():
            data = career_dataset[key]
            context = (
                f"Relevant field: {key}\n"
                f"Suggested skills: {', '.join(data['skills'])}\n"
                f"Recommended courses: {', '.join(data['courses'])}\n"
                f"Internship types: {', '.join(data['internships'])}\n"
            )
            break
#giving prompt to api
    prompt = f"""
You are a career planning assistant for college students.

Student Info:
Name: {name}
Year of Study: {year}
Interests: {interests}
Current Skills: {skills}

Context (from internal dataset):
{context}

Task:
Generate a personalized {months}-month career roadmap.
Respond STRICTLY in JSON with this structure:
{{
  "career_goal": "string",
  "learning_path": [
    {{"month": 1, "focus": "string", "resources": ["string1", "string2"]}},
    {{"month": 2, "focus": "string", "resources": ["string1", "string2"]}}
  ],
  "internship_ideas": ["string1", "string2"],
  "key_skills_to_master": ["string1", "string2"]
}}
"""
    return prompt
#web interface 
st.set_page_config(page_title="Career Path Coach", page_icon="🎯")
st.title("🎯 Career Path Coach for Students")
st.write("Plan your next 6 months towards your dream tech career using Gemini AI.")
#inputs
name = st.text_input(" Your Name")
year = st.selectbox(" Year of Study", ["1st", "2nd", "3rd", "4th"])
interests = st.text_area(" Your Career Interests (e.g., AI, Web, Cloud)")
skills = st.text_area(" Current Skills (e.g., Python, C++, HTML)")
months = st.number_input("📆 Number of Months for Roadmap", min_value=1, max_value=24, value=6)

#click button function
if st.button("Generate My Career Plan"):
    # else give warning
    if not name or not interests:
        st.warning("Please fill in your name and interests!")
    else:
        prompt = build_prompt(name, year, interests, skills,months)
        with st.spinner("Generating your personalized roadmap..."):
            try:
                response = model.generate_content(prompt)
                text = response.text.strip()

                # Try to parse JSON safely
                try:
                    data = json.loads(text)
                except:
                    # If Gemini adds explanations, extract JSON part
                    start = text.find("{")
                    end = text.rfind("}")
                    data = json.loads(text[start:end + 1])

                st.success(f"Career Goal: {data.get('career_goal', 'N/A')}")
                st.subheader("Learning Path")
                for step in data["learning_path"]:
                    st.markdown(f"**Month {step['month']}:** {step['focus']}")
                    st.markdown("- Resources: " + ", ".join(step["resources"]))

                st.subheader("Internship Ideas")
                st.markdown(", ".join(data["internship_ideas"]))

                st.subheader(" Key Skills to Master")
                st.markdown(", ".join(data["key_skills_to_master"]))

            except Exception as e:
                st.error(f"Error: {e}")

