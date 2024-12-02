<template>
  <div class="DaoRb">
    <!-- Login Heading -->
    <h1 id="login-heading" class="eSHwvX">Iniciar sesión</h1>
    
    <form @submit.prevent="login">
      <ErrorAlert :error-msg="authError" @clearError="clearError" />
      
      <!-- Email Input -->
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
        
        <!-- Password Input -->
        <div class="fdCSlG">
          <UInput 
            id="password-input"
            class="cmCuLh" 
            color="purple"
            icon="i-heroicons-lock-closed"
            type="password" 
            placeholder="Contraseña" 
            v-model="password" 
          />
        </div>
      </div>
      
      <!-- Login Button -->
      <div class="jGQTZC">
        <UButton 
          id="login-button"
          class="bjhGPG"
          color="purple"
          type="submit"  
          :loading="loading">
          Iniciar Sesion
        </UButton>
        
        <!-- Forgot Password Link -->
        <NuxtLink 
          id="forgot-password-link"
          to="/forgot-password" 
          class="fTZPOV block mt-4 text-sm text-gray-500 hover:underline">
          ¿Olvidaste tu contraseña?
        </NuxtLink>
      </div>
    </form>
    
    <!-- Register Link -->
    <div class="text-center">
      <span>¿No tienes cuenta? </span>
      <router-link 
        id="register-link"
        to="/register" 
        class="text-purple-800 hover:underline">
        Registrarse
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "auth"
})
useHead({
  title: 'Iniciar sesión | Filmify',
})

const user = useSupabaseUser();
const loading = ref(false);
const authError = ref('');
const email = ref('');
const password = ref('');
const client = useSupabaseAuthClient();

watchEffect(async () => {
  if (user.value) {
    await navigateTo('/');
  }
});

const login = async () => {
  loading.value = true;
  const { error } = await client.auth.signInWithPassword({
    email: email.value,
    password: password.value,
  });
  if (error) {
    loading.value = false;
    authError.value = 'Credenciales incorrectas';
    setTimeout(() => {
      authError.value = '';
    }, 5000);
  }
};

const clearError = () => {
  authError.value = '';
};
</script>