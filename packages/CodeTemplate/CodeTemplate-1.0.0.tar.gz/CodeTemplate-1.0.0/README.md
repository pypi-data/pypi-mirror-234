use the library in other Python scripts. 
Create a new Python script in a different directory and 
import and use the send function from the library

```
from potatoscript.potatoConfig import Config as config

potato = Config('config.ini')
a = potato.get("Data","localFolderPath")
b = a

```