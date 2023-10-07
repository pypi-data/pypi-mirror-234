# Assemble mock pipelines here.
from vectorshift.node import * 
from vectorshift.pipeline import *
from vectorshift.deploy import Config

# An expressly simple pipeline that just runs a LLM.
input = InputNode(name="input_1", input_type="text")
text = TextNode(text="Hello!")
llm = OpenAILLMNode(
    model="gpt-3.5-turbo",
    system_input=text.output(),
    prompt_input=input.output(),
    max_tokens=4096,
    top_p=1.,
    temperature=1.
)
output = OutputNode(name="output_1", output_type="text", input=llm.output())

simple_pipeline = Pipeline(
    name="Pipeline Test",
    description="test",
    nodes=[input, text, llm, output]
)

print(simple_pipeline.to_json())

# Email generator. A copy of https://docs.vectorshift.ai/vectorshift/example-pipelines/personalized-email-generator
question_text = TextNode(text="How can this company grow?")

system_text_raw = """You are a personalized sentence generator for a consulting firm. You take in data from a website and generate personalized sentence that explains how the consulting firm can help this company based on a question. Limit your response to 1 sentence. Present your sentence as a recommendation by using the first person.

Example output: For example, we can help improve your enterprise offering by defining the customer profile and making a list of potential customers."""
system_text = TextNode(text=system_text_raw)

input = InputNode(name="input_1", input_type="text")
url_loader = URLLoaderNode(url_input=input.output())
vdb_loader = VectorDBLoaderNode(input=url_loader.output())
vdb_reader = VectorDBReaderNode(
    query_input=question_text.output(), 
    database_input=vdb_loader.output()
)

prompt_text_raw = """Company Context: {{Context}}
Question: {{Question}}"""
prompt_text = TextNode(
    text=prompt_text_raw,
    text_inputs={
        "Context": vdb_reader.output(),
        "Question": question_text.output()
    }
)

llm = OpenAILLMNode(
    model="gpt-4", 
    system_input=system_text.output(), 
    prompt_input=prompt_text.output()
)

output_text_raw = """Hello,
We are XYZ consulting firm that specializes in crafting growth strategies for companies. {{Personalized_Message}}

Are you available anytime later this week to chat?

Best,
XYZ"""
output_text = TextNode(
    text=output_text_raw,
    text_inputs={
        "Personalized_Message": llm.output()
    }
)

output = OutputNode(
    name="output_1", 
    output_type="text", 
    input=output_text.output()
)

email_gen_pipeline_nodes = [
    question_text, system_text, input, url_loader, vdb_loader, vdb_reader,
    prompt_text, llm, output_text, output
]

email_gen_pipeline = Pipeline(
    name="Email Generator-inator 3000",
    description="foo bar baz",
    nodes=email_gen_pipeline_nodes
)

p_json = email_gen_pipeline.to_json_rep()
print(p_json)
print(email_gen_pipeline.to_json())

vs = Config(
    public_key="foo",
    private_key="bar"
)

response = vs.save_pipeline(email_gen_pipeline)
print(response)
