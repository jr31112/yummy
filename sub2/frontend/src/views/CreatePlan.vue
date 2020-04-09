<template>
  <v-container class="py-0">
      <v-alert class="mx-auto my-0 pa-0" type="info" style="text-alig">여행갈 도시를 골라주세요!</v-alert>
      <v-row>
          <v-col cols="3" class="py-0">
              <time-line :destinations="destinations" />
          </v-col>
          <v-divider vertical />
          <v-col cols="8" class="py-0">
              <select-map :destinations="destinations" />
          </v-col>
      </v-row>
  </v-container>
</template>

<script>
import TimeLine from "../components/createplan/TimeLine"
import SelectMap from "../components/createplan/SelectMap"
export default {
    name:"createplan",
    components:{
        SelectMap,
        TimeLine
    },
    data(){
        return{
            destinations:[],
        }
    }
}
</script>

<style>

</style>