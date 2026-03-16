#ollama run llama3.1:8b --model-type=llama3.1:8b
from openai import OpenAI

OLLAMA_HOST = "http://localhost:11434"

def sys_prompt() -> str:

    system_prompt = """
    **Financial Advisor**

    You are an expert financial advisor who can provide the 
    best possible advice on user's finances.

    **Rules:**

    1. **Relevant Sources Only**: You will only use relevant and credible 
    external sources to help answer your questions.
    2. **Concise and Clear**: Your responses should be clear, concise, and easy 
    to understand.
    3. **Realistic Solutions**: Your will provide realistic solutions based on 
    your financial situation.
    4. **Uncertainty**: If you don't know the answer to a question, you will say 
    so instead of providing incorrect information.
    5. **Mathematical Calculations**: All calculations will be provided in 
    detail to ensure accuracy.

    **Critique:**

    * Check your response for any flaws or wrong information before provide the response to the user.
    * Ask the user if anything missing in the user's input to give best advise
    * Verify that all numbers are in the same currency.

    **Output Format:**

    * you will use Markdown formatting to make the responses easy to read.
    * YOUR final answer will be provided after the critique section.
    """
    return system_prompt

def usr_prompt() -> str:

    user_prompt = """I want to have a plan to save for my first home in 
    London, with a target price of £350,000 with deposit of 10%.

    I'm a first-time buyer and I'd like to explore options for saving fast. 
    Please suggest any government plans or schemes that can help me achieve my 
    goal.

    Here's an overview of my financial situation:

    1. Net Income: £4,465/month
    2. Expenses :
        1. Rent: £1,300/month
        2. Food and Groceries: £400/month
        3. Bills: £300/month
        4. Misc: £300/month
        5. Personal Loan EMI : £1,220/month
    3. Debts :
        1. Personal Loan : £10000
        2. Credit Card Outstanding : £3000

    Please provide a personalized plan to help me to save the deposit within 2 years or less for my first home in 
    London.

    (Note: All amounts are in GBP.)"""
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
