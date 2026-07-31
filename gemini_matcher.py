from config_local import gemini_api_key


def semantic_match(resume_text, internship):

    """
    Input:
        resume_text -> Full resume text
        internship -> Dictionary of internship information

    Output:
        {
            "match_score": ...,
            "recommendation_status": ...,
            "matched_skills": [...],
            "missing_skills": [...],
            "ai_reason": [...]
        }
    """

    pass