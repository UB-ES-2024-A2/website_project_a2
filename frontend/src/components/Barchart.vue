<script>
import { Bar } from 'vue-chartjs'
export default {
  extends: Bar,
  props: {
    chartData: {
      type: Object,
      required: true
    },
    options: {
      type: Object,
      default: () => ({})
    }
  },
  mounted () {
    this.renderChart(this.chartData, this.options)
  }
}
</script>
<style scoped>
.chart-container {
  position: relative;
  margin: auto;
  height: 80vh;
  width: 80vw;
}
</style>
