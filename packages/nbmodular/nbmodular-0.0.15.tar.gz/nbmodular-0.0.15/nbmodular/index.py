def days (df, fy, x=1, /, y=3, *, n=4):

    df_group = df.groupby(['Year','Month']).agg({'Day': lambda x: len (x)})
    df_group = df.reset_index()
    print ('other args: fy', fy, 'x', x, 'y', y)
    return df_group

def index_pipeline (test=False, load=True, save=True, result_file_name="index_pipeline"):

    # load result
    result_file_name += '.pk'
    path_variables = Path ("index") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result

    df_group = days (y)

    # save result
    result = Bunch (df_group=df_group)
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result
