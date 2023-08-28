from flask import Flask, request, jsonify
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
import openai

app = Flask(__name__)

llm = OpenAI(openai_api_key="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")

openai.api_key = "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"

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

# Endpoint for uploading a file
@app.route('/upload_data', methods=['POST'])
def upload_data():
    data = request.json
    # Process the uploaded file and generate the desired JSON response
    # template = """Question: {data}
    #     Answer: Let's think step by step."""

    question = 'Study all the charts present in recharts library. You’re now an expert. Maintain list of all charts available with recharges assigning them by their unique module name. Now based on following data: /n {}. Suggest which charts will best represent following data? Also, only output code and no comments. Each chart component should be seperated by 3 x ==='.format(data)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])
    response = {
        "message": "File uploaded successfully",
        "data": chat_completion  # You can modify this according to your processing logic
    }
    return jsonify(response)

# Endpoint for selecting chart type
@app.route('/select_chart_type', methods=['POST'])
def select_chart_type():
    data = request.json
    # Process the selected chart type and generate the desired JSON response
    response = {
        "message": "Chart type selected",
        "data": data  # You can modify this according to your processing logic
    }
    return jsonify(response)

# Endpoint for updating chart
@app.route('/update_chart', methods=['POST'])
def update_chart():
    data = request.json
    # Process the chart update request and generate the desired JSON response
    response = {
        "message": "Chart updated successfully",
        "data": data  # You can modify this according to your processing logic
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
