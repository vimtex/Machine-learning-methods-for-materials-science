import pickle
import numpy as np
from atomic_constants import pauling, radius, Zval, Eatom, Emadelung, charge, mus
from read_json import read_json, get_elements_map
from split_dataset import *
from ml import *

mset = read_json("data.json")
mtest, mset = get_testset(mset)
mtrain, mcross, mset = get_train_validation_set(mset)
elmap = get_elements_map(mset)


#print "knn MAE", knn_regression(mtrain, mcross, 5)
for elmethod in (None, "composition", #"constant", 
                 #"coordination", "inverse_cord", 
                 "coulomb_ZiZj/d", 
                 "coulomb_1/d",):
    print elmethod
    print "knn MAE", knn_regression(mtrain, mcross, 5, elmap=elmap, elmethod=elmethod)
    print "krr MAE", krr_regression(mtrain, mcross, 50, 0.01, elmap=elmap, elmethod=elmethod)
    print "forest", sklearn_regression(mtrain, mcross, "forest", elmap=elmap, elmethod=elmethod)  
    print "svr",    sklearn_regression(mtrain, mcross, "svr", elmap=elmap, elmethod=elmethod)  











    

