def generate_recommendation(score):

    if score >= 90:
        return {
            "status": "Excellent Match ⭐⭐⭐⭐⭐",
            "message": "Apply immediately. Your profile strongly matches this internship."
        }

    elif score >= 75:
        return {
            "status": "Strong Match ⭐⭐⭐⭐",
            "message": "Highly recommended. You meet most of the required skills."
        }

    elif score >= 60:
        return {
            "status": "Good Match ⭐⭐⭐",
            "message": "Worth applying. Learning a few missing skills will improve your chances."
        }

    elif score >= 40:
        return {
            "status": "Average Match ⭐⭐",
            "message": "Apply only if you're interested and willing to learn the missing skills."
        }

    return {
        "status": "Weak Match ⭐",
        "message": "Not recommended unless you plan to build the required skills."
    }
    