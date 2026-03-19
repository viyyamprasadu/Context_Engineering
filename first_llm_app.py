#ollama run llama3.1:8b --model-type=llama3.1:8b
from openai import OpenAI

OLLAMA_HOST = "http://localhost:11434"

def input_set():

    input_details = [{"Income" : 4465 },
    {"Expenses": [{"Rent" : 1300},{"Food": 400},{"Bills": 300},{"Misc": 300}]},
    {"Debts":[{"Loan": 10000},{"Credit Outstanding": 3000}]},
    {"savings":[{"LISA": 10400},{"EmergencyFund": 2500}]}]
    return input_details


def rules_set() -> []:
    
    rules = [
        "Concise and Clear: Your responses should be clear, concise, and easy to understand.",
        "Relevant Sources Only: You will only use relevant and credible external sources to help answer your questions.",
        "Realistic Solutions: Your will provide realistic solutions based on your financial situation.",
        "Uncertainty: If you don't know the answer to a question, you will say so instead of providing incorrect information.",
        "Mathematical Calculations: All calculations will be provided in detail to ensure accuracy."
    ]

    return rules

def critique_Set() -> []:
    
    critique = [
        "Check your response for any flaws or wrong information before provide the response to the user.",
        "Ask the user if anything missing in the user's input to give best advise.",
        "Verify that all numbers are in the same currency."
    ]

    return critique

def format_Set() -> []:

    output_format = [
        "you will use Markdown formatting to make the responses easy to read.",
        "YOUR final answer will be provided after the critique section."
    ]

    return output_format

def sys_prompt() -> str:

    system_prompt = (
    "**Financial Advisor**\n\n"
        "You are an expert financial advisor who can provide the best possible advice on user's finances.\n\n"

    "**Rules:**\n"
    +"\n".join(f"- {r}" for r in rules_set())
    +"\n"

    +"**Critique:**"
    +"\n".join(f"- {c}" for c in critique_Set())
    +"\n"

    +"**Output Format:**"
    +"\n".join(f"- {of}" for of in format_Set())
    +"\n"
    )
    
    return system_prompt

def usr_prompt() -> str:
    detail_lines = []

    for block in input_set():
        for k, v in block.items():
            if isinstance(v, list):
                nested = " ,".join(f"{nk}: {nv}" for item in v for nk,nv in item.items())
                detail_lines.append(f"- {k}: {nested}")
            else:
                detail_lines.append(f"- {k}: {v}")
                

    user_prompt = ("I want to have a plan to save for my first home in\n\n" 
    "London, with a target price of £350,000 with deposit of 10%.I'm a first-time buyer and I'd like to explore options for saving fast.\n\n" 
    "Please suggest any government plans or schemes that can help me achieve my goal.\n\n"
    "Here's an overview of my financial situation:\n\n"
    +"\n".join(detail_lines)
    +"\n\n"

    "Note:\n" 
    "1. I don't have any other debts and no other income sources\n"
    "2. Income and Expenses stays same every month until the they are repaid.\n\n"
    "3. I have to pay GBP 1220 towards Loan until it is cleared. also need repay GBP 3000 towards outstanding\n\n"

    "Please provide a personalized plan to help me to save the deposit within 2 years or less for my first home in London.")

    return user_prompt

def main() -> None:

    client = OpenAI(base_url=OLLAMA_HOST)

    response = client.chat.completions.create(
        model = "llama3.2",
        messages = [
            {'role' : 'system', 'content' : sys_prompt()}, 
            {'role' : 'user', 'content' : usr_prompt()}
            ]
    )

    markdown_output = response.choices[0].message.content
    output_path = "savings_plan_new.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    print(f"saved answer to {output_path}")

if __name__ == "__main__":
    main()
