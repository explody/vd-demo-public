<template>
  <v-app>

    <v-main class="bg-grey-lighten-3">
      <v-container>
        <v-row>

          <v-col cols="2">
            <v-sheet rounded="lg">
              <CompanyNav></CompanyNav>
            </v-sheet>
          </v-col>

          <v-col>
            <v-sheet min-height="50vh" rounded="lg">
              <ColleagueTable></ColleagueTable>
            </v-sheet>
          </v-col>

        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import ColleagueTable from "/src/components/ColleagueTable.vue";
import CompanyNav from "/src/components/CompanyNav.vue";
</script>