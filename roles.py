INTERVIEW_ROLES = {
    "Software Engineer":{
        "keywords":["OOP","DAS","algorithms","complexity","systems","API"],
        "difficulty":"medium"
    },
    "python Developer":{
        "keywords":["python","flask","django","pandas","asyncio","oop"],
        "difficulty":"easy"
    },
    "data analyst":{
        "keywords":["sql","excel","visualization","power bi","pandas"],
        "difficulty":"medium"
    },
    "machine learning engineer":{
        "keywords":["python","pandas","sklearn","deep learning","neural networks"],
        "difficulty":"hard"
    },
    "cyber security analyst":{
        "keywords":["network security","encryption","vulnerabilities","firewalls","penetration testing"],
        "difficulty":"medium"
    },
    "cloud engineer":{
        "keywords":["aws","azure","gcp","cloud architecture","devops"],
        "difficulty":"medium"
    },
    "product manager":{
        "keywords":["roadmap","stakeholders","agile","user stories","prioritization"],
        "difficulty":"medium"
    }
}

def choose_role():
    print("\n Welcome to the AI Interview Coach - roles.py:33")
    print("Choose a role to begin your mock interview - roles.py:34")

    roles = list(INTERVIEW_ROLES.keys())

    for i, r in enumerate(roles, start=1):
        print(f"{i}. {r.title()} - roles.py:39")

    choice = int(input("\nEnter the number of the role you want to interview for:"))
    role = roles[choice-1]

    print (f"\n You Selected : {role.title()} - roles.py:44")  
    return role, INTERVIEW_ROLES[role]