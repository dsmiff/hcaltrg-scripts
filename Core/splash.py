import random
version = 'CMSSW_8_1_0_pre8'
logo = ""
logo = """                    ____  ___
           /     / /     /   |    /
          / ___ / /     / /| |   /
         /     / /     / ___ |  /
        /     / /____ /_/  |_/ /___
                """


tagLine = "HCal TP studies"
toolsVersion = version

def main():
    print ""
    printLogo(version)
    print "\n\t\t\t", tagLine, "\n\n\n"
    
    print "    HCal DPG version          :", toolsVersion
    print "\n"



def printLogo(version):
    lightDark = 0
    if lightDark == 0:
        lightDark ="3"
    else:
        lightDark ="9"

    colour = 2
    colour = str(int(colour) % 7+1)

    CSI="\x1B[49m\x1B["

    print CSI+lightDark+colour+"m" + logo + CSI + "0m"


if __name__ == "__main__":
    main()
