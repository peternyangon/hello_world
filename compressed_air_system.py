"""
Compressed Air Creation System
Models the complete process of creating compressed air from ambient air intake
through storage, including all intermediate stages.
"""

import time
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class CompressorType(Enum):
    """Types of air compressors"""
    RECIPROCATING = "reciprocating"
    ROTARY_SCREW = "rotary_screw"
    CENTRIFUGAL = "centrifugal"


class FilterType(Enum):
    """Types of air filters"""
    PARTICLE = "particle_filter"
    COALESCING = "coalescing_filter"
    ACTIVATED_CARBON = "activated_carbon"


@dataclass
class AirState:
    """Represents the state of air at any point in the system"""
    pressure_psi: float  # Pressure in PSI
    temperature_f: float  # Temperature in Fahrenheit
    humidity_percent: float  # Relative humidity
    particle_count: int  # Particles per million
    volume_cfm: float  # Volume in cubic feet per minute

    def __str__(self):
        return (f"Pressure: {self.pressure_psi:.2f} PSI, "
                f"Temp: {self.temperature_f:.2f}°F, "
                f"Humidity: {self.humidity_percent:.2f}%, "
                f"Flow: {self.volume_cfm:.2f} CFM")


class AirIntake:
    """Stage 1: Air intake from ambient environment"""

    def __init__(self, intake_filter_efficiency: float = 0.99):
        self.intake_filter_efficiency = intake_filter_efficiency

    def intake_air(self, ambient_temp_f: float = 70.0,
                   ambient_humidity: float = 50.0,
                   flow_rate_cfm: float = 100.0) -> AirState:
        """
        Draw in ambient air and perform initial filtration
        """
        print("\n=== STAGE 1: AIR INTAKE ===")
        print(f"Drawing ambient air at {ambient_temp_f}°F, {ambient_humidity}% humidity")

        # Initial air state at atmospheric pressure
        initial_particles = 10000000  # 10 million particles/m³ in ambient air

        # Filter removes particles
        filtered_particles = int(initial_particles * (1 - self.intake_filter_efficiency))

        air_state = AirState(
            pressure_psi=14.7,  # Atmospheric pressure
            temperature_f=ambient_temp_f,
            humidity_percent=ambient_humidity,
            particle_count=filtered_particles,
            volume_cfm=flow_rate_cfm
        )

        print(f"Intake filter removed {initial_particles - filtered_particles:,} particles")
        print(f"Air state after intake: {air_state}")

        return air_state


class CompressionStage:
    """Represents a single compression stage"""

    def __init__(self, stage_number: int, compression_ratio: float,
                 efficiency: float = 0.85):
        self.stage_number = stage_number
        self.compression_ratio = compression_ratio
        self.efficiency = efficiency

    def compress(self, air_state: AirState) -> AirState:
        """
        Compress air according to compression ratio
        Temperature increases with compression (adiabatic heating)
        """
        print(f"\n  Stage {self.stage_number} compression (ratio: {self.compression_ratio}:1)")

        # Calculate new pressure
        new_pressure = air_state.pressure_psi * self.compression_ratio

        # Adiabatic temperature rise: T2 = T1 * (P2/P1)^((k-1)/k)
        # For air, k (heat capacity ratio) ≈ 1.4
        temp_ratio = (new_pressure / air_state.pressure_psi) ** 0.286
        theoretical_temp = (air_state.temperature_f + 459.67) * temp_ratio - 459.67

        # Account for efficiency losses (generate more heat)
        actual_temp = theoretical_temp + (theoretical_temp - air_state.temperature_f) * (1 - self.efficiency) / self.efficiency

        # Volume decreases inversely with pressure (Boyle's Law)
        new_volume = air_state.volume_cfm / self.compression_ratio

        # As air compresses, relative humidity handling changes
        # We'll simplify by keeping absolute humidity constant
        new_humidity = air_state.humidity_percent * self.compression_ratio
        if new_humidity > 100:
            new_humidity = 100  # Saturation point

        compressed_air = AirState(
            pressure_psi=new_pressure,
            temperature_f=actual_temp,
            humidity_percent=new_humidity,
            particle_count=air_state.particle_count,
            volume_cfm=new_volume
        )

        print(f"  Output: {compressed_air}")

        return compressed_air


class Intercooler:
    """Cools air between compression stages"""

    def __init__(self, cooling_efficiency: float = 0.75,
                 coolant_temp_f: float = 85.0):
        self.cooling_efficiency = cooling_efficiency
        self.coolant_temp_f = coolant_temp_f

    def cool(self, air_state: AirState, stage_name: str = "Intercooler") -> AirState:
        """
        Cool compressed air using heat exchanger
        Also causes moisture condensation
        """
        print(f"\n  {stage_name}:")
        print(f"  Cooling from {air_state.temperature_f:.2f}°F")

        # Cool air towards coolant temperature based on efficiency
        temp_drop = (air_state.temperature_f - self.coolant_temp_f) * self.cooling_efficiency
        new_temp = air_state.temperature_f - temp_drop

        # Cooling causes moisture condensation
        # Simplified: reduce humidity as we cool
        dew_point_drop = temp_drop / 2
        new_humidity = air_state.humidity_percent * (1 - dew_point_drop / air_state.temperature_f)

        moisture_removed = air_state.humidity_percent - new_humidity

        cooled_air = AirState(
            pressure_psi=air_state.pressure_psi,
            temperature_f=new_temp,
            humidity_percent=new_humidity,
            particle_count=air_state.particle_count,
            volume_cfm=air_state.volume_cfm
        )

        print(f"  Cooled to {new_temp:.2f}°F, removed {moisture_removed:.2f}% moisture")
        print(f"  Output: {cooled_air}")

        return cooled_air


class MoistureSeparator:
    """Removes condensed moisture from compressed air"""

    def __init__(self, separation_efficiency: float = 0.90):
        self.separation_efficiency = separation_efficiency

    def separate(self, air_state: AirState) -> AirState:
        """
        Remove condensed moisture droplets
        """
        print(f"\n  Moisture Separator:")

        # Remove moisture based on efficiency
        moisture_removed = air_state.humidity_percent * self.separation_efficiency * 0.1
        new_humidity = air_state.humidity_percent - moisture_removed

        # Also removes some particles trapped in water droplets
        particles_removed = int(air_state.particle_count * 0.3)

        dry_air = AirState(
            pressure_psi=air_state.pressure_psi,
            temperature_f=air_state.temperature_f,
            humidity_percent=new_humidity,
            particle_count=air_state.particle_count - particles_removed,
            volume_cfm=air_state.volume_cfm
        )

        print(f"  Removed {moisture_removed:.2f}% humidity and {particles_removed:,} particles")
        print(f"  Output: {dry_air}")

        return dry_air


class AirDryer:
    """Final air drying stage"""

    def __init__(self, dryer_type: str = "refrigerated",
                 dew_point_f: float = 35.0):
        self.dryer_type = dryer_type
        self.dew_point_f = dew_point_f

    def dry(self, air_state: AirState) -> AirState:
        """
        Remove remaining moisture to achieve target dew point
        """
        print(f"\n  Air Dryer ({self.dryer_type}):")
        print(f"  Target dew point: {self.dew_point_f}°F")

        # Achieve target dew point
        final_humidity = max(5.0, air_state.humidity_percent * 0.1)

        dried_air = AirState(
            pressure_psi=air_state.pressure_psi,
            temperature_f=air_state.temperature_f,
            humidity_percent=final_humidity,
            particle_count=air_state.particle_count,
            volume_cfm=air_state.volume_cfm
        )

        print(f"  Reduced humidity to {final_humidity:.2f}%")
        print(f"  Output: {dried_air}")

        return dried_air


class FinalFilter:
    """Final filtration before storage"""

    def __init__(self, filter_rating_microns: float = 0.01):
        self.filter_rating_microns = filter_rating_microns

    def filter(self, air_state: AirState) -> AirState:
        """
        Remove remaining particles and oil aerosols
        """
        print(f"\n  Final Filter ({self.filter_rating_microns} micron):")

        # High-efficiency final filtration
        particles_removed = int(air_state.particle_count * 0.95)

        filtered_air = AirState(
            pressure_psi=air_state.pressure_psi,
            temperature_f=air_state.temperature_f,
            humidity_percent=air_state.humidity_percent,
            particle_count=air_state.particle_count - particles_removed,
            volume_cfm=air_state.volume_cfm
        )

        print(f"  Removed {particles_removed:,} particles")
        print(f"  Final particle count: {filtered_air.particle_count:,} particles")
        print(f"  Output: {filtered_air}")

        return filtered_air


class StorageTank:
    """Compressed air storage vessel"""

    def __init__(self, capacity_gallons: float = 120.0,
                 max_pressure_psi: float = 175.0):
        self.capacity_gallons = capacity_gallons
        self.max_pressure_psi = max_pressure_psi
        self.current_pressure_psi = 0.0
        self.current_volume_stored = 0.0

    def store(self, air_state: AirState, fill_time_seconds: float = 60.0) -> AirState:
        """
        Store compressed air in tank
        """
        print(f"\n=== STAGE 7: STORAGE TANK ===")
        print(f"Tank capacity: {self.capacity_gallons} gallons")
        print(f"Max pressure: {self.max_pressure_psi} PSI")

        # Simulate filling
        if air_state.pressure_psi > self.max_pressure_psi:
            print(f"WARNING: Pressure regulator limiting to {self.max_pressure_psi} PSI")
            self.current_pressure_psi = self.max_pressure_psi
        else:
            self.current_pressure_psi = air_state.pressure_psi

        self.current_volume_stored = self.capacity_gallons

        stored_air = AirState(
            pressure_psi=self.current_pressure_psi,
            temperature_f=air_state.temperature_f,
            humidity_percent=air_state.humidity_percent,
            particle_count=air_state.particle_count,
            volume_cfm=0.0  # Static storage
        )

        print(f"Tank filled to {self.current_pressure_psi:.2f} PSI")
        print(f"Stored air state: {stored_air}")

        return stored_air


class PressureRegulator:
    """Regulates output pressure for end use"""

    def __init__(self, output_pressure_psi: float = 90.0):
        self.output_pressure_psi = output_pressure_psi

    def regulate(self, air_state: AirState, demand_cfm: float = 10.0) -> AirState:
        """
        Regulate pressure to desired output level
        """
        print(f"\n=== STAGE 8: PRESSURE REGULATION ===")
        print(f"Regulating to {self.output_pressure_psi} PSI for end use")

        regulated_air = AirState(
            pressure_psi=self.output_pressure_psi,
            temperature_f=air_state.temperature_f,
            humidity_percent=air_state.humidity_percent,
            particle_count=air_state.particle_count,
            volume_cfm=demand_cfm
        )

        print(f"Regulated output: {regulated_air}")

        return regulated_air


class CompressedAirSystem:
    """
    Complete compressed air generation system
    Orchestrates all stages from intake to final delivery
    """

    def __init__(self, compressor_type: CompressorType = CompressorType.ROTARY_SCREW,
                 target_pressure_psi: float = 125.0,
                 flow_rate_cfm: float = 100.0):
        self.compressor_type = compressor_type
        self.target_pressure_psi = target_pressure_psi
        self.flow_rate_cfm = flow_rate_cfm

        # Initialize all components
        self.air_intake = AirIntake(intake_filter_efficiency=0.99)

        # Multi-stage compression (2-stage for typical industrial compressor)
        # Calculate compression ratios to achieve target pressure
        total_ratio = target_pressure_psi / 14.7  # From atmospheric
        stage_ratio = total_ratio ** 0.5  # Split evenly between stages

        self.compression_stages = [
            CompressionStage(1, stage_ratio, efficiency=0.85),
            CompressionStage(2, stage_ratio, efficiency=0.85)
        ]

        self.intercooler = Intercooler(cooling_efficiency=0.75, coolant_temp_f=85.0)
        self.aftercooler = Intercooler(cooling_efficiency=0.80, coolant_temp_f=85.0)
        self.moisture_separator = MoistureSeparator(separation_efficiency=0.90)
        self.air_dryer = AirDryer(dryer_type="refrigerated", dew_point_f=35.0)
        self.final_filter = FinalFilter(filter_rating_microns=0.01)
        self.storage_tank = StorageTank(capacity_gallons=120.0,
                                       max_pressure_psi=target_pressure_psi * 1.4)
        self.pressure_regulator = PressureRegulator(output_pressure_psi=90.0)

    def run_cycle(self, ambient_temp_f: float = 70.0,
                  ambient_humidity: float = 50.0) -> AirState:
        """
        Execute a complete compression cycle from intake to storage
        """
        print("=" * 70)
        print("COMPRESSED AIR SYSTEM - COMPLETE CYCLE")
        print(f"Compressor Type: {self.compressor_type.value}")
        print(f"Target Pressure: {self.target_pressure_psi} PSI")
        print(f"Flow Rate: {self.flow_rate_cfm} CFM")
        print("=" * 70)

        # Stage 1: Air Intake
        air = self.air_intake.intake_air(
            ambient_temp_f=ambient_temp_f,
            ambient_humidity=ambient_humidity,
            flow_rate_cfm=self.flow_rate_cfm
        )

        # Stage 2-3: Multi-stage Compression with Intercooling
        print("\n=== STAGE 2: COMPRESSION (Multi-Stage) ===")

        for i, stage in enumerate(self.compression_stages):
            air = stage.compress(air)

            # Intercool between stages (not after last stage)
            if i < len(self.compression_stages) - 1:
                air = self.intercooler.cool(air, f"Intercooler {i+1}")

        # Stage 4: Aftercooling
        print("\n=== STAGE 3: AFTERCOOLING ===")
        air = self.aftercooler.cool(air, "Aftercooler")

        # Stage 5: Moisture Separation
        print("\n=== STAGE 4: MOISTURE SEPARATION ===")
        air = self.moisture_separator.separate(air)

        # Stage 6: Air Drying
        print("\n=== STAGE 5: AIR DRYING ===")
        air = self.air_dryer.dry(air)

        # Stage 7: Final Filtration
        print("\n=== STAGE 6: FINAL FILTRATION ===")
        air = self.final_filter.filter(air)

        # Stage 8: Storage
        air = self.storage_tank.store(air)

        # Stage 9: Pressure Regulation for End Use
        final_air = self.pressure_regulator.regulate(air, demand_cfm=10.0)

        print("\n" + "=" * 70)
        print("CYCLE COMPLETE - Ready for end use")
        print("=" * 70)

        return final_air

    def get_system_status(self) -> dict:
        """Return current system status"""
        return {
            "compressor_type": self.compressor_type.value,
            "target_pressure_psi": self.target_pressure_psi,
            "flow_rate_cfm": self.flow_rate_cfm,
            "tank_pressure_psi": self.storage_tank.current_pressure_psi,
            "tank_capacity_gallons": self.storage_tank.capacity_gallons,
            "compression_stages": len(self.compression_stages)
        }


def main():
    """
    Demonstration of the compressed air system
    """
    print("\n" + "=" * 70)
    print("COMPRESSED AIR CREATION SYSTEM - DEMONSTRATION")
    print("=" * 70)

    # Create a typical industrial compressed air system
    # Target: 125 PSI, 100 CFM flow rate
    system = CompressedAirSystem(
        compressor_type=CompressorType.ROTARY_SCREW,
        target_pressure_psi=125.0,
        flow_rate_cfm=100.0
    )

    # Run a complete cycle
    final_air = system.run_cycle(
        ambient_temp_f=75.0,
        ambient_humidity=60.0
    )

    # Display system status
    print("\n" + "=" * 70)
    print("SYSTEM STATUS")
    print("=" * 70)
    status = system.get_system_status()
    for key, value in status.items():
        print(f"{key}: {value}")

    print("\n" + "=" * 70)
    print("FINAL OUTPUT AIR QUALITY")
    print("=" * 70)
    print(final_air)
    print("\nCompressed air is now ready for industrial applications!")
    print("=" * 70)


if __name__ == "__main__":
    main()
