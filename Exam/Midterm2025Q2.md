# Midterm Project: Quant Modeling for Data Scientists   
`Model and slides due on Oct 29th 2025 before Class`  

### I. Why Real Modeling?
  - As a budding modeler with exceptional talent, the midterm exam serves as a dynamic simulation of your future journey as a quant economist or data scientist. This is your opportunity to craft innovative models and showcase your analytical prowess. The insights derived from your quantitative modeling will not only demonstrate your skills but also illuminate the path toward a thriving and impactful career in the field. Embrace this challenge—it’s a stepping stone to your future success.   


### II. Workflow

 ##### 1. Data location: 

 - Data: https://datahub.ruc.edu.cn/org/RUC/dataset/68f359f07a0e19b0ec2ad308/file
 - Kaggle Hackathon participation link: https://www.kaggle.com/t/5eb48d87e3dc48ef9c99e53aa8dc0163

 ##### 2. Data Processing: 

  - data analysis, data clean, and data preprocessing (Please refer to  Ch2 codes from our textbook and my slides)  
  - delete the features with data leakage issues such as community price in the housing project
  - divide the sample into 80% training and 20% testing by using sklearn.model_selection.train_test_split (random_state==111)


 ##### 3. Feature Engineering:

  - create new features: log transformation, polynomial features, interaction terms, binning, dummies, and etc. 
  - feature selection: use correlation, VIF, Lasso and etc. to select the features
  - outlier detection and treatment: use IQR, Z-score, and etc. 
<div class="alert alert-block alert-danger">
<b>Caution:</b> No Data Leakage Here
</div>

##### 4. Modeling (Individual):

  - You must use linear models: **Linear Regression, Lasso, Ridge regression, Elastic Net**
  - Fine-tune model: try to improve your model by 1) add and drop features, 2) add non-linearity and interactions, 3) change hyperparameters (L1 and L2 regularizers) of model 
  - You can use sklearn.linear_model and sklearn.model_selection.GridSearchCV to fine-tune your model
  - Report both your: in-sample, out of sample and [6 folds cross validation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html) model performance for your OLS, LASSO, Ridge and best model (please use Mean Absolute Error, RMAE to report the performance). Also, please report the total number of predictions after you remove the outlier of the sample.  

  
- `In your presentation you need to show the metrics table below`:  

| Metrics| In sample | out of sample | Cross-validation |Kaggle Score |
| --- | --- | --- | --- | --- | 
| OLS | 0.94 |0.92 | 0.92 | 60 |
| LASSO | 0.94 |0.92 | 0.92 |61 |
| Best Linear Model | 0.94 |0.92 | 0.92 |62 |
| Any Other Model (Not Required) | 0.94 |0.92 | 0.92 |61 |


Note: `Metrics should be MAE for the original housing **price level or rent level**`  

##### 5. Modeling Merging (Group):
  - Merge your codes into one for the presentation and the final presentation
  - You can use the best model from your teammates as basemodel and incorprate your other models to improve the performance
  - In the presentation, you should attach the performances of your teammates' models and your merged model, so totally 5tables

   
### III. Submission      
   
1. Git submission (individual, before Oct 29th):   
    - Codes: **Midterm_codes_StudentID.ipynb**
           

    
2. kaggle submission (Individual, before presentation Oct 29th)    
    - Scoring: **prediction.csv**
    - **!!!This score is not for midterm grading!!!**, `your presentation and modeling matters`
    - https://www.kaggle.com/t/5eb48d87e3dc48ef9c99e53aa8dc0163


3. Git submission (in group folder Oct 29th):
    - Slides: **Midterm_slides_GroupID.pdf** ( 4 slides, not counts on the frontpage, each person only 1 slide)
    - Slides: **Midterm_Performance_GroupID.pdf** (performance of your teammates' models and your merged model, so totally 5 tables)
    - Merge your codes into one and for the next homework model validation
    - Codes: **Midterm_codes_Team1a.ipynb** 
   
#### IV. Real Presentation
-  Presentation (**!!!Important!!!**): 
- `Presentation is important`, it is a simulation of the job interview for the quant researcher, data scientist, and economist position (As young talents, please show your talents)
- You should **highline** the `innovations` during the presentation 
- Your score `only depends` on the contents and innovations mentioned by your presentations, but your presentation should be backed by your codes and results (!!!Your results should be checked during the presentation!!!)
- Only talk keys points
- Only Linear Algorithms in midterm (OLS, LASSO, Ridge and etc., but you can use fancy feature engineering)
- max 4 slides (not counts on the frontpage)
- `6 min` presentation and `8 questions` to check your works, innovations and other key points, each person only 1 slide 
- penalties for the long presentation or slides: up to 5% off  




- Due date: EOD Oct 29th 2025 
-------

