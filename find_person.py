import os
from typing import Tuple

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parser import Summary, summary_parser
from third_parties.linkedin import scrape_linkedin_profile


def find_person(name: str) -> Tuple[Summary, str]:
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    summary_template = """
        given the information {information} about a person from I want you to create:
            1. a short summary
            2. two interesting facts about them
        
        Use information from Linkedin
        \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions
        },
    )

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o-mini",
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )
    # llm = ChatOllama(model="llama3.2")

    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser
    print(linkedin_profile_url)
    linkedin_data = scrape_linkedin_profile(
        # linkedin_profile_url="https://www.linkedin.com/in/aaron-song-fullstack/",
        linkedin_profile_url=linkedin_profile_url,
        mock=False,
    )

    print(linkedin_data)

    res = chain.invoke(input={"information": linkedin_data})
    return (res, linkedin_data.get("profile_pic_url"))


if __name__ == "__main__":
    load_dotenv()
    print("Finding person...")
    print(find_person(name="Eden Marco"))
