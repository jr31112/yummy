<template>
  <v-timeline dense>
    <v-timeline-item v-for="i in destinations.length" :key="i" right @dblclick.native.stop="deletePlan(i-1)">
      <v-card>
          <v-card-title>{{destinations[i-1][1]}}</v-card-title>
          {{destinations[i-1][2]}}
          {{destinations[i-1][3]}}
      </v-card>
    </v-timeline-item>
  </v-timeline>
</template>

<script>
export default {
    name:"timeline",
    props:{
        destinations:{
            type:Array,
            required:true
        }
    },
    methods:{
        deletePlan(i){
            var a = new Date(this.destinations[i][3])
            var b = new Date(this.destinations[i][2])
            var days = (a-b)/1000/3600/24
            for (var j=i+1; j < this.destinations.length; j++){
                var startDate = new Date(this.destinations[j][2])
                var endDate = new Date(this.destinations[j][3])
                startDate.setDate(startDate.getDate() - days)
                endDate.setDate(endDate.getDate() - days)
                this.destinations[j][2] = startDate.toISOString().substr(0, 10)
                this.destinations[j][3] = endDate.toISOString().substr(0, 10)
            }
            this.destinations.splice(i,1)
        }
    }
}
</script>

<style>

</style>