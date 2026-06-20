from mcp.server.fastmcp import FastMCP
from mcp.mock_audi_ecu import audi_car

mcp = FastMCP("Audi Diagnostic Gateway")


@mcp.tool()
def read_car_fault_codes() -> dict:
    """Reads active Diagnostic Trouble Codes (DTCs) and freeze frame parameters from the Audi network."""
    return audi_car.read_dtcs()


@mcp.tool()
def read_audi_sensor_parameter(did_hex: str) -> dict:
    """Queries live telemetry values via UDS Data Identifiers (e.g., '0x2000' for Oil Temp, '0x2002' for Boost)."""
    val = audi_car.read_did(did_hex)
    return {"did": did_hex, "value": val}


@mcp.tool()
def clear_car_fault_codes() -> dict:
    """Attempts a write sequence to clear vehicle diagnostic code registers. Protected by automated safety guardrails."""
    try:
        res = audi_car.clear_dtcs()
        return {"status": "success", "data": res}
    except PermissionError as e:
        return {"status": "failed", "safety_violation": True, "error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
