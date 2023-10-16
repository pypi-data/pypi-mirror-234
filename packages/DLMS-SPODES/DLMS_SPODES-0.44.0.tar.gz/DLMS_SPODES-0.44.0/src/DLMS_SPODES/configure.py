from .types import cst
from .cosem_interface_classes import cosem_interface_class as ic, collection
from . import exceptions as exc
from .cosem_interface_classes.overview import ClassID


empty_dict = dict()


def get_saved_parameters(obj: ic.COSEMInterfaceClasses) -> dict[int, int]:
    """ return attribute indexes for saved keep configuration dictionary(attr_index: 0-for value 1-for type, ...)"""
    ln = obj.logical_name
    match obj.CLASS_ID, obj.logical_name:
        case collection.Data.CLASS_ID, cst.LogicalName(0, 0, 96, 1, 1 | 3 | 6 | 8) | cst.LogicalName(1, 0, 0, 8, 4):  return {2: 0}
        case collection.Data.CLASS_ID, cst.LogicalName(0, 0, 96, 11, 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8): return empty_dict
        case collection.Data.CLASS_ID, _:                                                        return {2: 1}
        case collection.Register.CLASS_ID, cst.LogicalName(1, 0, 0, 6, 0 | 1 | 2 | 3 | 4):       return {2: 1, 3: 1}
        case collection.Register.CLASS_ID, _:                                                    return {2: 1, 3: 0}
        case collection.ExtendedRegister.CLASS_ID, _:                                            return {2: 1, 3: 0}
        case collection.ProfileGenericVer1.CLASS_ID, cst.LogicalName(1, _, 94, 7, 1 | 2 | 3 | 4): return {6: 0, 3: 0, 2: 0, 4: 0, 5: 0, 8: 0}
        case collection.ProfileGenericVer1.CLASS_ID, _:                                          return {6: 0, 3: 0, 4: 0, 5: 0, 8: 0}
        case collection.Clock.CLASS_ID, _:                                                       return {8: 0, 9: 0}
        case collection.ScriptTable.CLASS_ID, _:                                                 return {2: 0}
        case collection.Schedule.CLASS_ID, _:                                                    return {2: 0}
        case collection.SpecialDaysTable.CLASS_ID, _:                                            return empty_dict
        case collection.ActivityCalendar.CLASS_ID, _:                                            return empty_dict
        case collection.SingleActionSchedule.CLASS_ID, _:                                        return {2: 0, 3: 0, 4: 0}
        case collection.AssociationLNVer0.CLASS_ID, cst.LogicalName(0, 0, 40, 0, 0):             return {3: 0}
        case collection.AssociationLNVer0.CLASS_ID, _:                                           return {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 9: 0}
        case collection.IECHDLCSetupVer1.CLASS_ID, _:                                            return {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
        case collection.DisconnectControl.CLASS_ID, _:                                           return {3: 0, 4: 0}
        case collection.Limiter.CLASS_ID, _:                                                     return {2: 0, 11: 0}
        case collection.PSTNModemConfiguration.CLASS_ID, _:                                      return {2: 0}
        case collection.ImageTransfer.CLASS_ID, _:                                               return {2: 0}
        case collection.GPRSModemSetup.CLASS_ID, _:                                              return {2: 0}
        case collection.GSMDiagnosticVer0.CLASS_ID, _:                                           return empty_dict
        case collection.ClientSetup.CLASS_ID, _:                                                 return empty_dict  # not need only for client
        case collection.TCPUDPSetup.CLASS_ID, _:                                                 return {2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        case collection.IPv4Setup.CLASS_ID, _:                                                   return empty_dict
        case collection.Arbitrator.CLASS_ID, _:                                                  return {2: 0}
        case collection.SecuritySetupVer0.CLASS_ID, _:                                           return {2: 0, 3: 0, 5: 0}
        case collection.RegisterMonitor.CLASS_ID, _:                                             return {3: 0, 2: 0, 4: 0}
        case ClassID.DEMAND_REGISTER, _:                                                         return {2: 1, 3: 1, 4: 0, 5: 1, 8: 0, 9: 0}
        case _: raise exc.NoObject(F'Save configure. Not found {obj} with {obj.CLASS_ID} for read attributes')
