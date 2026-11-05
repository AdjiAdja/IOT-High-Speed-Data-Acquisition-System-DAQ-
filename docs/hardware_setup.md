# Hardware & Wiring Setup

Konfigurasi ini menggunakan standar penamaan pin STM32F4xx/H7xx, namun bisa disesuaikan lewat file `.ioc` (STM32CubeMX).

## Pinout Default

| Komponen / Fungsi | Pin STM32 | Keterangan |
| :--- | :--- | :--- |
| **Analog In 1** | `PA0` (ADC1_IN0) | Gunakan buffer op-amp (misal TL072/LM358) jika impedansi sensor tinggi. |
| **Analog In 2** | `PA1` (ADC1_IN1) | Sama dengan atas. Jaga jalur trace PCB sependek mungkin. |
| **MicroSD D0** | `PC8` (SDIO_D0) | Tarik resistor pull-up 47k ke 3V3. |
| **MicroSD D1** | `PC9` (SDIO_D1) | Pull-up 47k. |
| **MicroSD D2** | `PC10` (SDIO_D2) | Pull-up 47k. |
| **MicroSD D3** | `PC11` (SDIO_D3) | Pull-up 47k. |
| **MicroSD CLK** | `PC12` (SDIO_CK) | Series resistor ~22 ohm disarankan untuk mencegah ringing. |
| **MicroSD CMD** | `PD2` (SDIO_CMD) | Pull-up 47k. |
| **Debug UART** | `PA9` (TX), `PA10` (RX) | UART baudrate 115200 untuk log status. |

## Catatan Isolasi Industri
Untuk pemakaian di lingkungan industri sesungguhnya (dekat motor 3-phase, kontaktor, dll):
1.  **Jangan langsung hubungkan sensor ke pin PA0/PA1**. Gunakan *isolation amplifier* (seperti AMC1301) atau minimal rangkaian pengkondisi sinyal dengan TVS diode untuk proteksi over-voltage dan transien.
2.  Gunakan *linear regulator* (LDO) terpisah dengan noise rendah (low-dropout, high PSRR) khusus untuk pin `VDDA` di STM32 agar hasil bacaan ADC tidak kotor oleh noise dari power supply digital.
