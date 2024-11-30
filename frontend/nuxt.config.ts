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
  },

  runtimeConfig: {
    private: {
      
    },
    public: {
      SUPABASE_URL: process.env.DATABASE_URL,  // Tomará el valor de la variable de entorno
      SUPABASE_KEY: process.env.API_KEY,  // Tomará el valor de la variable de entorno
    }
  }
})

// Aquí también puedes poner los console.log para verificar
console.log('Supabase URL:', process.env.DATABASE_URL);
console.log('Supabase Key:', process.env.API_KEY);
