# Memahami Ping-Pong Buffer & DMA

Sistem berkecepatan tinggi tidak bisa menggunakan fungsi standard seperti `HAL_ADC_PollForConversion()`. Kita menggunakan DMA.

## Konsep Circular / Ping-Pong Buffer

Kita mengalokasikan satu array besar di RAM, dibagi menjadi dua paruh:
*   **Half 0** (Index 0 sampai N/2 - 1)
*   **Half 1** (Index N/2 sampai N - 1)

**Alur kerjanya:**
1.  DMA secara otomatis menulis hasil konversi ADC ke *Half 0*. CPU santai.
2.  Saat *Half 0* penuh, DMA men-trigger interrupt `HAL_ADC_ConvHalfCpltCallback`. DMA otomatis lanjut menulis ke *Half 1*.
3.  *Di dalam interrupt Half-Cplt*, CPU segera mem-parsing/menyalin/menyimpan data dari *Half 0* ke SD Card. Selama CPU sibuk menulis ke SD Card, data baru dari sensor tidak hilang karena DMA sedang menuliskannya ke *Half 1*.
4.  Saat *Half 1* penuh, interrupt `HAL_ADC_ConvCpltCallback` terpanggil. DMA berputar (*circular*) kembali menulis ke *Half 0*. CPU mengamankan data dari *Half 1*.

```mermaid
sequenceDiagram
    participant Timer
    participant ADC
    participant DMA
    participant SRAM
    participant CPU

    Timer->>ADC: Trigger (misal tiap 10us)
    ADC->>DMA: Data Ready
    DMA->>SRAM: Tulis ke Half 0
    Note over DMA,SRAM: ... proses berulang ...
    DMA->>CPU: Interrupt: Half-Transfer Cplt
    DMA->>SRAM: Lanjut tulis ke Half 1
    CPU->>CPU: Pindahkan data Half 0 ke SDIO/USB
    Note over DMA,SRAM: ... proses berulang ...
    DMA->>CPU: Interrupt: Full-Transfer Cplt
    DMA->>SRAM: Lanjut putar tulis ke Half 0
    CPU->>CPU: Pindahkan data Half 1 ke SDIO/USB
```
