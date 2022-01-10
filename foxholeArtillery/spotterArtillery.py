# %%
import pandas as pd
import math
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)
pd.set_option('display.max_colwidth', None)


# %%
def findTSGAngle(spotterToTargetAzimuth, spotterToGunAzimuth):
    azimuthArray = [spotterToTargetAzimuth, spotterToGunAzimuth]
    aziMin = min(azimuthArray)
    aziMax = max(azimuthArray)    


    if (aziMax - aziMin) >= 180:
        return 360 - (aziMax - aziMin)
    else:
        return (aziMax - aziMin)
    
# print(findTSGAngle(250,103))


# %%
def findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance):
    dST = spotterToTargetDistance
    dSG = spotterToGunDistance
    aTSG = findTSGAngle(spotterToTargetAzimuth,spotterToGunAzimuth)

    # Law of Cosines to solve 3rd unknown angle
    # a^2 = b^2 + c^2 − 2*b*c*cos(A)

    # math.radians() inputs degrees, outputs radians
    # math.cos() inputs radians, outputs degrees?
    # math.degrees inputs radians, outputs degrees


    distGunToTarget = math.sqrt(dST**2 + dSG**2 - 2*dST*dSG*math.cos(math.radians(aTSG)))

    return distGunToTarget

# print(findDistanceGunToTarget(253, 66, 173, 16))

# %%
def findTGSAngle(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance):
    # https://courses.lumenlearning.com/suny-osalgebratrig/chapter/non-right-triangles-law-of-cosines/ intuition
    # reference figure 3
    # distance GT = a
    # distance ST = b
    # distance SG = c
    # angle TSG = alpha
    # objective: find angle Beta
    # use equation cos(beta) = (a**2 + c**2 - b**2)/(2*a*c)

    dGT = findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)
    dST = spotterToTargetDistance
    dSG = spotterToGunDistance

    # math.acos() inputs radians & outputs radians
    aTGS = math.degrees(math.acos((dGT**2 + dSG**2 - dST**2)/(2*dGT*dSG)))
    return aTGS

# print(findTGSAngle(83,20,313,40))


# %%
def findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance):
    aTGS = findTGSAngle(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)
    aTSG = findTSGAngle(spotterToTargetAzimuth, spotterToGunAzimuth)
    aSTG = 180 - (aTGS + aTSG)
    aziSG = spotterToGunAzimuth
    aziST = spotterToTargetAzimuth


# Intuition: find back azimuth of aziSG, then add or subtract aTGS..?
    if (aziSG >= 180) and (aziST < 180) and (aziSG - 180 > aziST):
        result = (aziSG - 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result
    
    elif (aziSG >= 180) and (aziST < 180) and (aziSG - 180 < aziST):
        result = (aziSG - 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result 
    
    
    elif (aziSG < 180) and (aziST >= 180) and (aziSG + 180 > aziST):
        result = (aziSG + 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result 
    
    elif (aziSG < 180) and (aziST >= 180) and (aziSG + 180 < aziST):
        result = (aziSG + 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result 
    
    
    elif (aziSG >= 180) and (aziST >= 180) and (aziSG > aziST):
        result = (aziSG - 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result 
    
    elif (aziSG >= 180) and (aziST >= 180) and (aziSG < aziST):
        result = (aziSG - 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result 
    
    
    elif (aziSG < 180) and (aziST < 180) and (aziSG > aziST):
        result = (aziSG + 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result 
        
    elif (aziSG < 180) and (aziST < 180) and (aziSG < aziST):
        result = (aziSG + 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result 
    
# print(findAzimuthGunToTarget(254,65,173,50))

# %%
# weapon type
    # 1 = normal artillery (i.e. 120mm & 150mm)
    # 2 = storm cannon (i.e. 300mm)
    # 3 = mortars
def findWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce, weaponType):
    # target takes the spotter role in the triangle calculation
    # adjustedTarget takes the role of target in the triangle calculation
    # accounts for wind force 1-3
    
    # oppositeWindAzimuth is the back azimuth of windAzimuth
    if windAzimuth < 180:
        oppositeWindAzimuth = windAzimuth + 180
    elif windAzimuth >= 180:
        oppositeWindAzimuth = windAzimuth - 180
    
    
    # ******* add more weapon types and windForce to meter conversions whenever possible *******
    if weaponType == 1: #120mm & 150mm
        windForceMetersArray = [0,15,30]
    elif weaponType == 2: #storm cannon
        windForceMetersArray = [0,125,250]
    elif weaponType == 3: #mortars
        windForceMetersArray = [0,10,20]
        
        
    # spotterToGunAzimuth is unadjustedGunToTarget back azimuth
    if unadjustedGunToTargetAzimuth < 180:
        targetToGunAzimuth = unadjustedGunToTargetAzimuth + 180
    else:
        targetToGunAzimuth = unadjustedGunToTargetAzimuth - 180
        
    adjustedGunToTargetAzimuth = findAzimuthGunToTarget(oppositeWindAzimuth,windForceMetersArray[windForce-1], targetToGunAzimuth, unadjustedGunToTargetDistance)
    adjustedGunToTargetDist = findDistanceGunToTarget(oppositeWindAzimuth,windForceMetersArray[windForce-1], targetToGunAzimuth, unadjustedGunToTargetDistance)
    return [unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, adjustedGunToTargetAzimuth, adjustedGunToTargetDist]

# findWindAdjustedGunToTargetAziDist(158.4,760,0,3,2)


# %%
def comprehensiveSpotterArtillery(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance, windAzimuth, windForce, weaponType):
    unadjustedGunToTargetAzimuth = findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)
    unadjustedGunToTargetDistance = findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)

    return findWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce, weaponType)

# print(comprehensiveSpotterArtillery(205,50,103,80,271,3))

# %%
import pandas as pd

# to be used when only spotting for 1 gun, if # of guns > 1, => use multipleGunSpotterArtillery() function
def spotterArtillery(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance, windAzimuth, windForce, weaponType):
    firingHistoryArray = pd.DataFrame(columns=list(["spotterToTargetAzimuth", "spotterToTargetDistance", "spotterToGunAzimuth", "spotterToGunDistance", 
        "windAzimuth", "windForce", "unadjustedGunToTargetAziDist", "windAdjustedGunToTargetAziDist"]))
    print("Keep in mind multiple input responses should be space separated.")
    
    while True:
        print(firingHistoryArray.tail(2))
        userInput = input("Enter <S> to stop or <C> to change variables\n").lower() # potentially add another option to change values in dataframe if a mistake was entered


        if userInput == "s":
            print("Exiting..")
            break

        # changes inputs if inputs change, ask user if these are the correct inputs before applying
        elif (userInput == "c"):
            # display possible inputs
            # changes inputs to what the other puts in
            while True:
                currentVariableValuesArray = [spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance, windAzimuth, windForce]
                print(f"\nEnter numbers 1 through 6 to change or Enter <N> to leave: \n spotterToTargetAzimuth(1), spotterToTargetDistance(2), spotterToGunAzimuth(3), spotterToGunDistance(4), windAzimuth(5), windForce(6) \n {currentVariableValuesArray}")
                variableNumbers = input()
                if variableNumbers.lower() == "n":
                    break
                else:
                    variableNumbers = variableNumbers.split()

                # converts variables to int
                variableNumbers = [int(x) for x in variableNumbers]

                columnNames = firingHistoryArray.columns

                # prints out variables that can be changed
                print("\n")
                for x in variableNumbers:
                    print(f"{columnNames[x-1]}",end=" ")
                print("\n These are the respective values to change.\nEnter the values to change.")

                
                variableValues = input().split()
                variableValues = [float(x) for x in variableValues]

                # assigns new values to existing array
                for i in range(len(variableNumbers)):
                    currentVariableValuesArray[variableNumbers[i]-1] = variableValues[i]

                # assigns values in array to variables 
                spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance, windAzimuth, windForce = currentVariableValuesArray

                # confirm these are the correct variables?
                print(f"\nAre these the correct variables? Enter <Y> to leave. \n{currentVariableValuesArray}\n")
                userInputToLeaveChange = input().lower()
                if userInputToLeaveChange == "y":
                    break

        gunToTargetNewVals = comprehensiveSpotterArtillery(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance, windAzimuth, windForce, weaponType)
        gunToTargetNewVals = [round(x, 3) for x in gunToTargetNewVals]
        
        print(f"\nWind Adjusted Gun To Target Azimuth: {gunToTargetNewVals[2]}")
        print(f"Wind Adjusted Gun To Target Distance: {gunToTargetNewVals[3]} \n")
        print("---------------------------------------------------------------------- \n")

        valuesToStoreInDataframe = [spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance, windAzimuth, windForce, gunToTargetNewVals[0:2], gunToTargetNewVals[2:]]  
        firingHistoryArrayLength = len(firingHistoryArray)
        firingHistoryArray.reset_index(drop=True, inplace=True)
        firingHistoryArray.loc[firingHistoryArrayLength] = valuesToStoreInDataframe

        
 # input variables
# (spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance, windAzimuth, windForce)

# weaponType: 1 = 120mm & 150mm
# weaponType: 2 = storm cannon
# weaponType: 3 = mortar
# note can only take windForce values 1-3, when wind drift data is collected for wind 4 and 5, add to windForceMetersArray in findWindAdjustedGunToTargetAziDist function
 
# press <Space> to scroll to bottom to see output

# spotterArtillery(209,92,320,50,90,3,1)


# %%
import pandas as pd

# to be used for mortar tanks, mortars, or when spotter is right beside artillery position and is able to find aGT and dGT from just using binoculars
def noSpotterArtillery(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce, weaponType):
    firingHistoryArray = pd.DataFrame(columns=list(["unadjustedGunToTargetAzimuth", "unadjustedGunToTargetDistance", "windAzimuth", "windForce", "windAdjustedGunToTargetAziDist"]))
    print("Keep in mind multiple input responses should be space separated.")
    
    
    windAdjustedGunToTargetAziDist = findWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce, weaponType)
    windAdjustedGunToTargetAziDist = [round(x, 3) for x in windAdjustedGunToTargetAziDist]
    print(f"Wind Adjusted Gun To Target Azimuth: {windAdjustedGunToTargetAziDist[2]}")
    print(f"Wind Adjusted Gun To Target Distance: {windAdjustedGunToTargetAziDist[3]} \n")
    print("---------------------------------------------------------------------- \n")
    
    while True:
        print(firingHistoryArray.tail(2))
        userInput = input("\nEnter <S> to stop or <C> to change variables. \n").lower() # potentially add another option to change values in dataframe if a mistake was entered


        if userInput == "s":
            print("Exiting..")
            break

        # changes inputs if inputs change, ask user if these are the correct inputs before applying
        elif (userInput == "c"):
            # display possible inputs
            # changes inputs to what the other puts in
            while True:
                currentVariableValuesArray = [unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce]
                print(f"\nEnter numbers 1 through 4 to change or Enter <N> to leave: \n unadjustedGunToTargetAzimuth(1), unadjustedGunToTargetDistance(2), windAzimuth(3), windForce(4) \n {currentVariableValuesArray}")
                variableNumbers = input("\n")
                if variableNumbers.lower() == "n":
                    break
                else:
                    variableNumbers = variableNumbers.split()

                # converts variables to int
                variableNumbers = [int(x) for x in variableNumbers]

                columnNames = firingHistoryArray.columns

                # prints out variables that can be changed 
                for x in variableNumbers:
                    print(f"{columnNames[x-1]}",end=" ")
                print("\n These are the respective values to change. \n")

                
                variableValues = input("Enter the values to change. \n").split()
                variableValues = [float(x) for x in variableValues]

                # assigns new values to existing array
                for i in range(len(variableNumbers)):
                    currentVariableValuesArray[variableNumbers[i]-1] = variableValues[i]

                # assigns values in array to variables 
                unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce = currentVariableValuesArray

                # confirm these are the correct variables?
                print(f"Are these the correct variables? Enter <Y> to leave. \n{currentVariableValuesArray} \n")
                userInputToLeaveChange = input().lower()
                if userInputToLeaveChange == "y":
                    break

    

        windAdjustedGunToTargetAziDist = findWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce, weaponType)
        windAdjustedGunToTargetAziDist = [round(x, 3) for x in windAdjustedGunToTargetAziDist]
        print(f"Wind Adjusted Gun To Target Azimuth: {windAdjustedGunToTargetAziDist[2]}")
        print(f"Wind Adjusted Gun To Target Distance: {windAdjustedGunToTargetAziDist[3]} \n")
        print("---------------------------------------------------------------------- \n")

        valuesToStoreInDataframe = [unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce, windAdjustedGunToTargetAziDist[2:]]
        firingHistoryArrayLength = len(firingHistoryArray)
        firingHistoryArray.reset_index(drop=True, inplace=True)
        firingHistoryArray.loc[firingHistoryArrayLength] = valuesToStoreInDataframe


# input variables
# (unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce, weaponType)

# weaponType: 1 = 120mm & 150mm
# weaponType: 2 = storm cannon
# weaponType: 3 = mortar
# note can only take windForce values 1-3, when wind drift data is collected for wind 4 and 5, add to windForceMetersArray in findWindAdjustedGunToTargetAziDist function
 
# press <Space> to scroll to bottom to see output


# noSpotterArtillery(171.6,710,315,3,2)


# %%
import pandas as pd

# Spotter triangulates potentially indefinite number of friendly artillery guns onto specific target and adjusts for wind
# Probably best used when spotter can see both guns and target, => limited range, but higher concentration of firepower
def multipleGunSpotterArtillery(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist, windAzimuth, windForce, weaponType):
    firingHistoryArray = pd.DataFrame(columns=list(["spotterToTargetAzimuth", "spotterToTargetDistance", "spotterToGunsAziDist", 
        "windAzimuth", "windForce", "unadjustedGunToTargetAziDist", "windAdjustedGunToTargetAziDist"]))
    print("Keep in mind multiple input responses should be space separated.")
    
    while True:
        print(firingHistoryArray.tail(2))
        userInput = input("Enter <S> to stop or <C> to change variables\n").lower() 

        if userInput == "s":
            print("Exiting..")
            break

        # changes inputs if inputs change, ask user if these are the correct inputs before applying
        elif (userInput == "c"):
            # display possible inputs
            # changes inputs to what the other puts in
            while True:
                currentVariableValuesArray = [spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist, windAzimuth, windForce]
                print(f"\nEnter numbers 1 through 6 to change or Enter <N> to leave: \n spotterToTargetAzimuth(1), spotterToTargetDistance(2), spotterToGunsAziDist(3), windAzimuth(4), windForce(5) \n {currentVariableValuesArray}")
                variableNumbers = input()
                if variableNumbers.lower() == "n":
                    break
                else:
                    variableNumbers = variableNumbers.split()

                # converts variables to int
                variableNumbers = [int(x) for x in variableNumbers]

                columnNames = firingHistoryArray.columns

                # prints out variables that can be changed
                print("\n")
                for x in variableNumbers:
                    print(f"{columnNames[x-1]}",end=" ")
                print("\n These are the respective values to change.\nEnter the values to change.")

                # converts parses input string into array
                variableValues = input().split()
                for i in range(len(variableValues)):
                    if variableNumbers[i] == 3:
                        line = variableValues[i].replace("[", "")
                        line = line.replace("]", "")
                        line = line.split(",")
                        variableValues[i] = [float(x) for x in line]
                    else:
                        variableValues[i] = float(variableValues[i])

                # assigns new values to existing array
                for i in range(len(variableNumbers)):
                    currentVariableValuesArray[variableNumbers[i]-1] = variableValues[i]

                # assigns values in array to variables 
                spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist, windAzimuth, windForce = currentVariableValuesArray

                # confirm these are the correct variables?
                print(f"\nAre these the correct variables? Enter <Y> to leave. \n{currentVariableValuesArray}\n")
                userInputToLeaveChange = input().lower()
                if userInputToLeaveChange == "y":
                    break

    
        unadjustedGunToTargetAziDist = []
        adjustedGunToTargetAziDist = []
        for i in range(int(len(spotterToGunsAziDist) / 2)):
            unadjustedAndAdjustedVals = comprehensiveSpotterArtillery(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist[i*2], spotterToGunsAziDist[i*2+1], windAzimuth, windForce, weaponType)
            unadjustedGunToTargetAziDist.append(unadjustedAndAdjustedVals[0:2])
            adjustedGunToTargetAziDist.append(unadjustedAndAdjustedVals[2:])

            print(f"\nWind Adjusted Gun {i+1} To Target Azimuth: {adjustedGunToTargetAziDist[i][0]}")
            print(f"Wind Adjusted Gun {i+1} To Target Distance: {adjustedGunToTargetAziDist[i][1]} \n")
        print("---------------------------------------------------------------------- \n")

        unadjustedGunToTargetAziDist = [round(x, 3) for x in unadjustedGunToTargetAziDist]
        adjustedGunToTargetAziDist = [round(x, 3) for x in unadjustedGunToTargetAziDist]
        
        valuesToStoreInDataframe = [spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist, windAzimuth, windForce, unadjustedGunToTargetAziDist, adjustedGunToTargetAziDist]
        firingHistoryArrayLength = len(firingHistoryArray)
        firingHistoryArray.reset_index(drop=True, inplace=True)
        firingHistoryArray.loc[firingHistoryArrayLength] = valuesToStoreInDataframe

# input variables
# (spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance, windAzimuth, windForce, weaponType)

# weaponType: 1 = 120mm & 150mm
# weaponType: 2 = storm cannon
# weaponType: 3 = mortar
# argument 3: takes an array, which is composed of [spotterToGun1Azi, spotterToGun1Dist, spotterToGun2Azi, spotterToGun2Dist, ...]
# note can only take wind values 1-3, when wind drift data is collected for wind 4 and 5, add to windForceMetersArray in findWindAdjustedGunToTargetAziDist function
 
# press <Space> to scroll to bottom to see output


# multipleGunSpotterArtillery(254,65,[173,50,250,50],124,3,3)


# %%
# Experimental functions below

# %%
def findImpliedWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, impliedWindAzimuth, impliedWindDriftMeters):
    # target takes the spotter role in the triangle calculation
    # adjustedTarget takes the role of target in the triangle calculation
    # accounts for wind force 1-3
    
    # oppositeWindAzimuth is the back azimuth of impliedWindAzimuth
    if impliedWindAzimuth < 180:
        oppositeWindAzimuth = impliedWindAzimuth + 180
    elif impliedWindAzimuth >= 180:
        oppositeWindAzimuth = impliedWindAzimuth - 180
    
    
    # spotterToGunAzimuth is unadjustedGunToTarget back azimuth
    if unadjustedGunToTargetAzimuth < 180:
        targetToGunAzimuth = unadjustedGunToTargetAzimuth + 180
    else:
        targetToGunAzimuth = unadjustedGunToTargetAzimuth - 180
        
    adjustedGunToTargetAzimuth = findAzimuthGunToTarget(oppositeWindAzimuth,impliedWindDriftMeters, targetToGunAzimuth, unadjustedGunToTargetDistance)
    adjustedGunToTargetDist = findDistanceGunToTarget(oppositeWindAzimuth,impliedWindDriftMeters, targetToGunAzimuth, unadjustedGunToTargetDistance)
    return [unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, adjustedGunToTargetAzimuth, adjustedGunToTargetDist]

# print(findImpliedWindAdjustedGunToTargetAziDist(323.2,5,270,4))

# %%
import pandas as pd

# ouputs [impliedWindAzimuth, impliedWindDriftMeters]
def findImpliedWindAziDist(gunToImpactAzi, gunToImpactDist, gunToTargetAzi, gunToTargetDist):
    impliedWindAzimuth = findAzimuthGunToTarget(gunToImpactAzi, gunToImpactDist, gunToTargetAzi, gunToTargetDist)
    impliedWindDriftMeters = findDistanceGunToTarget(gunToImpactAzi, gunToImpactDist, gunToTargetAzi, gunToTargetDist)
    return [impliedWindAzimuth, impliedWindDriftMeters]

# print(findImpliedWindAziDist(323.2,5,0,4))

# %%
import pandas as pd

# to be used when only spotting for 1 gun, if # of guns > 1, => use multipleGunSpotterArtillery() function
def impliedSpotterArtillery(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance):
    firingHistoryArray = pd.DataFrame(columns=list(["spotterToTargetAzimuth", "spotterToTargetDistance", "spotterToGunAzimuth", "spotterToGunDistance", 
        "impliedWindAzimuth", "impliedWindDriftMeters", "unadjustedGunToTargetAziDist", "windAdjustedGunToTargetAziDist"]))
    print("Keep in mind multiple input responses should be space separated.")
    
    
    print("Enter space delimited impactAzimuth and impactDistance")
    impactAziDist = input("\n").split()
    impactAziDist = [float(x) for x in impactAziDist]

    unadjustedGunToTargetAzimuth = findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)
    unadjustedGunToTargetDistance = findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)

    gunToImpactAzimuth = findAzimuthGunToTarget(impactAziDist[0], impactAziDist[1], spotterToGunAzimuth, spotterToGunDistance)
    gunToImpactDistance = findDistanceGunToTarget(impactAziDist[0], impactAziDist[1], spotterToGunAzimuth, spotterToGunDistance)

    impliedWindAzimuth, impliedWindDriftMeters = findImpliedWindAziDist(gunToImpactAzimuth, gunToImpactDistance, unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance)

    windAdjustedGunToTargetAziDist = findImpliedWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, impliedWindAzimuth, impliedWindDriftMeters)
    windAdjustedGunToTargetAziDist = [round(x, 3) for x in windAdjustedGunToTargetAziDist]

    print(f"\nWind Adjusted Gun To Target Azimuth: {windAdjustedGunToTargetAziDist[2]}")
    print(f"Wind Adjusted Gun To Target Distance: {windAdjustedGunToTargetAziDist[3]} \n")
    print("---------------------------------------------------------------------- \n")    

    while True:
        print(firingHistoryArray.tail(2))
        userInput = input("Enter <S> to stop, <C> to change variables, or <W> to change impliedWindValues\n").lower() # potentially add another option to change values in dataframe if a mistake was entered


        if userInput == "s":
            print("Exiting..")
            break

        # changes inputs if inputs change, ask user if these are the correct inputs before applying
        elif (userInput == "c"):
            # display possible inputs
            # changes inputs to what the other puts in
            while True:
                currentVariableValuesArray = [spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance]
                print(f"\nEnter numbers 1 through 4 to change or Enter <N> to leave: \n spotterToTargetAzimuth(1), spotterToTargetDistance(2), spotterToGunAzimuth(3), spotterToGunDistance(4) \n {currentVariableValuesArray}")
                variableNumbers = input()
                if variableNumbers.lower() == "n":
                    break
                else:
                    variableNumbers = variableNumbers.split()

                # converts variables to int
                variableNumbers = [int(x) for x in variableNumbers]

                columnNames = firingHistoryArray.columns

                # prints out variables that can be changed
                print("\n")
                for x in variableNumbers:
                    print(f"{columnNames[x-1]}",end=" ")
                print("\n These are the respective values to change.\nEnter the values to change.")

                
                variableValues = input().split()
                variableValues = [float(x) for x in variableValues]

                # assigns new values to existing array
                for i in range(len(variableNumbers)):
                    currentVariableValuesArray[variableNumbers[i]-1] = variableValues[i]

                # assigns values in array to variables 
                spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance = currentVariableValuesArray

                # confirm these are the correct variables?
                print(f"\nAre these the correct variables? Enter <Y> to leave. \n{currentVariableValuesArray}\n")
                userInputToLeaveChange = input().lower()
                if userInputToLeaveChange == "y":
                    break
                    
        elif (userInput == "w"):
            while True:
                print("Enter space delimited impactAzimuth and impactDistance")
                impactAziDist = input().split()
                impactAziDist = [float(x) for x in impactAziDist]

                print(f"\nAre these the correct impact variables? Enter <Y> to leave. \n{impactAziDist} \n")
                userInputToLeaveChange = input().lower()
                if userInputToLeaveChange == "y":
                    break
                    
        unadjustedGunToTargetAzimuth = findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)
        unadjustedGunToTargetDistance = findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)

        gunToImpactAzimuth = findAzimuthGunToTarget(impactAziDist[0], impactAziDist[1], spotterToGunAzimuth, spotterToGunDistance)
        gunToImpactDistance = findDistanceGunToTarget(impactAziDist[0], impactAziDist[1], spotterToGunAzimuth, spotterToGunDistance)

        impliedWindAzimuth, impliedWindDriftMeters = findImpliedWindAziDist(gunToImpactAzimuth, gunToImpactDistance, unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance)
        
        windAdjustedGunToTargetAziDist = findImpliedWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, impliedWindAzimuth, impliedWindDriftMeters)
        windAdjustedGunToTargetAziDist = [round(x, 3) for x in windAdjustedGunToTargetAziDist]
                
        print(f"\nWind Adjusted Gun To Target Azimuth: {windAdjustedGunToTargetAziDist[2]}")
        print(f"Wind Adjusted Gun To Target Distance: {windAdjustedGunToTargetAziDist[3]} \n")
        print("---------------------------------------------------------------------- \n")

        valuesToStoreInDataframe = [spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance, impliedWindAzimuth, impliedWindDriftMeters, windAdjustedGunToTargetAziDist[0:2], windAdjustedGunToTargetAziDist[2:]]  
        firingHistoryArrayLength = len(firingHistoryArray)
        firingHistoryArray.reset_index(drop=True, inplace=True)
        firingHistoryArray.loc[firingHistoryArrayLength] = valuesToStoreInDataframe
        
# impliedSpotterArtillery(209,92,320,50)

# %%
import pandas as pd

def impliedNoSpotterArtillery(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance):
    firingHistoryArray = pd.DataFrame(columns=list(["unadjustedGunToTargetAzimuth", "unadjustedGunToTargetDistance", "impliedWindAzimuth", "impliedWindDriftMeters", "windAdjustedGunToTargetAziDist"]))
    print("Keep in mind multiple input responses should be space separated.")
    
    print("Enter space delimited impactAzimuth and impactDistance")
    impactAziDist = input("\n").split()
    impactAziDist = [float(x) for x in impactAziDist]
    impliedWindAzimuth, impliedWindDriftMeters = findImpliedWindAziDist(impactAziDist[0], impactAziDist[1], unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance)


    windAdjustedGunToTargetAziDist = findImpliedWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, impliedWindAzimuth, impliedWindDriftMeters)
    windAdjustedGunToTargetAziDist = [round(x, 3) for x in windAdjustedGunToTargetAziDist]

    print(f"Wind Adjusted Gun To Target Azimuth: {windAdjustedGunToTargetAziDist[2]}")
    print(f"Wind Adjusted Gun To Target Distance: {windAdjustedGunToTargetAziDist[3]} \n")
    print("---------------------------------------------------------------------- \n")

    while True:
        print(firingHistoryArray.tail(2))
        userInput = input("\nEnter <S> to stop, <T> to change target, or <W> to change impliedWindValues. \n").lower() # potentially add another option to change values in dataframe if a mistake was entered


        if userInput == "s":
            print("Exiting..")
            break

        # changes inputs if inputs change, ask user if these are the correct inputs before applying
        elif (userInput == "t"):
            # display possible inputs
            # changes inputs to what the other puts in
            while True:
                print(f"\nEnter space delimited target values or Enter <N> to leave: \nCurrent Values:\nunadjustedGunToTargetAzimuth: {unadjustedGunToTargetAzimuth} \nunadjustedGunToTargetDistance: {unadjustedGunToTargetDistance} \n ")
                variableValues = input("\n")
                if variableValues.lower() == "n":
                    break
                else:
                    variableValues = variableValues.split()

                # converts inputs to float
                variableValues = [float(x) for x in variableValues]


                # assigns values in array to variables 
                unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance = variableValues

                # confirm these are the correct variables?
                print(f"Are these the correct target variables? Enter <Y> to leave. \n{variableValues} \n")
                userInputToLeaveChange = input().lower()
                if userInputToLeaveChange == "y":
                    break

        elif (userInput == "w"):
            while True:
                print("Enter space delimited impactAzimuth and impactDistance")
                impactAziDist = input().split()
                impactAziDist = [float(x) for x in impactAziDist]

                print(f"\nAre these the correct impact variables? Enter <Y> to leave. \n{impactAziDist} \n")
                userInputToLeaveChange = input().lower()
                if userInputToLeaveChange == "y":
                    impliedWindAzimuth, impliedWindDriftMeters = findImpliedWindAziDist(impactAziDist[0], impactAziDist[1], unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance)
                    break
    

        windAdjustedGunToTargetAziDist = findImpliedWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, impliedWindAzimuth, impliedWindDriftMeters)
        windAdjustedGunToTargetAziDist = [round(x, 3) for x in windAdjustedGunToTargetAziDist]
        
        print(f"Wind Adjusted Gun To Target Azimuth: {windAdjustedGunToTargetAziDist[2]}")
        print(f"Wind Adjusted Gun To Target Distance: {windAdjustedGunToTargetAziDist[3]} \n")
        print("---------------------------------------------------------------------- \n")

        valuesToStoreInDataframe = [unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, impliedWindAzimuth, impliedWindDriftMeters, windAdjustedGunToTargetAziDist[2:]]
        valuesToStoreInDataframe = [round((x), 3) for x in valuesToStoreInDataframe[0:4]] + [valuesToStoreInDataframe[4]]
        firingHistoryArrayLength = len(firingHistoryArray)
        firingHistoryArray.reset_index(drop=True, inplace=True)
        firingHistoryArray.loc[firingHistoryArrayLength] = valuesToStoreInDataframe

# impliedNoSpotterArtillery(0,4)

# %%
import pandas as pd

# to be used when only spotting for 1 gun, if # of guns > 1, => use multipleGunSpotterArtillery() function
def impliedMultipleGunSpotterArtillery(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist):
    firingHistoryArray = pd.DataFrame(columns=list(["spotterToTargetAzimuth", "spotterToTargetDistance", "spotterToGunsAziDist", "impliedWindAzimuth",
                                                    "impliedWindDriftMeters", "unadjustedGunToTargetAziDist", "windAdjustedGunToTargetAziDist"]))
    print("Keep in mind multiple input responses should be space separated.")
    
    # first spotterToGunAziDist pair used to find impliedWindValues from impactValues, this gun must be the one firing to observe impacts

    
    print("Enter space delimited impactAzimuth and impactDistance")
    impactAziDist = input("\n").split()
    impactAziDist = [float(x) for x in impactAziDist]

    unadjustedGunToTargetAzimuth = findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist[0], spotterToGunsAziDist[1])
    unadjustedGunToTargetDistance = findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist[0], spotterToGunsAziDist[1])

    gunToImpactAzimuth = findAzimuthGunToTarget(impactAziDist[0], impactAziDist[1], spotterToGunsAziDist[0], spotterToGunsAziDist[1])
    gunToImpactDistance = findDistanceGunToTarget(impactAziDist[0], impactAziDist[1], spotterToGunsAziDist[0], spotterToGunsAziDist[1])

    impliedWindAzimuth, impliedWindDriftMeters = findImpliedWindAziDist(gunToImpactAzimuth, gunToImpactDistance, unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance)    

    unadjustedGunToTargetAziDist = []
    adjustedGunToTargetAziDist = []

    for i in range(int(len(spotterToGunsAziDist) / 2)):
        unadjustedGunToTargetAzimuth = findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist[i*2], spotterToGunsAziDist[i*2+1])
        unadjustedGunToTargetDistance = findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist[i*2], spotterToGunsAziDist[i*2+1])

        windAdjustedGunToTargetAziDist = findImpliedWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, impliedWindAzimuth, impliedWindDriftMeters)
        windAdjustedGunToTargetAziDist = [round(x, 3) for x in windAdjustedGunToTargetAziDist]

        unadjustedGunToTargetAziDist.append(windAdjustedGunToTargetAziDist[0:2])
        adjustedGunToTargetAziDist.append(windAdjustedGunToTargetAziDist[2:])

        print(f"\nWind Adjusted Gun To Target Azimuth: {windAdjustedGunToTargetAziDist[2]}")
        print(f"Wind Adjusted Gun To Target Distance: {windAdjustedGunToTargetAziDist[3]} \n")

    print("---------------------------------------------------------------------- \n")
    
    
    while True:
        print(firingHistoryArray.tail(2))
        userInput = input("Enter <S> to stop, <C> to change variables, or <W> to change impliedWindValues\n").lower() # potentially add another option to change values in dataframe if a mistake was entered


        if userInput == "s":
            print("Exiting..")
            break

        # changes inputs if inputs change, ask user if these are the correct inputs before applying
        elif (userInput == "c"):
            # display possible inputs
            # changes inputs to what the other puts in
            while True:
                currentVariableValuesArray = [spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist]
                print(f"\nEnter numbers 1 through 4 to change or Enter <N> to leave: \n spotterToTargetAzimuth(1), spotterToTargetDistance(2), spotterToGunAzimuth(3), spotterToGunDistance(4) \n {currentVariableValuesArray}")
                variableNumbers = input()
                if variableNumbers.lower() == "n":
                    break
                else:
                    variableNumbers = variableNumbers.split()

                # converts variables to int
                variableNumbers = [int(x) for x in variableNumbers]

                columnNames = firingHistoryArray.columns

                # prints out variables that can be changed
                print("\n")
                for x in variableNumbers:
                    print(f"{columnNames[x-1]}",end=" ")
                print("\n These are the respective values to change.\nEnter the values to change.")

                
                variableValues = input().split()
                for i in range(len(variableValues)):
                    if variableNumbers[i] == 3:
                        line = variableValues[i].replace("[", "")
                        line = line.replace("]", "")
                        line = line.split(",")
                        variableValues[i] = [float(x) for x in line]
                    else:
                        variableValues[i] = float(variableValues[i])

                        
                # assigns new values to existing array
                for i in range(len(variableNumbers)):
                    currentVariableValuesArray[variableNumbers[i]-1] = variableValues[i]

                # assigns values in array to variables 
                spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist = currentVariableValuesArray

                # confirm these are the correct variables?
                print(f"\nAre these the correct variables? Enter <Y> to leave. \n{currentVariableValuesArray}\n")
                userInputToLeaveChange = input().lower()
                if userInputToLeaveChange == "y":
                    break
                    
        elif (userInput == "w"):
            while True:
                print("Enter space delimited impactAzimuth and impactDistance")
                impactAziDist = input().split()
                impactAziDist = [float(x) for x in impactAziDist]

                print(f"\nAre these the correct impact variables? Enter <Y> to leave. \n{impactAziDist} \n")
                userInputToLeaveChange = input().lower()
                if userInputToLeaveChange == "y":
                    break
          
        unadjustedGunToTargetAzimuth = findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist[0], spotterToGunsAziDist[1])
        unadjustedGunToTargetDistance = findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist[0], spotterToGunsAziDist[1])

        gunToImpactAzimuth = findAzimuthGunToTarget(impactAziDist[0], impactAziDist[1], spotterToGunsAziDist[0], spotterToGunsAziDist[1])
        gunToImpactDistance = findDistanceGunToTarget(impactAziDist[0], impactAziDist[1], spotterToGunsAziDist[0], spotterToGunsAziDist[1])

        impliedWindAzimuth, impliedWindDriftMeters = findImpliedWindAziDist(gunToImpactAzimuth, gunToImpactDistance, unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance)


        unadjustedGunToTargetAziDist = []
        adjustedGunToTargetAziDist = []
        
        for i in range(int(len(spotterToGunsAziDist) / 2)):
            unadjustedGunToTargetAzimuth = findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist[i*2], spotterToGunsAziDist[i*2+1])
            unadjustedGunToTargetDistance = findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist[i*2], spotterToGunsAziDist[i*2+1])
            
            windAdjustedGunToTargetAziDist = findImpliedWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, impliedWindAzimuth, impliedWindDriftMeters)
            windAdjustedGunToTargetAziDist = [round(x, 3) for x in windAdjustedGunToTargetAziDist]
                
            unadjustedGunToTargetAziDist.append(windAdjustedGunToTargetAziDist[0:2])
            adjustedGunToTargetAziDist.append(windAdjustedGunToTargetAziDist[2:])
                
            print(f"\nWind Adjusted Gun To Target Azimuth: {windAdjustedGunToTargetAziDist[2]}")
            print(f"Wind Adjusted Gun To Target Distance: {windAdjustedGunToTargetAziDist[3]} \n")
            
        print("---------------------------------------------------------------------- \n")

        valuesToStoreInDataframe = [spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunsAziDist, impliedWindAzimuth, impliedWindDriftMeters, unadjustedGunToTargetAziDist, adjustedGunToTargetAziDist]  
        firingHistoryArrayLength = len(firingHistoryArray)
        firingHistoryArray.reset_index(drop=True, inplace=True)
        firingHistoryArray.loc[firingHistoryArrayLength] = valuesToStoreInDataframe
        
# impliedMultipleGunSpotterArtillery(254,65,[173,50,250,50])

# %%



