<script>
import { ref } from 'vue'

export default {
    setup() {
        console.log("setup test")
        const count = ref(0)

        // expose to template and other options API hooks
        return {
            count
        }
    },

    mounted() {
        console.log(this.count) // 0
    }
}
</script>

<template>
    <button @click="count++">{{ count }}</button>
</template>