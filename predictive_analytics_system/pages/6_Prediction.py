import streamlit as st

from utils.prediction import predict_business


# Page Configuration

st.set_page_config(
    page_title="Business Prediction",
    page_icon="🤖",
    layout="wide"
)


# Title

st.title("🤖 Business Success Prediction")
st.markdown(
    """
    Use Machine Learning to predict the business performance level
    based on Google Maps business information.
    """
)

st.divider()


# Input Section

st.subheader("📌 Enter Business Details")

col1, col2 = st.columns(2)


with col1:
    category = st.selectbox(

        "Business Category",
        [
            "Restaurant",
            "Hotel",
            "Cafe",
            "Shopping",
            "Healthcare",
            "Education",
            "Services",
            "Other"
        ]
    )

    area = st.text_input(
        "Area / Locality",
        placeholder="Enter area or locality"
    )

    rating = st.number_input(
        "Google Rating",
        min_value=0.0,
        max_value=5.0,
        value=4.0,
        step=0.1
    )

with col2:

    reviews = st.number_input(
        "Total Reviews",
        min_value=0,
        value=100,
        step=10
    )

    website = st.selectbox(
        "Website Available",
        [
            "Yes",
            "No"
        ]
    )

st.divider()

# Prediction

if st.button(
    "🚀 Predict Business Performance",
    use_container_width=True
):

    if area.strip() == "":
        st.warning(
            "Please enter Area / Locality."
        )

    else:

        try:

            result = predict_business(
                category,
                area,
                rating,
                reviews,
                website
            )

            prediction = result["prediction"]
            confidence = result["confidence"]

            st.subheader(
                "📊 Prediction Result"
            )

            col1, col2 = st.columns(2)

            with col1:
                if prediction == "High":
                    st.success(
                        f"""
                        ⭐ Business Potential
                        ## {prediction}
                        """
                    )

                elif prediction == "Medium":

                    st.warning(
                        f"""
                        ⭐ Business Potential
                        ## {prediction}
                        """
                    )

                else:
                    st.error(
                        f"""
                        ⭐ Business Potential
                        ## {prediction}
                        """
                    )

            with col2:

                st.metric(
                    "Model Confidence",
                    f"{confidence}%"

                )

            st.divider()

            st.subheader(
                "💡 Recommendation"
            )


            if prediction == "High":

                st.write(
                    """
                    ✅ Strong business potential.

                    Recommendations:
                    - Maintain customer satisfaction
                    - Increase online presence
                    - Collect more reviews
                    - Improve digital marketing
                    """
                )


            elif prediction == "Medium":

                st.write(
                    """
                    ⚠️ Moderate business potential.

                    Recommendations:
                    - Improve ratings
                    - Increase customer engagement
                    - Add website/social media presence
                    """
                )

            else:

                st.write(
                    """
                    ❌ Business needs improvement.

                    Recommendations:
                    - Improve service quality
                    - Respond to reviews
                    - Increase customer visibility
                    """
                )


        except Exception as e:
            st.error(
                f"Prediction Error: {e}"
            )