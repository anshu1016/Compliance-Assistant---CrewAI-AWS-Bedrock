import streamlit as st
import os
from datetime import datetime
from src.compliance_assistant.crew import ComplianceAssistant

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="Compliance Assistant", page_icon="🛡️", layout="wide")
st.title("🛡️ Compliance Assistant - CrewAI + AWS Bedrock")
st.sidebar.markdown("""
### 🧑‍💼 Compliance Analyst  
- Investigates risks, summarizes laws & regulations.  
**Try asking:**  
- "What are the top compliance risks in cloud data storage?"  
- "Summarize GDPR obligations for data processing."  

### 🎯 Compliance Specialist  
- Deep subject-matter expert, validates findings, compares regulations.  
**Try asking:**  
- "Does our cloud storage plan comply with HIPAA?"  
- "Compare GDPR vs CCPA requirements for data deletion."  

### 🏗️ Solutions Architect  
- Designs technical solutions and remediation plans for compliance.  
**Try asking:**  
- "Design a secure AWS architecture that meets GDPR rules."  
- "Propose an audit logging system for PCI-DSS."  
""")

# --------------------------
# SESSION STATE
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------
# CHAT UI
# --------------------------
st.subheader("💬 Interactive Chat with Compliance Crew")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about compliance, policies, or solutions..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run Crew (single-turn analysis)
    try:
        inputs = {
            "topic": prompt,
            "current_year": str(datetime.now().year)
        }

        with st.chat_message("assistant"):
            with st.spinner("Crew is working..."):
                result = ComplianceAssistant().crew().kickoff(inputs=inputs)

                # Kickoff usually returns structured output
                if isinstance(result, dict):
                    response_text = result.get("output", str(result))
                else:
                    response_text = str(result)

                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

    except Exception as e:
        st.error(f"Error running crew: {str(e)}")

# --------------------------
# RUN FULL TASK PIPELINE
# --------------------------
st.subheader("📑 Run Compliance Analysis & Generate Report")

if st.button("Run Full Compliance Workflow"):
    with st.spinner("Running compliance workflow..."):
        try:
            inputs = {
                "topic": os.environ.get("TOPIC", "General Compliance Review"),
                "current_year": str(datetime.now().year)
            }
            result = ComplianceAssistant().crew().kickoff(inputs=inputs)
            st.success("Workflow completed ✅")

            # If report.md is generated, show it
            if os.path.exists("report.md"):
                with open("report.md", "r", encoding="utf-8") as f:
                    report_content = f.read()
                st.download_button("📥 Download Report", report_content, file_name="report.md")
                st.text_area("Generated Report", report_content, height=300)

        except Exception as e:
            st.error(f"Error running workflow: {str(e)}")


# import streamlit as st
# import os
# from datetime import datetime
# from src.compliance_assistant.crew import ComplianceAssistant

# # --------------------------
# # PAGE CONFIG
# # --------------------------
# st.set_page_config(page_title="Compliance Assistant", page_icon="🛡️", layout="wide")
# st.title("🛡️ Compliance Assistant - CrewAI + AWS Bedrock")

# # --------------------------
# # SIDEBAR INFO (Agents + Demo Questions)
# # --------------------------
# st.sidebar.title("ℹ️ About the Agents")

# st.sidebar.markdown("""
# ### 🧑‍💼 Compliance Analyst  
# - Investigates risks, summarizes laws & regulations.  
# **Try asking:**  
# - "What are the top compliance risks in cloud data storage?"  
# - "Summarize GDPR obligations for data processing."  

# ### 🎯 Compliance Specialist  
# - Deep subject-matter expert, validates findings, compares regulations.  
# **Try asking:**  
# - "Does our cloud storage plan comply with HIPAA?"  
# - "Compare GDPR vs CCPA requirements for data deletion."  

# ### 🏗️ Solutions Architect  
# - Designs technical solutions and remediation plans for compliance.  
# **Try asking:**  
# - "Design a secure AWS architecture that meets GDPR rules."  
# - "Propose an audit logging system for PCI-DSS."  
# """)

# # Agent selection
# agent_choice = st.sidebar.radio(
#     "Choose Agent or Full Crew",
#     ["Compliance Analyst", "Compliance Specialist", "Solutions Architect", "Full Crew Workflow"]
# )

# # --------------------------
# # SESSION STATE
# # --------------------------
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # --------------------------
# # CHAT UI
# # --------------------------
# st.subheader("💬 Interactive Chat")

# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# if prompt := st.chat_input("Ask about compliance, policies, or solutions..."):
#     # Save user message
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     try:
#         inputs = {
#             "topic": prompt,
#             "current_year": str(datetime.now().year)
#         }

#         with st.chat_message("assistant"):
#             with st.spinner("Crew is working..."):

#                 if agent_choice == "Full Crew Workflow":
#                     result = ComplianceAssistant().crew().kickoff(inputs=inputs)
#                 elif agent_choice == "Compliance Analyst":
#                     result = ComplianceAssistant().compliance_analyst().execute(inputs)
#                 elif agent_choice == "Compliance Specialist":
#                     result = ComplianceAssistant().compliance_specialist().execute(inputs)
#                 elif agent_choice == "Solutions Architect":
#                     result = ComplianceAssistant().solutions_architect().execute(inputs)
#                 else:
#                     result = "Invalid choice."

#                 response_text = result.get("output", str(result)) if isinstance(result, dict) else str(result)

#                 st.markdown(response_text)
#                 st.session_state.messages.append({"role": "assistant", "content": response_text})

#     except Exception as e:
#         st.error(f"Error running crew: {str(e)}")

# # --------------------------
# # RUN FULL TASK PIPELINE (Button)
# # --------------------------
# st.subheader("📑 Generate Structured Compliance Report")

# if st.button("Run Full Workflow & Generate Report"):
#     with st.spinner("Running compliance workflow..."):
#         try:
#             inputs = {
#                 "topic": os.environ.get("TOPIC", "General Compliance Review"),
#                 "current_year": str(datetime.now().year)
#             }
#             result = ComplianceAssistant().crew().kickoff(inputs=inputs)
#             st.success("Workflow completed ✅")

#             # If report.md is generated, show it
#             if os.path.exists("report.md"):
#                 with open("report.md", "r", encoding="utf-8") as f:
#                     report_content = f.read()
#                 st.download_button("📥 Download Report", report_content, file_name="report.md")
#                 st.text_area("Generated Report", report_content, height=300)

#         except Exception as e:
#             st.error(f"Error running workflow: {str(e)}")
