def bunch_data():
    x = Bunch (a=1, b=2)
    return x
def bunch_processor(x, day):
    a = x["a"]
    b = x["b"]
    c = 3
    a = 4
    x["a"] = a
    x["c"] = c
    x["day"] = day
    return x
def myf (a=1,
         b=2,
         c=3):
    
    print ('hello')

def index_pipeline (test=False, load=True, save=True, result_file_name="index_pipeline"):

    # load result
    result_file_name += '.pk'
    path_variables = Path ("index") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result

    x = bunch_data ()
    x = bunch_processor (x, day)
    myf (a, b, c)

    # save result
    result = Bunch (x=x)
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result
