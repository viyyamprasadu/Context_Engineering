#ollama run llama3.1:8b --model-type=llama3.1:8b
from openai import OpenAI

OLLAMA_HOST = "http://localhost:11434"

system_prompt = """ you are a finacial advisor who can give best possible avice on the finances based on the user's inputs

 #RULES:
 - You are allowed to use ONLY relavent external sources to help the user's query.
 - You are answer SHOULD be clean and concise. 
 - MUST be LESS wordy and more use of table format
 - you MUST porvide ONLY realstic ways as per the user's financial situation.
 - if anything you do not know, you can say that to user. DON'T mixup something.
 - Any mathemaical calculations provide STEP-BY-STEP process.

 #CRITIQUE:
 - check your answer has any flaw or wrong information, if so, revisit the answer properly and correct it.
 - CHECK all the numbers are in same currency 


 #OUTPUT FORMAT:
 - Use markdown to format your answer.
 - Provide the final answer after the CRITIQUE 
 """

user_prompt = """I want to have plan to save for the 1/10th deposit to buy house of cost GBP : 350000 in London area.
I am a first time buyer. Create plan to save fast including any govt plans or schemes
1. my income : 4465/month
2. rent : 1300/month
3. food and groceries : 400/month
4. bills : 300/month
5. misc : 300/month
6. personal loan : 1220/month
7. Credit Card Outstanding : 3000 

Note : All the Numbers are in GBP.

"""
client = OpenAI(base_url=OLLAMA_HOST)

response = client.chat.completions.create(
    model = "llama3.2",
    messages = [{'role' : 'system', 'content' : system_prompt}, {'role' : 'user', 'content' : user_prompt}]
)

markdown_output = response.choices[0].message.content
output_path = "financial_plan.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(markdown_output)

print(f"saved answer to {output_path}")
