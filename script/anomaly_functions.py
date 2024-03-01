from script.requirements import *

def percentuale_errori_func(plant):
    if plant == 'IN10':
        percentuale_errori = 0.2
    elif plant == 'CN10':
        percentuale_errori = 0.15
    elif plant == 'JP11':
        percentuale_errori = 0.1
    elif plant == 'US10':
        percentuale_errori = 0.05
    elif plant == 'BR10':
        percentuale_errori = 0.05
    elif plant == 'DE10':
        percentuale_errori = 0.01
    return percentuale_errori

def qta_anomaly(diff, EKDS, EKPO, RSEG, EKKO):
    c = len(EKDS)
    for q in range(len(EKPO)):
        change_for_item = random.randint(1,3)
        for k in range(change_for_item):
            werks_to_change = EKPO.loc[q, 'WERKS']
            percentuale_errori = percentuale_errori_func(werks_to_change)
            if random.random() < percentuale_errori:
                ebeln = EKPO.loc[q, 'EBELN']
                ebelp = EKPO.loc[q, 'EBELP']
                itdat = EKPO.loc[q, 'ITDAT']
                aedat = EKKO.loc[EKKO['EBELN'] == ebeln, 'AEDAT'].iloc[0]

                x = random.choice(diff)
                new_value = RSEG.loc[q, 'MENGE'] + x
                if new_value <= 0:
                    new_value = RSEG.loc[q, 'MENGE'] + 1
                
                rand = random.random()
                # diverso menge, delge e rseg menge
                # no anomaly
                if rand < 0.7:
                    RSEG.loc[q, 'MENGE'] = new_value
                    EKPO.loc[q, 'DELGE'] = new_value
                    EKPO.loc[q, 'MENGE'] = new_value
                    EKDS.loc[c, 'EBELN'] = ebeln
                    EKDS.loc[c, 'EBELP'] = ebelp
                    udate = random_dates_business(aedat, itdat)
                    EKDS.loc[c, 'UDATE'] = udate
                    EKDS.loc[c, 'FIELD'] = 'Q'
                    EKDS.loc[c, 'VALUE'] = new_value
                
                # no anomaly
                if (rand >= 0.7) & (rand < 0.8):
                    EKPO.loc[q, 'DELGE'] = new_value
                    EKPO.loc[q, 'MENGE'] = new_value
                    EKDS.loc[c, 'EBELN'] = ebeln
                    EKDS.loc[c, 'EBELP'] = ebelp
                    udate = random_dates_business(aedat, itdat)
                    EKDS.loc[c, 'UDATE'] = udate
                    EKDS.loc[c, 'FIELD'] = 'Q'
                    EKDS.loc[c, 'VALUE'] = new_value
                    
                # anomaly menge e delge
                else:
                    EKPO.loc[q, 'MENGE'] = new_value
                    
                    EKDS.loc[c, 'EBELN'] = ebeln
                    EKDS.loc[c, 'EBELP'] = ebelp
                    udate = random_dates_business(aedat, itdat)
                    EKDS.loc[c, 'UDATE'] = udate
                    EKDS.loc[c, 'FIELD'] = 'Q'
                    EKDS.loc[c, 'VALUE'] = new_value
                c += 1
    return EKDS, EKPO, RSEG

# def qta_anomaly_RSEG(diff, RSEG):
#     for q in range(len(RSEG)):
#         werks_to_change = RSEG.loc[q, 'WERKS']
#         if werks_to_change == 'IN10':
#             percentuale_errori = 0.3
#         elif werks_to_change == 'CN10':
#             percentuale_errori = 0.25
#         elif werks_to_change == 'JP11':
#             percentuale_errori = 0.2
#         elif werks_to_change == 'US10':
#             percentuale_errori = 0.15
#         elif werks_to_change == 'BR10':
#             percentuale_errori = 0.1
#         elif werks_to_change == 'DE10':
#             percentuale_errori = 0.01

#         if random.random() < percentuale_errori:
#             x = random.choice(diff)
#             new_value = RSEG.loc[q, 'MENGE'] + x
#             if new_value <= 0:
#                 new_value = RSEG.loc[q, 'MENGE'] + 1
#             RSEG.loc[q, 'MENGE'] = new_value

#     return RSEG

def drop_PR(EBAN):
    for q in range(len(EBAN)):
        werks_to_change = EBAN.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() < percentuale_errori:
            EBAN = EBAN.drop(q)
            #EBAN = EBAN.reset_index(drop=True)
    return EBAN

def price_anomaly(EKDS, EKPO, EKKO):
    c = len(EKDS)
    for q in range(len(EKPO)):
        
        change_for_item = random.randint(1,5)
        for k in range(change_for_item):
            
            werks_to_change = EKPO.loc[q, 'WERKS']
            percentuale_errori = percentuale_errori_func(werks_to_change)
            if random.random() <= percentuale_errori:
                if EKPO.loc[q, 'NETPR'] != '':
                    ebeln = EKPO.loc[q, 'EBELN']
                    ebelp = EKPO.loc[q, 'EBELP']
                    itdat = EKPO.loc[q, 'ITDAT']
                    aedat = EKKO.loc[EKKO['EBELN'] == ebeln, 'AEDAT'].iloc[0]
                    netpr = EKPO.loc[q, 'NETPR']

                    diff = np.arange(-netpr*5/100, netpr*5/100)
                    x = random.choice(diff)
                    new_price = int(np.round(EKPO.loc[q, 'NETPR'] + x))
                    if (new_price <= 0):
                        new_price = EKPO.loc[q, 'NETPR'] + 1

                    EKPO.loc[q, 'NETPR'] = new_price
                    EKDS.loc[c, 'EBELN'] = ebeln
                    EKDS.loc[c, 'EBELP'] = ebelp
                    udate = random_dates_business(aedat, itdat)
                    EKDS.loc[c, 'UDATE'] = udate
                    EKDS.loc[c, 'FIELD'] = 'P'
                    EKDS.loc[c, 'VALUE'] = new_price
                    c += 1
    return EKDS, EKPO, EKKO

def price_anomaly_RSEG(RSEG):
    for q in range(len(RSEG)):
        werks_to_change = RSEG.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() <= percentuale_errori:
            netpr = RSEG.loc[q, 'NETPR']
            diff = np.arange(-netpr*5/100, netpr*5/100)
            x = random.choice(diff)
            new_price = np.round(RSEG.loc[q, 'NETPR'] + x)
            if (new_price <= 0):
                new_price = RSEG.loc[q, 'NETPR'] + 1
            RSEG.loc[q, 'NETPR'] = new_price
    return RSEG

# def invoice_anomaly_RBKP(RBKP):
#     for q in range(len(RBKP)):
#         werks_to_change = RBKP.loc[q, 'WERKS']
#         if werks_to_change == 'IN10':
#             percentuale_errori = 0.3
#         elif werks_to_change == 'CN10':
#             percentuale_errori = 0.25
#         elif werks_to_change == 'JP11':
#             percentuale_errori = 0.2
#         elif werks_to_change == 'US10':
#             percentuale_errori = 0.15
#         elif werks_to_change == 'BR10':
#             percentuale_errori = 0.1
#         elif werks_to_change == 'DE10':
#             percentuale_errori = 0.01
        
#         if random.random() <= percentuale_errori:
#             bpdat = RBKP.loc[q, 'BPDAT']
#             x = random.randint(0,10)
#             new_bpdat = dates_business(bpdat + dt.timedelta(days = x))
#             RBKP.loc[q, 'BPDAT'] = new_bpdat
#     return RBKP

def payment_block(RBKP):
    for q in range(len(RBKP)):
        werks_to_change = RBKP.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() <= percentuale_errori:
            block_date = dates_business(RBKP.loc[q, 'BLDAT'] + dt.timedelta(random.randint(1,10)))
            rlock_date = dates_business(block_date + dt.timedelta(random.randint(1,10)))

            RBKP.loc[q, 'BLOCK'] = block_date
            RBKP.loc[q, 'RLOCK'] = rlock_date
            RBKP.loc[q, 'BPDAT'] = dates_business(rlock_date + dt.timedelta(random.randint(1,10)))
    return RBKP

def LOEKZ_anomaly(EBAN):
    for q in range(len(EBAN)):
        werks_to_change = EBAN.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() < percentuale_errori:
            EBAN.loc[q, 'LOEKZ'] = 'x'
    return EBAN

def end_process(EBAN, RBKP, EKKO, EKPO, RSEG, EKDS):
    EBAN_reduced = EBAN.loc[EBAN['LOEKZ'] == 'x'].reset_index(drop = True)
    for q in range(len(EBAN_reduced)):
        werks_to_change = EBAN_reduced.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() > percentuale_errori:
            ebeln = EBAN_reduced.iloc[q][['EBELN']][0]
            ebelp = EBAN_reduced.iloc[q][['EBELP']][0]
            belnr = EKPO.loc[(EKPO['EBELN'] == ebeln) & (EKPO['EBELP'] == ebelp), 'BELNR'].iloc[0]
            
            EKPO.loc[(EKPO['EBELN'] == ebeln) & (EKPO['EBELP'] == ebelp), ['LEWED', 'DRDAT', 'BUZEI', 'BELNR', 'ITDAT', 'SEDAT', 'LCWED']] = pd.NaT
            EKPO.loc[(EKPO['EBELN'] == ebeln) & (EKPO['EBELP'] == ebelp), 'ELIKZ'] = 'x'
            EKKO.loc[(EKKO['EBELN'] == ebeln), 'AEDAT'] = pd.NaT
            
            EKDS.loc[(EKDS['EBELN'] == ebeln) & (EKDS['EBELP'] == ebelp), 'UDATE'] = pd.NaT

            # RBKP = RBKP.drop(RBKP.loc[(RBKP['BELNR'] == belnr)].index).reset_index(drop = True)
            # EKPO = EKPO.drop(EKPO.loc[(EKPO['EBELN'] == ebeln) & (EKPO['EBELP'] == ebelp)].index).reset_index(drop = True)
            if EKPO.loc[(EKPO['EBELN'] == ebeln), 'DRDAT'].isnull().all():
                EKKO = EKKO.drop(EKKO.loc[(EKKO['EBELN'] == ebeln)].index).reset_index(drop = True)
            
            RSEG = RSEG.drop(RSEG.loc[(RSEG['EBELN'] == ebeln) & (RSEG['EBELP'] == ebelp)].index).reset_index(drop = True)
            if len(RSEG.loc[(RSEG['BELNR'] == belnr)]) == 0:
                RBKP = RBKP.drop(RBKP.loc[(RBKP['BELNR'] == belnr)].index).reset_index(drop = True)
            
    return EBAN, RBKP, EKKO, EKPO, RSEG, EKDS

def LOEKE_anomaly(EKPO):
    for q in range(len(EKPO)):
        werks_to_change = EKPO.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() < percentuale_errori:
            EKPO.loc[q, 'LOEKE'] = 'x'
    return EKPO

def end_process_ekpo(EKPO, RBKP, RSEG, EKDS):
    EKPO_reduced = EKPO.loc[EKPO['LOEKE'] == 'x'].reset_index(drop = True)
    for q in range(len(EKPO_reduced)):
        werks_to_change = EKPO_reduced.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() > percentuale_errori:

            ebeln = EKPO_reduced.iloc[q][['EBELN']][0]
            ebelp = EKPO_reduced.iloc[q][['EBELP']][0]
            belnr = EKPO.loc[(EKPO['EBELN'] == ebeln) & (EKPO['EBELP'] == ebelp), 'BELNR'].iloc[0]
            drdat = EKPO.loc[(EKPO['EBELN'] == ebeln) & (EKPO['EBELP'] == ebelp), 'DRDAT'].iloc[0]

            EKPO.loc[(EKPO['EBELN'] == ebeln) & (EKPO['EBELP'] == ebelp), ['LEWED', 'BUZEI', 'BELNR', 'ITDAT', 'SEDAT', 'LCWED']] = pd.NaT
            EKDS.loc[(EKDS['EBELN'] == ebeln) & (EKDS['EBELP'] == ebelp) & (EKDS['UDATE'] > drdat), 'UDATE'] = pd.NaT
            EKPO.loc[(EKPO['EBELN'] == ebeln) & (EKPO['EBELP'] == ebelp), 'ELIKZ'] = 'x'

            # RBKP = RBKP.drop(RBKP.loc[(RBKP['BELNR'] == belnr)].index).reset_index(drop = True)
            RSEG = RSEG.drop(RSEG.loc[(RSEG['EBELN'] == ebeln) & (RSEG['EBELP'] == ebelp)].index).reset_index(drop = True)
            if len(RSEG.loc[(RSEG['BELNR'] == belnr)]) == 0:
                RBKP = RBKP.drop(RBKP.loc[(RBKP['BELNR'] == belnr)].index).reset_index(drop = True)
    return EKPO, RBKP, RSEG, EKDS

def PR_anomaly(EBAN):
    for q in range(len(EBAN)):
        werks_to_change = EBAN.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() < percentuale_errori:
            new_date = dates_business(EBAN.loc[q, 'BADAT'] + dt.timedelta(random.randint(1,10)))
            EBAN.loc[q, 'BADAT'] = new_date
            EBAN.loc[q, 'FRGDT'] = dates_business(new_date + dt.timedelta(random.randint(1,10)))
    return EBAN

def fatture_anticipo(RBKP):
    for q in range(len(RBKP)):
        werks_to_change = RBKP.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() <= percentuale_errori:
            diff = dt.timedelta(random.randint(5,20))
            
            RBKP.loc[q, 'BLDAT'] = dates_business(RBKP.loc[q, 'BLDAT'] - diff)
            RBKP.loc[q, 'BUDAT'] = dates_business(RBKP.loc[q, 'BUDAT'] - diff)
            RBKP.loc[q, 'BPDAT'] = dates_business(RBKP.loc[q, 'BPDAT'] - diff)
            
            if pd.isnull(RBKP.loc[q, 'BLOCK']) != True:
                RBKP.loc[q, 'BLOCK'] = dates_business(RBKP.loc[q, 'BLOCK'] - diff)
                RBKP.loc[q, 'RLOCK'] = dates_business(RBKP.loc[q, 'RLOCK'] - diff)
    return RBKP

def merce_anticipo(EKPO):
    for q in range(len(EKPO)):
        werks_to_change = EKPO.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() <= percentuale_errori:
            if pd.isnull(EKPO.loc[q, 'DRDAT']) != True:
                diff = dt.timedelta(random.randint(1,10))
                EKPO.loc[q, 'DRDAT'] = dates_business(EKPO.loc[q, 'DRDAT'] + diff)
    return EKPO

def wrong_approver(EBAN, P0002):
    df_approver = P0002.loc[P0002['MATKL'] != ''].reset_index(drop=True)
    for q in range(len(EBAN)):
        werks_to_change = EBAN.loc[q, 'WERKS']
        percentuale_errori = percentuale_errori_func(werks_to_change)
        if random.random() <= percentuale_errori:
            new_approver = np.random.choice(np.array(df_approver.loc[df_approver['WERKS'] == werks_to_change, 'PERNR']))      
            EBAN.loc[q, 'PERNR'] = new_approver
    return EBAN
