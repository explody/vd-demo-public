/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */
import $bus from './services/events.js';

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'

const app = createApp(App)

app.config.globalProperties.$bus = $bus;

registerPlugins(app)

app.mount('#app')
