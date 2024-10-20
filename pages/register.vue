<template>
  <div class="DaoRb">
    <h1 class="eSHwvX">Regístrate</h1>
    <form @submit.prevent="signUp">
      <ErrorAlert :error-msg="authError" @clearError="clearError" />
      <div class="jGQTZC">
        <div class="fdCSlG" >
          <UInput 
            class="cmCuLh" 
            color="purple"
            icon="i-heroicons-user"
            type="text" 
            placeholder="Usuario" 
            v-model="username" />
        </div>
        <div class="fdCSlG">
          <UInput 
            class="cmCuLh" 
            color="purple"
            icon="i-heroicons-envelope"
            type="text" 
            placeholder="Correo" 
            v-model="email" />
        </div>
        <div class="fdCSlG">
          <UInput 
            class="cmCuLh" 
            color="purple"
            icon="i-heroicons-lock-closed"
            type="password" 
            placeholder="Contraseña" 
            v-model="password" />
        </div>
      </div>
      <div class="jGQTZC">
        <UButton 
          class="bjhGPG"
          color="purple"
          type="submit"  
          :loading="loading">
          Crear cuenta
        </UButton>
      </div>
      <div class="mt-4 text-center">
      <span>Ya tienes cuenta? </span>
      <router-link to="/login" class="text-purple-800 hover:underline">Iniciar sesión</router-link>
    </div>
  </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "auth"
})
useHead({
  title: 'Registro | supaAuth'
})

const email = ref('')
const password = ref('')
const username = ref('')
const client = useSupabaseAuthClient()
const user = useSupabaseUser()
const loading = ref(false)
const authError = ref('')

watchEffect(async () => {
  if (user.value) {
    await navigateTo('/')
  }
});

const signUp = async () => {
  if (!username.value) return authError.value = 'Usuario requerido';
  loading.value = true
  const { error }  = await client.auth.signUp({
    email: email.value,
    password: password.value,
    options: {
      data: {
        username: username.value,
      }
    }
  })
  if (error) {
    loading.value = false
    authError.value = 'Error'
  }
}

const clearError = () => {
  authError.value = ''
}
</script>
