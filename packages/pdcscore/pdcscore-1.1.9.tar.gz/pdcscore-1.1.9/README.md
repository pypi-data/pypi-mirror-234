## README.md

The objective of this package is to offer a Python-based solution for computing the Proportion of Days Covered (PDC), a widely used metric in the healthcare industry to evaluate medication adherence. As the healthcare analytics sector shifts away from SAS, there is a growing need to recreate key metrics in alternative platforms. This package aims to simplify the process and reduce the workload for business analysts in the healthcare ecosystem by providing a readily available PDC calculation tool, thereby eliminating the need to build it from scratch.


Please use as described below:

**INPUT PARAMETERS:**

**dataframe** - *A pandas dataframe containing the required columns described below.*

**patient_id_col** - *A unique patient identifier. Format = STRING or INTEGER*

**drugname_col** - *The name of the drug being filled or drug class or Generic name, per usual PDC requirements. Format = STRING*

**filldate_col** - *The date of the fill being dispensed. Format = DATE*

**supply_days_col** - *Days of supply being dispensed at fill. Format = INTEGER*

**msr_start_dt_col** - *start date of measurement period for the patient or a reference START DATE. Format = DATE*

**msr_end_dt_col** - *end date of measurement period for the patient or a reference END DATE. Format = DATE*

**overlap_adjustment** - *Set to True to accommodate early refills, otherwise set to False*



**OUTPUT DATAFRAME** - *A Pandas dataframe containing the following columns*

**patient_id_col** - *This will return a column name representing a unique patient identifier as provided in original input dataframe. FORMAT = STRING*

**drugname_col** - *The name of the drug being filled or drug class or Generic name, as provided in original input dataframe.*

**dayscovered**- *The number of unique days of drug coverage. FORMAT = INTEGER*

**totaldays** - *The total number of days in patient analysis window. Set to 0 if days of coverage is 0. FORMAT = INTEGER*

**pdc_score** - *The patient's PDC score, calculated as dayscovered / totaldays. Set to 0 if days of coverage is 0. FORMAT = FLOAT*



## USAGE EXAMPLE
```python

#  Import required libraries
import pandas as pd
import numpy as np
from datetime import datetime
from pdcscore import pdcCalc

# Create a sample dataframe
df = pd.DataFrame({
    'patient_id': ['A001', 'A001', 'A001', 'B001', 'B001', 'B001', 'C001', 'C001', 'C001','C001', 'C001', 'C001'],
    'drugname': ['DRUG_X', 'DRUG_X', 'DRUG_X', 'DRUG_Y', 'DRUG_Y', 'DRUG_Y', 'DRUG_Y', 'DRUG_Y', 'DRUG_Y',
                    'DRUG_Z', 'DRUG_Z', 'DRUG_Z'],
    'filldate': pd.to_datetime(['2021-10-21', '2022-01-21', '2022-03-20',
                                '2022-01-01', '2022-02-01', '2022-03-01',
                                   '2022-02-18', '2022-03-01', '2022-03-22',
                                   '2021-06-18', '2022-02-11', '2022-03-05']),
    'supply_days': [90, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
    'msr_start_dt': pd.to_datetime(['2022-01-01', '2022-01-01', '2022-01-01',
                                         '2022-01-01', '2022-01-01', '2022-01-01',
                                       '2022-01-01', '2022-01-01', '2022-01-01',
                                       '2022-01-01', '2022-01-01', '2022-01-01']),
    'msr_end_dt': pd.to_datetime(['2022-03-31', '2022-03-31', '2022-03-31',
                                       '2022-03-31', '2022-03-31', '2022-03-31',
                                     '2022-03-31', '2022-03-31', '2022-03-31',
                                     '2022-03-31', '2022-03-31', '2022-03-31'])
})

# Inspect sample data
df.head(n=len(df))

# calculate PDC scores on the input DataFrame
calcfunc = pdcCalc(dataframe=df,patient_id_col='patient_id', drugname_col='drugname', filldate_col='filldate'
                   , supply_days_col='supply_days', msr_start_dt_col='msr_start_dt', msr_end_dt_col='msr_end_dt',overlap_adjustment=True) # Set to True to adjust for early refills
pdc_scores_df = calcfunc.calculate_pdc()

# Inspect output
pdc_scores_df.head()
