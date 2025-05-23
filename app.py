import streamlit as st
import numpy  as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder,StandardScaler,OneHotEncoder
import pandas as pd
import pickle
model = tf.keras.models.load_model('model.h5')

with open('model_files/label_encoder_gender.pkl','rb') as file:
    label_encoder = pickle.load(file)

with open('model_files/one_hit_encoder_geo.pkl','rb') as file:
    one_hot = pickle.load(file)

with open('model_files/scalar.pkl','rb') as file:
    scalar = pickle.load(file)

st.title("customer churn prediction")

geography = st.selectbox('Geography',one_hot.categories_[0])
gender = st.selectbox('Gender',label_encoder.classes_)
age = st.slider('Age',18,92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_Salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure',0,10)
num_of_products = st.slider('Number of Products',1,4)
has_cr_card = st.selectbox('Has Credit Card',[0,1])
is_Active_member = st.selectbox('Is Active Member',[0,1])

input_data = pd.DataFrame({
    'CreditScore' : [credit_score],
    'Gender' : [label_encoder.transform([gender])[0]],
    'Age': [age],
    'Tenure' : [tenure],
    'Balance':[balance],
    'NumOfProducts':[num_of_products],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_Active_member],
    'EstimatedSalary':[estimated_Salary]
})

geo_encoded = one_hot.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded,columns=one_hot.get_feature_names_out(['Geography']))
input_data = pd.concat([input_data.reset_index(drop=True),geo_encoded_df],axis=1)
input_data_scaled = scalar.transform(input_data)

#predict churn

prediction = model.predict(input_data_scaled)
pred_prob = prediction[0][0]
if pred_prob > 0.5:
    st.write('the customer will likely to churn')
else:
    st.write('the customer will not likely to churn')