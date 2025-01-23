import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str):
    llm = ChatOpenAI(
        temperature=0, model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")
    )
    template = """given the full name {name_of_person} I want you to find a link to their Twitter profile page,
    and extract from it their username in your final answer only the person's username,
    which is extracted from: https://x.com/USERNAME"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Twitter profile page",
            func=get_profile_url_tavily,
            description="useful when you need to get the Twitter Page URL",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_excutor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_excutor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url

    # return "https://www.linkedin.com/in/aaron-song-fullstack/"


if __name__ == "__main__":
    print(lookup(name="Eden Marco"))
