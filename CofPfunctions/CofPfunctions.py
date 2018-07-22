from scipy import signal 
import numpy
from PyEMD import EMD
import neurokit

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

def getCenteredSummaryStatistics(CofP, df=1):
    '''
    Inputs:
        CofP: numpy nd array of type float with center of pressure data
    Outputs:
        minimum : float, minimum of the absolute/centered values 
        maximum : float, maximum of the absolute/centered values
        mean : float, mean of the absolute/centered values
        sd : float, standard deviation of the absolute/centered values. 
    Notes: 
    The minimum value is kind of useless and should essentially be at zero. 
    '''
    centeredCofP = CofP - CofP.mean()
    absCenteredCofP = abs(centeredCofP)
    minimum = numpy.min(absCenteredCofP)
    maximum = numpy.max(absCenteredCofP)
    mean = numpy.mean(absCenteredCofP)
    sd = numpy.std(absCenteredCofP, ddof=df)
    return(minimum, maximum, mean, sd)

def getRMS(data):
    '''
    Inputs:
        Data: numpy arrray with one-dimensional data
    Outputs:
        rms: float of the root mean square of the centered data
    '''
    return(numpy.sqrt(numpy.mean(numpy.square(data))))

def filterData(data, freqCutoff=20, samplingRate = 1000, order=2):
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
    if filter==True:
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
    if filter==True:
        CofPx = filterData(CofPx, freqCutoff=freqCutoff, samplingRate=samplingRate, order=order)
        CofPy = filterData(CofPy, freqCutoff=freqCutoff, samplingRate=samplingRate, order=order)
    diffX = numpy.diff(CofPx)
    diffY = numpy.diff(CofPy)
    distance = numpy.sqrt((numpy.square(diffX) + numpy.square(diffY)))
    absDistance = numpy.abs(distance)
    totalDistance = numpy.sum(absDistance)
    return(totalDistance)

def getFreqDataOfIMF(imf, samplingRate=1000/4):
    '''
    Inputs:
        imf: numpy arrray with one-dimensional data - individual IMF
    Outputs:
        medianFreq: numpy float of the dominant frequency of IMF
    '''
    spectrumOfData = abs(numpy.fft.fft(imf))
    freq = abs(numpy.fft.fftfreq(len(spectrumOfData), (1./samplingRate)))
    threshold =  numpy.sort((spectrumOfData))[-4]
    dominantData = freq[spectrumOfData > threshold]
    medianFreq = numpy.median(dominantData)
    return(medianFreq)

def EMDfilterData(data, samplingRate, lowerFreqCutoff=0.28,upperFreqCutoff=20):
    '''
    Inputs:
        Data: numpy arrray with one-dimensional data
    Outputs:
        filteredData: numpy array of data after filtering
    '''
    emd = EMD()
    IMFs = emd.emd(data)
    outputSignal = numpy.zeros_like(data)
    for imf in range(IMFs.shape[0]):
        imfFrequency = getFreqDataOfIMF(IMFs[imf,:])
        if imfFrequency > upperFreqCutoff:
            pass
        elif imfFrequency < lowerFreqCutoff:
            pass
        else:
            outputSignal += IMFs[imf,:]
    return(outputSignal)


def getMSE_coarse(data, r_fraction=0.15, max_scale_factor=20, m=2):
    '''
    Inputs:
        Data: numpy arrray with one-dimensional data
    Outputs:
        coarse_result: numpy array of sample entropy for each scale factor upto max_scale_factor. 
    '''
    r = r_fraction*numpy.std(data)
    dict_results = neurokit.complexity_entropy_multiscale(data, max_scale_factor=40, 
                                                           m=m, r=r)
    coarse_results = dict_results['MSE_Values']
    auc = dict_results['MSE_AUC']
    
    return(coarse_results, auc)


def filterGetMSE_coarse(data, r_fraction=0.15, max_scale_factor=20, 
                        m=2, pointsLastMSE =300, upperFreqCutoff=20, 
                        samplingRate=1000):
    '''
    Inputs:
        Data: numpy arrray with one-dimensional data
    Outputs:
        coarse_result: numpy array of sample entropy for each scale factor upto max_scale_factor.
        Data is filtered before performing analysis. 
    Notes:
    We used a default sampling rate of 100 Hz as this was deemed to be the minimum appropriaate based on the 
    paper by Gow. We are assuming that at most we want data with frequency content of 20Hz. Even though 
    This is much higher than most physiologic signals for human motion. We want to sample at 5 times this rate 
    to allow achievement of reconstruction of true signal. 
    '''
    trialLength = (1./float(samplingRate))*len(data)
    minimumDesiredSampling = upperFreqCutoff*5
    desiredSamplingRate = (float(pointsLastMSE)*float(max_scale_factor))/ (trialLength)
    if desiredSamplingRate < minimumDesiredSampling:
        desiredSamplingRate = minimumDesiredSampling

    lowerFreqCutoff = pointsLastMSE/(2*(m+1)*trialLength)

    downsampleFactor = numpy.ceil(float(samplingRate)/float(desiredSamplingRate)).astype(numpy.int)
    effectiveSamplingRate = samplingRate/downsampleFactor
    downsampledData = data[0::downsampleFactor]
    downsampledSamplingRate = samplingRate/downsampleFactor
    filtered_data = EMDfilterData(data, downsampledSamplingRate, 
                                  lowerFreqCutoff=lowerFreqCutoff,
                                  upperFreqCutoff=upperFreqCutoff)
    coarse_mse_result, auc_mse = getMSE_coarse(filtered_data, r_fraction=r_fraction, 
                                      max_scale_factor=max_scale_factor, m=m)
    return(coarse_mse_result, auc_mse, effectiveSamplingRate, lowerFreqCutoff)