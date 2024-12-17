<template>
  <div class="DaoRb">
    <h1 class="eSHwvX">Recuperar contraseña</h1>
    <form @submit.prevent="resetPassword">
      <ErrorAlert id='error_alert' :error-msg="authError" @clearError="clearError" />
      <SuccessAlert id='success_alert' :success-msg="authSuccess" @clearSuccess="clearSuccess" />
      <div class="jGQTZC">
        <div class="fdCSlG">
          <UInput 
          id="email-input"
          class="cmCuLh" 
          color="purple"
          icon="i-heroicons-envelope"
          type="text" 
          placeholder="Correo electrónico" 
          v-model="email" 
        />
        </div>
        <UButton 
        id="reset-password-button"
        class="bjhGPG"
        color="purple"
        type="submit"  
        :loading="loading">
        Solicitar
      </UButton>
      <NuxtLink 
          id="login-return-link"
          to="/login" 
          class="fTZPOV block mt-4 text-sm text-gray-500 hover:underline">
          Volver
        </NuxtLink>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "auth"
})
useHead({
  title: 'Recuperar Contraseña | supaAuth'
})
const email = ref('')
const client = useSupabaseAuthClient()
const loading = ref(false)
const authSuccess = ref('')
const authError = ref('')

const resetPassword = async () => {
  loading.value = true
  const { error }  = await client.auth.resetPasswordForEmail(email.value, {
    redirectTo: `${window.location.origin}/new-password`
  })
  if (error) {
    loading.value = false
    authError.value = 'Correo inválido.'
    setTimeout(() => {
      authError.value = ''
    }, 5000)
  } else {
    loading.value = false
    authSuccess.value = `Se ha enviado un correo.`
    setTimeout(() => {
      authSuccess.value = ''
    }, 5000)
  }
}

const clearError = () => {
  authError.value = '';
};

const clearSuccess = () => {
  authSuccess.value = '';
};
</script>
