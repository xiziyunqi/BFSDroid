from sklearn.datasets import load_iris
import xgboost as xgb
from xgboost import plot_importance
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy
# read in the iris data
#iris = load_iris()
import codecs
import json
#qita fenlei suanfa
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
svc = SVC(kernel='rbf', class_weight='balanced',)
c_range = np.logspace(-5, 15, 11, base=2)
gamma_range = np.logspace(-9, 3, 13, base=2)
# 网格搜索交叉验证的参数范围，cv=3,3折交叉
param_grid = [{'kernel': ['rbf'], 'C': c_range, 'gamma': gamma_range}]
grid = GridSearchCV(svc, param_grid, cv=3, n_jobs=-1)
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
#from sklearn.grid_search import GridSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
import matplotlib.pylab as plt
from sklearn.ensemble import GradientBoostingClassifier



with codecs.open("xunlianji_1.json","r",'utf-8') as fid_json:
	xunlianji_dic=json.load(fid_json)

ben_pd1=pd.read_csv("ben_data_opcode_4000.csv")
ben_pd2=pd.read_csv("ben_permission_4000.csv")
print(ben_pd1.shape)
print(ben_pd2.shape)
ben = pd.concat([ben_pd1, ben_pd2],axis = 1)

mal_pd1=pd.read_csv("mal_data_opcode_4000.csv")
mal_pd2=pd.read_csv("mal_permission_4000.csv")
mal = pd.concat([mal_pd1, mal_pd2],axis = 1)

print(ben.shape)
print(mal.shape)

ben_mal = pd.concat([ben, mal],axis = 0)

juzhen=[]
labels=[]
la=0
for k,v in xunlianji_dic.items():
	la+=1
	juzhen=juzhen+v
	for i in range(len(v)):
		labels.append(la)
features=numpy.array(juzhen)
features=numpy.array(ben_mal)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
print(type(features))
print(type(labels))
labels=[]
for i in range(1978):
	labels.append(0)
for i in range(1987):
	labels.append(1)
 
X = numpy.array(features)
print(features.shape)
y = numpy.array(labels)
print(type(X))
print(type(y))
print(X)  
print(y)
print(len(X))
print(len(y))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)



#knn
from sklearn import neighbors
from sklearn import datasets

model = neighbors.KNeighborsClassifier()
model = GridSearchCV(svc, param_grid, cv=3, n_jobs=-1)
#不管任何参数，都用默认的，拟合下数据看看
#model = RandomForestClassifier()
#model = GradientBoostingClassifier(n_estimators=3000)
# 训练模型 
# 训练模型
#model = xgb.XGBClassifier(max_depth=5, learning_rate=0.1, n_estimators=1200, silent=True, objective='multi:softmax')
model.fit(X_train, y_train)
 
# 对测试集进行预测
ans = model.predict(X_test)
 
# 计算准确率
cnt1 = 0
cnt2 = 0
for i in range(len(y_test)):
    if ans[i] == y_test[i]:
        cnt1 += 1
    else:
        cnt2 += 1
 
print("Accuracy: %.2f %% " % (100 * cnt1 / (cnt1 + cnt2)))
 
from sklearn import metrics
y_predict_gb = ans 

precision_score_gb = metrics.precision_score(y_test, y_predict_gb, average="micro")
recall_score_gb = metrics.recall_score(y_test, y_predict_gb, average="micro")
f1_score_gb = metrics.f1_score(y_test, y_predict_gb, average="micro")
accuracy_score_gb = metrics.accuracy_score(y_test, y_predict_gb)
auc_score_gb = metrics.roc_auc_score(y_test, y_predict_gb, average="micro")


print(precision_score_gb,recall_score_gb,accuracy_score_gb,f1_score_gb,auc_score_gb)
fjieguo=open("xgbm_z_300.txt","w")
fjieguo.write(str(precision_score_gb))
fjieguo.write(str(recall_score_gb))
fjieguo.write(str(accuracy_score_gb))
fjieguo.write(str(f1_score_gb))

# 显示重要特征
a=[]
a.append(cnt1) 
a.append(cnt2)
# 显示重要特征
with codecs.open("jieguo_800.json","w",'utf-8') as fid_jsonakl11:
	json.dump(a,fid_jsonakl11,ensure_ascii=False)