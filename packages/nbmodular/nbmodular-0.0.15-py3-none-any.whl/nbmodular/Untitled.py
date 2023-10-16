def f (x, y, z=3, w=4):

    print (x, y, z)

def Untitled_pipeline (test=False, load=True, save=True, result_file_name="Untitled_pipeline"):

    # load result
    result_file_name += '.pk'
    path_variables = Path ("Untitled") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result

    f (x, y, z, w)

    # save result
    result = Bunch ()
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result
