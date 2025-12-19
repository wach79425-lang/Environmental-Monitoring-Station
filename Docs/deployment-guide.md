# DEPLOYMENT GUIDE

## 1. Pre-Deployment Preparation

### 1.1 Equipment Checklist
```
Required Components:
- [ ] Arduino Uno with USB cable
- [ ] HC-SR04 Ultrasonic Sensor
- [ ] TCRT5000 IR Reflectance Sensor
- [ ] RGB LED (Common Cathode)
- [ ] Active Buzzer
- [ ] 3x 220Ω Resistors
- [ ] Breadboard and jumper wires
- [ ] Protective enclosure (optional)
- [ ] Power supply (USB power bank or 9V battery)
- [ ] Laptop/computer for initial setup
- [ ] Serial cable or Bluetooth module

Optional Components:
- [ ] Weatherproof enclosure
- [ ] Solar panel and charge controller
- [ ] SD card module for data storage
- [ ] WiFi or GSM module for remote data
- [ ] Mounting brackets and hardware
```

### 1.2 Site Assessment Checklist
```
Environmental Factors:
- [ ] Temperature range: 0°C to 50°C
- [ ] Humidity: Below 80% for electronics
- [ ] Sun exposure: Partial shade preferred
- [ ] Wind exposure: Protected from strong winds
- [ ] Precipitation: Protected from direct rain

Infrastructure Factors:
- [ ] Power source available
- [ ] Data retrieval access
- [ ] Security from theft/vandalism
- [ ] Maintenance access
- [ ] Local community awareness

Scientific Factors:
- [ ] Representative of monitoring area
- [ ] Clear line of sight for sensors
- [ ] Minimal environmental disturbance
- [ ] Compliance with local regulations
```

## 2. System Assembly

### 2.1 Circuit Assembly Step-by-Step

**Step 1: Prepare the Breadboard**
```
1. Place Arduino Uno near one end of breadboard
2. Ensure good access to all pins
```

**Step 2: Connect Ultrasonic Sensor**
```
HC-SR04 Connections:
VCC  → Arduino 5V
Trig → Arduino Pin 2
Echo → Arduino Pin 3
GND  → Arduino GND
```

**Step 3: Connect IR Sensor**
```
TCRT5000 Connections:
VCC  → Arduino 5V
OUT  → Arduino A0
GND  → Arduino GND
```

**Step 4: Connect RGB LED**
```
RGB LED Connections:
Red Pin   → 220Ω resistor → Arduino Pin 5
Green Pin → 220Ω resistor → Arduino Pin 6
Blue Pin  → 220Ω resistor → Arduino Pin 7
Common Cathode → Arduino GND
```

**Step 5: Connect Buzzer**
```
Active Buzzer Connections:
+ Pin → Arduino Pin 4
- Pin → Arduino GND
```

### 2.2 Enclosure Preparation
```
For Outdoor Deployment:
1. Select IP54 or better enclosure
2. Cut holes for sensors (ensure proper sealing)
3. Install cable glands for wires
4. Add desiccant pack for moisture control
5. Secure all components with mounting tape or screws

For Indoor Deployment:
1. Standard plastic enclosure sufficient
2. Ensure ventilation to prevent overheating
3. Label all connections clearly
```

## 3. Software Setup

### 3.1 Arduino IDE Installation
```
1. Download Arduino IDE from https://www.arduino.cc
2. Install on your computer
3. Select correct board (Arduino Uno)
4. Select correct port (COM port for your Arduino)
```

### 3.2 Uploading the Code
```
1. Open environmental_station.ino from hardware folder
2. Verify the code compiles (Ctrl+R)
3. Upload to Arduino (Ctrl+U)
4. Open Serial Monitor (Ctrl+Shift+M)
5. Set baud rate to 9600
6. Verify "SISTEMA_INICIADO" message appears
```

### 3.3 Initial Testing
```
Test Sequence:
1. Verify RGB LED shows blue initially
2. Place object within 10cm - should turn red with buzzer
3. Place object at 10-30cm - should turn green
4. Remove object - should return to blue
5. Check Serial Monitor for data output
```

## 4. Field Deployment

### 4.1 Site Preparation
```
Day Before Deployment:
1. Clear vegetation from sensor area
2. Install mounting platform if needed
3. Test power source availability
4. Inform local authorities/community

Deployment Day:
1. Transport system securely
2. Verify all components survived transport
3. Set up in planned location
4. Secure against weather and theft
```

### 4.2 Sensor Placement Guidelines

**Ultrasonic Sensor Placement:**
```
- Mount 1-2 meters above ground for vegetation monitoring
- Ensure clear line of sight to target area
- Angle slightly downward for ground measurements
- Protect from direct rain and debris
```

**IR Sensor Placement:**
```
- Mount 2-5cm above surface
- Ensure consistent distance to target
- Protect from direct sunlight
- Clean lens regularly
```

**General Placement Tips:**
```
- Avoid areas with frequent human disturbance
- Consider seasonal variations (flooding, vegetation growth)
- Ensure maintenance access
- Document exact location with GPS coordinates
```

### 4.3 Power System Setup
```
USB Power Bank Option:
1. Use 10,000mAh or larger power bank
2. Expected runtime: 100+ hours
3. Charge weekly or as needed

Solar Power Option:
1. 10W solar panel minimum
2. Charge controller for battery protection
3. 12V battery with 5V regulator
4. Expected indefinite operation with good sun

Grid Power Option:
1. Use quality USB charger
2. Surge protector recommended
3. Uninterruptible power supply for reliability
```

## 5. Data Collection Setup

### 5.1 Serial Data Logging
```
Using Laptop:
1. Connect via USB cable
2. Use serial terminal software
3. Set to append to file
4. Verify data recording

Using Raspberry Pi:
1. Connect via USB
2. Use Python script for logging
3. Configure automatic startup
4. Set up remote access

Using SD Card Module:
1. Add SD card module to Arduino
2. Modify code to write to SD card
3. Format SD card as FAT32
4. Retrieve data periodically
```

### 5.2 Data Management
```
File Naming Convention:
YYYY-MM-DD_location_parameter.csv
Example: 2024-12-12_gorongosa_vegetation.csv

Data Backup Schedule:
- Daily: Quick verification
- Weekly: Full backup to external drive
- Monthly: Archive to cloud storage

Metadata Recording:
- Location coordinates
- Deployment date and time
- Environmental conditions
- Any disturbances or issues
```

## 6. Calibration Procedures

### 6.1 Initial Calibration
```
Ultrasonic Sensor:
1. Measure known distances (10, 50, 100cm)
2. Compare with sensor readings
3. Calculate correction factor if needed
4. Update code constants if necessary

IR Sensor:
1. Test on reference surfaces (white paper, black paper)
2. Record reflectance values
3. Create calibration curve
4. Set thresholds for different materials
```

### 6.2 Field Calibration
```
Weekly Calibration:
1. Verify sensor alignment
2. Check for obstructions
3. Test with reference object
4. Record any adjustments

Monthly Calibration:
1. Full system test
2. Compare with manual measurements
3. Update calibration factors
4. Document calibration results
```

### 6.3 Temperature Compensation
```
Automatic Compensation:
Speed of sound = 331.4 + (0.606 × temperature°C)

Implementation:
1. Add temperature sensor (optional)
2. Adjust distance calculation
3. Update every measurement cycle
```

## 7. Maintenance Procedures

### 7.1 Daily Checks (Remote)
```
Visual Indicators:
- Blue LED: System normal
- Flashing patterns: Error conditions
- No LED: Power issue

Data Monitoring:
- Check data file growth
- Verify regular timestamps
- Look for error patterns
```

### 7.2 Weekly Maintenance
```
On-site Tasks:
1. Clean sensor lenses
2. Check power connections
3. Verify mounting security
4. Download data
5. Record observations

Cleaning Procedure:
1. Use soft, dry cloth
2. Avoid chemicals on sensors
3. Check for spider webs/debris
4. Ensure no water accumulation
```

### 7.3 Monthly Maintenance
```
Comprehensive Check:
1. Full system calibration
2. Battery check/replacement
3. Enclosure inspection
4. Cable condition check
5. Firmware update check

Preventive Maintenance:
1. Replace desiccant packs
2. Apply dielectric grease to connections
3. Check for corrosion
4. Update documentation
```

## 8. Troubleshooting Guide

### 8.1 Common Issues
```
No Power:
- Check battery/connection
- Verify power switch position
- Test with different power source

No Data Output:
- Check Serial Monitor settings
- Verify baud rate (9600)
- Check USB cable connection

Incorrect Measurements:
- Clean sensor lenses
- Check for obstructions
- Recalibrate sensors

LED Not Working:
- Check resistor values
- Verify common cathode connection
- Test LED with direct power
```

### 8.2 Error Codes and Solutions
```
Serial Output Patterns:
- "ERR_SENSOR": Sensor connection issue
- "ERR_POWER": Voltage out of range
- "ERR_MEMORY": Data logging issue
- Continuous beeping: Critical error

Solutions:
1. Restart system
2. Check all connections
3. Recalibrate sensors
4. Contact support if persistent
```

### 8.3 Emergency Procedures
```
Weather Events:
- Heavy rain: Check waterproofing
- High winds: Secure mounting
- Lightning: Disconnect if possible

Security Issues:
- Theft attempt: Document and report
- Vandalism: Photograph and repair
- Animal disturbance: Relocate if necessary

System Failure:
- Document error symptoms
- Attempt basic troubleshooting
- Contact technical support
- Prepare replacement if needed
```

## 9. Data Retrieval and Analysis

### 9.1 Retrieval Methods
```
Direct Connection:
1. Connect laptop via USB
2. Use serial terminal to save data
3. Transfer to analysis computer

Remote Access:
1. SSH into Raspberry Pi
2. Download data files
3. Use cloud sync if configured

Physical Retrieval:
1. Remove SD card
2. Copy files to computer
3. Return SD card to system
```

### 9.2 Data Processing Pipeline
```
Step 1: Data Cleaning
- Remove header rows
- Fix formatting issues
- Handle missing values

Step 2: Quality Control
- Flag out-of-range values
- Identify sensor errors
- Calculate data completeness

Step 3: Analysis
- Run provided Python scripts
- Generate visualizations
- Calculate statistics

Step 4: Reporting
- Create summary reports
- Generate alerts if needed
- Update monitoring database
```

### 9.3 Analysis Tools
```
Provided Software:
- data_analyzer.py: Comprehensive analysis
- visualization.py: Advanced plots
- Sample Jupyter notebooks

Third-Party Tools:
- Excel/Google Sheets for basic analysis
- R for statistical analysis
- QGIS for spatial analysis
```

## 10. Safety Considerations

### 10.1 Electrical Safety
```
Low Voltage Safety:
- All circuits under 12V
- Proper insulation required
- Ground connections important
- Water protection essential

Battery Safety:
- Use quality batteries
- Prevent short circuits
- Proper disposal procedures
- No exposed terminals
```

### 10.2 Environmental Safety
```
Protected Areas:
- Obtain necessary permits
- Follow park regulations
- Minimize environmental impact
- Leave no trace principles

Wildlife Safety:
- Avoid nesting seasons
- Don't disturb animals
- Secure against animal damage
- No feeding wildlife
```

### 10.3 Personal Safety
```
Field Work:
- Work in pairs when possible
- Carry communication device
- Inform others of location
- Have emergency contacts

Equipment Safety:
- Use proper tools
- Lift with care
- Watch for sharp edges
- Wear protective gear
```

## 11. Documentation Requirements

### 11.1 Deployment Log
```
Required Information:
- Date and time of deployment
- GPS coordinates
- Personnel involved
- Weather conditions
- Initial readings
- Photos of setup
- Contact information
```

### 11.2 Maintenance Log
```
Record for Each Visit:
- Date and time
- Tasks performed
- Issues found
- Parts replaced
- Calibration results
- Next visit date
- Signature
```

### 11.3 Data Log
```
Metadata for Each Dataset:
- File name and location
- Time period covered
- Sensor configuration
- Environmental conditions
- Known issues or gaps
- Processing steps applied
```

## 12. Training Requirements

### 12.1 Basic Training (2 hours)
```
Topics Covered:
- System components and purpose
- Basic operation
- Data collection procedures
- Simple troubleshooting
- Safety procedures

Hands-on Practice:
- Assembly demonstration
- Software setup
- Data retrieval
- Basic maintenance
```

### 12.2 Advanced Training (4 hours)
```
Additional Topics:
- Calibration procedures
- Data analysis techniques
- Advanced troubleshooting
- Network deployment
- Quality control methods

Certification:
- Written test
- Practical demonstration
- Maintenance competency
- Safety compliance
```

### 12.3 Ongoing Support
```
Resources Provided:
- Technical manual
- Video tutorials
- Online forum
- Email support
- Regular updates

Community Building:
- User meetings
- Experience sharing
- Problem solving sessions
- New feature requests
```

## 13. Cost Analysis and Budgeting

### 13.1 Initial Costs
```
Equipment (per station):
- Components: $20
- Enclosure: $10
- Cables/connectors: $5
- Tools: $15 (one-time)
- Training materials: $10

Total per station: ~$50
```

### 13.2 Operating Costs
```
Monthly Costs:
- Power: $2-5
- Maintenance: $10
- Data management: $5
- Transportation: Variable

Annual Costs:
- Component replacement: $20
- Software updates: Free
- Training refresher: $50
```

### 13.3 Budget Planning
```
Small Project (5 stations):
- Initial: $250
- Annual: $500
- 3-year total: $1,750

Medium Project (20 stations):
- Initial: $1,000
- Annual: $2,000
- 3-year total: $7,000

Large Project (100 stations):
- Initial: $5,000
- Annual: $10,000
- 3-year total: $35,000
```

This deployment guide provides complete instructions for successfully implementing the environmental monitoring station in various settings in Mozambique. Following these procedures will ensure reliable operation and valuable data collection for environmental monitoring and research.
