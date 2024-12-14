<template>
  <div class="buJnuC">
    <div class="fvfNpo">
      <div class="uXyMu">
        <AppBackToLogin />
        <div class="fNAZQD">
          <div class="dgrFox">
            <NuxtLink
                :to="{ path: '/'}"
                class="text-5xl font-bold text-purple-800 font-display"
            >
              Filmify 🎞️
            </NuxtLink>
            <slot />
          </div>
        </div>
        <p class="cyDNyc">
          Este sitio está autenticado por supabase.com y la.
          <a target="_blank" href="https://supabase.com/privacy" rel="noreferrer"> Política de Privacidad </a>
          y <a target="_blank" href="https://supabase.com/terms" rel="noreferrer"> Términos de servicio </a>
          de Supabase aplican.
        </p>
      </div>
    </div>
  </div>
</template>
