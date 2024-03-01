from script.requirements import *
from script.anomaly_functions import *



diff = np.delete(np.arange(-5,5), 5)
EKDS, EKPO, RSEG = qta_anomaly(diff, EKDS, EKPO, RSEG, EKKO)
EKPO.loc[EKPO['DELGE'] <= 0, 'DELGE'] = 1
RSEG.loc[RSEG['MENGE'] <= 0, 'MENGE'] = 1
EKDS.loc[EKDS['VALUE'] <= 0, 'VALUE'] = 1
EKDS = EKDS.sort_values(by = ['EBELN', 'EBELP', 'UDATE'])
EKDS, EKPO, EKKO = price_anomaly(EKDS, EKPO, EKKO)
RSEG = price_anomaly_RSEG(RSEG)
EKDS = EKDS.sort_values(by = ['EBELN', 'EBELP', 'UDATE'])
RBKP = payment_block(RBKP)
EBAN = LOEKZ_anomaly(EBAN)
EBAN, RBKP, EKKO, EKPO, RSEG, EKDS = end_process(EBAN, RBKP, EKKO, EKPO, RSEG, EKDS)
EKPO = LOEKE_anomaly(EKPO)
EKPO, RBKP, RSEG, EKDS = end_process_ekpo(EKPO, RBKP, RSEG, EKDS)
EBAN = PR_anomaly(EBAN)
EBAN = drop_PR(EBAN).reset_index(drop=True)
RBKP = fatture_anticipo(RBKP)
EKPO = merce_anticipo(EKPO)
EBAN = wrong_approver(EBAN, P0002)