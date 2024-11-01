from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import sys
import json
import re

# Define input-output pairs
responses = {
    "hi": "Hello!",
    "cse syllabus": "You can find the CSE syllabus here: <a href='https://crescent.education/university/schools/school-of-computer-information-and-mathematical-sciences/department-of-computer-science-and-engineering/programmes-approved-2/' target='_blank'>CSE Syllabus Link</a>",
    "Lost and found": "You can find the Lost and found in crescent college here: <a href='https://crescentlostandfound.netlify.app' target='_blank'>LOST AND FOUND LINK</a>",
    " student affairs Dean Details" : "You can find the Studentaffairs Dean Details here: <a href='https://crescent.education/student-affairs/about-student-affairs/' target='_blank'>Student Affairs Dean</a>",
    "bye": "Goodbye!"
}

# Predefined inputs for vectorization
input_questions = list(responses.keys())

# Create the CountVectorizer instance and fit it on the input questions
count_vectorizer = CountVectorizer()
count_vectorizer.fit(input_questions)

def get_response(user_input):
    user_vector = count_vectorizer.transform([user_input])
    similarities = np.dot(user_vector.toarray(), count_vectorizer.transform(input_questions).T.toarray())
    best_match_index = np.argmax(similarities)
    
    if similarities[0][best_match_index] > 0:
        response = responses[input_questions[best_match_index]]
        # Check if the response contains a URL and format it as an HTML anchor tag
        return response
    else:
        return "I'm sorry, I don't understand that."

if __name__ == "__main__":
    # Read input from command line
    user_input = sys.argv[1]
    response = get_response(user_input)
    print(json.dumps({"response": response}))
