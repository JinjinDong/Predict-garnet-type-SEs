import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix,roc_curve, auc

# EAH
df = pd.read_csv("EAH.csv")
X = df.drop('Energy Above Hull', axis=1)
y = df['Energy Above Hull']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#XGBoost
params = {
    'max_depth': 3,
    'learning_rate': 0.05,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'n_estimators': 100,
    'objective': 'binary:logistic',
    'min_child_weight': 1,
    'lambda': 1,
    'alpha': 0,
    'seed': 45,
    'verbosity': 1,
}



xgb_model = xgb.XGBClassifier(**params, eval_metric="logloss")
cv = 10
stratified_kf = StratifiedKFold(n_splits=cv)

for fold, (train_index, test_index) in enumerate(stratified_kf.split(X_train, y_train)):
    X_train_fold, X_test_fold = X_train.iloc[train_index], X_train.iloc[test_index]
    y_train_fold, y_test_fold = y_train.iloc[train_index], y_train.iloc[test_index]

    # train
    xgb_model.fit(X_train_fold, y_train_fold, eval_set=[(X_test_fold, y_test_fold)], verbose=0)
    # predict
    y_pred_proba = xgb_model.predict_proba(X_test_fold)[:, 1]
    y_pred_class = (y_pred_proba > 0.5).astype(int)

    # Calculate true case Rate (TPR) and False Positive Case Rate (FPR)
    fpr, tpr, thresholds = roc_curve(y_test_fold, y_pred_proba)
    # Calculate the value of the AUC-ROC
    roc_auc = auc(fpr, tpr)

    classification_report_str = classification_report(y_test_fold, y_pred_class)
    confusion_matrix_str = confusion_matrix(y_test_fold, y_pred_class)
    print(f"Fold {fold + 1} - Classification Report:\n{classification_report_str}\n")
    print(f"Fold {fold + 1} - Confusion Matrix:\n{confusion_matrix_str}\n")
    print(f"Fold {fold + 1} - AUC:\n{roc_auc}\n")