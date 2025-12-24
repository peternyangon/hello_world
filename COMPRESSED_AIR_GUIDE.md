# Compressed Air Creation System

## Overview
This implementation models the complete industrial process of creating compressed air, from ambient air intake through final delivery to end-use applications.

## How Compressed Air is Created - Complete Process

### Stage 1: Air Intake & Filtration
- **Purpose**: Draw ambient air and remove large particles
- **Process**:
  - Air enters through intake valve at atmospheric pressure (14.7 PSI)
  - Initial particle filter removes 99% of airborne contaminants
  - Typical flow rates: 50-500 CFM depending on system size

### Stage 2: Multi-Stage Compression
- **Purpose**: Increase air pressure to target level (typically 100-175 PSI)
- **Process**:
  - **First Stage**: Compresses air to intermediate pressure (~40-50 PSI)
    - Adiabatic compression increases temperature significantly
    - Compression ratio typically 3:1 to 4:1
  - **Intercooling**: Cools air between stages
    - Removes heat generated during compression
    - Increases efficiency of next compression stage
    - Condenses moisture for removal
  - **Second Stage**: Compresses to final pressure (100-175 PSI)
    - Additional compression to reach target pressure
    - Further temperature increase
- **Physics**:
  - Pressure increases follow Boyle's Law (P₁V₁ = P₂V₂)
  - Temperature increases follow Gay-Lussac's Law
  - Heat generated: T₂ = T₁ × (P₂/P₁)^((k-1)/k) where k=1.4 for air

### Stage 3: Aftercooling
- **Purpose**: Reduce air temperature after final compression
- **Process**:
  - Heat exchanger uses water or air cooling
  - Reduces temperature from 300-400°F to 100-150°F
  - Causes moisture condensation
  - Improves efficiency and safety

### Stage 4: Moisture Separation
- **Purpose**: Remove condensed water from compressed air
- **Process**:
  - Centrifugal or gravity separator
  - Removes 80-90% of condensed moisture
  - Collects water in drain trap
  - Automatic or manual drain valves

### Stage 5: Air Drying
- **Purpose**: Remove remaining moisture to prevent corrosion and freezing
- **Types**:
  - **Refrigerated Dryers**: Cool air to 35-45°F dew point
  - **Desiccant Dryers**: Absorb moisture, achieve -40°F to -100°F dew point
  - **Membrane Dryers**: Selective permeation for moisture removal
- **Process**: Reduces relative humidity to 5-10%

### Stage 6: Final Filtration
- **Purpose**: Remove remaining particles and oil aerosols
- **Process**:
  - Coalescing filters remove oil and water aerosols
  - Particulate filters down to 0.01 microns
  - Activated carbon filters remove oil vapors and odors
  - Achieves "breathing air" quality if needed

### Stage 7: Storage
- **Purpose**: Provide compressed air reservoir to meet demand fluctuations
- **Process**:
  - Air stored in pressure vessels (receivers)
  - Typical sizes: 60-500 gallons for industrial use
  - Maximum pressure: 20-40% above operating pressure
  - Allows compressor to cycle on/off efficiently
- **Safety**: Pressure relief valves prevent over-pressurization

### Stage 8: Pressure Regulation & Distribution
- **Purpose**: Provide consistent pressure to end-use equipment
- **Process**:
  - Pressure regulators reduce to application pressure (typically 90 PSI)
  - Distribution piping delivers to workstations
  - Point-of-use filters provide final filtration
  - Flow control valves manage air consumption

## Key Components

### Compressor Types
1. **Reciprocating (Piston)**:
   - Best for intermittent use
   - High pressure capability
   - 5-30 HP typical

2. **Rotary Screw** (Implemented in this code):
   - Continuous duty cycle
   - Efficient for constant demand
   - 20-500 HP typical
   - Quieter operation

3. **Centrifugal**:
   - Very high flow rates
   - Oil-free air
   - 100+ HP
   - Used in large facilities

### Cooling Systems
- **Air-Cooled**: Fans blow air over heat exchangers
- **Water-Cooled**: Circulating water removes heat (more efficient)

### Control Systems
- **Pressure Switch**: On/off control
- **Load/Unload**: Unloads compressor at max pressure
- **Variable Speed Drive (VSD)**: Adjusts motor speed to match demand

## Technical Specifications (This Implementation)

```
Compressor Type: Rotary Screw
Target Pressure: 125 PSI
Flow Rate: 100 CFM
Compression Stages: 2
Compression Ratio per Stage: ~2.9:1
Total Compression Ratio: ~8.5:1
Intercooling: Yes (between stages)
Aftercooling: Yes
Moisture Separation: Yes (90% efficiency)
Air Dryer: Refrigerated (35°F dew point)
Final Filtration: 0.01 micron
Storage Tank: 120 gallons @ 175 PSI max
Output Regulation: 90 PSI
Final Air Quality: <3,500 particles, 6% humidity
```

## Energy Efficiency Considerations

1. **Proper Sizing**: Match compressor to actual demand
2. **Leak Prevention**: Fix air leaks (20-30% typical losses)
3. **Pressure Optimization**: Reduce pressure by 2 PSI = 1% energy savings
4. **Heat Recovery**: Capture compressor heat for building heating
5. **VSD Compressors**: Save 35% energy with variable loads
6. **Intake Air Quality**: Clean intake filter maintains efficiency

## Running the Simulation

```bash
python compressed_air_system.py
```

This will execute a complete compression cycle showing:
- Air state at each stage
- Temperature and pressure changes
- Moisture removal
- Particle filtration
- Final output quality

## Applications

Compressed air systems are used in:
- Manufacturing (pneumatic tools, automation)
- Automotive (paint spraying, tire inflation)
- Food & Beverage (packaging, cleaning)
- Medical (dental tools, breathing air)
- Construction (jackhammers, nail guns)
- Industrial processes (conveying, mixing, agitation)

## Safety Notes

- Pressure vessels must be ASME certified
- Regular inspections required
- Pressure relief valves mandatory
- Never exceed rated pressure
- Condensate may contain oil (proper disposal required)
- Breathing air requires special filtration and monitoring
