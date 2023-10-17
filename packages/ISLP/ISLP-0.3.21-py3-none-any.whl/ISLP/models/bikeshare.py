# IPython log file

from ISLP import load_data
bike = load_data('Bikeshare')
bike['mnth']
from ISLP.models import model_spec
print(model_spec.ModelSpec(['mnth']).fit_transform(bike).columns)
