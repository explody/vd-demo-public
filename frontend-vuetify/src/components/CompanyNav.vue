<template>
    <v-card>
        <v-list rounded="rounded">
            <v-list-item v-for="item in serverItems" :key="item.name" :title="item.name"
                :to="{ name: 'CompanyPeople', params: { company: item.id } }" @click="companyNavClick(item)" link>

            </v-list-item>
        </v-list>
    </v-card>
</template>
  
<script>

import Backend from '/src/services/backend.js';
import ColleagueTable from './ColleagueTable.vue';
import EventBus from '../services/events.ts'
import { ref, onMounted } from 'vue'


export default {
    data: () => ({
        serverItems: [],
        page: 0,
        count: 0
    }),
    methods: {
        loadCompanies() {
            const baseUrl = "http://localhost:8000/api/company"
            const params = {}
            const page = 0
            const itemsPerPage = 50
            const sortBy = "name"
            Backend.fetch({ baseUrl, params, page, itemsPerPage, sortBy }).then(({ items, total }) => {
                this.serverItems = items
                this.totalItems = total
            });
        },
        async companyNavClick(action) {
            console.log("Sending companySwitch event")
            EventBus.emit('companySwitch', { page: 0, itemsPerPage: 10, sortBy: 'first_name' })
        }

    },
    mounted() {
        this.loadCompanies()
    }
}
</script>