import streamlit as st
import pandas as pd
import plotly.express as px

from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import (
    load_skill_dictionary,
    extract_skills,
    group_skills_by_category
)
from job_matcher import (
    load_job_roles,
    calculate_match_scores,
    get_required_skills,
    calculate_skill_gap,
    calculate_skill_match_percentage
)
from roadmap_generator import generate_roadmap


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📄 AI Resume Analyzer and Job Recommendation System")

st.write(
    """
    Upload your resume and analyze how well it matches
    different job roles based on job-related skills and requirements.
    """
)

st.info(
    "This system provides an educational estimate only. "
    "It should not be used for automatic hiring or rejection."
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    skill_dictionary = load_skill_dictionary()

    job_roles = load_job_roles()

except Exception as e:

    st.error(f"Error loading project data: {e}")

    st.stop()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("⚙️ Settings")

target_role = st.sidebar.selectbox(
    "Select Target Role",
    job_roles["role"].tolist()
)

st.sidebar.write(
    "Upload a PDF or DOCX resume to begin."
)


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload your Resume",
    type=["pdf", "docx"]
)


if uploaded_file is not None:

    st.success(
        f"Uploaded file: {uploaded_file.name}"
    )

    # --------------------------------------------------
    # EXTRACT TEXT
    # --------------------------------------------------

    try:

        raw_text = extract_resume_text(
            uploaded_file
        )

    except Exception as e:

        st.error(
            f"Could not extract resume text: {e}"
        )

        st.stop()


    if not raw_text.strip():

        st.warning(
            "No readable text was found in the resume."
        )

        st.stop()


    # --------------------------------------------------
    # CLEAN TEXT
    # --------------------------------------------------

    cleaned_text = clean_text(raw_text)


    # --------------------------------------------------
    # EXTRACT SKILLS
    # --------------------------------------------------

    found_skills = extract_skills(
        cleaned_text,
        skill_dictionary
    )


    # --------------------------------------------------
    # SKILLS SECTION
    # --------------------------------------------------

    st.header("🛠️ Skills Found in Resume")

    if found_skills:

        columns = st.columns(4)

        for index, skill in enumerate(found_skills):

            columns[index % 4].success(
                f"✓ {skill}"
            )

    else:

        st.warning(
            "No skills from the current skill dictionary were detected."
        )


    # --------------------------------------------------
    # SKILLS BY CATEGORY
    # --------------------------------------------------

    st.header("📊 Skills by Category")

    grouped_skills = group_skills_by_category(
        found_skills,
        skill_dictionary
    )

    if grouped_skills:

        category_data = []

        for category, skills in grouped_skills.items():

            category_data.append({
                "Category": category,
                "Number of Skills": len(skills)
            })

        category_df = pd.DataFrame(
            category_data
        )

        fig_category = px.bar(
            category_df,
            x="Category",
            y="Number of Skills",
            title="Skills Detected by Category"
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )


    # --------------------------------------------------
    # JOB MATCHING
    # --------------------------------------------------

    st.header("🎯 Job Role Recommendations")

    match_results = calculate_match_scores(
        cleaned_text,
        job_roles
    )


    # --------------------------------------------------
    # MATCHING TABLE
    # --------------------------------------------------

    display_results = match_results[
        ["role", "match_score"]
    ].copy()

    display_results.columns = [
        "Job Role",
        "Match Score (%)"
    ]

    st.dataframe(
        display_results,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------
    # MATCH SCORE CHART
    # --------------------------------------------------

    fig = px.bar(
        match_results,
        x="role",
        y="match_score",
        title="Resume Match Score by Job Role",
        labels={
            "role": "Job Role",
            "match_score": "Match Score (%)"
        }
    )

    fig.update_yaxes(
        range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------
    # TOP 3 ROLES
    # --------------------------------------------------

    st.subheader("🏆 Recommended Roles")

    top_three = match_results.head(3)

    for index, row in top_three.iterrows():

        st.write(
            f"**{index + 1}. {row['role']} — "
            f"{row['match_score']}%**"
        )


    # --------------------------------------------------
    # SELECTED TARGET ROLE
    # --------------------------------------------------

    st.header(
        f"🔍 Analysis for {target_role}"
    )

    selected_role = job_roles[
        job_roles["role"] == target_role
    ].iloc[0]


    # --------------------------------------------------
    # TARGET ROLE SCORE
    # --------------------------------------------------

    target_result = match_results[
        match_results["role"] == target_role
    ].iloc[0]

    target_score = target_result[
        "match_score"
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "TF-IDF Match Score",
            f"{target_score}%"
        )

    with col2:

        required_skills = get_required_skills(
            selected_role
        )

        skill_percentage = calculate_skill_match_percentage(
            found_skills,
            required_skills
        )

        st.metric(
            "Skill Match",
            f"{skill_percentage}%"
        )


    # --------------------------------------------------
    # SKILL GAP
    # --------------------------------------------------

    matched_skills, missing_skills = calculate_skill_gap(
        found_skills,
        required_skills
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader("✅ Skills Found")

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.write(
                "No required skills detected."
            )


    with col2:

        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in missing_skills:

                st.error(
                    f"✗ {skill}"
                )

        else:

            st.success(
                "No major missing skills detected!"
            )


    # --------------------------------------------------
    # LEARNING ROADMAP
    # --------------------------------------------------

    st.header("📚 Personalized Learning Roadmap")

    roadmap = generate_roadmap(
        missing_skills
    )

    if roadmap:

        roadmap_df = pd.DataFrame(
            roadmap
        )

        st.dataframe(
            roadmap_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "Your resume already contains all the "
            "required skills for this role."
        )


    # --------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------

    st.header("📋 Target Role Requirements")

    st.write(
        selected_role["description"]
    )

    st.write(
        "**Required Skills:**"
    )

    st.write(
        ", ".join(required_skills)
    )


    # --------------------------------------------------
    # RESUME TEXT
    # --------------------------------------------------

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text_area(
            "Extracted Text",
            raw_text,
            height=300
        )


    # --------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------

    st.header("📥 Download Analysis Report")

    report = f"""
AI RESUME ANALYZER AND JOB RECOMMENDATION SYSTEM
================================================

Resume:
{uploaded_file.name}

Target Role:
{target_role}

TF-IDF Match Score:
{target_score}%

Skill Match:
{skill_percentage}%

------------------------------------------------
SKILLS FOUND
------------------------------------------------

{", ".join(found_skills)}

------------------------------------------------
MATCHED REQUIRED SKILLS
------------------------------------------------

{", ".join(matched_skills)}

------------------------------------------------
MISSING SKILLS
------------------------------------------------

{", ".join(missing_skills)}

------------------------------------------------
TOP RECOMMENDED ROLES
------------------------------------------------

"""

    for index, row in top_three.iterrows():

        report += (
            f"{index + 1}. {row['role']} - "
            f"{row['match_score']}%\n"
        )


    report += """
------------------------------------------------
LEARNING ROADMAP
------------------------------------------------
"""

    for item in roadmap:

        report += (
            f"{item['Week']} - "
            f"{item['Skill']}: "
            f"{item['Learning Goal']}\n"
        )


    report += """
------------------------------------------------
DISCLAIMER
------------------------------------------------

This analysis is an educational estimate based on
the skills and job-role information available in the
system. A match score does not represent a hiring,
rejection, or recruiter decision.
"""


    st.download_button(
        label="⬇️ Download Analysis Report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain"
    )


else:

    st.info(
        "👆 Upload a PDF or DOCX resume to start the analysis."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "AI Resume Analyzer and Job Recommendation System | "
    "Educational Student Project"
)