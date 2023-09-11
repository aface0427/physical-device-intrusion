import json
from typing import List

from DeviceEntity.Branch import Branch
from DeviceEntity.Breaker import Breaker
from DeviceEntity.Energymeter import EnergyMeter
from DeviceEntity.Gateway import GateWay


def dict_to_gateway(o: dict) -> GateWay:
    decoded_gateway = GateWay(
        o.get('ip'),
        o.get('port')
    )
    return decoded_gateway


def dict_to_energymeter(o: dict) -> EnergyMeter:
    decoded_energymeter = EnergyMeter(
        o.get('type'),
        o.get('addr')
    )
    return decoded_energymeter


def dict_to_breaker(o: dict) -> Breaker:
    decoded_breaker = Breaker(
        o.get('addr')
    )
    return decoded_breaker


def dict_to_branch(o: dict) -> Branch:
    decoded_energymeter = Branch(
        o.get('name'),
        dict_to_breaker(o.get('breaker')),
        dict_to_energymeter(o.get("meter")),
        o.get("voltThreshold"),
        o.get("elecThreshold"),
        o.get("activePowerThreshold")
    )
    return decoded_energymeter


def BranchDecode(jsonPath: str) -> Branch:
    with open(jsonPath, encoding="utf-8") as f:
        o = json.load(f)
    return dict_to_branch(o)


def BranchListDecode(jsonPath: str) -> List[Branch]:
    with open(jsonPath, encoding="utf-8") as f:
        o = json.load(f)
    branchList = []
    for key, value in o.items():
        branchList.append(dict_to_branch(value))
    return branchList


def GatewayDecode(jsonPath: str) -> GateWay:
    with open(jsonPath, encoding="utf-8") as f:
        o = json.load(f)
    return dict_to_gateway(o)


def CommonDecode(jsonPath: str) -> dict:
    with open(jsonPath, encoding="utf-8") as f:
        o = json.load(f)
    return o


# def EnergyMeterDecode(jsonPath:str)->EnergyMeter:
#     with open(jsonPath) as f:
#         o=json.load(f)
#     return dict_to_energymeter(o)


if __name__ == '__main__':
    a = BranchListDecode("../Config/branch.json")
    print(a)
