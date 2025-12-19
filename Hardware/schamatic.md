# CIRCUIT SCHEMATIC

## Arduino Pin Connections

### Input Sensors:
1. **Ultrasonic Sensor (HC-SR04)**:
   ```
   VCC → 5V
   Trig → Pin 2
   Echo → Pin 3
   GND → GND
   ```

2. **Infrared Reflectance Sensor** → Pin A0
   ```
   VCC → 5V
   OUT → A0
   GND → GND
   ```

### Output Devices:
3. **Buzzer** → Pin 4
   ```
   Pin 4 → Buzzer (+) → Buzzer (-) → GND
   ```

4. **RGB LED**:
   ```
   Pin 5 (Red) → 220Ω → R LED → GND
   Pin 6 (Green) → 220Ω → G LED → GND
   Pin 7 (Blue) → 220Ω → B LED → GND
   ```

## Sensor Specifications

### HC-SR04 Ultrasonic Sensor:
- **Range**: 2cm to 400cm
- **Accuracy**: ±3mm
- **Measuring Angle**: 15°
- **Operating Voltage**: 5V DC
- **Principle**: Time-of-flight measurement

### Infrared Reflectance Sensor:
- **Detection Method**: Infrared reflection
- **Output**: Analog voltage (0-5V)
- **Range**: 1-3cm (adjustable)
- **Applications**: Surface reflectance, object detection
- **Wavelength**: 940nm infrared

## Color Coding System

### LED Status Indicators:
- **BLUE (0,0,255)**: Normal state, no object detected
- **GREEN (0,255,0)**: Object at ideal distance (10-30cm)
- **RED (255,0,0)**: Object too close (<10cm) - alert state

### Alert System:
- **Distance <10cm**: Red LED + 1000Hz buzzer pulse
- **Distance 10-30cm**: Green LED (no sound)
- **Distance >30cm**: Blue LED (no sound)

## Data Output Format
```
Timestamp(ms),Distance(cm),Reflectance(IR),State
0,999,512,NORMAL
500,25,480,OBJECT_DETECTED
1000,5,620,ALERT_CLOSE
```

## Environmental Considerations

### Deployment Tips:
1. Place ultrasonic sensor facing area to monitor
2. Position IR sensor for surface reflectance measurement
3. Use protective enclosure for outdoor deployment
4. Ensure stable power supply for continuous operation

### Calibration:
- Ultrasonic: Test with known distances
- IR Sensor: Adjust based on surface reflectivity
- LED Colors: Verify color output matches states
