#ollama run llama3.1:8b --model-type=llama3.1:8b
import argparse
from openai import OpenAI
from  LLM_utils import LLMUtils

OLLAMA_HOST = "http://localhost:11434"


def sys_prompt(persona_key:str) -> str:
    #key = "Financial Advisor"
    persona = LLMUtils.persona_set()
    #for d in persona:
     #   if key in d:
    persona_text = next(d[persona_key] for d in persona if persona_key in d)
      #      break
    #persona_text = next(iter(persona[0].values()))
    rules = "\n".join(f"- {r}" for r in LLMUtils.rules_set())
    critique = "\n".join(f"- {c}" for c in LLMUtils.critique_Set())
    output_format = "\n".join(f"- {of}" for of in LLMUtils.format_Set())

    system_prompt = f"""{persona_text}

        **Rules:**
        {rules}

        **Critique:**
        {critique}

        **Output Format:**
        {output_format}
        """
    return system_prompt

def usr_prompt() -> str:
    detail_lines = []
    data = LLMUtils.input_set()
    for k,v in data.items():
        if isinstance(v, dict):
            nested = " ,".join(f"{nk}: {nv}" for nk,nv in v.items())
            detail_lines.append(f"- {k}: {nested}")
        else:
            detail_lines.append(f"- {k}: {v}")
    
    details = "\n".join(detail_lines)       

    user_prompt = f"""I want to have a plan to save for my first home in
    London, with a target price of £350,000 with deposit of 10%.I'm a first-time buyer and I'd like to explore options for saving fast. 
    Please suggest any government plans or schemes that can help me achieve my goal.
    Here's an overview of my financial situation:
    {details}
    
    Note:
    1. I don't have any other debts and no other income sources.
    2. Income and Expenses stays same every month until the they are repaid.
    3. I have to pay GBP 1220 towards Loan until it is cleared. also need repay GBP 3000 towards outstanding
    4. The debts are fixed amounts, no interest on them.

    Please provide a personalized plan to help me to save the deposit within 2 years or less for my first home in London.
    """
    return user_prompt

def main() -> None:

    persona_arg = argparse.ArgumentParser(description= "Define the persona")
    persona_arg.add_argument(
        "--persona",
        required=True,
        choices=["Financial Advisor", "Movie Analyst"]
    )
    args = persona_arg.parse_args()
    persona_key = args.persona

    client = OpenAI(base_url=OLLAMA_HOST)
    response = client.chat.completions.create(
        model = "llama3.2",
        messages = [
            {'role' : 'system', 'content' : sys_prompt(persona_key)}, 
            {'role' : 'user', 'content' : usr_prompt()}
            ]
    )

    markdown_output = response.choices[0].message.content
    output_path = "savings_plan_new1.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    print(f"saved answer to {output_path}")

if __name__ == "__main__":
    main()
