# How to Run the Streamlit Application Locally

Follow these steps to set up and run the provided Streamlit application on your local machine.

## Step 1: Set Up Your Environment

1. **Install Python**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Create a Virtual Environment**:
    ```sh
    python -m venv interview_assistant_env
    ```

3. **Activate the Virtual Environment**:
    
    - On macOS/Linux:
      ```sh
      source interview_assistant_env/bin/activate
      ```

## Step 2: Install Required Packages

1. **Install Required Python Packages**:
    ```sh
    pip install -r requirements.txt
    ```


## Step 3: Run the Application

1. **Run the Streamlit Application**:
    ```sh
    streamlit run streamlit.py
    ```

## Step 4: Use the Application

1. **Open the Application in Your Browser**: After running the above command, a local web server will start, and Streamlit will automatically open a new tab in your default web browser pointing to `http://localhost:8501`.

2. **Enter the Required Information**:
    - **OpenAI API Key**: Enter your OpenAI API key.
    - **Resume**: Paste your resume in the provided text area.
    - **Job Offer URL**: Enter the URL of the job offer.
    - **Start the Conversation**: Click the "Start Conversation" button to generate interview questions and start the interview simulation.



     
