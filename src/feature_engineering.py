import logging
import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import AverageTrueRange, BollingerBands
from ta.volume import OnBalanceVolumeIndicator
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class FeatureEngineer:
    def __init__(self):
        pass

    def add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculates over 20 technical indicators from raw OHLCV columns."""
        df = df.copy()
        logger.info("Engineering technical indicators...")

        # 1. Trend Indicators (Moving Averages & MACD)
        for window in [5, 10, 20, 50, 100, 200]:
            df[f'sma_{window}'] = SMAIndicator(close=df['close'], window=window).sma_indicator()
            df[f'ema_{window}'] = EMAIndicator(close=df['close'], window=window).ema_indicator()
        
        macd_obj = MACD(close=df['close'])
        df['macd'] = macd_obj.macd()
        df['macd_signal'] = macd_obj.macd_signal()
        df['macd_diff'] = macd_obj.macd_diff()

        # 2. Momentum Indicators
        df['rsi_14'] = RSIIndicator(close=df['close'], window=14).rsi()
        df['rsi_30'] = RSIIndicator(close=df['close'], window=30).rsi()
        
        stoch = StochasticOscillator(high=df['high'], low=df['low'], close=df['close'], window=14, smooth_window=3)
        df['stoch_k'] = stoch.stoch()
        df['stoch_d'] = stoch.stoch_signal()

        # 3. Volatility Indicators (Bollinger Bands & ATR)
        bb = BollingerBands(close=df['close'], window=20, window_dev=2)
        df['bb_hband'] = bb.bollinger_hband()
        df['bb_lband'] = bb.bollinger_lband()
        df['bb_pband'] = bb.bollinger_pband()
        df['bb_wband'] = bb.bollinger_wband()
        
        df['atr_14'] = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14).average_true_range()

        # 4. Volume Indicators
        df['obv'] = OnBalanceVolumeIndicator(close=df['close'], volume=df['volume']).on_balance_volume()

        # 5. Price Returns & Lag Features
        df['return_1d'] = df['close'].pct_change(1)
        df['return_5d'] = df['close'].pct_change(5)
        df['vol_pct_change'] = df['volume'].pct_change(1)

        # Drop rows with NaN values resulting from rolling indicators to clean the dataset
        initial_len = len(df)
        df = df.dropna()
        logger.info(f"Dropped {initial_len - len(df)} rows containing NaN values from feature calculation.")
        
        return df

if __name__ == "__main__":
    from preprocessing import DataPreprocessor
    
    raw_data_path = config.DATA_DIR / "raw_stock_data.csv"
    if raw_data_path.exists():
        raw_df = pd.read_csv(raw_data_path, index_col=0)
        
        # Run through sequential pipeline
        preprocessor = DataPreprocessor()
        cleaned = preprocessor.clean_data(raw_df)
        with_target = preprocessor.create_target(cleaned)
        
        engineer = FeatureEngineer()
        final_features_df = engineer.add_technical_indicators(with_target)
        
        # Save processed features for part 3 & 4
        features_path = config.DATA_DIR / "processed_features.csv"
        final_features_df.to_csv(features_path)
        print(f"Generated {final_features_df.shape[1]} features. Saved to {features_path}")
    else:
        logger.error("Raw data missing. Run data_loader.py first.")