<template>
    <v-card>
        <v-card-title>
            Colleagues
            <v-spacer></v-spacer>
        </v-card-title>
        <v-data-table-server id="people-table" v-model:items-per-page="itemsPerPage" :headers="headers"
            :items-length="totalItems" :items="serverItems" :loading="loading" :search="search" class="elevation-1"
            item-value="preferred_name" @update:options="loadPeople" @click="handleClick">

            <template v-slot:top>
                <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" class="mx-4"></v-text-field>
            </template>
            <template v-slot:item="{ item }">
                <tr>
                    <td>
                        <div class="d-flex px-2 py-1 align-items-center">
                            <div>
                                <img :src=item.selectable.primary_company.icon alt="Company Icon" />
                            </div>
                            <div class="ms-4">
                                <h6 class="mb-0 text-sm">{{ item.selectable.primary_company.name }}</h6>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="d-flex px-2 py-1 align-items-center">
                            <div>
                                <img src="https://placehold.co/50x50" alt="Country flag">
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="d-flex px-2 py-1">
                            <div>
                                <a :href="`/person/${item.selectable.id}`">
                                    <img src="https://placehold.co/50x50" class="avatar avatar-sm me-3" alt="user1">
                                </a>
                            </div>
                            <div class="d-flex flex-column justify-content-center">
                                <h6 class="mb-0 text-sm">{{ item.selectable.additional_name }} {{ item.selectable.last_name
                                }}</h6>
                                <p class="text-xs text-secondary mb-0"><a
                                        :href="`mailto:${item.selectable.primary_email}`">{{
                                            item.selectable.primary_email
                                        }}</a></p>
                            </div>
                        </div>
                    </td>
                    <td>{{ item.selectable.title }}</td>
                </tr>
            </template>

        </v-data-table-server>
    </v-card>
</template>
  
<script>
import { useRoute, useRouter } from 'vue-router'
import Backend from '/src/services/backend.js';
import EventBus from '../services/events.ts'
import { ref } from 'vue'



export default {
    data: () => ({
        itemsPerPage: 10,
        headers: [
            { title: 'Company', key: 'company.name', sortable: true, },
            { title: 'Country', key: 'country', sortable: true, },
            {
                title: 'Person',
                align: 'start',
                sortable: true,
                key: 'preferred_name',
            },
            { title: 'Role', key: 'title', sortable: true, },
        ],
        search: '',
        serverItems: ref([]),
        loading: true,
        totalItems: 0,
        route: useRoute(),

    }),
    methods: {
        async loadPeople({ page, itemsPerPage, sortBy, groupBy, search }) {

            var column_filter;

            // temporary
            const baseUrl = "http://localhost:8000/api/people"
            const params = { expand: "primary_company" }


            // debug
            console.log("loadPeople this.$route.params")
            console.log(this.$route.params)
            console.log("loadPeople this.$router.currentRoute.value")
            console.log(this.$router.currentRoute.value)
            console.log("loadPeople this.$router.currentRoute")
            console.log(this.$router.currentRoute)

            if ('company' in this.$route.params) {
                column_filter = `company_roles..company_id:${this.route.params.company}|primary:1`
            }

            this.loading = true

            Backend.fetch({ baseUrl, params, page, itemsPerPage, sortBy, groupBy, column_filter, search }).then(({ items, total }) => {
                this.serverItems = items
                this.items = items
                this.totalItems = total
                this.loading = false
            })
        },
        handleClick(...args) {
            // Just for testing
            console.log("row clicked")
            console.log(this.$route.params)

        }
    },
    setup() {

    },
    mounted() {
        // this works fine to get events from the CompanyNav when a list item is clicked
        EventBus.addEventListener('companySwitch', (event) => {
            this.loadPeople(event.data)
        })
    }
}
</script>