/*
 * Pseudocode/Boilerplate untuk inisialisasi ADC + DMA 
 * Referensi integrasi dengan STM32 HAL Library
 */

#include "main.h"

#define ADC_BUF_LEN 4096
uint16_t adc_buffer[ADC_BUF_LEN];
volatile uint8_t data_ready_flag = 0;

ADC_HandleTypeDef hadc1;
DMA_HandleTypeDef hdma_adc1;

void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_ADC1_Init(void);

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_DMA_Init();
    MX_ADC1_Init();

    // Start ADC dengan DMA dalam mode Circular
    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_buffer, ADC_BUF_LEN);

    while (1) {
        if (data_ready_flag == 1) {
            // Proses data dari Half 0
            // Contoh: tulis_ke_sd_card(&adc_buffer[0], ADC_BUF_LEN / 2);
            data_ready_flag = 0;
        } 
        else if (data_ready_flag == 2) {
            // Proses data dari Half 1
            // Contoh: tulis_ke_sd_card(&adc_buffer[ADC_BUF_LEN / 2], ADC_BUF_LEN / 2);
            data_ready_flag = 0;
        }
    }
}

// Callback DMA Half Transfer
void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef* hadc) {
    data_ready_flag = 1;
}

// Callback DMA Full Transfer
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    data_ready_flag = 2;
}
