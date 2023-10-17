from multiprocessing import Pool

def runMultiProcess(job, rTe, rtau_e, *args):
    """!
    Run a job across multiple processes. 
    A job needs to be specified, given a range of electron temperatures.

    @params job Function to run in parallel.
    @params rTe Range of electron temperatures to run in parallel
    """


