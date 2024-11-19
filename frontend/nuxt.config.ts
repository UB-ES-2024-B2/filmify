import dotenv from 'dotenv'

// Load environment variables from a specific path
dotenv.config({ path: '../frontend/.env' })

export default defineNuxtConfig({
  modules: ['@nuxtjs/supabase', '@nuxt/ui', '@nuxtjs/tailwindcss', "nuxt-rating", "@nuxt/image"],

  tailwindcss: {
    cssPath: '~/assets/css/tailwind.postcss'
  },

  app: {
    layoutTransition: { name: 'layout', mode: 'out-in' },
    pageTransition: { name: 'page', mode: 'out-in' },
    head: {
      charset: 'utf-16',
      viewport: 'width=500, initial-scale=1',
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono&display=swap' },
      ]
    }
  }
})
