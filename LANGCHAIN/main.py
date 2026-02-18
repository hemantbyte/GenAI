import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from pprint import pprint
load_dotenv()

assert os.getenv("GROQ_API_KEY")
assert os.getenv("LANGSMITH_API_KEY")

# Initialize the ChatGroq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7, #it handles the randomness of the output, higher values (e.g., 0.8) make the output more random, while lower values (e.g., 0.2) make it more focused and deterministic.
    max_tokens=2048, #it limits the maximum number of tokens in the generated response. This helps control the length of the output and can prevent excessively long responses. 
    timeout = 30, #it specifies the maximum time (in seconds) that the model will take to generate a response.If the model takes longer than this time, it will stop and return whatever it has generated so far. This is useful for preventing long waits in case of complex queries or issues with the model.
    max_retries=3, #it defines the maximum number of times to retry a request if it fails due to network issues or other transient errors. This helps improve the robustness of your application by allowing it to recover from temporary problems without crashing.
)

# Create a chat prompt template
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant."),
#     ("user", "{text}")
# ])

# # Format the prompt with user input
# response = llm.invoke([
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "What is Generative ai?."}
# ])
# print(response.content)

# Create an agent with the LLM
agent = create_agent(llm)

# response = agent.invoke([
#     SystemMessage(content="You are a helpful assistant."),
#     HumanMessage(content="What is Generative ai?.")
# ])
response = agent.invoke(
    {"messages": [HumanMessage(content="What is the capital of the Moon?"),
    AIMessage(content="The capital of the Moon is luna city."),
    HumanMessage(content="Intresting, can you tell me more about luna city?")]})

pprint(response)
# print(response['messages'][-1].content)