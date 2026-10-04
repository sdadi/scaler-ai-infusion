from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from llm import create_model

model = RunnableLambda(lambda prompt_value: create_model().invoke(prompt_value))
parser = StrOutputParser()

classify_prompt = ChatPromptTemplate.from_template(
    "Classify this shipment exception as exactly one label: delayed, damaged, lost, "
    "or unknown. Use unknown if the report is unclear or does not describe a "
    "shipment exception. Return only the label.\n\nReport: {report}"
)
escalate_prompt = ChatPromptTemplate.from_template(
    "Write a concise internal note for a Northwind Logistics manager. Include the "
    "exception category, shipment value,  proposedcompensation, policy reason, "
    "and customer report. State that a manager decision is required.\n\n"
    "Category: {category}\nShipment value: ${shipment_value:.2f}\n"
    "Proposed compensation: ${compensation_amount:.2f}\nReason: {reason}\n"
    "Customer report: {report}"
)
draft_email_prompt = ChatPromptTemplate.from_template(
    "Draft a concise, empathetic customer email about this shipment exception. "
    "Explain the category and compensation clearly, and do not promise anything "
    "beyond the stated compensation.\n\nCategory: {category}\n"
    "Compensation: ${compensation_amount:.2f}\nReason: {reason}\n"
    "Customer report: {report}"
)

classify_chain = classify_prompt | model | parser
escalate_chain = escalate_prompt | model | parser
draft_email_chain = draft_email_prompt | model | parser