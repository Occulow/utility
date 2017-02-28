# Grideye Testing
## How to run
Put main.py on a raspberry pi with GridEye connected via i2c. The default parameters will capture frames at 10 FPS over 10 seconds. It will also print out the value of the thermistor register.

On Pi:
```bash
python main.py
```

On Local:
```bash
scp pi@xxx.xxx.x.x:grideye/data.csv .
python plot.py
```
