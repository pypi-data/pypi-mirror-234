def days (df, fy):
    if True:
    
        df_group = df.groupby(['Year','Month']).agg({'Day': lambda x: len (x)})
        df_group = df.reset_index()
    return df_group

def Untitled_pipeline (test=False, load=True, save=True, result_file_name="Untitled_pipeline"):

    # load result
    result_file_name += '.pk'
    path_variables = Path ("Untitled") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result

    df_group = days (df, fy)

    # save result
    result = Bunch (df_group=df_group)
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result
