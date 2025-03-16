import utits
import os

if __name__ == "__main__":
    Mov_Dir = './assets' #.MOV file dirs
    Heic_Dir = './assets'  #.HEIC file dirs

    ####################################################  Method 1: Image Hashing
    #First you need to hashing your files
    instance = utits.Core.Indexing()  # Of course you can resume your hashing by  utits.Core.Indexing(Index_File='./xxx.json')
    instance.Create_Index(
        HEIC_Path=Heic_Dir,
        Mov_Videos_Path=Mov_Dir,
        Thread_Num=8
    )
    #After Indexed, Compare is necessary
    Indexed = './Indexed.json'
    isinstance = utits.Core.Connect(Indexed_File=Indexed)
    print(isinstance.Compare())

    ####################################################  Method 2: VLM Comparing
