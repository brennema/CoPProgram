from scipy import signal 
import numpy

def getDistance_Coverage(CofP, percent_coverage):
    '''
    Inputs:
        CofP: numpy nd array of type float with center of pressure data
        percent_coverage: numpy float representing percentage of points in coverage
    Outputs:
        distance: numpy float object of distance from center which covers the 
        specified percent_coverage
    '''
    centeredCofP = CofP - CofP.mean()
    absCenteredCofP = abs(centeredCofP)
    indexOfCoverage = numpy.ceil(len(absCenteredCofP)*percent_coverage).astype(numpy.int)
    distance_coverage = numpy.sort(absCenteredCofP, kind='mergesort')[indexOfCoverage]
    return(distance_coverage)

def filterData(data, freqCutoff=20, samplingRate=1000, order=2):
    '''
    Inputs:
        Data: numpy arrray with one-dimensional data
    Outputs:
        filteredData: numpy array of data after filtering
    '''
    Wn = (freqCutoff / 0.82)/(samplingRate/2)
    b, a = signal.butter(order, Wn)
    filteredData = signal.filtfilt(b,a,data)
    return(filteredData)
    
def getDistanceCofP(CofP, filter=True, freqCutoff=20, samplingRate=1000, order=2):
    '''
    Inputs:
        CofP: numpy nd array of type float with center of pressure data
    Outputs:
        distance: numpy float object of distance traveled. 
    '''
    if filter == True:
        CofP = filterData(CofP, freqCutoff=freqCutoff, samplingRate=samplingRate, order=order)
    
    diff = numpy.diff(CofP)
    absDiff = numpy.abs(diff)
    distance = numpy.sum(absDiff)
    return(distance)

def getDistanceBothAxes(CofPx, CofPy, filter=True, freqCutoff=20, samplingRate=1000, order=2):
    '''
    Inputs:
        CofPx: numpy nd array of type float with center of pressure data
        CofPy: numpy nd array of type float with cneter of pressure data
    Outputs:
        distance: numpy float object of distance traveled - over both directions 
    '''
    if filter == True:
        CofPx = filterData(CofPx, freqCutoff=freqCutoff, samplingRate=samplingRate, order=order)
        CofPy = filterData(CofPy, freqCutoff=freqCutoff, samplingRate=samplingRate, order=order)
    diffX = numpy.diff(CofPx)
    diffY = numpy.diff(CofPy)
    distance = numpy.sqrt((numpy.square(diffX) + numpy.square(diffY)))
    absDistance = numpy.abs(distance)
    totalDistance = numpy.sum(absDistance)
    return(totalDistance)