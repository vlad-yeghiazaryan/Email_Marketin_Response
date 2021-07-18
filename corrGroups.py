import numpy as np


def corrGrouper(data, threshold=0.95):
    # Create the Correlation pairs table
    corr = data.corr()
    corr = corr.mask(np.tril(np.ones(corr.shape)).astype(np.bool))
    corr = corr.unstack().reset_index().dropna()
    corr.columns = ['Var1', 'Var2', 'Corr']
    corr['AbsCorr'] = corr['Corr'].abs()
    corr = corr.sort_values('AbsCorr', ascending=False)

    # Grouping based on threshold
    recs = corr[corr['AbsCorr'] > threshold].to_dict('records')
    groups = [set()]
    for rec in recs:
        columns = set(list(rec.values())[:2])
        grouped = False
        index = 0
        while (not grouped) and (index < len(groups)):
            group = groups[index]
            if bool(columns & group):
                group.update(columns)
                grouped = True
            index += 1
        if not grouped:
            groups.append(columns)

    # Removing empty set
    groups = groups[1:]

    # Combining duplicate or similar groups
    index = 0
    grouping = True
    while grouping:
        if index + 1 < len(group):
            if bool(bool(groups[index] & groups[index + 1])):
                groups[index].update(groups[index + 1])
                groups.pop(index + 1)
            else:
                index += 1
        else:
            grouping = False
    return groups
