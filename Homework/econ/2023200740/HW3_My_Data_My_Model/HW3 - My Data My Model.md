## Project Overview
This project analyzes housing market data through web scraping, statistical modeling, and predictive analysis. I divide the workflow into two main components: data collection and data analysis.

## File Structure
- **`Housing_Price_Rent_Mining.ipynb`**: Web scraping module that collects housing price and rent data from real estate websites
- **`Housing_Price_Rent_Analysis.ipynb`**: Data analysis and modeling module that processes the collected data and builds predictive models
- **`HW3 - My Data My Model.md`**: Project documentation (this file)

## Dataset
The complete dataset is available in my repository: [https://github.com/junhaochen-econ/RUC-Coursework/tree/main/Quant](https://github.com/junhaochen-econ/RUC-Coursework/tree/main/Quant)

## Model Specifications (IMPORTANT)

### Basic Models

**Model 1: Housing Price per m2**
price/m2 = β₁·m2 + β₂·Xisanqi + β₃·Qinghe + β₄·Xierqi + β₅·Shangdi + ε

**Model 2: Rent per m2**
rent/m2 = β₁·m2 + β₂·Xisanqi + β₃·Qinghe + β₄·Xierqi + β₅·Shangdi + ε

**Model Specification Notes:**
- **No Intercept Term**: The models exclude the constant (intercept) term because we include a complete set of location dummy variables. Including both would create perfect multicollinearity (the "dummy variable trap"), as the location dummies sum to 1.
- **Full Set of Location Dummies**: All location indicators are included without omitting a reference category, making each coefficient directly interpretable as the location-specific effect relative to zero baseline.

### Extended Models

**Model 1+: Enhanced Housing Price Model**
price/m2 = β₁·m2² + β₂·Xisanqi + β₃·Qinghe + β₄·Xierqi + β₅·Shangdi + β₆·Xisanqi·m2 + β₇·Qinghe·m2 + β₈·Xierqi·m2 + β₉·Shangdi·m2 + ε

**Model 2+: Enhanced Rent Model**
rent/m2 = β₁·m2² + β₂·Xisanqi + β₃·Qinghe + β₄·Xierqi + β₅·Shangdi + β₆·Xisanqi·m2 + β₇·Qinghe·m2 + β₈·Xierqi·m2 + β₉·Shangdi·m2 + ε

**Extended Model Specification Notes:**
- **No Linear m2 Term**: The linear m2 term is excluded because we include a complete set of location-area interaction terms (location dummies × m2). Including both would create perfect multicollinearity, as the interaction terms collectively represent the linear area effect across all locations.
- **Nonlinear Quadratic Term**: The m2² term captures potential nonlinear relationships between property area and price/rent per square meter, allowing for curvature in the response function.
- **Interaction Effects**: The location × m2 interaction terms allow the marginal effect of area on price/rent to vary across different locations, capturing heterogeneous price gradients.
- **Complete Specification**: This formulation avoids multicollinearity while flexibly capturing both location-specific intercepts and location-specific slopes for the area effect.

**Economic Interpretation:**
The extended models recognize that the relationship between property size and price/rent may not be constant across locations, and that this relationship may exhibit nonlinear patterns. The interaction terms allow us to test whether larger properties command different premiums in different neighborhoods.
