# datalibro_utils
Utils in datalibro make life easier

## Install
```pip install -U datalibro_utils```

## Example

### get_sku_extra()
```
import pandas as pd
import datalibro_utils as du
df = pd.DataFrame({'sku':['PL-AF203-01W', 'PL-FF013-01W', 'PL-IT001-01W', 'PL-AF006-03W'], 'sales':[20, 40, 10, 100]})
df = du.get_sku_extra(df, ['brand','product_line','product_type','sku_code','model', 'scu', 'app_supported', 'series'])
```