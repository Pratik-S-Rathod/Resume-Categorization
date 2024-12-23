import os
import pandas as pd
import pickle
from pypdf import PdfReader
from docx import Document
import re
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load models
word_vector = pickle.load(open("tfidf.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)  
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

category_mapping = {
    15: "Java Developer",
    23: "Testing",
    8: "DevOps Engineer",
    20: "Python Developer",
    24: "Web Designing",
    12: "HR",
    13: "Hadoop",
    3: "Blockchain",
    10: "ETL Developer",
    18: "Operations Manager",
    6: "Data Science",
    22: "Sales",
    16: "Mechanical Engineer",
    1: "Arts",
    7: "Database",
    11: "Electrical Engineering",
    14: "Health and fitness",
    19: "PMO",
    4: "Business Analyst",
    9: "DotNet Developer",
    2: "Automation Testing",
    17: "Network Security Engineer",
    21: "SAP Developer",
    5: "Civil Engineer",
    0: "Advocate",
}

# Function to read .docx files
def read_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def categorize_resumes(uploaded_files, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    results = []
    resume_texts = []  # Store all resume texts for word cloud
    
    for uploaded_file in uploaded_files:
        file_extension = uploaded_file.name.split('.')[-1].lower()

        # Handle PDF files
        if file_extension == 'pdf':
            reader = PdfReader(uploaded_file)
            page = reader.pages[0]
            text = page.extract_text()

        # Handle DOCX files
        elif file_extension == 'docx':
            text = read_docx(uploaded_file)

        else:
            continue  # Skip unsupported file types

        cleaned_resume = cleanResume(text)
        resume_texts.append(cleaned_resume)  # Collect resume text for word cloud

        input_features = word_vector.transform([cleaned_resume])
        prediction_id = model.predict(input_features)[0]
        category_name = category_mapping.get(prediction_id, "Unknown")
        
        category_folder = os.path.join(output_directory, category_name)
        
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)
        
        target_path = os.path.join(category_folder, uploaded_file.name)
        with open(target_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        results.append({'filename': uploaded_file.name, 'category': category_name})
    
    results_df = pd.DataFrame(results)
    
    # Display graphs (category distribution, word cloud)
    plot_category_distribution(results_df)
    plot_word_cloud(resume_texts)
    
    return results_df

# Visualizations
def plot_category_distribution(results_df):
    category_counts = results_df['category'].value_counts()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_counts.index, y=category_counts.values, palette="viridis")
    plt.title("Resume Distribution by Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Resumes")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(plt)

def plot_word_cloud(text_data):
    text = ' '.join(text_data)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Streamlit UI
st.title("Resume Categorizer Application")
st.subheader("With Python & Machine Learning")

uploaded_files = st.file_uploader("Choose PDF or DOCX files", type=["pdf", "docx"], accept_multiple_files=True)
output_directory = st.text_input("Output Directory", "categorized_resumes")

if st.button("Categorize Resumes"):
    if uploaded_files and output_directory:
        # Store the results in session state
        st.session_state.results_df = categorize_resumes(uploaded_files, output_directory)
        st.session_state.output_directory = output_directory
        st.success("Resumes categorization and processing completed.")

# Ensure results exist before allowing filtering
if "results_df" in st.session_state:
    results_df = st.session_state.results_df
    
    # Filter by category
    st.write("### Filter Resumes by Category")
    categories = results_df['category'].unique()
    selected_category = st.selectbox("Choose a category", options=["All"] + list(categories))

    # Handle filtering logic
    if selected_category == "All":
        filtered_resumes = results_df  # Show all resumes
    else:
        filtered_resumes = results_df[results_df['category'] == selected_category]
    
    # Display filtered resumes
    st.write(f"### Resumes in Category: {selected_category}", filtered_resumes)
    
    # Download button for filtered results
    filtered_results_csv = filtered_resumes.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Results as CSV",
        data=filtered_results_csv,
        file_name=f"{selected_category}_resumes.csv",
        mime='text/csv',
    )
else:
    st.warning("Please categorize resumes before filtering.")
