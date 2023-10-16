import numpy as np
import pandas as pd
import scipy
import copy
from bisect import bisect_left
from statsmodels.tsa.arima.model import ARIMA

# 1. Covariance Estimation
def calculate_exponential_weights(lags, lamb):
    weights = []
    for i in range(1, lags + 1):
        weight = (1 - lamb) * lamb ** (i - 1)
        weights.append(weight)
    weights = np.array(weights)
    weights = np.flip(weights)
    normalized_weights = weights / weights.sum()
    return normalized_weights

# calculate exponentially weighted covariance matrix
def calculate_ewcov(data, lamb):
    weights = calculate_exponential_weights(data.shape[1], lamb)
    error_matrix = data - data.mean(axis=1)
    ewcov = error_matrix @ np.diag(weights) @ error_matrix.T
    return ewcov



# 2. Non-PSD Fixes
#copy chol_psd code
def chol_psd(root, a):
    n = a.shape[0]
    # Initialize the root matrix with 0 values
    root.fill(0.0)

    # Loop over columns
    for j in range(n):
        s = 0.0
        # If we are not on the first column, calculate the dot product of the preceding row values.
        if j > 0:
            s = np.dot(root[j, :j], root[j, :j])

        # Diagonal Element
        root[j, j] = np.sqrt(a[j, j] - s)

        ir = 1.0 / root[j, j]
        # Update off-diagonal rows of the column
        for i in range(j+1, n):
            s = np.dot(root[i, :j], root[j, :j])
            root[i, j] = (a[i, j] - s) * ir
    return root


#copy near_psd code
def near_psd(a, epsilon=0.0):
    n = a.shape[0]

    invSD = None
    out = np.copy(a)

    # Calculate the correlation matrix if we got a covariance
    if np.count_nonzero(np.isclose(np.diag(out), 1.0)) != n:
        invSD = np.diag(1.0 / np.sqrt(np.diag(out)))
        out = np.dot(np.dot(invSD, out), invSD)

    # SVD, update the eigen value and scale
    vals, vecs = np.linalg.eigh(out)
    vals = np.maximum(vals, epsilon)
    T = 1.0 / (vecs * vecs @ vals)
    T = np.diag(np.sqrt(T))
    l = np.diag(np.sqrt(vals))
    B = np.dot(np.dot(T, vecs), l)
    out = np.dot(B, B.T)

    # Add back the variance
    if invSD is not None:
        invSD = np.diag(1.0 / np.diag(invSD))
        out = np.dot(np.dot(invSD, out), invSD)

    return out


#Implement Higham’s 2002 nearest psd correlation function.
def frobenius_norm(matrix):
    return np.sqrt(np.square(matrix).sum())

def projection_u(matrix):
    out = copy.deepcopy(matrix)
    np.fill_diagonal(out, 1.0)
    return out

def projection_s(matrix, epsilon=0.0):
    vals, vecs = np.linalg.eigh(matrix)
    vals = np.maximum(vals, epsilon)
    return vecs @ np.diag(vals) @ vecs.T

# Higham
def higham_psd(a, max_iter=100, tol=1e-10):
    delta_s = 0.0
    y = a
    prev_gamma = np.inf
    for i in range(max_iter):
        r = y - delta_s
        x = projection_s(r)
        delta_s = x - r
        y = projection_u(x)
        gamma = frobenius_norm(y - a)
        if abs(gamma - prev_gamma) < tol:  
            break
        prev_gamma = gamma   
    return y

#Confirm the matrix is now PSD
def is_psd(matrix, tol=1e-7):
    return np.all(np.linalg.eigvals(matrix) >= -tol)

# 3. Simulation Methods
def direct_simulation(cov, n_samples=25000):
    root = np.full(cov.shape, 0.0)
    B = chol_psd(root, cov)
    r = np.random.randn(len(B[0]), n_samples)
    return B @ r

def pca_simulation(cov, pct_explained, n_samples=25000):
    # Eigenvalue decomposition and sorting
    eigen_values, eigen_vectors = np.linalg.eigh(cov)
    sorted_idx = np.argsort(eigen_values)[::-1]
    sorted_eigenvalues = eigen_values[sorted_idx]
    sorted_eigenvectors = eigen_vectors[:, sorted_idx]
    
    # Explained variance and cumulative explained variance
    total_variance = sorted_eigenvalues.sum()
    evr = sorted_eigenvalues / total_variance
    cumulative_evr = np.cumsum(evr)
    cumulative_evr[-1] = 1.0
    
    # Find index based on the desired percentage of explained variance
    idx = bisect_left(cumulative_evr, pct_explained)
    
    # Extract relevant eigenvalues and eigenvectors
    explained_vals = np.clip(sorted_eigenvalues[:idx + 1], 0, np.inf)
    explained_vecs = sorted_eigenvectors[:, :idx + 1]
    
    # Generate the random samples
    B = explained_vecs @ np.diag(np.sqrt(explained_vals))
    r = np.random.randn(B.shape[1], n_samples)
    
    return B @ r

def weighted_cov(data, lamb):
    # Generate exponentially weighted factors
    n = data.shape[1]  # Number of observations (rows)
    weights = [(1 - lamb) * lamb ** (i - 1) for i in range(1, n + 1)]
    weights = np.array(weights)
    weights_norm = weights / weights.sum()
    
    error_matrix = data - data.mean(axis=1)
    cov = error_matrix @ np.diag(weights_norm) @ error_matrix.T
    return cov

def PCA(cov_matrix):
    eigen_values, eigen_vectors = np.linalg.eigh(cov_matrix)

    # Sort eigenvalues and eigenvectors
    sorted_index = np.argsort(eigen_values)[::-1]
    sorted_eigenvalues = eigen_values[sorted_index]
    sorted_eigenvectors = eigen_vectors[:,sorted_index]
    
    # Calculate explained variance ratio
    total_variance = sorted_eigenvalues.sum()
    evr = sorted_eigenvalues / total_variance
    cumulative_evr = np.cumsum(evr)
    cumulative_evr[-1] = 1.0
    
    return cumulative_evr

# 4. VaR Calculation Methods
def calculate_var(data, mean=0, alpha=0.05):
    return mean - np.quantile(data, alpha)

def normal_var(data, mean=0, alpha=0.05, nsamples=10000):
    sigma = np.std(data)
    simulation_norm = np.random.normal(mean, sigma, nsamples)
    var_norm = calculate_var(simulation_norm, mean, alpha)
    return var_norm

def ewcov_normal_var(data, mean=0, alpha=0.05, nsamples=10000):
    ew_cov = calculate_ewcov(np.matrix(data).T, 0.94)
    ew_variance = ew_cov[0, 0]
    sigma = np.sqrt(ew_variance)
    simulation_ew = np.random.normal(mean, sigma, nsamples)
    var_ew = calculate_var(simulation_ew, mean, alpha)
    return var_ew

def t_var(data, mean=0, alpha=0.05, nsamples=10000):
    params = scipy.stats.t.fit(data, method="MLE")
    df, loc, scale = params
    simulation_t = scipy.stats.t(df, loc, scale).rvs(nsamples)
    var_t = calculate_var(simulation_t, mean, alpha)
    return var_t

def historic_var(data, mean=0, alpha=0.05):
    return calculate_var(data, mean, alpha)

def kde_var(data, mean=0, alpha=0.05):
    def quantile_kde(x):
        return kde.integrate_box(0, x) - alpha
    kde = scipy.stats.gaussian_kde(data)
    return mean - scipy.optimize.fsolve(quantile_kde, x0=mean)[0]

def ar1_var(data, arima_order=(1,0,0), n_simulation_points=1000, alpha=0.05):
    # ARIMA Model
    model = ARIMA(data, order=arima_order)
    res = model.fit()
    print(res.summary)
    # Simulate AR(1)
    sigma = np.sqrt(res.params[2])
    simulation_ar = np.random.normal(0, sigma, n_simulation_points)

    # Calculate VAR
    var_ar = calculate_var(simulation_ar, alpha=alpha)
    return var_ar

# 5. ES calculation
def calculate_es(data, mean=0, alpha=0.05):
    var = calculate_var(data, mean, alpha)
    return -np.mean(data[data <= -var])


# 6. the other methods
# rewrite the return calculation function for pandas
def pd_return_calculate(series, method="arithmetic"):
    price_change_percent = ((series.shift(-1) - series) / series).dropna()
    if method == "arithmetic":
        return price_change_percent
    elif method == "log":
        return np.log(price_change_percent)
    
def return_calculate(arr, method="DISCRETE", date_column=None):
    n, m = arr.shape
    p2 = np.empty((n - 1, m), dtype=np.float64)

    # Loop through rows and columns to fill p2
    for i in range(n - 1):
        for j in range(m):
            p2[i, j] = arr[i + 1, j] / arr[i, j]

    if method.upper() == "DISCRETE":
        p2 -= 1.0
    elif method.upper() == "LOG":
        p2 = np.log(p2)
    else:
        raise ValueError(f"method: {method} must be in ('LOG', 'DISCRETE')")

    # Create DataFrame
    columns = [f'var_{i+1}' for i in range(m)]
    out = pd.DataFrame(p2, columns=columns)
    
    # Add date column if provided
    if date_column is not None:
        out[date_column] = date_column[1:]

    return out

