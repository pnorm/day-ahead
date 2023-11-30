from datetime import date, datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, Field
from loguru import logger

from utils.predictions_handler import get_predictions, get_backtest_results


app = FastAPI(title="Axpo recruitment task", version="1.0",
              description="Day ahead market, forecasting electricity prices")


# Define the operating hours
OPEN_HOUR = 9
CLOSE_HOUR = 10


class DateRange(BaseModel):
    from_date: date
    to_date: date

    @field_validator('from_date', 'to_date')
    def validate_date_boundaries(cls, v):
        start_date = date(2020, 4, 20)
        end_date = date.today() - timedelta(days=3)
        if not start_date <= v <= end_date:
            raise ValueError(f'Date must be between {start_date} and {end_date}')
        return v
    
    
class BacktestDataPoint(BaseModel):
    date: datetime = Field(..., example="2023-01-01T00:00:00.000")
    y: float
    y_pred: float

class PredictDataPoint(BaseModel):
    date: datetime = Field(..., example="2023-01-01T00:00:00.000")
    y: float


@app.get("/predict")
async def get_prediction():
    current_hour = datetime.now().hour

    # Check if the current hour is within operating hours
    if OPEN_HOUR <= current_hour < CLOSE_HOUR:
        logger.info("Predicting data for the next 24 hours")
        predicted_data = get_predictions(
            "utils/model_random_forest_regressor.joblib"
        )
        return [PredictDataPoint(**data) for data in predicted_data]
    else:
        raise HTTPException(status_code=403, detail="Please try during operating hours.")


@app.post("/backtest")
def get_backtest(date_range: DateRange):
    data = get_backtest_results(date_range.from_date, date_range.to_date, "utils/model_random_forest_regressor.joblib")
    return [BacktestDataPoint(**item) for item in data]

