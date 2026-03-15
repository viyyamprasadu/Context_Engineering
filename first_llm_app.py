#ollama run llama3.1:8b --model-type=llama3.1:8b
from openai import OpenAI

OLLAMA_HOST = "http://localhost:11434"
 
# system_prompt = """ you are a proffessional finacial expert who can give best possible advise on the finances
# based on the user's inputs

# #RULES:
# - You are allowed to use ONLY relavent external sources to help the user's query.
# - Your answer SHOULD be LESS wordy , clean and concise. 
# - you MUST porvide ONLY realstic ways as per the user's financial situation.
# - if anything you do not know, you can say that to user. DON'T mixup something.
# - MUST provide step-by-step mathematical calculations.

# #CRITIQUE:
# - check your answer has any flaw or wrong information, if so, revisit the answer properly and correct it.
# - CHECK all the numbers are in same currency 


# #OUTPUT FORMAT:
# - Use markdown to format your answer.
# - Provide the final answer after the CRITIQUE 
# """ 

# user_prompt = """I want to have plan to save for the 1/10th deposit to buy house of cost GBP : 350000 in London area.
# I am a first time buyer. Create plan to save fast including any govt plans or schemes
# 1. Income : 4465/month
# 2. Rent : 1300/month
# 3. Food and Groceries : 400/month
# 4. Bills : 300/month
# 5. Misc : 300/month
# 6. Personal Loan : 1220/month
# 7. Credit Card Outstanding : 3000 

# Note : All the Numbers are in GBP.

# """


system_prompt = """
**Financial Advisor**

You are speaking with a professional financial expert who can provide the 
best possible advice on your finances.

**Rules:**

1. **Relevant Sources Only**: I will only use relevant and credible 
external sources to help answer your questions.
2. **Concise and Clear**: My responses should be clear, concise, and easy 
to understand.
3. **Realistic Solutions**: I will provide realistic solutions based on 
your financial situation.
4. **Uncertainty**: If I don't know the answer to a question, I will say 
so instead of providing incorrect information.
5. **Mathematical Calculations**: All calculations will be provided in 
detail to ensure accuracy.

**Critique:**

* Check my response for any flaws or wrong information and let me know if 
you spot anything.
* Verify that all numbers are in the same currency.

**Output Format:**

* I will use Markdown formatting to make my responses easy to read.
* My final answer will be provided after the critique section.
"""



user_prompt = """I want to have a plan to save for my first home in 
London, with a target price of £350,000 with deposit of 10%.

I'm a first-time buyer and I'd like to explore options for saving fast. 
Please suggest any government plans or schemes that can help me achieve my 
goal.

Here's an overview of my financial situation:

1. Income: £4,465/month
2. Rent: £1,300/month
3. Food and Groceries: £400/month
4. Bills: £300/month
5. Misc: £300/month
6. Personal Loan: £1,220/month
7. Credit Card Outstanding: £3,000

Please provide a personalized plan to help me save for my first home in 
London.

(Note: All amounts are in GBP.)"""

client = OpenAI(base_url=OLLAMA_HOST)

response = client.chat.completions.create(
    model = "llama3.2",
    messages = [{'role' : 'system', 'content' : system_prompt}, {'role' : 'user', 'content' : user_prompt}]
)

markdown_output = response.choices[0].message.content
output_path = "savings_plan.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(markdown_output)

print(f"saved answer to {output_path}")
