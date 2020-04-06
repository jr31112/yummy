<template>
    <h1>{{StoreName}}</h1>
</template>

<script>
export default {
    created() {
        this.StoreName = this.$route.params.StoreName
    },
    data:() => {
        return {
            StoreName:''
        }
    }
};
</script>