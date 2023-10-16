# IPython log file

from ISLP import load_data
bike = load_data('Bikeshare')
bike['mnth']
from ISLP.models import model_spec
model_spec(['mnth']).fit_transform(bike).column_names
model_spec.ModelSpec(['mnth']).fit_transform(bike).column_names
model_spec.ModelSpec(['mnth']).fit_transform(bike).columns
model_spec.__file__
model_spec.dtype
bike['mnth'].dtype
bike['mnth'].dtype == 'category'
get_ipython().run_line_magic('logstart', '')
get_ipython().run_line_magic('edit', 'ipython_log.py')
get_ipython().run_line_magic('edit', 'ipython_log.py')
get_ipython().run_line_magic('edit', 'bikeshare')
get_ipython().run_line_magic('edit', 'bikeshare')
