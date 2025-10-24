# STEP3: Build models and compare three methods
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Read data
sell_data = pd.read_csv('total_sell_data_cleaned.csv')
rental_data = pd.read_csv('total_rental_data_cleaned.csv')

# Data preprocessing
rental_data['unit_monthly_rent'] = rental_data['monthly_rent'] / rental_data['area']

def create_region_dummies(df):
    region_dummies = pd.get_dummies(df['region'], prefix='region')
    return pd.concat([df, region_dummies], axis=1)

# Create region dummy variables for datasets
sell_data_with_dummies = create_region_dummies(sell_data)
rental_data_with_dummies = create_region_dummies(rental_data)

def calculate_direct_price_to_rent_ratio():
    median_unit_price_by_region = sell_data.groupby('region')['unit_price'].median()
    median_monthly_rent_by_region = rental_data.groupby('region')['unit_monthly_rent'].median()
    direct_ratio_by_region = median_unit_price_by_region / median_monthly_rent_by_region
    
    direct_ratio_df = pd.DataFrame({
        'region': direct_ratio_by_region.index,
        'price_to_rent_ratio': direct_ratio_by_region.values
    })
    
    return direct_ratio_by_region, direct_ratio_df

# Calculate direct price-to-rent ratio
direct_ratios, direct_ratio_df = calculate_direct_price_to_rent_ratio()

print("=== Method 3 (Direct Calculation - Based on Median) ===")
for region, ratio in direct_ratios.items():
    print(f"{region}: {ratio:.0f} months (approx. {ratio/12:.1f} years)")

def plot_direct_price_to_rent_ratio():
    plt.figure(figsize=(12, 7))
    bars = plt.bar(direct_ratios.index, direct_ratios.values, 
                   color='lightgreen', edgecolor='darkgreen', alpha=0.7)
    
    plt.axhline(y=200, color='green', linestyle='-', linewidth=2, label='200 months')
    
    for bar, value in zip(bars, direct_ratios.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
                f'{value:.0f} months\n({value/12:.1f} years)', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.title("Figure A: Median Price-to-Rent Ratio by Region (Direct Calculation)", fontsize=14, fontweight='bold')
    plt.xlabel('Region', fontsize=12)
    plt.ylabel('Price-to-Rent Ratio (months)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

plot_direct_price_to_rent_ratio()

def build_basic_models():
    X_sell = sell_data_with_dummies[['area'] + 
                                   [col for col in sell_data_with_dummies.columns if col.startswith('region_')]]
    y_sell = sell_data_with_dummies['unit_price']
    
    model1 = LinearRegression()
    model1.fit(X_sell, y_sell)
    y_sell_pred = model1.predict(X_sell)
    r2_sell = r2_score(y_sell, y_sell_pred)
    
    X_rental = rental_data_with_dummies[['area'] + 
                                       [col for col in rental_data_with_dummies.columns if col.startswith('region_')]]
    y_rental = rental_data_with_dummies['unit_monthly_rent']
    
    model2 = LinearRegression()
    model2.fit(X_rental, y_rental)
    y_rental_pred = model2.predict(X_rental)
    r2_rental = r2_score(y_rental, y_rental_pred)
    
    print(f"\nBasic Model R-squared - Housing: {r2_sell:.4f}, Rental: {r2_rental:.4f}")
    
    return model1, model2, X_sell, X_rental

model1, model2, X_sell, X_rental = build_basic_models()

def calculate_price_to_rent_ratio_basic():
    sell_features_for_rent = sell_data_with_dummies[['area'] + 
                                                   [col for col in sell_data_with_dummies.columns if col.startswith('region_')]]
    predicted_rent_for_sell = model2.predict(sell_features_for_rent)
    
    sell_data_with_ratio = sell_data_with_dummies.copy()
    sell_data_with_ratio['predicted_unit_monthly_rent'] = predicted_rent_for_sell
    sell_data_with_ratio['price_to_rent_ratio_method1'] = (
        sell_data_with_ratio['unit_price'] / sell_data_with_ratio['predicted_unit_monthly_rent']
    )
    
    rental_features_for_price = rental_data_with_dummies[['area'] + 
                                                        [col for col in rental_data_with_dummies.columns if col.startswith('region_')]]
    predicted_price_for_rental = model1.predict(rental_features_for_price)
    
    rental_data_with_ratio = rental_data_with_dummies.copy()
    rental_data_with_ratio['predicted_unit_price'] = predicted_price_for_rental
    rental_data_with_ratio['price_to_rent_ratio_method2'] = (
        rental_data_with_ratio['predicted_unit_price'] / rental_data_with_ratio['unit_monthly_rent']
    )
    
    combined_ratio_data = pd.concat([
        sell_data_with_ratio[['region', 'area', 'price_to_rent_ratio_method1']].rename(
            columns={'price_to_rent_ratio_method1': 'price_to_rent_ratio'}),
        rental_data_with_ratio[['region', 'area', 'price_to_rent_ratio_method2']].rename(
            columns={'price_to_rent_ratio_method2': 'price_to_rent_ratio'})
    ], ignore_index=True)
    
    return combined_ratio_data

combined_ratio_basic = calculate_price_to_rent_ratio_basic()

def plot_median_price_to_rent_ratio(data, title):
    median_ratio_by_region = data.groupby('region')['price_to_rent_ratio'].median().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 7))
    bars = plt.bar(median_ratio_by_region.index, median_ratio_by_region.values, 
                   color='skyblue', edgecolor='navy', alpha=0.7)
    
    plt.axhline(y=200, color='green', linestyle='-', linewidth=2, label='200 months')
    
    for bar, value in zip(bars, median_ratio_by_region.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
                f'{value:.0f} months\n({value/12:.1f} years)', ha='center', va='bottom', fontsize=9)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Region', fontsize=12)
    plt.ylabel('Price-to-Rent Ratio (months)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    return median_ratio_by_region

median_ratios_basic = plot_median_price_to_rent_ratio(
    combined_ratio_basic, "Figure B: Median Price-to-Rent Ratio by Region (Basic Model)"
)

def build_advanced_models():
    sell_features = ['area'] + [col for col in sell_data_with_dummies.columns if col.startswith('region_')]
    rental_features = ['area'] + [col for col in rental_data_with_dummies.columns if col.startswith('region_')]
    
    X_sell_adv = sell_data_with_dummies[sell_features]
    X_rental_adv = rental_data_with_dummies[rental_features]
    
    y_sell = sell_data_with_dummies['unit_price']
    y_rental = rental_data_with_dummies['unit_monthly_rent']
    
    poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
    
    X_sell_poly = poly.fit_transform(X_sell_adv)
    model1_plus = LinearRegression()
    model1_plus.fit(X_sell_poly, y_sell)
    y_sell_pred_plus = model1_plus.predict(X_sell_poly)
    r2_sell_plus = r2_score(y_sell, y_sell_pred_plus)
    
    X_rental_poly = poly.fit_transform(X_rental_adv)
    model2_plus = LinearRegression()
    model2_plus.fit(X_rental_poly, y_rental)
    y_rental_pred_plus = model2_plus.predict(X_rental_poly)
    r2_rental_plus = r2_score(y_rental, y_rental_pred_plus)
    
    print(f"\nAdvanced Model R-squared - Housing: {r2_sell_plus:.4f}, Rental: {r2_rental_plus:.4f}")
    
    return model1_plus, model2_plus, poly

model1_plus, model2_plus, poly = build_advanced_models()

def calculate_price_to_rent_ratio_advanced():
    sell_features = ['area'] + [col for col in sell_data_with_dummies.columns if col.startswith('region_')]
    rental_features = ['area'] + [col for col in rental_data_with_dummies.columns if col.startswith('region_')]
    
    sell_features_for_rent = sell_data_with_dummies[sell_features]
    sell_features_poly_for_rent = poly.transform(sell_features_for_rent)
    predicted_rent_for_sell_plus = model2_plus.predict(sell_features_poly_for_rent)
    
    sell_data_with_ratio_plus = sell_data_with_dummies.copy()
    sell_data_with_ratio_plus['predicted_unit_monthly_rent_plus'] = predicted_rent_for_sell_plus
    sell_data_with_ratio_plus['price_to_rent_ratio_method1_plus'] = (
        sell_data_with_ratio_plus['unit_price'] / sell_data_with_ratio_plus['predicted_unit_monthly_rent_plus']
    )
    
    rental_features_for_price = rental_data_with_dummies[rental_features]
    rental_features_poly_for_price = poly.transform(rental_features_for_price)
    predicted_price_for_rental_plus = model1_plus.predict(rental_features_poly_for_price)
    
    rental_data_with_ratio_plus = rental_data_with_dummies.copy()
    rental_data_with_ratio_plus['predicted_unit_price_plus'] = predicted_price_for_rental_plus
    rental_data_with_ratio_plus['price_to_rent_ratio_method2_plus'] = (
        rental_data_with_ratio_plus['predicted_unit_price_plus'] / rental_data_with_ratio_plus['unit_monthly_rent']
    )
    
    combined_ratio_data_plus = pd.concat([
        sell_data_with_ratio_plus[['region', 'area', 'price_to_rent_ratio_method1_plus']].rename(
            columns={'price_to_rent_ratio_method1_plus': 'price_to_rent_ratio'}),
        rental_data_with_ratio_plus[['region', 'area', 'price_to_rent_ratio_method2_plus']].rename(
            columns={'price_to_rent_ratio_method2_plus': 'price_to_rent_ratio'})
    ], ignore_index=True)
    
    return combined_ratio_data_plus

combined_ratio_advanced = calculate_price_to_rent_ratio_advanced()

median_ratios_advanced = plot_median_price_to_rent_ratio(
    combined_ratio_advanced, "Figure C: Median Price-to-Rent Ratio by Region (Advanced Model)"
)

def compare_all_methods():
    # Set pandas display options to show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    method1_ratios = combined_ratio_basic.groupby('region')['price_to_rent_ratio'].median()
    method2_ratios = combined_ratio_advanced.groupby('region')['price_to_rent_ratio'].median()
    method3_ratios = direct_ratios
    
    comparison_df = pd.DataFrame({
        'Basic Model': method1_ratios,
        'Advanced Model': method2_ratios, 
        'Direct Calculation': method3_ratios
    })
    
    print("\n=== Comparison of Three Methods (Months) ===")
    print(comparison_df.round(1))
    
    # Reset pandas display options to default
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.max_colwidth')
    
    return comparison_df

comparison_results = compare_all_methods()