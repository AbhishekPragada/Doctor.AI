from lime import lime_tabular
from flask import Flask, render_template, request
import pickle, numpy as np


with open('60_important_features_rf_fml.pkl', mode='rb') as f:
  fairml_features=pickle.load(f)

with open('rf_fml_model.pkl', mode='rb') as f:
  rf_fml=pickle.load(f)

with open('class_names.pkl', mode='rb') as f:
  class_names=pickle.load(f)

with open('x_train.pkl', 'rb') as f:
  x_train=pickle.load(f)

app=Flask(__name__, template_folder='templates', 
          static_folder='static')

train=x_train[fairml_features]

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
  if request.method=='POST':
    symptoms=request.form.getlist('checkbox_values')

    final, test_vector=[],[]
    for symptom in symptoms:
      if symptom in fairml_features:
        final.append(symptom)

    for feature in fairml_features:
      if feature in final:
        test_vector.append(1)
      else:
        test_vector.append(0)

    test_vector=np.array(test_vector)
    label=class_names[rf_fml.predict(test_vector.reshape(1,-1))]
    explainer=lime_tabular.LimeTabularExplainer(training_data=train.values, class_names=class_names, feature_names=fairml_features, categorical_features=range(len(train.columns))) #categorical_features=final_rf_features)
    exp = explainer.explain_instance(test_vector, rf_fml.predict_proba, num_features=10, top_labels=1)
    exp = exp.as_html()
    
    return render_template('results.html', explainer_=exp,  output=", ".join(symptoms), class_=label[0].title())

if __name__ == "__main__":
  app.run(debug=True)