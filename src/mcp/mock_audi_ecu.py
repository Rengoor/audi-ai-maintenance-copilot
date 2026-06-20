class AudiGatewayECU:
    def __init__(self):
        # Simulated live vehicle bus state
        self.vehicle_speed = 0  # km/h - Change to > 0 to trigger safety trip
        self.active_dtcs = ["P0299"]

        self.freeze_frame_data = {
            "Engine_RPM": 2450,
            "Coolant_Temperature": "92 C",
            "Odometer": "142030 km",
            "Calculated_Load": "78 %",
        }

        # Unified Diagnostic Services (UDS) Data Identifiers (DIDs)
        self.uds_dids = {
            "0x2000": "88 C",  # Engine Oil Temperature
            "0x2001": f"{self.vehicle_speed} km/h",
            "0x2002": "1.2 bar",  # Actual Boost Pressure
            "0x2003": "1.9 bar",  # Specified (Target) Boost Pressure
        }

    def read_dtcs(self) -> dict:
        """UDS Service 0x19: Read Diagnostic Trouble Codes."""
        return {
            "dtcs": self.active_dtcs,
            "freeze_frame": self.freeze_frame_data if self.active_dtcs else {},
        }

    def read_did(self, did_hex: str) -> str:
        """UDS Service 0x22: Read Data By Identifier."""
        clean_did = did_hex.strip().lower()
        # Synchronize dynamic speed reading
        if clean_did == "0x2001":
            return f"{self.vehicle_speed} km/h"
        return self.uds_dids.get(clean_did, "UDS_ERR_REQUEST_OUT_OF_RANGE")

    def clear_dtcs(self) -> dict:
        """
        UDS Service 0x14: Clear Diagnostic Information.
        CRITICAL SAFETY CHECK: Blocks physical modification if vehicle is moving.
        """
        if self.vehicle_speed > 0:
            raise PermissionError(
                f"UDS_SAFETY_ABORT: Vehicle velocity is {self.vehicle_speed} km/h. "
                "Write execution denied. Vehicle must be stationary (0 km/h) to clear non-volatile DTC registers."
            )

        self.active_dtcs.clear()
        self.freeze_frame_data.clear()
        return {
            "status": "UDS_STATUS_SUCCESS",
            "message": "DTC memory cleared successfully.",
        }


# Instantiate global vehicle state object for import
audi_car = AudiGatewayECU()
