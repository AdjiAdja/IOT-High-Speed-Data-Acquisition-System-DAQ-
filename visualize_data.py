#!/usr/bin/env python3
# Script untuk memplot data dari file log (CSV) yang dihasilkan SD Card
# atau ditangkap via Serial/USB.

import pandas as pd
import matplotlib.pyplot as plt
import argparse

def plot_daq_data(file_path):
    # Mengasumsikan file format: Timestamp, Channel_1, Channel_2
    try:
        df = pd.read_csv(file_path, names=['Timestamp_ms', 'CH1_Raw', 'CH2_Raw'], header=0)
        
        # Konversi nilai raw ADC (0-4095) ke Voltage (asumsi referensi 3.3V)
        V_REF = 3.3
        ADC_RES = 4095.0
        
        df['CH1_Volts'] = (df['CH1_Raw'] / ADC_RES) * V_REF
        df['CH2_Volts'] = (df['CH2_Raw'] / ADC_RES) * V_REF

        plt.style.use('dark_background') # Sesuai preferensi developer
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        ax1.plot(df['Timestamp_ms'], df['CH1_Volts'], color='#00ff00', linewidth=1)
        ax1.set_title('Channel 1 (Analog Sensor)')
        ax1.set_ylabel('Voltage (V)')
        ax1.grid(True, alpha=0.3)

        ax2.plot(df['Timestamp_ms'], df['CH2_Volts'], color='#00ccff', linewidth=1)
        ax2.set_title('Channel 2 (Analog Sensor)')
        ax2.set_xlabel('Time (ms)')
        ax2.set_ylabel('Voltage (V)')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error membaca atau memplot data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot data dari sistem DAQ STM32")
    parser.add_argument("file", help="Path ke file data (CSV)")
    args = parser.parse_args()
    
    plot_daq_data(args.file)
