# STEP2: Integrate data and perform data cleaning
import pandas as pd
import re
import os

def detect_outliers_iqr(data, column_name):
    """Detect outliers using IQR method"""
    Q1 = data[column_name].quantile(0.25)
    Q3 = data[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data[column_name] < lower_bound) | (data[column_name] > upper_bound)]
    return outliers, lower_bound, upper_bound

def clean_rental_data():
    """Clean rental data"""
    try:
        if not os.path.exists("xiahuayuan_rental_data.csv"):
            return None
            
        df = pd.read_csv("xiahuayuan_rental_data.csv", encoding="utf-8")
        
        # Ensure correct data types
        df['monthly_rent'] = pd.to_numeric(df['monthly_rent'], errors='coerce')
        df['area'] = pd.to_numeric(df['area'], errors='coerce')
        
        # Remove rows with NaN values
        df = df.dropna(subset=['monthly_rent', 'area'])
        
        # Outlier detection
        monthly_rent_outliers, rent_lower, rent_upper = detect_outliers_iqr(df, 'monthly_rent')
        area_outliers, area_lower, area_upper = detect_outliers_iqr(df, 'area')
        
        # Create outlier flags
        df['monthly_rent_outlier'] = (df['monthly_rent'] < rent_lower) | (df['monthly_rent'] > rent_upper)
        df['area_outlier'] = (df['area'] < area_lower) | (df['area'] > area_upper)
        df['any_outlier'] = df['monthly_rent_outlier'] | df['area_outlier']
        
        # Save cleaned data
        df_cleaned = df[~df['any_outlier']].copy()
        df_cleaned = df_cleaned.drop(columns=['monthly_rent_outlier', 'area_outlier', 'any_outlier'])
        
        # Keep only needed columns
        rental_columns = ['region', 'area', 'monthly_rent']
        df_cleaned = df_cleaned[rental_columns]
        
        df_cleaned.to_csv("xiahuayuan_rental_data_cleaned.csv", index=False, encoding="utf-8-sig")
        
        return df_cleaned
    except Exception as e:
        return None

def clean_sell_data():
    """Clean housing sale data"""
    try:
        if not os.path.exists("xiahuayuan_sell_data.csv"):
            return None
            
        df = pd.read_csv("xiahuayuan_sell_data.csv", encoding="utf-8")
        
        # Data cleaning - convert to float
        df["area"] = df["area"].astype(str).str.extract(r"(\d+\.?\d*)")[0].astype(float)
        
        def convert_total_price(price_str):
            if pd.isna(price_str):
                return None
            price_str = str(price_str)
            match = re.search(r"(\d+\.?\d*)", price_str)
            if match:
                return float(match.group(1)) * 10000
            return None
        
        df["total_price"] = df["total_price"].apply(convert_total_price)
        df["unit_price"] = df["unit_price"].astype(str).str.extract(r"(\d+\.?\d*)")[0].astype(float)
        
        # Remove rows with NaN values
        df = df.dropna(subset=['area', 'total_price', 'unit_price'])
        
        # Outlier detection
        area_outliers, area_lower, area_upper = detect_outliers_iqr(df, "area")
        total_price_outliers, total_price_lower, total_price_upper = detect_outliers_iqr(df, "total_price")
        unit_price_outliers, unit_price_lower, unit_price_upper = detect_outliers_iqr(df, "unit_price")
        
        # Create outlier flags
        df["area_outlier"] = (df["area"] < area_lower) | (df["area"] > area_upper)
        df["total_price_outlier"] = (df["total_price"] < total_price_lower) | (df["total_price"] > total_price_upper)
        df["unit_price_outlier"] = (df["unit_price"] < unit_price_lower) | (df["unit_price"] > unit_price_upper)
        df["any_outlier"] = df["area_outlier"] | df["total_price_outlier"] | df["unit_price_outlier"]
        
        # Save cleaned data
        df_cleaned = df[~df["any_outlier"]].copy()
        
        # Keep only needed columns
        sell_columns = ["region", "area", "total_price", "unit_price"]
        df_cleaned = df_cleaned[sell_columns]
        
        df_cleaned.to_csv("xiahuayuan_sell_data_cleaned.csv", index=False, encoding="utf-8-sig")
        
        return df_cleaned
    except Exception as e:
        return None

def clean_region_data(file_path, data_type):
    """Clean data for a single region"""
    try:
        if not os.path.exists(file_path):
            return pd.DataFrame()
            
        df = pd.read_csv(file_path, encoding="utf-8")
        
        if data_type == "sell":
            # Clean sale data
            df["建筑面积"] = df["建筑面积"].astype(str).str.extract(r"(\d+\.?\d*)")[0].astype(float)
            df["总价"] = df["总价"].astype(str).str.extract(r"(\d+\.?\d*)")[0].astype(float) * 10000
            df["单价"] = df["单价"].astype(str).str.extract(r"(\d+\.?\d*)")[0].astype(float)
            
            # Remove rows with NaN values
            df = df.dropna(subset=['建筑面积', '总价', '单价'])
            
            # Outlier detection
            area_outliers, area_lower, area_upper = detect_outliers_iqr(df, "建筑面积")
            price_outliers, price_lower, price_upper = detect_outliers_iqr(df, "单价")
            
            # Filter outliers
            mask = ((df["建筑面积"] >= area_lower) & (df["建筑面积"] <= area_upper) &
                   (df["单价"] >= price_lower) & (df["单价"] <= price_upper))
            
            return df[mask].copy()
            
        elif data_type == "rental":
            # Clean rental data
            df["面积"] = df["面积"].astype(str).str.extract(r"(\d+\.?\d*)")[0].astype(float)
            df["租金"] = df["租金(元/月)"].astype(str).str.extract(r"(\d+\.?\d*)")[0].astype(float)
            
            # Remove rows with NaN values
            df = df.dropna(subset=['面积', '租金'])
            
            # Outlier detection
            area_outliers, area_lower, area_upper = detect_outliers_iqr(df, "面积")
            rent_outliers, rent_lower, rent_upper = detect_outliers_iqr(df, "租金")
            
            # Filter outliers
            mask = ((df["面积"] >= area_lower) & (df["面积"] <= area_upper) &
                   (df["租金"] >= rent_lower) & (df["租金"] <= rent_upper))
            
            return df[mask].copy()
            
    except Exception:
        return pd.DataFrame()

def integrate_all_data():
    """Integrate data from all regions"""
    total_sell_data = []
    total_rental_data = []
    regions = ["huailai", "zhangbei", "qiaoxi"]
    
    # Process data from three teammate regions
    for region in regions:
        # Process sale data
        sell_df = clean_region_data(f"{region}_sell_data.csv", "sell")
        if not sell_df.empty:
            for _, row in sell_df.iterrows():
                total_sell_data.append({
                    "region": region,
                    "area": row["建筑面积"],
                    "total_price": row["总价"],
                    "unit_price": row["单价"]
                })
        
        # Process rental data
        rental_df = clean_region_data(f"{region}_rental_data.csv", "rental")
        if not rental_df.empty:
            for _, row in rental_df.iterrows():
                total_rental_data.append({
                    "region": region,
                    "area": row["面积"],
                    "monthly_rent": row["租金"]
                })
    
    # Add Xiahuayuan data
    try:
        if os.path.exists("xiahuayuan_sell_data_cleaned.csv"):
            df_xiahuayuan_sell = pd.read_csv("xiahuayuan_sell_data_cleaned.csv", encoding="utf-8")
            for _, row in df_xiahuayuan_sell.iterrows():
                total_sell_data.append({
                    "region": "xiahuayuan",
                    "area": row["area"],
                    "total_price": row["total_price"],
                    "unit_price": row["unit_price"]
                })
    except Exception:
        pass
    
    try:
        if os.path.exists("xiahuayuan_rental_data_cleaned.csv"):
            df_xiahuayuan_rental = pd.read_csv("xiahuayuan_rental_data_cleaned.csv", encoding="utf-8")
            for _, row in df_xiahuayuan_rental.iterrows():
                total_rental_data.append({
                    "region": "xiahuayuan",
                    "area": row["area"],
                    "monthly_rent": row["monthly_rent"]
                })
    except Exception:
        pass
    
    # Save integrated data
    df_total_sell = pd.DataFrame(total_sell_data)
    df_total_rental = pd.DataFrame(total_rental_data)
    
    df_total_sell.to_csv("total_sell_data_cleaned.csv", index=False, encoding="utf-8-sig")
    df_total_rental.to_csv("total_rental_data_cleaned.csv", index=False, encoding="utf-8-sig")
    
    return df_total_sell, df_total_rental

def main():
    """Main function"""
    # Clean Xiahuayuan data
    clean_rental_data()
    clean_sell_data()
    
    # Integrate all region data
    df_sell, df_rental = integrate_all_data()

if __name__ == "__main__":
    main()