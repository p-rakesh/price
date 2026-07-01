import logging
from pathlib import Path
import pandas as pd
import yfinance as yf
import config
import time
print(config.START_DATE, config.END_DATE)


# Setup basic logging for standalone execution
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, ticker: str, start_date: str, end_date: str):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def fetch_data(self) -> pd.DataFrame:
        """Downloads historical stock data from Yahoo Finance."""
        # logger.info(f"Fetching data for {self.ticker} from {self.start_date} to {self.end_date}...")
        for attempt in range(3):  # Retry mechanism
            try:
                # print(self.start_date, self.end_date)
                df = yf.download(self.ticker, start=self.start_date, end=self.end_date)
                print(df.head())
                if df.empty:
                    raise ValueError(f"No data returned for ticker '{self.ticker}'. Check ticker or dates.")
                    
                logger.info(f"Successfully downloaded {len(df)} rows of data.")
                return df
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                # if attempt < 2:
                #     time.sleep(60)
                # else:
                raise

    def save_data(self, df: pd.DataFrame, filename: str = "raw_stock_data.csv") -> Path:
        """Saves the downloaded dataframe to the designated data directory."""
        output_path = config.DATA_DIR / filename
        try:
            df.to_csv(output_path)
            logger.info(f"Data successfully saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to save data to {output_path}: {e}")
            raise

if __name__ == "__main__":
    # Test execution of the data loader
    loader = DataLoader(
        ticker=config.TICKER, 
        start_date= config.START_DATE, 
        end_date=config.END_DATE
    )
    raw_df = loader.fetch_data()
    loader.save_data(raw_df)