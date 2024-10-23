import { createApp } from 'vue'
import { createPinia } from 'pinia'
import VueDOMPurifyHTML from 'vue-dompurify-html'
import App from './App.vue'
import router from './router'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import './index.css'

const vuetify = createVuetify({
    components,
    directives,
  })
  
const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueDOMPurifyHTML)
app.use(vuetify)
app.mount('#app')
