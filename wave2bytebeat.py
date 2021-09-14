import wave
import time
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def write(type,text):
    if type=="LOG":
        print('\x1b[6;30;47m' + 'LOG' + '\x1b[0m ' + str(text))
    if type=="ERR":
        print('\x1b[6;30;41m' + 'ERR' + '\x1b[0m ' + str(text))
    if type=="WARN":
        print('\x1b[6;30;43m' + 'WARN' + '\x1b[0m ' + str(text))

clearConsole()
write("LOG","Sleeping for 1 second...")
time.sleep(1)
filename=input('\x1b[6;30;47m' + 'INPUT' + '\x1b[0m ' + "Enter filename to open: ")
write("LOG","Opening '"+filename+"' in read-only mode")
fileopened=False
try:
    file=wave.open(filename,mode="rb")
    fileopened=True
except:
    write("ERR","File open failed! Make sure to use the 'Unsigned 8-bit PCM' format!")
if fileopened==True:
    samp=file.getframerate()
    write("LOG","Sampling rate: "+str(samp)+"Hz")
    condition1=False
    if samp==8000 or samp==11025 or samp==22050 or samp==32000 or samp==44100:
        condition1=True
    if condition1==True:
        write("LOG",'Sampling frequency is compatible')
        chan=file.getnchannels()
        if chan == 1:
            write("LOG",'Audio is mono')
            frames=file.getnframes()
            write("LOG",'Frame count: '+str(frames))
            write("LOG","Grabbing wave frames...")
            start=time.time()
            truestart=time.time()
            bytetable=[]
            script=""
            for x in range(frames):
                frame=int(int.from_bytes(file.readframes(1),"big"))
                bytetable.append(frame)
                #print(int(int.from_bytes(file.readframes(1),"big")))
                if time.time()-start >= 1:
                    print("Progress: "+str(x)+"/"+str(frames)+", Elapsed Time: "+str(int(time.time()-truestart))+" seconds.")
                    start=time.time()
                if frame > 255:
                    break
            if bytetable[len(bytetable)-1] > 255:
                write("ERR","Frame position value too high! Make sure to use the 'Unsigned 8-bit PCM' format!")
            else:
                #print(len(bytetable))
                write("LOG","Constructing script...")
                script=script+"bytes=["
                loops=0
                segloops=0
                start=time.time()
                truestart=time.time()
                scriptsegments=[]
                for x in bytetable:
                    loops+=1
                    segloops+=1
                    if segloops==65535:
                        #write("LOG","Adding script segment #"+str(len(scriptsegments)+1)+" to array...")
                        segloops=0
                        scriptsegments.append(script)
                        script=""
                    if loops==len(bytetable):
                        #write("LOG","Adding final script segment #"+str(len(scriptsegments)+1)+" to array...")
                        script=script+str(x)+"],\n\nbytes[t]"
                        scriptsegments.append(script)
                        script=""
                        break
                    else:
                        script=script+str(x)+","
                    if time.time()-start >= 1:
                        write("LOG","Progress: "+str(loops)+"/"+str(len(bytetable))+", Elapsed Time: "+str(int(time.time()-truestart))+" seconds.")
                        start=time.time()
                script=""
                write("LOG","Combining all script segments...")
                loops=0
                for x in scriptsegments:
                    loops+=1
                    script=script+x
                    #write("LOG","Finished part "+str(loops)+"/"+str(len(scriptsegments)))
                write("LOG","Writing to file...")
                outfile=open("out.txt","w")
                outfile.write(script)
                outfile.close()
        else:
            write("ERR",'Audio is not mono sound! Channel count: '+str(chan))
    else:
        write("ERR", "Sampling frequency incompatible! W2BB supports 8000,11025,22050,32000 and 44100 Hz")
write("WARN","Script finished")
time.sleep(5)
