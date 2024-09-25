import streamlit as st
import pickle
import numpy as np

# Load the data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Function to recommend books
def recommend_books(book_title):
    recommended_books = []
    recommended_authors = []
    recommended_images = []
    
    if book_title in pt.index:
        index = np.where(pt.index == book_title)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            recommended_books.append(temp_df['Book-Title'].values[0])
            recommended_authors.append(temp_df['Book-Author'].values[0])
            recommended_images.append(temp_df['Image-URL-M'].values[0])
    else:
        st.error("Book not found in the database.")
    
    return recommended_books, recommended_authors, recommended_images

# Streamlit UI
st.header('Book Recommendation System')

# Book selection
book_list = pt.index.tolist()
selected_book = st.selectbox("Type or select a book from the dropdown", book_list)

# Display recommendations
if st.button('Show Recommendations'):
    recommended_books, recommended_authors, recommended_images = recommend_books(selected_book)
    if recommended_books:
        cols = st.columns(5)
        for col, book, author, image in zip(cols, recommended_books, recommended_authors, recommended_images):
            with col:
                st.image(image)
                st.text(book)
                st.text(f"by {author}")
                
