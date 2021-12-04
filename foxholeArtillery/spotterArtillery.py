import pandas as py

# inputs wind and direction, outputs adjusted azimuth & distance
# given impact point of wind, calculate implied wind distance & azimuth
# calculate length of third side given SGT angle and lengths of the two other sides (SGT = Spotter, Gun, Target)

def findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance):


