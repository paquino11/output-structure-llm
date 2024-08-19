# How to Get Structured Output from LLMs Applications Using Pydantic and Instrutor

This project demonstrates how to obtain consistent, structured output from Large Language Models (LLMs) using Pydantic and Instructor libraries. The example provided extracts key details from a software engineer's resume in PDF format and outputs the data in a structured JSON format.

## Installation

### Prerequisites

- Python 3.x
- API Key for [Anthropic API](https://console.anthropic.com/settings/keys)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/paquino11/output-structure-llm
cd output-structure-llm
```
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
3. Install the required packages:
```bash
pip install -r requirements.txt
```
4. Set up the environment variables:
- Create a `.env` file and add the following:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Usage
1. Ensure you have a resume.pdf file in the root directory of the project.
2. Run the script:
```bash
python3 output_structure.py
```
3. Check the output in the `resume.json` file.