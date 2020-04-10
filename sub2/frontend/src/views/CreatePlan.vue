<template>
  <v-container class="py-0">
      <v-alert class="mx-auto my-0 pa-0" type="info" style="text-alig">여행갈 도시를 골라주세요!</v-alert>
      <v-row>
          <v-col cols="3" class="py-0" style="bor">
              <date-plan :datePlan="datePlan" />
              <time-line :destinations="destinations" />
          </v-col>
          <v-col cols="9" class="py-0">
              <select-map :destinations="destinations" :datePlan="datePlan" />
          </v-col>
      </v-row>
  </v-container>
</template>

<script>
import DatePlan from "../components/createplan/DatePlan"
import TimeLine from "../components/createplan/TimeLine"
import SelectMap from "../components/createplan/SelectMap"
export default {
    name:"createplan",
    components:{
        SelectMap,
        TimeLine,
        DatePlan
    },
    data(){
        return{
            destinations:[],
            datePlan:{}
        }
    },
    methods:{
        setDatePlan(){
            var today = new Date().toISOString().substr(0, 10)
            this.datePlan = {
                start: today,
                end:null
            }
        },
    },
    mounted(){
        this.setDatePlan()
    }
}
</script>

<style>

</style>