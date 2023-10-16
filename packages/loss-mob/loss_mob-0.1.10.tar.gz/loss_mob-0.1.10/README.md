#### Introduction

To mimic the py\_mob package (https://pypi.org/project/py-mob) for binary outcomes, the loss\_mob is a collection of python functions that would generate the monotonic binning and perform the variable transformation for loss or severity such that the Spearman correlation between the transformed $X$, i.e. $F(X_i)$, and $E(Y_i | X_i)$ is equal to 1. In case of loss models with $Ln()$ link function, the transformation is derived as $F(x)_i = Ln \frac{\sum_i Y / \sum_i Exposure}{\sum Y / \sum Exposure}$ in the training sample, where $Exposure$ is the number of cases and $i$ refers to the $ith$ bin groupped by $x$ values.  

Should you have any question or suggestion about the package, please feel free to drop me a line. 

#### Core Functions

```
loss_mob
  |-- qtl_bin()  : Iterative discretization based on quantiles of X.  
  |-- los_bin()  : Revised iterative discretization for records with Y > 0.
  |-- iso_bin()  : Discretization driven by the isotonic regression. 
  |-- val_bin()  : Revised iterative discretization based on unique values of X.  
  |-- rng_bin()  : Revised iterative discretization based on the equal-width range of X.  
  |-- kmn_bin()  : Iterative discretization based on the k-means clustering of X.  
  |-- gbm_bin()  : Discretization based on the gradient boosting machine (GBM).  
  |-- cus_bin()  : Customized discretization based on pre-determined cut points.  
  |-- view_bin() : Displays the binning outcome in a tabular form. 
  |-- cal_newx() : Applies the variable transformation to a numeric vector based on the binning outcome.
  |-- chk_newx() : Verifies the transformation generated from the cal_newx() function.
  |-- mi_score() : Calculates the Mutual Information (MI) score between X and Y.
  |-- screen()   : Calculates Spearman and Distance Correlations between X and Y.
  |-- gini()     : Calculates the gini-coefficient between X and Y.
  |-- smape()    : Calculates the sMAPE value between Y and Yhat.
  `-- get_mtpl() : Extracts French Motor Third-Part Liability Claims dataset from OpenML.
```

#### Example

```python
import loss_mob as mob

# LOAD THE DATASET
data = mob.get_mtpl()

data.keys()
# dict_keys(['idpol', 'claimnb', 'exposure', 'area', 'vehpower', 'vehage', 'drivage', 
# 'bonusmalus', 'vehbrand', 'vehgas', 'density', 'region', 'claimamount', 'purepremium'])

var = ['vehpower', 'vehage', 'drivage', 'bonusmalus', 'density']

# SCREEN EACH VARIABLE OF INTEREST
rst = [{"variable": _, **mob.screen(data[_], data["purepremium"])} for _ in var]

# RANK VARIABLES BY DISTANCE CORRELATION
for _ in sorted(rst, key = lambda x: -abs(x["distance correlation"])):
  print(_)

# {'variable': 'bonusmalus', 'total records': 678013, 'nonmissing records': 678013, 'missing percent': 0.0, 'unique value count': 115, 'coefficient of variation': 0.26165082, 'spearman correlation': 0.05716908, 'distance correlation': 0.0434537}
# {'variable': 'drivage', 'total records': 678013, 'nonmissing records': 678013, 'missing percent': 0.0, 'unique value count': 83, 'coefficient of variation': 0.31071883, 'spearman correlation': -0.004906, 'distance correlation': 0.01428907}
# {'variable': 'density', 'total records': 678013, 'nonmissing records': 678013, 'missing percent': 0.0, 'unique value count': 1607, 'coefficient of variation': 2.20854394, 'spearman correlation': 0.02022122, 'distance correlation': 0.01106909}
# {'variable': 'vehage', 'total records': 678013, 'nonmissing records': 678013, 'missing percent': 0.0, 'unique value count': 78, 'coefficient of variation': 0.80437458, 'spearman correlation': 0.01952645, 'distance correlation': 0.01080137}
# {'variable': 'vehpower', 'total records': 678013, 'nonmissing records': 678013, 'missing percent': 0.0, 'unique value count': 12, 'coefficient of variation': 0.31774149, 'spearman correlation': 0.00230745, 'distance correlation': 0.00356986}

# GENERATE BINNING BASED ON GBM FOR EACH VARIABLE
bout = dict((v, mob.gbm_bin(data[v], data["purepremium"])) for v in var)
mob.view_bin(bout["vehage"])

# |  bin  |   freq |   miss |           ysum |     yavg |        newx |         rule              |
# |-------|--------|--------|----------------|----------|-------------|---------------------------|
# |   1   | 356354 |      0 | 114686591.4672 | 321.8333 | -0.17468183 | $X$ <= 6                  |
# |   2   | 194371 |      0 |  69559830.5303 | 357.8714 | -0.06854178 | $X$ > 6 and $X$ <= 12     |
# |   3   | 127288 |      0 |  75609359.3214 | 594.0023 |  0.43816751 | $X$ > 12                  |

# VARIABLE TRANSFORMATION
dout = mob.cal_newx(data['vehage'], bout["vehage"])
mob.head(dout)

# {'x': 1, 'bin': 1, 'newx': -0.17468183}
# {'x': 5, 'bin': 1, 'newx': -0.17468183}
# {'x': 0, 'bin': 1, 'newx': -0.17468183}

# VALIDATE THE TRANSFORMATION
mob.chk_newx(dout)

# |  bin  |        newx |   freq |    dist    |         xrng              |
# |-------|-------------|--------|------------|---------------------------|
# |   1   | -0.17468183 | 356354 |   52.5586% |                  0 <==> 6 |
# |   2   | -0.06854178 | 194371 |   28.6677% |                 7 <==> 12 |
# |   3   |  0.43816751 | 127288 |   18.7737% |               13 <==> 100 |
```

####  Authors

[WenSui Liu](mailto:liuwensui@gmail.com) is a seasoned data scientist with 15-year experience in the financial service industry. 

[Joyce Liu](mailto:joyce.jl.liu@gmail.com) is a college student majoring in Mathematics with a strong passion for data science.
