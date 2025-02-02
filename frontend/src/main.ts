import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import VueClickAway from 'vue3-click-away'
import './vee-validate-setup'

const app = createApp(App)

app.use(createPinia())
app.use(VueClickAway)

app.mount('#app')
