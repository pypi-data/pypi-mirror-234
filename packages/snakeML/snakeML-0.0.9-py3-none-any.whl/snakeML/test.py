from loads import loadData
import numpy
from preprocessing import oneHotEncoding
from visualization import histogram_attributeVSfrequency, scatter_attributeVSattribute

data, labels=loadData('iris.csv',separator=',', labels=True, row_attributes=True, numpyDataType=numpy.float32)
new_labels,label_dict=oneHotEncoding(labels, return_dictionary=True)
#print(label_dict)
features=['Sepal length', 'Sepal width', 'Petal length','Petal width']
print(data)
scatter_attributeVSattribute(data, new_labels,features, label_dict, row_attributes=True, is_label_dict=True, dense=True)