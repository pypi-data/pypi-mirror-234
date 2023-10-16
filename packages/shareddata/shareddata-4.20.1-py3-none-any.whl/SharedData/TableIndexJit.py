from numba.typed import List
import numpy as np
from numba import njit


###################### DATE_SYMBOL ########################
@njit(cache=True)
def create_pkey_date_symbol_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                symbollastidx, symbolprevidx, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int64(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = hash(records['date'][i])
        h1 = hash(records['symbol'][i])
        h = (h0 ^ h1) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update symbol index
        hs = h1 % n
        if symbollastidx[hs] == -1:  # symbol not found
            symbollastidx[hs] = i
            symbolprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['symbol'] != records[symbollastidx[hs]]['symbol']):
                hs = (hs + j**2) % n
                if symbollastidx[hs] == -1:
                    symbollastidx[hs] = i
                    symbolprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                symbolprevidx[i] = symbollastidx[hs]
                symbollastidx[hs] = i

    return True


@njit(cache=True)
def get_loc_date_symbol_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['symbol'][i])
        h = (h0 ^ h1) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_symbol_jit(records, count, new_records, pkey, dateiniidx, dateendidx,
                           symbollastidx, symbolprevidx, dateunit):
    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        h0 = hash(new_records['date'][i])
        h1 = hash(new_records['symbol'][i])
        h = (h0 ^ h1) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol']):
                    # record exists update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed jump hash
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int64(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update symbol index
                hs = h1 % n
                if symbollastidx[hs] == -1:  # symbol not found
                    symbollastidx[hs] = count
                    symbolprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_symbol = True
                    j = 1
                    while records[symbollastidx[hs]]['symbol'] != new_records[i]['symbol']:
                        hs = (hs + j ** 2) % n
                        if symbollastidx[hs] == -1:
                            symbollastidx[hs] = count
                            symbolprevidx[count] = -1
                            found_symbol = False
                            break
                        j += 1

                    if found_symbol:
                        symbolprevidx[count] = symbollastidx[hs]
                        symbollastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid

###################### DATE_SYMBOL_SYMBOL1 ########################


@njit(cache=True)
def create_pkey_date_symbol_symbol1_jit(records, count, pkey, dateiniidx, dateendidx, dateunit, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int64(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        if records['symbol'][i] != records['symbol1'][i]:
            h0 = hash(records['date'][i])
            h1 = hash(records['symbol'][i])
            h2 = hash(records['symbol1'][i])
            h = (h0 ^ h1 ^ h2) % n
        else:
            h0 = hash(records['date'][i])
            h1 = hash(records['symbol'][i])
            h = (h0 ^ h1) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol']) |
                    (records[pkey[h]]['symbol1'] != records[i]['symbol1'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False
    return True


@njit(cache=True)
def get_loc_date_symbol_symbol1_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        if keys['symbol'][i] != keys['symbol1'][i]:
            h0 = hash(keys['date'][i])
            h1 = hash(keys['symbol'][i])
            h2 = hash(keys['symbol1'][i])
            h = (h0 ^ h1 ^ h2) % n
        else:
            h0 = hash(keys['date'][i])
            h1 = hash(keys['symbol'][i])
            h = (h0 ^ h1) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol']) |
                    (records[pkey[h]]['symbol1'] != keys[i]['symbol1'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_symbol_symbol1_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit):
    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        if new_records['symbol'][i] != new_records['symbol1'][i]:
            h0 = hash(new_records['date'][i])
            h1 = hash(new_records['symbol'][i])
            h2 = hash(new_records['symbol1'][i])
            h = (h0 ^ h1 ^ h2) % n
        else:
            h0 = hash(new_records['date'][i])
            h1 = hash(new_records['symbol'][i])
            h = (h0 ^ h1) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol'] and
                        records[pkey[h]]['symbol1'] == new_records[i]['symbol1']):
                    # record exists update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed jump hash
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int64(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid

###################### DATE_PORTFOLIO ########################


@njit(cache=True)
def create_pkey_date_portfolio_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                   portlastidx, portprevidx, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int64(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = hash(records['date'][i])
        h1 = hash(records['portfolio'][i])
        h = (h0 ^ h1) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update port index
        hs = h1 % n
        if portlastidx[hs] == -1:  # port not found
            portlastidx[hs] = i
            portprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['portfolio'] != records[portlastidx[hs]]['portfolio']):
                hs = (hs + j**2) % n
                if portlastidx[hs] == -1:
                    portlastidx[hs] = i
                    portprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                portprevidx[i] = portlastidx[hs]
                portlastidx[hs] = i

    return True


@njit(cache=True)
def get_loc_date_portfolio_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['portfolio'][i])
        h = (h0 ^ h1) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_portfolio_jit(records, count, new_records, pkey, dateiniidx, dateendidx,
                              portlastidx, portprevidx, dateunit):
    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        h0 = hash(new_records['date'][i])
        h1 = hash(new_records['portfolio'][i])
        h = (h0 ^ h1) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio']):
                    # record exists update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed jump hash
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int64(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update portfolio index
                hs = h1 % n
                if portlastidx[hs] == -1:  # portfolio not found
                    portlastidx[hs] = count
                    portprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_portfolio = True
                    j = 1
                    while records[portlastidx[hs]]['portfolio'] != new_records[i]['portfolio']:
                        hs = (hs + j ** 2) % n
                        if portlastidx[hs] == -1:
                            portlastidx[hs] = count
                            portprevidx[count] = -1
                            found_portfolio = False
                            break
                        j += 1

                    if found_portfolio:
                        portprevidx[count] = portlastidx[hs]
                        portlastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL ########################


@njit(cache=True)
def create_pkey_date_portfolio_symbol_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                          portlastidx, portprevidx, symbollastidx, symbolprevidx, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int64(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = hash(records['date'][i])
        h1 = hash(records['portfolio'][i])
        h2 = hash(records['symbol'][i])
        h = (h0 ^ h1 ^ h2) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update port index
        hs = h1 % n
        if portlastidx[hs] == -1:  # port not found
            portlastidx[hs] = i
            portprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['portfolio'] != records[portlastidx[hs]]['portfolio']):
                hs = (hs + j**2) % n
                if portlastidx[hs] == -1:
                    portlastidx[hs] = i
                    portprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                portprevidx[i] = portlastidx[hs]
                portlastidx[hs] = i

        # update symbol index
        hs = h2 % n
        if symbollastidx[hs] == -1:  # symbol not found
            symbollastidx[hs] = i
            symbolprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['symbol'] != records[symbollastidx[hs]]['symbol']):
                hs = (hs + j**2) % n
                if symbollastidx[hs] == -1:
                    symbollastidx[hs] = i
                    symbolprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                symbolprevidx[i] = symbollastidx[hs]
                symbollastidx[hs] = i

    return True


@njit(cache=True)
def get_loc_date_portfolio_symbol_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['portfolio'][i])
        h2 = hash(keys['symbol'][i])
        h = (h0 ^ h1 ^ h2) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_portfolio_symbol_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                     portlastidx, portprevidx, symbollastidx, symbolprevidx):

    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        h0 = hash(new_records['date'][i])
        h1 = hash(new_records['portfolio'][i])
        h2 = hash(new_records['symbol'][i])
        h = (h0 ^ h1 ^ h2) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol']):
                    # record exists, update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed, jump hash
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int64(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update portfolio index
                hs = h1 % n
                if portlastidx[hs] == -1:  # portfolio not found
                    portlastidx[hs] = count
                    portprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_portfolio = True
                    j = 1
                    while records[portlastidx[hs]]['portfolio'] != new_records[i]['portfolio']:
                        hs = (hs + j ** 2) % n
                        if portlastidx[hs] == -1:
                            portlastidx[hs] = count
                            portprevidx[count] = -1
                            found_portfolio = False
                            break
                        j += 1

                    if found_portfolio:
                        portprevidx[count] = portlastidx[hs]
                        portlastidx[hs] = count

                # update symbol index
                hs = h2 % n
                if symbollastidx[hs] == -1:  # symbol not found
                    symbollastidx[hs] = count
                    symbolprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_symbol = True
                    j = 1
                    while records[symbollastidx[hs]]['symbol'] != new_records[i]['symbol']:
                        hs = (hs + j ** 2) % n
                        if symbollastidx[hs] == -1:
                            symbollastidx[hs] = count
                            symbolprevidx[count] = -1
                            found_symbol = False
                            break
                        j += 1

                    if found_symbol:
                        symbolprevidx[count] = symbollastidx[hs]
                        symbollastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL_CLORDID ########################


@njit(cache=True)
def create_pkey_date_portfolio_symbol_clordid_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                                  portlastidx, portprevidx, symbollastidx, symbolprevidx, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int64(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = hash(records['date'][i])
        h1 = hash(records['portfolio'][i])
        h2 = hash(records['symbol'][i])
        h3 = hash(records['clordid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol']) |
                    (records[pkey[h]]['clordid'] != records[i]['clordid'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False
            
        # update port index
        hs = h1 % n
        if portlastidx[hs] == -1:  # port not found
            portlastidx[hs] = i
            portprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['portfolio'] != records[portlastidx[hs]]['portfolio']):
                hs = (hs + j**2) % n
                if portlastidx[hs] == -1:
                    portlastidx[hs] = i
                    portprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                portprevidx[i] = portlastidx[hs]
                portlastidx[hs] = i

        # update symbol index
        hs = h2 % n
        if symbollastidx[hs] == -1:  # symbol not found
            symbollastidx[hs] = i
            symbolprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['symbol'] != records[symbollastidx[hs]]['symbol']):
                hs = (hs + j**2) % n
                if symbollastidx[hs] == -1:
                    symbollastidx[hs] = i
                    symbolprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                symbolprevidx[i] = symbollastidx[hs]
                symbollastidx[hs] = i
        
    return True


@njit(cache=True)
def get_loc_date_portfolio_symbol_clordid_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['portfolio'][i])
        h2 = hash(keys['symbol'][i])
        h3 = hash(keys['clordid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol']) |
                    (records[pkey[h]]['clordid'] != keys[i]['clordid'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_portfolio_symbol_clordid_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                             portlastidx, portprevidx, symbollastidx, symbolprevidx):

    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        h0 = hash(new_records['date'][i])
        h1 = hash(new_records['portfolio'][i])
        h2 = hash(new_records['symbol'][i])
        h3 = hash(new_records['clordid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol'] and
                   records[pkey[h]]['clordid'] == new_records[i]['clordid']):
                    # record exists, update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed, jump hash using quadratic probing
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int64(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update portfolio index
                hs = h1 % n
                if portlastidx[hs] == -1:  # portfolio not found
                    portlastidx[hs] = count
                    portprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_portfolio = True
                    j = 1
                    while records[portlastidx[hs]]['portfolio'] != new_records[i]['portfolio']:
                        hs = (hs + j ** 2) % n
                        if portlastidx[hs] == -1:
                            portlastidx[hs] = count
                            portprevidx[count] = -1
                            found_portfolio = False
                            break
                        j += 1

                    if found_portfolio:
                        portprevidx[count] = portlastidx[hs]
                        portlastidx[hs] = count

                # update symbol index
                hs = h2 % n
                if symbollastidx[hs] == -1:  # symbol not found
                    symbollastidx[hs] = count
                    symbolprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_symbol = True
                    j = 1
                    while records[symbollastidx[hs]]['symbol'] != new_records[i]['symbol']:
                        hs = (hs + j ** 2) % n
                        if symbollastidx[hs] == -1:
                            symbollastidx[hs] = count
                            symbolprevidx[count] = -1
                            found_symbol = False
                            break
                        j += 1

                    if found_symbol:
                        symbolprevidx[count] = symbollastidx[hs]
                        symbollastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL_TRADEID ########################


@njit(cache=True)
def create_pkey_date_portfolio_symbol_tradeid_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                                  portlastidx, portprevidx, symbollastidx, symbolprevidx, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int64(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = hash(records['date'][i])
        h1 = hash(records['portfolio'][i])
        h2 = hash(records['symbol'][i])
        h3 = hash(records['tradeid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol']) |
                    (records[pkey[h]]['tradeid'] != records[i]['tradeid'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update port index
        hs = h1 % n
        if portlastidx[hs] == -1:  # port not found
            portlastidx[hs] = i
            portprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['portfolio'] != records[portlastidx[hs]]['portfolio']):
                hs = (hs + j**2) % n
                if portlastidx[hs] == -1:
                    portlastidx[hs] = i
                    portprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                portprevidx[i] = portlastidx[hs]
                portlastidx[hs] = i

        # update symbol index
        hs = h2 % n
        if symbollastidx[hs] == -1:  # symbol not found
            symbollastidx[hs] = i
            symbolprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['symbol'] != records[symbollastidx[hs]]['symbol']):
                hs = (hs + j**2) % n
                if symbollastidx[hs] == -1:
                    symbollastidx[hs] = i
                    symbolprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                symbolprevidx[i] = symbollastidx[hs]
                symbollastidx[hs] = i

    return True


@njit(cache=True)
def get_loc_date_portfolio_symbol_tradeid_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['portfolio'][i])
        h2 = hash(keys['symbol'][i])
        h3 = hash(keys['tradeid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol']) |
                    (records[pkey[h]]['tradeid'] != keys[i]['tradeid'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_portfolio_symbol_tradeid_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                             portlastidx, portprevidx, symbollastidx, symbolprevidx):

    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        h0 = hash(new_records['date'][i])
        h1 = hash(new_records['portfolio'][i])
        h2 = hash(new_records['symbol'][i])
        h3 = hash(new_records['tradeid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol'] and
                   records[pkey[h]]['tradeid'] == new_records[i]['tradeid']):
                    # record exists, update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed, jump hash using quadratic probing
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int64(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update portfolio index
                hs = h1 % n
                if portlastidx[hs] == -1:  # portfolio not found
                    portlastidx[hs] = count
                    portprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_portfolio = True
                    j = 1
                    while records[portlastidx[hs]]['portfolio'] != new_records[i]['portfolio']:
                        hs = (hs + j ** 2) % n
                        if portlastidx[hs] == -1:
                            portlastidx[hs] = count
                            portprevidx[count] = -1
                            found_portfolio = False
                            break
                        j += 1

                    if found_portfolio:
                        portprevidx[count] = portlastidx[hs]
                        portlastidx[hs] = count

                # update symbol index
                hs = h2 % n
                if symbollastidx[hs] == -1:  # symbol not found
                    symbollastidx[hs] = count
                    symbolprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_symbol = True
                    j = 1
                    while records[symbollastidx[hs]]['symbol'] != new_records[i]['symbol']:
                        hs = (hs + j ** 2) % n
                        if symbollastidx[hs] == -1:
                            symbollastidx[hs] = count
                            symbolprevidx[count] = -1
                            found_symbol = False
                            break
                        j += 1

                    if found_symbol:
                        symbolprevidx[count] = symbollastidx[hs]
                        symbollastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid


####################### COMPOSITE INDEX ######################################


@njit(cache=True)
def get_date_portfolio_loc_jit(records, keys, pkey, portiniidx, portlist):
    n = pkey.size-1
    loc = List()
    keyloc = List()
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['portfolio'][i])
        h = (h0 ^ h1) % n
        if portiniidx[h] == -1:
            pass
        else:
            j = 1
            portfound = True
            recid = portlist[portiniidx[h]]
            while (
                    (records[recid]['date'] != keys[i]['date']) |
                    (records[recid]['portfolio'] != keys[i]['portfolio'])
            ):
                h = (h + j**2) % n
                if portiniidx[h] == -1:
                    portfound = False
                    break
                recid = portlist[portiniidx[h]]
                j += 1
            if portfound:
                curid = portiniidx[h]
                fid = portlist[curid]
                loc.append(fid)
                keyloc.append(i)
                nextid = portlist[curid+1]
                while nextid != -1:
                    curid = nextid
                    loc.append(portlist[curid])
                    keyloc.append(i)
                    nextid = portlist[curid+1]
    return loc, keyloc


def get_symbol_loc(records, symbollastidx, symbolprevidx, symbol, symbolhash, maxids):
    n = symbollastidx.size - 1
    h = symbolhash % n
    indexes = list()
    found = False

    # Find the initial position of the symbol in the hash table
    j = 1
    while symbollastidx[h] != -1:
        idx = symbollastidx[h]
        if records[idx]['symbol'] == symbol:
            indexes.append(idx)
            found = True
            break
        h = (h + j**2) % n
        j += 1

    if found:
        nids = 1
        # Backward traverse through the symbol indexes using symbolprevidx
        while symbolprevidx[idx] != -1:
            idx = symbolprevidx[idx]
            indexes.append(idx)
            nids += 1
            if (maxids != 0) & (nids >= maxids):
                break

    return indexes


def get_portfolio_loc(records, portlastidx, portprevidx, portfolio, porthash, maxids):
    n = portlastidx.size - 1
    h = porthash % n
    indexes = list()
    found = False

    # Find the initial position of the symbol in the hash table
    j = 1
    while portlastidx[h] != -1:
        idx = portlastidx[h]
        if records[idx]['portfolio'] == portfolio:
            indexes.append(idx)
            found = True
            break
        h = (h + j**2) % n
        j += 1

    if found:
        nids = 1
        # Backward traverse through the symbol indexes using portprevidx
        while portprevidx[idx] != -1:
            idx = portprevidx[idx]
            indexes.append(idx)
            nids += 1
            if (maxids != 0) & (nids >= maxids):
                break

    return indexes
