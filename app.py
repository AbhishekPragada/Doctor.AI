app=Flask(__name__, template_folder='templates', 
          static_folder='static')

# app=Flask(__name__, template_folder='your_name_for_template_folder')
# start ngrok when flask is made to run

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
    # print(final)

    for f in fairml_features:
      if f in final:
        test_vector.append(1)
      else:
        test_vector.append(0)
    # print(test_vector)

    test_vector=np.array(test_vector)
    label=class_names[rf_fml.predict(test_vector.reshape(1,-1))]
    explainer=lime_tabular.LimeTabularExplainer(training_data=train.values, class_names=class_names, feature_names=fairml_features, categorical_features=range(len(train.columns))) #categorical_features=final_rf_features)
    exp = explainer.explain_instance(test_vector, rf_fml.predict_proba, num_features=10, top_labels=1)
    exp = exp.as_html()
    # print(label)
    
    return render_template('results.html', explainer_=exp,  output=", ".join(symptoms), class_=label[0].title())

app.run()