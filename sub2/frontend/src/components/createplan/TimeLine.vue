<template>
  <v-timeline>
    <v-timeline-item v-for="destination in destinations" :key=destination[1]>
      <v-card>
          {{destination[1]}}
      </v-card>
    </v-timeline-item>
  </v-timeline>
</template>

<script>
export default {
    name:"timeline",
    props:{
        destinations:{type:Array,required:true}
    },
}
</script>

<style>

</style>