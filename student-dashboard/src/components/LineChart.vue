<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'LineChart',
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
        type: 'line',
        data: props.chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          elements: {
            line: {
              tension: 0 // Disable bezier curves
            },
            point: {
              radius: 0 // Hide points
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          },
          plugins: {
            legend: {
              display: false // Hide legend
            }
          }
        },
        plugins: [{
          id: 'customRender',
          beforeDraw: (chart) => {
            const ctx = chart.ctx;
            const xAxis = chart.scales.x;
            const yAxis = chart.scales.y;
            const dataset = chart.data.datasets[0];
            
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(xAxis.getPixelForValue(0), yAxis.getPixelForValue(dataset.data[0]));
            
            for (let i = 1; i < dataset.data.length; i++) {
              ctx.lineTo(xAxis.getPixelForValue(i), yAxis.getPixelForValue(dataset.data[i]));
            }
            
            ctx.strokeStyle = dataset.borderColor;
            ctx.lineWidth = 2;
            ctx.stroke();
            
            if (dataset.fill) {
              ctx.lineTo(xAxis.getPixelForValue(dataset.data.length - 1), yAxis.getPixelForValue(0));
              ctx.lineTo(xAxis.getPixelForValue(0), yAxis.getPixelForValue(0));
              ctx.fillStyle = dataset.backgroundColor;
              ctx.fill();
            }
            
            ctx.restore();
          }
        }]
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

<style scoped>
canvas {
  width: 100%;
  height: 300px;
}
</style>
