# LivePhoto_Connector
Connect Missing .HEIC file with .MOV file  
Why you need this tool?  
Let's persume you have a bunch of file named 'xxx.heic' and 'xxx.mov', and they are *Apple's Live Photo*, but the number of them are chaos.  
So how to connect them?  
Luckily, you got this.  
### Useage
```bash
git clone https://github.com/P-PPPP/LivePhoto_Connector.git
cd LivePhoto_Connector
pip install -r requirements.txt
```
Then you need to edit `main.py`
```python
import utits
import os

if __name__ == "__main__":
    Mov_Dir = './assets' #.MOV file dirs
    Heic_Dir = './assets'  #.HEIC file dirs
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
```
With result:
```json
[{
	"HEIC_File": "00817.heic",
	"MOV_File": "01470.mov",
	"Confidence": 0.33
}, {
	"HEIC_File": "00817.heic",
	"MOV_File": "01470.mov",
	"Confidence": 0.36
}, {
	"HEIC_File": "00817.heic",
	"MOV_File": "01470.mov",
	"Confidence": 0.33
}, {
	"HEIC_File": "00817.heic",
	"MOV_File": "01470.mov",
	"Confidence": 0.39
}, {
	"HEIC_File": "02183.heic",
	"MOV_File": "01597.mov",
	"Confidence": 0.36
}]
```
Need to be attention: One Single File Can Give many Results,like `00817.heic` in Example
