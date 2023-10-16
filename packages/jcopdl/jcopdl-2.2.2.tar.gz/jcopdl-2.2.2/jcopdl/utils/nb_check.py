def in_colab():
    "Check if the code is running in Google Colaboratory"
    try:
        from google import colab
        return True
    except: 
        return False


def in_notebook():
    "Check if the code is running in a jupyter notebook"
    if in_colab():
        return True
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell': # Jupyter notebook, Spyder or qtconsole
            import IPython
            # IPython version lower then 6.0.0 don't work with output you update
            return IPython.__version__ >= '6.0.0'
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

IN_NOTEBOOK = in_notebook()
