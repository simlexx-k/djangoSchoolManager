<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { Chart, BarController, CategoryScale, LinearScale, BarElement, Tooltip } from 'chart.js'

Chart.register(BarController, CategoryScale, LinearScale, BarElement, Tooltip)

export default {
  name: 'PerformanceChart',
  props: {
    chartData: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const chartCanvas = ref(null)
    let chart = null

    const createChart = () => {
      if (chart) {
        chart.destroy()
      }
      const ctx = chartCanvas.value.getContext('2d')
      chart = new Chart(ctx, {
        type: 'bar',
        data: props.chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          },
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              enabled: true,
              mode: 'index',
              intersect: false
            }
          }
        }
      })
    }

    onMounted(() => {
      if (props.chartData.datasets[0].data.length > 0) {
        createChart()
      }
    })

    watch(() => props.chartData, (newData) => {
      if (newData.datasets[0].data.length > 0) {
        createChart()
      }
    }, { deep: true })

    onUnmounted(() => {
      if (chart) {
        chart.destroy()
      }
    })

    return {
      chartCanvas
    }
  }
}
</script>
