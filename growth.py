import streamlit as st
import pandas as pd
import os 
from io import BytesIO

st.set_page_config(page_title="Mind Set Challenges", layout = "wide")
 
#Styling the background and text

st.markdown(
    """
<style>
.stApp{
background: white;
color: black;
}
.css-1v0mbdj p{
color: #ffffff;
}
.stButton>button {
background-color: #4CAF50;
color: white;
border: none;
border-radius: 8px;
padding: 10px 20px;
font-weight: bold;
}
.stDownloadButton>button {
background-color: #4CAF50;
color: white;
border-radius: 8px;
padding: 10px 20px;
}
</style>
""",
unsafe_allow_html= True
)

# Header section

st.title("🧹 Data sweeper Starting Agency")
st.write("🚀 Transform your files between any object pacing")

# File uploader
uploaded_files = st.file_uploader(
    "📤 Upload your files (CSV or Excel only):", 
    type=["csv", "xlsx", "json", "parquet"], 
    accept_multiple_files=True
)
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

    try:
        # Load data
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        elif file_ext == ".json":
             df = pd.read_json(file)
        elif file_ext == ".parquet":
             df = pd.read_parquet(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
           
        # Show preview

        st.write("🔎 Preview the **{file.name}**")  
        st.dataframe(df.head()) 

        st.subheader("🧹 Data Cleaning Option")
        if st.checkbox(f"clean data for **{file.name}**"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🧽 Remove duplicates from the file: {file.name} "):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates REmoved!")

            with col2:
                if st.button(f"🩹 File missing Value for {file.name}"):
                    numeric_cols = df.select_dtypes(includes=["number"]).columns        
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values filled!")

        st.subheader("🧩 Select columns to keeps")
        columns = st.multiselect(f"📌Choose columns for {file.name}" , df.columns, default=df.columns)
        df = df[columns]  

        st.subheader(" 📊 Data Visualization") 
        if st.checkbox(f"📈 Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2]) 

        st.subheader("🔁 Conversion Option")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CVS" , "Excel" , "JSON", "Parquet"], key=f"Convert_{file.name}")
        if st.button(f"🔄 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to.csv(buffer, index = False)  
                file_name = file.name.replace(file_ext, ".csv") 
                mime_type = "text/csv"   

            elif conversion_type == " Excel":
                df.to.to_excel(buffer, index= False)
                file_name = file.name.replace(file_ext, ".xlsx") 
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif conversion_type == "JSON":
                buffer.write(df.to_json(orient= "records").encode("utf-8"))
                file_name = file.name.replace(file_ext, ".json")
                mime_type = "application/json"
            elif conversion_type == "Parquet":
                df.to_parquet(buffer, index= False) 
                file_name = file.name.replace(file_ext, ".parquet")
                mime_type = "application/octet-stream"           
            buffer.seek(0)

            st.download_button(
                label= f" 📥 Download {file.name} as {conversion_type}",
                data = buffer,
                file_name= file_name,
                mime= mime_type
            )  
    except Exception as e:
            st.error(f"❌ Error processing {file.name}: {e} ")
st.balloons()
st.success("🎉 All files processed successfully!")          