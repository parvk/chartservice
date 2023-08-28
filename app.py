from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain import PromptTemplate, LLMChain
import openai
from chartTypes import chartTypes


app = Flask(__name__)
CORS(app)

# llm = OpenAI(openai_api_key="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")

openai.api_key = "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"

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

# Endpoint for uploading a file
@app.route('/get_chart_type', methods=['POST'])
def get_chart_type():
    data = request.json
    # Process the uploaded file and generate the desired JSON response
    # template = """Question: {data}
    #     Answer: Let's think step by step."""


    question = """You’re now an expert in Recharts library. You’re tasked with using recharts library. Can you return an array of objects as a JSON formatted string that are is relevant to an arbitrary data. Do not include any explanations, only provide a RFC8259 compliant JSON response with following properties as requirements
        REQUIREMENTS:
        - Each object in the array should contain 3 keys: component, usage, helpText
        - component is the actual component name of the chart used in recharts library
        - usage is a summary text on how it can be used in context of the given input
        - helptext is slight detailed version of usage
        \n
        Here is the arbitrary data...\n\n{}\n
        """.format(data)
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    resp = llm ([HumanMessage (content=question)])

    response = {
        "message": "File uploaded successfully",
        "data": resp.content  # You can modify this according to your processing logic
    }
    return jsonify(response)

# Endpoint for selecting chart type
@app.route('/get_chart_code', methods=['POST'])
def select_chart_type():
    data = request.get_json()
    chart_type = data.get("chartType")
    sample_data = data.get("sampleData")
    usage = data.get("usage")
    question = """You’re now an expert in Recharts library. We need to build {} chart, based on the following data \n {} \n for usecase {}.
        \n
        Only output code for it, do not include any explanations.
        """.format(chart_type,sample_data, usage)
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    resp = llm ([HumanMessage (content=question)])

    # Process the selected chart type and generate the desired JSON response
    response = {
        "message": "Chart code outputed",
        "data": resp.content  # You can modify this according to your processing logic
    }
    return jsonify(response)

# Endpoint for updating chart
@app.route('/update_chart', methods=['POST'])
def update_chart():
    data = request.get_json()
    chart_type = data.get("chartType")
    sample_data = data.get("sampleData")
    usage = data.get("usage")
    code = data.get("code")
    op = data.get("op")
    question = """You’re now an expert in Recharts library. We built {} chart, based on the following data \n {} \n for usecase {}.
        \n
        Following is the working code for it \n
        {}
        \n
        Can you modify this code to do following operation on the chart's code: \n
        {} \n
        Note: Strictly operate on above supplied code, modify it and return the modified code 
        Also, do not include any explanations.
        """.format(chart_type,sample_data, usage, code, op)
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    resp = llm ([HumanMessage (content=question)])

    # TODOPK - Run through pipeline to check if the code is correct 

    # Process the selected chart type and generate the desired JSON response
    response = {
        "message": "Chart code outputed",
        "data": resp.content  # You can modify this according to your processing logic
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
