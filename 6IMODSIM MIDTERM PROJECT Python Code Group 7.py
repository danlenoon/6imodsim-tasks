# imports
import numpy as np
import pandas as pd
from math import ceil
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)
rng = np.random.default_rng(42)

# storage
n = 10
ship_method = np.empty(n, dtype=object)
handling = np.empty(n, dtype=object)
time_days = np.zeros(n, dtype=float)
updated_time = np.zeros(n, dtype=float)
distance = np.zeros(n, dtype=float)
quantity = np.zeros(n, dtype=int)
weight = np.zeros(n, dtype=float)
total_weight = np.zeros(n, dtype=float)
inventory = np.empty(n, dtype=object)
functionality = np.empty(n, dtype=object)
satisfaction = np.zeros(n, dtype=float)
change = np.zeros(n, dtype=float)

for i in range(n):
    # shipping method
    ship_method[i] = rng.choice(["Local", "Foreign"])

    # base delivery time
    if ship_method[i] == "Local":
        time_i = rng.integers(1, 6)  # 1..5
    else:
        time_i = rng.integers(7, 15)  # 7..14

    # distance 
    if ship_method[i] == "Foreign":
        dist_i = np.round(rng.uniform(31, 100), 2)
    else:
        dist_i = np.round(rng.uniform(1, 30), 2)

    # distance effect: +1 day per 20 km
    time_i = time_i + (dist_i / 20.0)

    # product things
    q_i = int(rng.integers(1, 11))  # 1..10
    w_i = float(np.round(rng.uniform(1, 20), 2))  # kg per item
    tw_i = w_i * q_i

    # WEIGHT EFFECT: +0.5 days per 10 kg of total weight
    weight_effect = (tw_i / 10) * 0.5
    time_i = time_i + weight_effect

    # inventory status
    inv_i = rng.choice(["In-Stock", "Unavailable"])
    if inv_i == "Unavailable":
        delay_days = int(rng.integers(1, 4))  # 1..3
        time_i = time_i + delay_days

    # user satisfaction base (60-80)
    func_i = rng.choice(["Poor", "Average", "Excellent"])
    base_sat = rng.uniform(60, 80)

    # quality of product
    if func_i == "Poor":
        base_sat -= base_sat * rng.uniform(0.10, 0.20)
    elif func_i == "Excellent":
        base_sat += base_sat * rng.uniform(0.10, 0.20)

    # foreign affairs adjustments
    if ship_method[i] == "Foreign":
        base_sat -= base_sat * 0.10
        if func_i == "Excellent":
            base_sat += base_sat * rng.uniform(0.10, 0.20)
            if inv_i == "In-Stock":
                base_sat += base_sat * rng.uniform(0.10, 0.20)
        elif func_i == "Poor":
            base_sat -= base_sat * rng.uniform(0.10, 0.20)
            if inv_i == "Unavailable":
                base_sat -= base_sat * 0.30

    # round up time to whole days
    time_i = int(ceil(time_i))

    # handling choice
    han_i = rng.choice(["Expedited", "None", "Fragile"])

    # default updated_time equals original unless changed by handling
    upd_i = time_i
    
    if han_i == "Expedited":
        upd_i = time_i * 0.5
    elif han_i == "Fragile":
        delay = time_i * 0.5
        upd_i = time_i + delay

    # change in days
    chg_i = upd_i - time_i

    # penalty if delay > half of initial delivery time
    if chg_i > (time_i / 2.0):
        base_sat -= base_sat * rng.uniform(0.20, 0.50)

    # if handling is "None", no change
    if han_i == "None":
        chg_i = 0.0
        upd_i = time_i  # keep updated time equal to original

    # ENSURE SATISFACTION DECREASES WITH TIME AND CHANGE
    # Strong negative relationship with delivery time
    time_penalty = (upd_i / 30) * 30  # Up to 30 points penalty for long delivery
    base_sat -= time_penalty
    
    # Strong negative relationship with change in delivery time
    if chg_i > 0:  # Only penalize for delays, not for expedited shipping
        change_penalty = chg_i * 3  # 3 points penalty per day of delay
        base_sat -= change_penalty

    # clamp satisfaction
    sat_i = max(min(base_sat, 100.0), 0.0)  # Ensure between 0 and 100

    # store
    handling[i] = han_i
    time_days[i] = time_i
    updated_time[i] = ceil(upd_i)
    distance[i] = dist_i
    quantity[i] = q_i
    weight[i] = w_i
    total_weight[i] = tw_i
    inventory[i] = inv_i
    functionality[i] = func_i
    change[i] = ceil(chg_i)
    satisfaction[i] = np.round(sat_i, 2)

# assembly of results
results = pd.DataFrame({
    "Quantity": [int(rng.integers(1, 11)) for _ in range(n)],
    "WeightPerItemKG": weight,
    "TotalWeightKG": total_weight,
    "InventoryStatus": inventory,
    "Functionality": functionality,
    "ShippingMethod": ship_method,
    "Handling": handling,
    "DistanceKM": distance,
    "OriginalTimeDAYS": time_days.astype(int),
    "UpdatedTimeDAYS": updated_time.astype(int),
    "ChangeDAYS": change.astype(int),
    "Satisfaction": satisfaction
})

print("\n=== Simulated Results ===")
print(results.to_string(index=False))

# linear models 
# model 1: predict UpdatedTimeDAYS
X1 = results[["TotalWeightKG", "DistanceKM", "ShippingMethod", "Handling", "InventoryStatus"]]
y1 = results["UpdatedTimeDAYS"]

# model 2: predict Satisfaction
X2 = results[["UpdatedTimeDAYS", "InventoryStatus", "Functionality", "ChangeDAYS", "Handling"]]
y2 = results["Satisfaction"]

def fit_linear_model(X, y):
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

    preproc = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_features),
            ("cat", OneHotEncoder(drop="first", sparse_output=False), categorical_features)
        ],
        remainder="drop"
    )

    model = Pipeline(steps=[
        ("prep", preproc),
        ("linreg", LinearRegression())
    ])

    model.fit(X, y)

    # obtain names after preprocessing
    num_names = numeric_features
    if categorical_features:
        ohe = model.named_steps["prep"].named_transformers_["cat"]
        cat_names = ohe.get_feature_names_out(categorical_features).tolist()
    else:
        cat_names = []
        
    feature_names = num_names + cat_names
    lin = model.named_steps["linreg"]
    intercept = lin.intercept_
    coefs = lin.coef_

    coef_table = pd.DataFrame({
        "feature": feature_names,
        "coef": coefs
    })

    return model, intercept, coef_table

try:
    delivery_model, delivery_intercept, delivery_coefs = fit_linear_model(X1, y1)
    print("\n=== Delivery Model (UpdatedTimeDAYS) ===")
    print(f"Intercept: {delivery_intercept:.4f}")
    print(delivery_coefs.to_string(index=False))
    
    # Check if TotalWeightKG has positive effect
    weight_coef = delivery_coefs[delivery_coefs['feature'] == 'TotalWeightKG']['coef'].values
    if len(weight_coef) > 0 and weight_coef[0] > 0:
        print("✓ Confirmed: Delivery time increases as total weight increases")
    elif len(weight_coef) > 0:
        print("⚠ Warning: Delivery time does not increase as total weight increases")
        
except Exception as e:
    print(f"Error in delivery model: {e}")

try:
    customer_model, customer_intercept, customer_coefs = fit_linear_model(X2, y2)
    print("\n=== Customer Satisfaction Model (Satisfaction) ===")
    print(f"Intercept: {customer_intercept:.4f}")
    print(customer_coefs.to_string(index=False))
    
    # Check if the coefficients show the expected negative relationships
    updated_time_coef = customer_coefs[customer_coefs['feature'] == 'UpdatedTimeDAYS']['coef'].values
    change_coef = customer_coefs[customer_coefs['feature'] == 'ChangeDAYS']['coef'].values
    
    if len(updated_time_coef) > 0 and updated_time_coef[0] < 0:
        print("✓ Confirmed: Satisfaction decreases as delivery time increases")
    elif len(updated_time_coef) > 0:
        print("⚠ Warning: Satisfaction does not decrease as delivery time increases")
        
    if len(change_coef) > 0 and change_coef[0] < 0:
        print("✓ Confirmed: Satisfaction decreases as change in delivery time increases")
    elif len(change_coef) > 0:
        print("⚠ Warning: Satisfaction does not decrease as change in delivery time increases")
        
except Exception as e:
    print(f"Error in customer model: {e}")

try:
    delivery_pred = delivery_model.predict(X1)
    delivery_residuals = y1 - delivery_pred
    print("\n=== Delivery Model Residuals ===")
    print(np.round(delivery_residuals.values, 4))
except:
    print("Could not calculate delivery residuals")

try:
    customer_pred = customer_model.predict(X2)
    customer_residuals = y2 - customer_pred
    print("\n=== Customer Satisfaction Model Residuals ===")
    print(np.round(customer_residuals.values, 4))
except:
    print("Could not calculate customer residuals")

# LINEAR REGRESSION PLOTS
try:
    # 1. Distance vs UpdatedTimeDAYS
    plt.figure(figsize=(10, 6))
    plt.scatter(results["DistanceKM"], results["UpdatedTimeDAYS"], color='blue', alpha=0.7)
    plt.xlabel("Distance (KM)")
    plt.ylabel("Updated Delivery Time (Days)")
    plt.title("Distance vs Updated Delivery Time")
    z = np.polyfit(results["DistanceKM"], results["UpdatedTimeDAYS"], 1)
    p = np.poly1d(z)
    x_range = np.linspace(results["DistanceKM"].min(), results["DistanceKM"].max(), 100)
    plt.plot(x_range, p(x_range), "r--", alpha=0.8)
    plt.grid(True, alpha=0.3)
    plt.savefig("distance_vs_delivery_time.png", dpi=300, bbox_inches='tight')
    plt.show()
except Exception as e:
    print(f"Error in plot 1: {e}")

try:
    # 2. TotalWeightKG vs UpdatedTimeDAYS
    plt.figure(figsize=(10, 6))
    plt.scatter(results["TotalWeightKG"], results["UpdatedTimeDAYS"], color='green', alpha=0.7)
    plt.xlabel("Total Weight (KG)")
    plt.ylabel("Updated Delivery Time (Days)")
    plt.title("Total Weight vs Updated Delivery Time")
    
    # Fit polynomial regression for better curve fitting
    z = np.polyfit(results["TotalWeightKG"], results["UpdatedTimeDAYS"], 1)
    p = np.poly1d(z)
    x_range = np.linspace(results["TotalWeightKG"].min(), results["TotalWeightKG"].max(), 100)
    plt.plot(x_range, p(x_range), "r--", alpha=0.8, linewidth=2)
    
    # Add correlation coefficient
    correlation = np.corrcoef(results["TotalWeightKG"], results["UpdatedTimeDAYS"])[0, 1]
    plt.text(0.05, 0.95, f'Correlation: {correlation:.2f}', transform=plt.gca().transAxes,
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    
    plt.grid(True, alpha=0.3)
    plt.savefig("weight_vs_delivery_time.png", dpi=300, bbox_inches='tight')
    plt.show()
except Exception as e:
    print(f"Error in plot 2: {e}")

try:
    # 3. UpdatedTimeDAYS vs Satisfaction
    plt.figure(figsize=(10, 6))
    plt.scatter(results["UpdatedTimeDAYS"], results["Satisfaction"], color='purple', alpha=0.7)
    plt.xlabel("Updated Delivery Time (Days)")
    plt.ylabel("Satisfaction")
    plt.title("Delivery Time vs Customer Satisfaction")
    z = np.polyfit(results["UpdatedTimeDAYS"], results["Satisfaction"], 1)
    p = np.poly1d(z)
    x_range = np.linspace(results["UpdatedTimeDAYS"].min(), results["UpdatedTimeDAYS"].max(), 100)
    plt.plot(x_range, p(x_range), "r--", alpha=0.8)
    
    # Add correlation coefficient to the plot
    correlation = np.corrcoef(results["UpdatedTimeDAYS"], results["Satisfaction"])[0, 1]
    plt.text(0.05, 0.95, f'Correlation: {correlation:.2f}', transform=plt.gca().transAxes,
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    
    plt.grid(True, alpha=0.3)
    plt.savefig("delivery_time_vs_satisfaction.png", dpi=300, bbox_inches='tight')
    plt.show()
except Exception as e:
    print(f"Error in plot 3: {e}")

try:
    # 4. ChangeDAYS vs Satisfaction
    plt.figure(figsize=(10, 6))
    plt.scatter(results["ChangeDAYS"], results["Satisfaction"], color='orange', alpha=0.7)
    plt.xlabel("Change in Delivery Time (Days)")
    plt.ylabel("Satisfaction")
    plt.title("Change in Delivery Time vs Customer Satisfaction")
    z = np.polyfit(results["ChangeDAYS"], results["Satisfaction"], 1)
    p = np.poly1d(z)
    x_range = np.linspace(results["ChangeDAYS"].min(), results["ChangeDAYS"].max(), 100)
    plt.plot(x_range, p(x_range), "r--", alpha=0.8)
    correlation = np.corrcoef(results["ChangeDAYS"], results["Satisfaction"])[0, 1]
    
    plt.text(0.05, 0.95, f'Correlation: {correlation:.2f}', transform=plt.gca().transAxes,
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    
    plt.grid(True, alpha=0.3)
    plt.savefig("change_vs_satisfaction.png", dpi=300, bbox_inches='tight')
    plt.show()
except Exception as e:
    print(f"Error in plot 4: {e}")