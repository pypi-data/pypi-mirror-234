class Config:
    INDOOR_SCENARIO_LENGTH_ROOM = 20  # Length of scene in metters
    INDOOR_SCENARIO_HEIGHT_ROOM = 3  # Height of scene in metters
    INDOOR_SCENARIO_MT_HEIGHT = 0.85  # Height of mobile terminal in metters
    INDOOR_SCENARIO_BER_TARGET = 1e-5  # BER target

    VLC_SYSTEM_HEIGHT_LED = 2.5  # Height of LED in metters
    VLC_SYSTEM_POWER_LED = 20  # Power of LED in Wats
    VLC_SYSTEM_NUMBER_OF_LEDS = 16  # Number of LED array
    VLC_SYSTEM_SEMI_ANGLE_HALF_POWER = 70  # Semi angle at half power in degrees
    VLC_SYSTEM_WIDTH_FIELD_VIEW = 60  # Width of the field of view in degrees
    VLC_SYSTEM_DETECTOR_PHYSICAL_AREA_PD = 1  # Detector physical area of a PD in cm^2
    VLC_SYSTEM_REFRACTIVE_INDEX_LENS_PD = 1.5  # Refractive index of a lens at a PD
    VLC_SYSTEM_OE_CONVERSION_EFFICIENCY = 0.53  # O/E Conversion Efficiency in A/W
    VLC_SYSTEM_AVAILABLE_BANDWIDTH = 10  # Available Bandwidth in MHz
    VLC_SYSTEM_REFLECTANCE_FACTOR = 0.8  # Reflectance factor
    VLC_SYSTEM_BACKGROUND_CURRENT = 5.1e-3  # Background current in A
    VLC_SYSTEM_OPEN_LOOP_VOLTAGE_GAIN = 10  # Open-loop voltage gain
    VLC_SYSTEM_FIXED_CAPACITANCE_PD_UNIT_AREA = (
        1.12e-6  # Fixed capacitance of the PD per unit area
    )
    VLC_SYSTEM_FET_CHANNEL_NOISE_FACTOR = 1.5  # FET channel noise factor
    VLC_SYSTEM_FET_TRANSCONDUCTANCE = 3e-2  # FET transconductance

    FEMTOCELL_SYSTEM_POSITION_AP = (
        -10,
        -10,
        2.5,
    )  # Position of the femtocell AP (x, y, z), in metters
    FEMTOCELL_SYSTEM_TRANSMISSION_POWER_BS = (
        0.02  # Transmission power of the femtocell BS in W
    )
    FEMTOCELL_SYSTEM_INDOOR_PATHLOSS_EXPONENT = 3  # Indoor path-loss exponent
    FEMTOCELL_SYSTEM_INDOOR_PATHLOSS_CONSTANT = 37  # Indoor path-loss constant in dB
    FEMTOCELL_SYSTEM_AVAILABLE_BANDWIDTH = 5  # Available bandwidth in MHz

    ACCESS_PROTOCOL_RTS = 144  # RTS in microseconds
    ACCESS_PROTOCOL_CTS = 120  # CTS in microseconds
    ACCESS_PROTOCOL_ACK = 120  # ACK in microseconds
    ACCESS_PROTOCOL_BA = 128  # BA in microseconds
    ACCESS_PROTOCOL_DIFS = 34  # DIFS in microseconds
    ACCESS_PROTOCOL_SIFS = 16  # SIFS in microseconds
    ACCESS_PROTOCOL_SIGMA = 15  # sigma in microseconds
    ACCESS_PROTOCOL_M = 6  # M
    ACCESS_PROTOCOL_N = 50  # N
