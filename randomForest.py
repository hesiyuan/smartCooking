from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

reg = RandomForestClassifier(max_depth=5, random_state=0)


#construct a list for each example
file = open("centerPointsData3.txt", "r") 
X = []
y = []
j = 0
for line in file:
	example = line.split()
	# construct a list for the example excluding the label
	l = []
	i = 0
	for data in example:
		if i == 10:
			y.append(int(data))
		else:
			l.append(float(data))
		i = i + 1   
	X.append(l)
	j = j + 1

#ut all lists into a big list
# print(j, end=" ")
print("data examples ready")

#construct a list for all labels

#traniing
reg.fit(X, y)
#LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
print(reg.get_params())
print(reg.predict(X))
print(reg.score(X,y))
joblib.dump(reg, 'randomForest_v2.pkl', protocol=2) 
# clf = joblib.load('model.pkl') 
# print(clf.predict([[199.0, 199.0, 78.03135367296292, 72.125, 129.25, 65.57003514400586]]))



