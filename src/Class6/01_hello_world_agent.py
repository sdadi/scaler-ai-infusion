from strands import Agent, tool
from strands.modes.bedrock import BedrockModel
from strands_tools import calculator
from config import NOVA_LITE

model = BedrockModel(model_id=NOVA_LITE)
agent = Agent(model=model)

response = agent.run("Hello!, Tell mea fun fact  about AI agents")
print (response)