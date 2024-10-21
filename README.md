# Document/Text Correction Application

This project is a **Document/Text Correction Application** built using **LangChain** and **Gradio**. It provides two input options for the user: uploading a PDF document or entering text manually. The application then identifies grammatical mistakes and rewrites the text to enhance its quality, ensuring it is clear, concise, and impactful. Users can select from multiple output styles such as `Standard`, `Natural`, `Formal`, and `Fluency`.

## Features

- **PDF File Upload**: Users can upload PDF files, which are split into chunks for processing.
- **Text Input**: Users can directly enter text to be corrected and rewritten.
- **Text Correction**: Identifies grammatical errors and provides corrections.
- **Text Rewriting**: Rewrites the text based on the user's selected style:
  - **Standard**: Rewrites text with new vocabulary and word order.
  - **Natural**: Rewrites text in a more human, conversational tone.
  - **Formal**: Rephrases text in a more sophisticated, formal style.
  - **Fluency**: Improves the clarity and readability of the text.

## Technologies Used

- **LangChain**: For handling document loading, splitting, text processing, and running multiple tasks in parallel.
- **Gradio**: Provides an easy-to-use web interface for uploading files, entering text, and viewing results.
- **OpenAI GPT**: Used for generating grammar corrections and rewriting the text based on user preferences.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/document-text-correction.git
   cd document-text-correction
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key**:
   You will need an OpenAI API key to run the project. Set your API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

   Alternatively, you can set the API key directly in your Python code:
   ```python
   import os
   os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'
   ```

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Open the Gradio interface**:
   After running the above command, a URL will be provided in the terminal (e.g., `http://127.0.0.1:7860/`). Open this URL in your browser to access the Gradio web interface.

3. **Select Input Mode**:
   - Choose either **PDF File** or **Text Input** mode.
   - If **PDF File** is selected, upload a PDF file for correction.
   - If **Text Input** is selected, enter the text to be corrected in the provided textbox.

4. **Select Output Style**:
   - Select one of the output styles from the dropdown: `Standard`, `Natural`, `Formal`, `Fluency`.

5. **Get Results**:
   - The corrected and rewritten text will be displayed in the interface, along with an explanation of the corrections.

## Project Structure

- **main.py**: The main application file that contains the logic for handling inputs, grammar correction, rewriting, and interaction with the Gradio interface.
- **requirements.txt**: A list of required Python libraries.
- **README.md**: This readme file, explaining the project setup and usage.

## Code Overview

1. **Document Loading and Splitting**:
   - PDF documents are loaded and split into chunks using `PyPDFLoader` and LangChain’s `RecursiveCharacterTextSplitter`.

2. **Grammar Correction**:
   - The text is corrected for grammatical errors using OpenAI's GPT models.

3. **Text Rewriting**:
   - The corrected text is rewritten based on the selected style (`Standard`, `Natural`, `Formal`, `Fluency`).

4. **Parallel Processing**:
   - For PDF files, the document chunks are processed in parallel using LangChain’s `RunnableParallel` to speed up the correction and rewriting process.

## Example

Here’s a quick example of how the application works:

1. **Text Input Mode**:
   - Input: `Helo am fine wat are you doin`
   - Output (Fluency style):
     ```
     Result:
     Hello, I am fine. What are you doing?

     Explanation: This text has been corrected for grammar and improved for fluency.
     ```

2. **PDF File Mode**:
   - Upload a PDF with similar content.
   - Output: The PDF content is corrected in a similar format, with explanations provided for each chunk of corrected text.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License.
