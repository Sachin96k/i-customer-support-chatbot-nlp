# Project Report: AI-Based Customer Support Chatbot Using Natural Language Processing (NLP)

## 1. Introduction
Customer-support teams receive many repeated questions about delivery, refunds, cancellations, product information, and account access. Responding to every question manually can take time. This project demonstrates a chatbot that classifies a customer's message and returns a relevant prepared answer.

## 2. Problem Statement
Manual customer support can be slow for common queries and may require staff to repeat the same information. A lightweight automated assistant can answer routine questions quickly and direct unfamiliar queries toward a human support channel.

## 3. Objectives
- Build a simple web-based chatbot.
- Apply NLP text features to customer messages.
- Classify messages into predefined intent categories.
- Return appropriate responses from a knowledge base.
- Provide a fallback when the message is unfamiliar.
- Demonstrate a modular Python project that can be extended.

## 4. Scope
The prototype covers greetings, order tracking guidance, shipping, delivery estimates, returns, refunds, cancellations, payment problems, account help, product information, warranty questions, and contacting human support. It does not retrieve real order status or process transactions.

## 5. Technologies Used
- Python: backend and model-training code.
- Flask: HTTP routes and web application.
- Scikit-learn: TF-IDF vectorization and Logistic Regression classification.
- JSON: intent patterns and prepared responses.
- HTML: page structure.
- CSS: responsive styling.
- JavaScript: send messages to the backend without reloading the page.
- Joblib: save and load the trained model.

## 6. System Architecture
The user enters a message in the browser. JavaScript sends the text to the Flask `/chat` endpoint. The backend normalizes whitespace, passes the message to the trained pipeline, and reads the highest predicted class probability. If confidence is below the configured threshold, the chatbot returns a fallback answer. Otherwise, it selects a response associated with the predicted intent and returns JSON to the browser.

## 7. Methodology
1. Collect example questions for each customer-support intent.
2. Store patterns and responses in `intents.json`.
3. Convert training text to TF-IDF numerical features.
4. Train Logistic Regression on the intent labels.
5. Save the trained pipeline to the `models` folder.
6. Load the model when Flask starts.
7. Receive messages through the chat interface.
8. Predict intent and select a response.
9. Test the web routes and common error conditions.

## 8. Installation and Execution
Install dependencies using `python -m pip install -r requirements.txt`. Run `python train.py` to train and save the model. Run `python app.py` to start the local web server. Open `http://127.0.0.1:5000` in a browser. For automated tests, run `python -m unittest discover -s tests`.

## 9. Testing Plan
| Test case | Input/action | Expected result |
|---|---|---|
| Home page | Open `/` | Chat interface loads |
| Greeting | Enter “Hello” | Greeting response |
| Order query | Enter “Where is my order?” | Order guidance |
| Empty message | Submit whitespace | Prompt to enter a message |
| Long message | Submit over 1000 characters via API | HTTP 400 error |
| Invalid JSON type | Send a number as message | HTTP 400 error |
| Unfamiliar question | Enter unrelated text | Fallback may be returned |

Actual model predictions can vary because this is a small demonstration dataset. Test and record observed outputs on the machine used for submission.

## 10. Advantages
- Provides quick answers for common questions.
- Available through a simple browser interface.
- Can be expanded by adding intents and patterns.
- Separates the user interface, backend, model, and response data.
- Demonstrates practical use of NLP and machine learning.

## 11. Limitations
- The training dataset is small.
- A classifier can confuse similar questions.
- The confidence score is not a guarantee of correctness.
- There is no live order lookup, authentication, database, or agent dashboard.
- The prepared responses may not cover every customer question.

## 12. Future Enhancements
- Add a larger, representative and reviewed training dataset.
- Add database-backed support tickets and order lookup with proper authentication.
- Integrate an agent handoff workflow.
- Add multilingual support.
- Add feedback collection and model evaluation.
- Add analytics dashboards, monitoring, rate limiting, and deployment security.
- Evaluate precision, recall, F1 score, and confusion matrix on a held-out dataset.

## 13. Conclusion
This project shows how a simple NLP intent classifier can support routine customer service. TF-IDF converts text into numerical features, Logistic Regression predicts an intent, and Flask returns a corresponding prepared response to a browser-based chat interface. The project is suitable as a learning prototype and can be extended into a more complete support platform after dataset improvement, evaluation, security review, and integration with real business systems.
