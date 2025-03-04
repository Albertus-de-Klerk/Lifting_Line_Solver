import ctypes as ct
import os




def CallXfoilcl(Cl, Re, AirfoilName, Flap,xpos,ypos):

    
    mydll = ct.cdll.LoadLibrary("../XFOIL/XFOIL.dll")

    if os.path.exists(AirfoilName) == True:
        ISCONV = ct.c_bool(False)
        RE_IN = ct.c_double(Re)
        CL_IN = ct.c_double(Cl)
        l = ct.c_int(0)
        array = (ct.c_double * 11) (0,0,0,0,0,0,0,Flap,xpos,ypos,0)

        my_string = AirfoilName.encode() # Convert string to bytes
        l = len(my_string)     
#        _= mydll.xfoil_cl(ct.byref(array), ct.byref(CL_IN),ct.byref(RE_IN),ct.byref(ISCONV),ct.c_char_p(my_string))
        _= mydll.xfoil_test(ct.byref(array), ct.byref(CL_IN),ct.byref(RE_IN),ct.byref(ISCONV),ct.c_char_p(my_string),ct.c_int(l))
        print(my_string,l)
                # Array1(1) = ADEG
                # Array1(2) = CD
                # Array1(3) = CDF
                # Array1(4) = CM
                # Array1(5) = HMOM
                # Array1(6) = HFX
                # Array1(7) = HFY
        if ISCONV.value == False:
            print(AirfoilName,Re,Cl,array[1])         #[uncomment if you want to see whether iteration for station has converged]
        return array[0],array[1],array[3],ISCONV.value
    else:
        print("Airfoil Filename does not exist->" + str(AirfoilName))
        return(1,1,1,False)
        
        
AOA, Cd,Cm,ISCONV = CallXfoilcl(0.5,1000000,"./A5",5,0.86,0.00)
print(AOA)
