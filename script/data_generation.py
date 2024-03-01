# Dataframe con nuovi dati generati
n_mat_per_ordine = np.ceil(np.random.beta(2,5, size = n_PR) * 5).astype(int)
mat_to_append = [np.random.choice(material_list, size = n_mat_per_ordine[i], replace=False, p=df_materiali['Probability']).astype(int) for i in range(n_PR)]
quantity_to_append = [np.random.randint(1,100, size = n_mat_per_ordine[i]) for i in range(n_PR)]
ordini = np.arange(0, n_PR)
df = pd.DataFrame([[str(ordini[i]), str(mat_to_append[i].item(j)), str(quantity_to_append[i].item(j)),
                    date_purchase_order[i]]
         for i in range(n_PR) for j in range(n_mat_per_ordine[i])],  columns = ['BANFN', 'MATNR', 'MENGE', 'BADAT'])

# Faccio merge con la tabella materiali per unire il codice al materiale corrispondente
df = df.merge(df_materiali[['MATNR','MATKL', 'NETPR', 'PLIFZ','PLICZ', 'PEINH', 'MEINS', 'RKDST', 'LIFNR']], on = 'MATNR', how="left")
# Aggregare stessi materiali e sommare quantità
df = df.groupby(['BANFN','MATKL','MATNR'], as_index=False).agg({'BANFN': 'first', 'MATNR': 'first', 'MENGE': 'sum', 'BADAT' : 'first',
                                                                 'MATKL' : 'first', 'NETPR' : 'first', 'PLIFZ' : 'first','PLICZ' : 'first',
                                                                 'PEINH' : 'first', 'MEINS' : 'first', 'RKDST' : 'first',
                                                                 'LIFNR' : 'first'})

# Aggiorno contatore numero ordini
df['BANFN'] = (df['BANFN'].apply(int) + last_PR).apply(str)
df['BADAT'] = pd.to_datetime(df['BADAT'])

df['BNFPO'] = df.groupby(['BANFN']).cumcount()+1
df['BNFPO'] = df['BNFPO'].astype(str)

# ERNAM
ernam_series = pd.Series(np.random.choice(df_anagraf['PERNR'], size=n_PR, replace=True), index=np.unique(df['BANFN']))
df['ERNAM'] = df['BANFN'].map(ernam_series)
werks_series = pd.Series(np.random.choice(df_anagraf['WERKS'], size=len(df_anagraf), replace=True), index=np.unique(df_anagraf['PERNR']))
df['WERKS'] = df['ERNAM'].map(werks_series)
df['LOEKZ'] = ' '

# FRGDT
diff_array = (np.ceil(np.random.beta(2,4, size = len(df)) * 7) + np.random.choice([0, 1, 2, 3, 4],
                                                                                  size=len(df), replace=True,
                                                                                  p=[0.5, 0.25, 0.15, 0.05, 0.05])).astype(int).tolist()
diff_array = [1 if item == 0 else item for item in diff_array]
diff_dates = [businesstimedelta.BusinessTimeDelta(businesshrs, hours = i*8+1) for i in diff_array]
df['FRGDT'] = (df['BADAT'] + np.array(diff_dates)).map(dates_business)
df['FRGDT'] = pd.to_datetime(df['FRGDT'])

df = pd.merge(df, df_anagraf[['PERNR', 'WERKS', 'MATKL']], on=['WERKS', 'MATKL'], how='left')

# BADAT
df['AEDAT'] = df.apply(lambda row: row.FRGDT + businesstimedelta.BusinessTimeDelta(businesshrs, hours=1*8+1), axis = 1).map(dates_business)
df['AEDAT'] = pd.to_datetime(df['AEDAT'])

df.loc[df['RKDST'] != 'x', ['BADAT', 'FRGDT']] = pd.NaT

prova = df[['WERKS', 'AEDAT']]
n_order = len(prova.drop_duplicates())
count = np.array(prova.groupby(['WERKS', 'AEDAT'], as_index=False).value_counts()['count'])

orders_new = []
for f in range(n_order):
    while True:
        cod_or = str(np.random.randint(100000, 999999))
        if cod_or not in orders:
            break
    orders_new = np.append(orders_new, cod_or).astype(str)
    orders = np.append(orders, cod_or).astype(str)
df = df.sort_values(by = ['WERKS', 'AEDAT'])
ebeln = np.repeat(orders_new, count)
df['EBELN'] = ebeln
df['EBELP'] = df.groupby(['EBELN']).cumcount()+1
df['EBELP'] = df['EBELP'].astype(str)

df['LOEKE'] = ' '

# EKNAM
eknam_series = pd.Series(np.random.choice(df_anagraf['PERNR'], size=len(pd.unique(df['EBELN'])), replace=True), index=np.unique(df['EBELN']))
df['EKNAM'] = df['EBELN'].map(eknam_series)
# EKRNR
ekrnr_series = pd.Series(np.random.choice(df_anagraf['PERNR'], size=len(pd.unique(df['EBELN'])), replace=True), index=np.unique(df['EBELN']))
df['EKRNR'] = df['EBELN'].map(ekrnr_series)

# DRDAT
df['DRDAT'] = df['AEDAT']
diff_array = (np.random.choice([0, 1, 2, 3], size=len(df), replace=True)).tolist()
diff_dates = [businesstimedelta.BusinessTimeDelta(businesshrs, hours = i*8+1) for i in diff_array]
df['DRDAT'] = (df['AEDAT'] + np.array(diff_dates)).map(dates_business)
df['DRDAT'] = pd.to_datetime(df['DRDAT'])

# SEDAT
diff_array = (np.ceil((np.random.beta(13, 1.5, size = len(df)) / 0.98)) * df['PLIFZ']).astype(int).tolist()
diff_dates = [businesstimedelta.BusinessTimeDelta(businesshrs, hours = i*8+1) for i in diff_array]
df['SEDAT'] = (df['DRDAT'] + np.array(diff_dates)).map(dates_business)
grouped = df.groupby(['LIFNR', 'DRDAT']).SEDAT.max().reset_index()
df = df.drop(columns=['SEDAT'])
df = pd.merge(df, grouped, on=['LIFNR', 'DRDAT'], how='left')
df['SEDAT'] = pd.to_datetime(df['SEDAT'])

# LEWED
diff_array = df['PLIFZ'].astype(int).tolist()
diff_dates = [businesstimedelta.BusinessTimeDelta(businesshrs, hours = i*8+1) for i in diff_array]
df['LEWED'] = (df['DRDAT'] + np.array(diff_dates)).map(dates_business)
grouped = df.groupby(['LIFNR', 'DRDAT']).LEWED.max().reset_index()
df = df.drop(columns=['LEWED'])
df = pd.merge(df, grouped, on=['LIFNR', 'DRDAT'], how='left')
df['LEWED'] = pd.to_datetime(df['LEWED'])

# ITDAT
diff_array = (np.ceil((np.random.beta(13,1.5, size = len(df)) / 0.98)) * df['PLICZ']).astype(int).tolist()
diff_dates = [businesstimedelta.BusinessTimeDelta(businesshrs, hours = i*8+1) for i in diff_array]
df['ITDAT'] = (df['SEDAT'] + np.array(diff_dates)).map(dates_business)
grouped = df.groupby(['LIFNR', 'SEDAT']).ITDAT.max().reset_index()
df = df.drop(columns=['ITDAT'])
df = pd.merge(df, grouped, on=['LIFNR', 'SEDAT'], how='left')
df['ITDAT'] = pd.to_datetime(df['ITDAT'])

# LCWED
diff_array = df['PLICZ'].astype(int).tolist()
diff_dates = [businesstimedelta.BusinessTimeDelta(businesshrs, hours = i*8+1) for i in diff_array]
df['LCWED'] = (df['SEDAT'] + np.array(diff_dates)).map(dates_business)
grouped = df.groupby(['LIFNR', 'SEDAT']).LCWED.max().reset_index()
df = df.drop(columns=['LCWED'])
df = pd.merge(df, grouped, on=['LIFNR', 'SEDAT'], how='left')
df['LCWED'] = pd.to_datetime(df['LCWED'])

# DEDAT
diff_array = (np.ceil((np.random.beta(13,1.5, size = len(df)) / 0.98)) * df['PLICZ']).astype(int).tolist()
diff_dates = [businesstimedelta.BusinessTimeDelta(businesshrs, hours = i*8+1) for i in diff_array]
df['DEDAT'] = (df['ITDAT'] + np.array(diff_dates)).map(dates_business)
grouped = df.groupby(['LIFNR', 'ITDAT']).DEDAT.max().reset_index()
df = df.drop(columns=['DEDAT'])
df = pd.merge(df, grouped, on=['LIFNR', 'ITDAT'], how='left')
df['DEDAT'] = pd.to_datetime(df['DEDAT'])

df['DELGE'] = df['MENGE']
# Colonne aggiuntive
df['ELIKZ'] = 'x' # delivery completed indicator


# FATTURE
start_week = pd.to_datetime('2018-12-31')
df['WEEK'] = 0
df['WEEK'] = (df['DRDAT'] - start_week).dt.days//7
fatt_df = df.copy()
invoices_new = []
fatt_df = df[['LIFNR', 'WEEK', 'WERKS']].drop_duplicates()
for f in range(len(fatt_df)):
    while True:
        cod_fatture = str(np.random.randint(4932445, 9748345))
        if cod_fatture not in invoices:
            break
    invoices = np.append(invoices, cod_fatture)
    invoices_new = np.append(invoices_new, cod_fatture)
fatt_df['BELNR'] = [str(int(x)) for x in invoices_new]
df = df.merge(fatt_df[['WEEK', 'LIFNR', 'BELNR', 'WERKS']], on=['WEEK', 'LIFNR', 'WERKS'], how="left")
df['BUZEI'] = df.groupby(['BELNR']).cumcount()+1
df['BUZEI'] = df['BUZEI'].astype(str)
df['EREKZ'] = 'x'

# BLDAT
df['BLDAT'] = (start_week + ((df['WEEK'] + 3)*7).map(dt.timedelta)).map(dates_business)
df = df.sort_values(by = ['BLDAT'])
date, counts = np.unique(df['BLDAT'], return_counts = True)
additions = np.random.choice([0,1,2], size = len(date), replace = True)
bldat = np.repeat(additions, counts)
df['BLDAT'] = df['BLDAT'] + pd.to_timedelta(bldat,  unit='d')
df['BLDAT'] = pd.to_datetime(df['BLDAT'])
# BUDAT
df['BUDAT'] = df['BLDAT'] + dt.timedelta(21)
df['BUDAT'] = pd.to_datetime(df['BUDAT'])

# BPDAT
diff_array = (np.ceil(np.random.beta(2, 5, size = len(df)) * 30)).astype(int).tolist()
diff_dates = [businesstimedelta.BusinessTimeDelta(businesshrs, hours = i*8+1) for i in diff_array]
df['BPDAT'] = (df['BLDAT'] + np.array(diff_dates)).map(dates_business)
grouped = df.groupby(['BELNR']).BPDAT.max()
df['BPDAT'] = df['BELNR'].map(grouped)
df['BPDAT'] = pd.to_datetime(df['BPDAT'])

df['MENGE'] = df['MENGE'].astype(int)
df['DELGE'] = df['DELGE'].astype(int)
df['NETPR'] = df['NETPR'].astype(int)