import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Get started:
st.title("Hello, welcome to the Sarin-ai")

# Display a Simple Text
st.write("Upload a CSV file to generate a smooth line chart, histogram, or scatter chart with markers.")

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the DataFrame
    st.write("Here is the uploaded dataframe:")
    st.write(df)

    # Check if the DataFrame has numerical columns
    if df.select_dtypes(include=[np.number]).shape[1] > 0:
        # Option to choose between chart types
        chart_type = st.selectbox("Choose chart type", ["Line Chart", "Histogram", "Scatter Chart"])
        
        if chart_type == "Line Chart":
            # Melt the DataFrame to long format for Altair
            df_long = df.reset_index().melt(id_vars='index', var_name='variable', value_name='value')

            # Define the base chart
            base = alt.Chart(df_long).encode(
                x='index:O',
                y='value:Q'
            )

            # Define the line chart with smoothing
            line = base.mark_line(interpolate='monotone').encode(
                color='variable:N'
            )

            # Define the points with tooltips
            points = base.mark_point(filled=True).encode(
                color='variable:N',
                tooltip=['index:O', 'value:Q']
            ).interactive()

            # Combine line and points
            smooth_chart = line + points

            # Display the chart in Streamlit
            st.altair_chart(smooth_chart, use_container_width=True)

        elif chart_type == "Histogram":
            # Choose a column for histogram
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            selected_col = st.selectbox("Choose a column for histogram", numeric_cols)
            
            # Create a histogram
            hist = alt.Chart(df).mark_bar().encode(
                x=alt.X(selected_col, bin=alt.Bin(maxbins=30)),
                y='count():Q'
            ).properties(
                title=f'Histogram of {selected_col}'
            )

            # Add interactivity
            hover = alt.selection_single(on='mouseover', nearest=True, empty="none")
            points = alt.Chart(df).mark_point(filled=True).encode(
                x=alt.X(selected_col, bin=alt.Bin(maxbins=30)),
                y='count():Q',
                tooltip=[f'{selected_col}:Q', 'count():Q']
            ).add_selection(hover)

            # Combine histogram and interactive points
            hist_chart = hist + points

            # Display the histogram in Streamlit
            st.altair_chart(hist_chart, use_container_width=True)

        elif chart_type == "Scatter Chart":
            # Choose two columns for scatter chart
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            x_col = st.selectbox("Choose X column for scatter chart", numeric_cols)
            y_col = st.selectbox("Choose Y column for scatter chart", numeric_cols)
            
            # Create a scatter chart
            scatter = alt.Chart(df).mark_point(filled=True).encode(
                x=alt.X(x_col, title=x_col),
                y=alt.Y(y_col, title=y_col),
                tooltip=[x_col, y_col]
            ).interactive()

            # Add smooth line (regression line) to the scatter chart
            trend_line = alt.Chart(df).mark_line(color='red').transform_regression(
                x_col, y_col
            ).encode(
                x=x_col,
                y=y_col
            )

            # Combine scatter and trend line
            scatter_chart = scatter + trend_line

            # Display the scatter chart in Streamlit
            st.altair_chart(scatter_chart, use_container_width=True)
    else:
        st.write("The uploaded file does not contain numerical data for charts.")
else:
    st.write("Please upload a CSV file to see the charts.")
