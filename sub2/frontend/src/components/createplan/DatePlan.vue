<template>
  <v-container>
    <v-row @click.prevent="dialog_start=true">
      <v-text-field
        v-model="start"
        label="출발일"
        prepend-icon="mdi-calendar"
        readonly
      />
    </v-row>
    <v-dialog v-model="dialog_start" z-index="3" overlay-opacity="1" max-width="545px">
      <v-date-picker v-model="datePlan.start" scrollable @input="dialog_start=false" />
    </v-dialog>
    <v-row>
      <v-text-field v-model="end"
        label="도착일"
        prepend-icon="mdi-calendar"
        readonly
        @click.prevent="dialog_end=true"
      />
    </v-row>
  </v-container>
</template>

<script>
export default {
    name:"dateplan",
    props: {
        datePlan:{
            type:Object,
            require:true
        }
    },
    data(){
        return{
            dialog_start:false,
            dialog_end:false,
            start: "",
            end: ""
        }
    },
    methods: {
        updateDate(){
            if (this.datePlan.start){
                this.start = this.datePlan.start
            }
            if (this.datePlan.end){
                this.end = this.datePlan.end
            }
            else{
                this.end = ""
            }
        }
    },
    watch:{
        datePlan:{
            deep:true,
            immediate:true,
            handler:"updateDate"
        }
    }

}
</script>

<style>

</style>