'''
Author: Nathan Sturdivant (for funsies)
basic calculator attempt, using turtle for GUI(tbd), should basically just do my stats hw for me lol
Currently planning on including no rounding except for in final returns for large
functions, rounding has to be to a decimal prompted because the requirements change for each hw problem

Long term goal convert it to run on a basic html page I can send to classmates and stuff idk, idk anything about pyodide so it's gonna need JS

Credit: csv files provided by ChatGPT interpereting PDFs of the individual tables provided for the class-that's the only bit of vibe coding I promise

To Do: add start prompt for global rounding variable, i.e. 2 vs 4, that can be called into any function,
bring in t values with degrees of freedom, maybe just a function that prompts for t value, requiring manual table search

'''

import math
import csv

#calc functions:
def standardError(deviation, sampleSize):
    '''
    divide the standard deviation by the square root of the sample size
    ex:
    >>>standardError(10,5)
    >>>4.4721...
    '''
    denom = math.sqrt(sampleSize)
    numer = deviation
    return (numer / denom)

def zScore(M, deviation, sM, sampleSize):
    '''
    calculates z score - use sample size of 1 if not looking at a sample distribution, in which case sample mean is just 'observed'
    ex:
    >>>zScore(11, 10, 14, 5)
    >>>11.54...
    '''
    SE = standardError(deviation, sampleSize)
    numerator = sM - M

    return (numerator / SE)

def pValue(z):
    '''
    Looks up P value from the z_table, asks for tails and whether to subtract from 1.
    ex:
    >>>pValue(1.02)
    >>>"Your P Value is: 0.8461"
    '''
    try:
        z = round(float(z), 2)
        if abs(z) > 3.49:
            print("Z-score out of range. Table only covers -3.49 to +3.49.")
            return None

        # Use symmetry for negative z-scores
        if z < 0:
            pNum = 1 - z_table.get(abs(z), 0.0)
        else:
            pNum = z_table.get(z, 0.0)

        tail = int(input("How many tails? (1 or 2): "))
        sub = input("Do we need to subtract the P Value from 1? (y/n): ").strip().lower()

        if sub == "y":
            pNum = 1 - pNum

        if tail == 2:
            pNum *= 2

        print("Your P value is:", round(pNum, 4))
        return pNum

    except ValueError:
        print("Invalid input. Please enter a numeric Z-score.")
        return None


def getZStar(confidence_level, tails):
    '''
    Returns the critical z-value from table_c for the given confidence level and tails (1 or 2).
    '''
    try:
        key = "one-tailed" if tails == 1 else "two-tailed"
        zStar = table_c[key][confidence_level]
        print("Z*: ", zStar)
        return zStar
    except KeyError:
        print("Invalid confidence level or tail count.")
        return None

def marginError(sE):
    '''
    Calculate margin of error using user-supplied confidence level and tails.
    '''
    try:
        cLevel = float(input("What confidence level are you testing? (e.g. 0.95): "))
        tails = int(input("How many tails? (1/2): "))
        zStar = getZStar(cLevel, tails)
        if zStar is None:
            return None
        mE = round(zStar * sE, 4)
        print("Your Margin of Error: ", mE)
        return mE
    except ValueError:
        print("Invalid input.")
        return None


def confidenceInterval(sampleMean, deviation, sampleSize):
    '''
    Finds the confidence interval using margin of error and standard error.
    '''
    sE = standardError(deviation, sampleSize)
    mE = marginError(sE)
    lowerBound = round(sampleMean - mE, 4)
    upperBound = round(sampleMean + mE, 4)
    print("Your Confidence Interval is: [", lowerBound, ",", upperBound, "]")
    return (lowerBound, upperBound)

def reject(p, a):
    '''
    check if we reject or fail to reject the null hypothesis (H0), compares two parameters as a boolean
    ex:
    >>>reject(0.0439, 0.05)
    >>>Your P value is less than the Significance level, so in this case we can reject the null hypothesis
    '''
    reject = (p < a)
    if reject == True:
        print("Your P value is less than the Significance level, so in this case we can reject the null hypothesis")
    elif reject == False:
        print("Your P value is greater than the Significance level, so in this case we fail to reject the null hypothesis")
    
    return reject

def problemToP():
    '''prompts user for necessary variables'''
    popMean = float(input("Enter the Population Mean:"))
    popSD = float(input("Enter the Population Standard Deviation:"))
    n = int(input("Enter the sample size:"))
    sampleMean = float(input("Enter the Sample Mean:"))
    z = zScore(popMean, popSD, sampleMean, n)
    pResult = pValue(z)
    
    return pResult

def fullHypTest():
    pVal = problemToP()
    sigLvl = float(input("At what Significance level should we test?"))
    reject(pVal, sigLvl)
    runItBack = input("Would you like to test at a different significance level? (y/n)")
    while runItBack == "y":
        sigLvl = float(input("At what Significance level should we test?"))
        reject(pVal, sigLvl)
        runItBack = input("Would you like to test at a different significance level? (y/n)")

    return

def problemToBounds():
    '''
    prompts user from basic data to a confidence interval in [x, y] format
    '''
    #popMean = float(input("Enter the Population Mean:"))
    popSD = float(input("Enter the Population Standard Deviation:"))
    n = int(input("Enter the sample size:"))
    sampleMean = float(input("Enter the Sample Mean:"))
    confidenceInterval(sampleMean, popSD, n)




#driver functions:
def key():
    print("Key:")
    print("-problemToP() to run through an entire problem set with prompts")
    print("-Individual steps can be performed through:")
    print("-standardError(standard deviation, sample size)")
    print("-zScore(population Mean, Standard deviation, Observed mean/sample mean, sample size(just put 1 if n/a))")
    print("-pValue(z score)")
    print("-reject(p value, a value)")
    print("-fullHypTest() will run through an entire problem from basic data to a rejection analysis")
    print("-marginError(standard Error) will prompt you to find the z* and multiply it by the provided standard error")
    print("-problemToBounds() to be prompted through getting confidence intveral [] (note: always state 2 tails)")
    
    return

def start():
    print("If you need to start over at any point just type 'start()' :D")
    popUp = input("Would you like to see a key of functions you can perform?(y/n)")
    if popUp == "y":
        key()
    
    return

#driver:
start()

#Table A / Table C arrays / csvs
def load_z_table(filename='z_table_full.csv'):
    z_table = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            z_table[float(row['z'])] = float(row['p'])
    return z_table  

def load_table_c():
    return {
        "one-tailed": {
            0.80: 0.841,
            0.85: 1.036,
            0.90: 1.282,
            0.95: 1.645,
            0.96: 1.960,
            0.98: 2.054,
            0.99: 2.326,
            0.995: 2.576,
            0.999: 3.091
        },
        "two-tailed": {
            0.80: 1.282,
            0.90: 1.645,
            0.95: 1.96,
            0.96: 2.054,
            0.98: 2.326,
            0.99: 2.576,
            0.995: 2.807,
            0.999: 3.291
        }
    }

#global scope z table
z_table = load_z_table()  
table_c = load_table_c()



#In Progress: would it be better to calc for p value ala excel?
def tTest():
    '''prompts user for necessary variables'''
    popMean = float(input("Enter the Population Mean:"))
    popSD = float(input("Enter the Population Standard Deviation:"))
    n = int(input("Enter the sample size:"))
    sampleMean = float(input("Enter the Sample Mean:"))
    t = zScore(popMean, popSD, sampleMean, n)
    conLvl = float(input("At what Significance level should we test? (90, 95 etc.)"))
    tTest(n, conLvl)
    est_tValue(t, degFreedom)
    
    return

'''
def est_tValue(tScore, degFreedom):

    #provide confidence level as a whole number without % sign-not decimal like in other functions

    conLvl = float(input("At what Significance level should we test? (90, 95 etc.)"))

    return
'''
def tTest(sampleSize, conLevel):
    '''
    returns table c result for deg freedom x confidence level
    '''
    degFree = sampleSize - 1
    try:
        tVal = table_t[conLevel][degFree]
        print("t: ", tVal)
        return zStar
    except KeyError:
        print("Invalid confidence level or sample size")
        return None



t_table = load_t_table()
def load_t_table():
    '''
    degrees of freedom:p value
    '''
    return {
        "80":{
            1: 3.078,
            2: 1.886,
            3: 1.638,
            4: 1.533,
            5: 1.476,
            6: 1.440,
            7: 1.415,
            8: 1.397,
            9: 1.383,
            10: 1.372,
        },
        "90":{
            1: 6.314,
            2: 2.920,
            3: 2.353,
            4: 2.132,
            5: 2.015,
            6: 1.943,
            7: 1.895,
            8: 1.860,
            9: 1.833,
            10: 1.812,
        },
        "95":{
            1: 12.71,
            2: 4.303,
            3: 3.182,
            4: 2.776,
            5: 2.571,
            6: 2.447,
            7: 2.365,
            8: 2.306,
            9: 2.262,
            10: 2.228,
        },
        "96":{
            1: 15.89,
            2: 3.849,
            3: 3.482,
            4: 2.999,
            5: 2.757,
            6: 2.612,
            7: 2.517,
            8: 2.449,
            9: 2.398,
            10: 2.359,
        },
        "98":{
            1: 31.82,
            2: 6.965,
            3: 4.541,
            4: 3.747,
            5: 3.365,
            6: 3.143,
            7: 2.998,
            8: 2.896,
            9: 2.821,
            10: 2.764,
        },
        "99":{
            1: 63.66,
            2: 9.925,
            3: 5.841,
            4: 4.604,
            5: 4.032,
            7: 3.499,
            8: 3.355,
            9: 3.250,
            10: 3.169,
        },

    }
