from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge, LassoCV, LassoLarsCV, LarsCV, BayesianRidge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor

def get_models():
    return {
        'LarsCV': LarsCV(),
        'BayesianRidge': BayesianRidge(),
        'LinearRegression': LinearRegression()
    }

def split_data(df, target='Note'):
    X = df.drop(columns=[target])
    y = df[target]
    return train_test_split(X, y, test_size=0.2, random_state=42)
