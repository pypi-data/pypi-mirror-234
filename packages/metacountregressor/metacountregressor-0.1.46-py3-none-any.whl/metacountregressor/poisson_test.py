import numpy as np
import statsmodels.api as sm

# Generate some sample data
# Generate some simulated data
np.random.seed(1)
nobs = 1000
x = np.random.normal(size=(nobs, 2))
beta_true = np.array([0.5, -0.5])
alpha_true = np.array([0.5, 0.5])
mu_true = np.exp(np.dot(x, beta_true))
nb_true = sm.distributions.NegativeBinomial(mu_true, alpha_true)
y = nb_true.rvs()

# Define the random parameters negative binomial model
def rpnegbinom_loglike(params, exog, endog):
    beta = params[:-len(alpha_true)]
    alpha = params[-len(alpha_true):]
    mu = np.exp(np.dot(exog, beta))
    nb = sm.distributions.NegativeBinomial(mu, alpha)
    return -np.sum(nb.loglike(endog))

# Define the gradient function
def rpnegbinom_gradient(params, exog, endog):
    beta = params[:-len(alpha_true)]
    alpha = params[-len(alpha_true):]
    mu = np.exp(np.dot(exog, beta))
    d_beta = np.dot((endog-mu)/(mu+alpha*mu**2), exog)
    d_alpha = np.sum(np.log(endog+alpha) - np.log(alpha) - np.log(mu+alpha*mu**2))
    return -np.concatenate((d_beta, [d_alpha]))

# Perform maximum likelihood estimation
model = sm.MNLogit(y, sm.add_constant(x))
result = model.fit(method='bfgs')

# Calculate the gradient at the MLE estimates
params_mle = np.concatenate((result.params[:-1], alpha_true))
grad = rpnegbinom_gradient(params_mle, sm.add_constant(x), y)
print(grad)


