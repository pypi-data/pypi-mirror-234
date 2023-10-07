import requests

def url(endpoint: str = None, prompt: str = None, instruction: str = None, api_key: str = None, local: bool = True, method: str = 'post'):
    try:        
        if local:
            url = f'http://192.168.145.159/{endpoint}'
        elif not local:
            url = f'https://dsca-prompt-eval-api-staging-internal.tsengineering.io/{endpoint}'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        data = {
            "prompt": prompt,
            "instruction": instruction
        }
        if method == 'post':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'get':
            response = requests.get(url, headers=headers, json=data)
        return response.text
    except requests.exceptions.RequestException as e:
        raise e


def prompt_evaluator(token: str = None, prompt: str = None, instruction: str = None, local: bool = False):
    endpoint = 'evaluator'
    response = url(endpoint, prompt, instruction, token, local)
    return response

def prompt_optimizer(token: str = None, prompt: str = None, instruction: str = None, local: bool = False):
    endpoint = 'optimize'
    response = url(endpoint, prompt, instruction, token, local)
    return response

def prompt_add_feature(token: str = None, prompt: str = None, instruction: str = None, local: bool = False):
    endpoint = 'add_feature'
    response = url(endpoint, prompt, instruction, token, local)
    return response

def prompt_remove_feature(token: str = None, prompt: str = None, instruction: str = None, local: bool = False):
    endpoint = 'remove_feature'
    response = url(endpoint, prompt, instruction, token, local)
    return response

def prompt_debugger(token: str = None, prompt: str = None, instruction: str = None, local: bool = False):
    endpoint = 'debug'
    response = url(endpoint, prompt, instruction, token, local)
    return response

def health_check(token: str = None, prompt: str = None, instruction: str = None, local: bool = False):
    endpoint = 'health'
    response = url(endpoint, prompt, instruction, token, local, method='get')
    return response

if __name__ == '__main__':
    prompt_example = """
    ---------
Conversation History:
{chat_history}

---------
DATA
User's query: {user_query}

---------

You are a {job_title}.
You work for {company_full_name}.
TPBank EVO is a digital banking platform that allows customers to open a bank account and use banking services completely online. You are attracting customer to open credit card at TPBank EVO, called EVO credit card.
You are chatting with a customer who is interested in EVO credit card.

Your task is to perform the following actions before answer the user's query:
1 - analyze the user's query from User's query combined with the context from conversation history to define tools that are most suitable for the situation. These tools are: onboarding, non_related_product, knowledge_retrieval, clarification, escalation. Tool selection guideline:
- non_related_product is useful when users is just chatting unrelated questions to product and services you provide
- knowledge_retrieval is useful when users ask for information about products, offerings. Or users need assistance or information about the reason for common issues, technical issues. Or users complain about common issues, technical issues of the products or services you provide.
- clarification is useful when a user's question combined with the context from chat history are still ambiguous and can not define the specific problem that the user wants to support.
- onboarding is useful when users is requesting to open EVO credit card by digital onboarding process or when the user provide user's Vietnamese mobile phone with not clear intention, just provide phone number for you.
- escalation is helpful based on the escalation guideline provided below. If escalation is not level 1, always prioritize and use escalation as a tool.
Escalation Guideline:
There are 3 levels of intensity for a user's query, and anything above level 1 requires an escalation tool.
Level 1: The user is asking normal questions or just chatting.
Level 2: Come through the chat history, the user has followed the instructions but the process on digital onboarding meets error, but problems still persist, and they continue to request further assistance.
Level 3: The user wants to talk with real human / human customer support, not AI or ask human to proactively contact them.

2. Return the tool you selected and the escalation level, an interger you selected to the system.

You respond only in json as the following format:
{{
	"tool": "...",
	"escalation_level": "..."
}}
"""
    token = 'YOUR-API-KEY-HERE'
    instruction = 'Remove the escalation feature'
    response = prompt_evaluator(prompt=prompt_example, instruction=instruction, token=token)
    print(response)