# Resume_Categorization_Application

This application uses Machine Learning to automatically categorize resumes based on their content. It accepts PDF and DOCX files, processes them using a pre-trained model, and classifies them into predefined categories such as "Data Science", "Java Developer", "HR", and many others. Additionally, users can filter and download categorized resumes in CSV format.

Features
File Upload: Upload multiple PDF and DOCX files.
Resume Categorization: Automatically categorize resumes into different job categories based on content using a pre-trained model.
Category Distribution: Visualize resume distribution by category using bar charts.
Word Cloud: Generate a word cloud for all the resumes to visualize commonly used words.
Filter by Category: Filter the results by selecting a specific category from a dropdown.
CSV Download: Download categorized results in CSV format for further analysis.
Technologies Used
Python: The primary programming language.
Streamlit: For the user interface and app framework.
Scikit-learn: For machine learning model and vectorization (TF-IDF).
Matplotlib/Seaborn: For visualizations like bar charts.
WordCloud: To generate word clouds for the uploaded resumes.
Pandas: For data handling and manipulation.
PyPDF2: For reading PDF files.
python-docx: For reading DOCX files.

<h2>To run this project use the fillowing steps:</h2>

1) Install anaconda
2) Download project and store on your location
3) open the spyder from the anaconda set the path
4) open the anaconda prompt and give the path with command "cd"
5) After reaching at the project directory use command **stramlit run app.py**
6) if streamlit is not installed then install it first
7) after running above command you can run the project
