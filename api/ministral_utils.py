from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
ministral_url = os.getenv("MINISTRAL_URL")

MODEL_ID = "mistralai/Ministral-3-3B-Instruct-2512"

client = OpenAI(
    base_url=ministral_url,
    api_key="not-needed"        # currently the Ministral service expects no auth
)

# Ministral-3 is running locally in a Docker container available at the URL specified in the .env file

def generate_rag_prompt(query: str, context):
    prompt = f"""
     ## SYSTEM ROLE
     You are a knowledgeable and factual chatbot designed to assist with questions about the rules of **Dungeons & Dragons**, 
     exclusively based on the context that you will be provided from the Player's Handbook.
     
     ## USER QUESTION
     The user has asked:
     "{query}"
     
     ## CONTEXT
     Here is the relevant context from the Player's Handbook:
     '''
     {context}
     '''
     
     #GUIDELINES
     1 **Accuracy**:
        - Only use the context provided in the CONTEXT section. 
        - If no answer is found, explicitly state "The provided context does not contain an answer to the question."
    2. **Transparency**:
        - Do not speculate or provide opinions.
    3. **Clarity**:
        - Use clear and concise language.
        - Format your response with limited markdown as following:
    
    ## RESPONSE FORMAT
    You may output Markdown using only:
    - paragraphs
    - **bold** and _italic_
    - ordered and unordered lists
    
    Do not use Markdown headings (#, ##, ###)
    Do not output HTML, links, images, code blocks, or inline styles.
    """

    return prompt

def get_rag_answer(query: str, context):
    """
    Uses the Ministral end-point to generate an answer based on the provided conxt
    :param query: User question
    :param context: Relevant context fetched from vector store
    :return: Generated answer in string format
    """
    prompt = generate_rag_prompt(query, context)

    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing answers based only on the provided context."},
            {"role": "user", "content": prompt}
        ]
    )

    return resp.choices[0].message.content


def generate_summary_context(notes: list[str]):
    prompt = f"""Summarise and combine the following notes:
    ## SYSTEM ROLE
    You are a helpful assistant designed to assist in note-keeping for **Dungeons & Dragons** by providing clear summaries
    of the notes from the players.
    
    ## NOTES
    Here are the notes the players have written that need to be summarised and combined. They are separated by --:
    '''
    {' -- '.join(notes)}
    '''
    
    #GUIDELINES
    1 **Accuracy**:
        - Only use the notes provided in the NOTES section. 
    2. **Transparency**:
        - Do not speculate or provide opinions.
    3. **Clarity**:
        - Use clear and concise language.
        - Format your response with limited markdown as following:
        
    ## RESPONSE FORMAT
    You may output Markdown using only:
    - paragraphs
    - **bold** and _italic_
    - ordered and unordered lists
    
    Do not use Markdown headings (#, ##, ###)
    Do not output HTML, links, images, code blocks, or inline styles.
    """

    return prompt

def generate_notes_summary(notes: list[str]):
    """
    Generate a summary of notes
    :param notes: List of notes to summarise
    :return: Generated summary of notes in string format
    """
    prompt = generate_summary_context(notes)

    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are helpful assistant creating simple summaries without injecting further information."},
            {"role": "user", "content": prompt},
        ]
    )

    return resp.choices[0].message.content