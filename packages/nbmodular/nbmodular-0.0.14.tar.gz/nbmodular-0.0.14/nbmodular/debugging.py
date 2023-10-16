
def debugging_pipeline (test=False, load=True, save=True, result_file_name="debugging_pipeline"):

    # load result
    result_file_name += '.pk'
    path_variables = Path ("debugging") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result


    # save result
    result = Bunch ()
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result
