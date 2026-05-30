# =========================================================
# MULTI-AGENT PROJECT BUILDER + MCP FILESYSTEM + N8N
# =========================================================

import asyncio
import os
from pathlib import Path
from textwrap import dedent

import requests
import streamlit as st
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools


# =========================================================
# LOAD API KEY FROM .env
# =========================================================

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


# =========================================================
# N8N WEBHOOK URL
# =========================================================

N8N_WEBHOOK_URL = "http://localhost:5678/webhook/build-project"


# =========================================================
# OUTPUT FOLDER FOR MCP FILESYSTEM
# =========================================================

BASE_OUTPUT_FOLDER = Path(
    r"C:\Users\cano1\n8n-mcp-server\awesome-llm-apps\advanced_ai_agents\multi_agent_apps\mcp_project_builder\generated_projects"
)

BASE_OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# =========================================================
# STREAMLIT PAGE
# =========================================================

st.title("Multi-Agent Project Builder + MCP + n8n 🛠️")
st.caption("Planner Agent → Coder Agent → Reviewer Agent → MCP saves files → n8n receives results.")


# =========================================================
# SEND RESULTS TO N8N
# =========================================================

def send_to_n8n(user_request: str, plan: str, coding: str, review: str):
    """
    Sends the completed agent results to your published n8n webhook.
    """

    payload = {
        "project_request": user_request,
        "plan": plan,
        "coding": coding,
        "review": review,
        "saved_folder": str(BASE_OUTPUT_FOLDER),
    }

    response = requests.post(
        N8N_WEBHOOK_URL,
        json=payload,
        timeout=20,
    )

    return response


# =========================================================
# MULTI-AGENT BUILD FUNCTION
# =========================================================

async def build_project(user_request: str):
    """
    Runs the full workflow:
    1. Planner Agent creates project plan
    2. Coder Agent uses MCP filesystem tools to save files
    3. Reviewer Agent reviews the final result
    """

    # Start MCP filesystem server limited to the generated_projects folder
    mcp_command = f'npx -y @modelcontextprotocol/server-filesystem "{BASE_OUTPUT_FOLDER}"'

    # Connect to MCP filesystem tools
    mcp_tools = MCPTools(command=mcp_command)
    await mcp_tools.connect()

    try:
        # =================================================
        # PLANNER AGENT
        # =================================================

        planner_agent = Agent(
            name="Planner Agent",
            role="Plans project structure and file list.",
            model=OpenAIChat(
                id="gpt-4o",
                api_key=openai_api_key,
            ),
            instructions=[
                "You are a software project planner.",
                "Create a clear project plan.",
                "Decide what files should be created.",
                "Keep the project small, simple, and runnable.",
                "Return the plan in markdown.",
            ],
            markdown=True,
        )

        # =================================================
        # CODER AGENT WITH MCP FILESYSTEM
        # =================================================

        coder_agent = Agent(
            name="Coder Agent",
            role="Writes project files using MCP filesystem tools.",
            model=OpenAIChat(
                id="gpt-4o",
                api_key=openai_api_key,
            ),
            tools=[mcp_tools],
            instructions=dedent("""
                You are a coding agent with access to MCP filesystem tools.

                Your job:
                1. Create a new project folder.
                2. Write all needed project files.
                3. Use MCP filesystem tools to save the files.
                4. Keep the app simple and runnable.
                5. Include helpful comments inside the code.
                6. Create a README.md explaining how to run the project.

                Rules:
                - Save files only inside the allowed MCP folder.
                - Do not write outside the allowed directory.
                - Prefer HTML, CSS, and JavaScript unless the user asks for Python.
                - Use simple file names like index.html, style.css, script.js, README.md.
            """),
            markdown=True,
        )

        # =================================================
        # REVIEWER AGENT
        # =================================================

        reviewer_agent = Agent(
            name="Reviewer Agent",
            role="Reviews the generated project.",
            model=OpenAIChat(
                id="gpt-4o",
                api_key=openai_api_key,
            ),
            instructions=[
                "Review the generated project.",
                "Explain what was created.",
                "Check if the project is beginner-friendly and runnable.",
                "Mention the folder where files were saved if available.",
                "Suggest one clear improvement.",
            ],
            markdown=True,
        )

        # =================================================
        # STEP 1 — PLAN PROJECT
        # =================================================

        plan_prompt = f"""
        User request:
        {user_request}

        Create a project plan and file structure.
        """

        plan_response = await planner_agent.arun(
            plan_prompt,
            stream=False,
        )

        # =================================================
        # STEP 2 — CODE PROJECT AND SAVE FILES WITH MCP
        # =================================================

        coding_prompt = f"""
        User request:
        {user_request}

        Project plan:
        {plan_response.content}

        Create the project files using MCP filesystem tools.
        Save everything inside the allowed output directory.
        """

        coding_response = await coder_agent.arun(
            coding_prompt,
            stream=False,
        )

        # =================================================
        # STEP 3 — REVIEW PROJECT
        # =================================================

        review_prompt = f"""
        User request:
        {user_request}

        Project plan:
        {plan_response.content}

        Coder result:
        {coding_response.content}

        Review the result.
        """

        review_response = await reviewer_agent.arun(
            review_prompt,
            stream=False,
        )

        return (
            plan_response.content,
            coding_response.content,
            review_response.content,
        )

    finally:
        # Always close MCP connection
        await mcp_tools.close()


# =========================================================
# STREAMLIT UI
# =========================================================

if not openai_api_key:
    st.warning("Missing OPENAI_API_KEY. Copy your .env into this folder.")

else:
    user_request = st.text_area(
        "What should the agent team build?",
        value="Build a simple modern landing page for a transportation company.",
        height=120,
    )

    if st.button("Build Project"):

        if user_request.strip():

            with st.spinner("Agents are planning, coding, and saving files with MCP..."):

                # Run async multi-agent workflow
                plan, coding, review = asyncio.run(
                    build_project(user_request)
                )

            # Display planner result
            st.subheader("Planner Agent Output")
            st.markdown(plan)

            # Display coder result
            st.subheader("Coder Agent Output")
            st.markdown(coding)

            # Display reviewer result
            st.subheader("Reviewer Agent Output")
            st.markdown(review)

            # Show saved project location
            st.success(
                f"Project files saved inside: {BASE_OUTPUT_FOLDER}"
            )

            # Send final results to n8n webhook
            try:
                n8n_response = send_to_n8n(
                    user_request=user_request,
                    plan=plan,
                    coding=coding,
                    review=review,
                )

                if n8n_response.status_code in [200, 201]:
                    st.success("n8n webhook received the agent results successfully.")
                else:
                    st.warning(
                        f"n8n responded with status code: {n8n_response.status_code}"
                    )

            except Exception as e:
                st.error(f"n8n webhook error: {e}")

        else:
            st.warning("Enter a project request first.")