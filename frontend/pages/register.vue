<template>
  <div class="DaoRb">
    <h1 id="register-heading" class="eSHwvX">Regístrate</h1>
    <form @submit.prevent="signUp">
      <SuccessAlert :success-msg="succAlert" @clearError="clearError" />
      <ErrorAlert :error-msg="authError" @clearError="clearError" />
      <div class="jGQTZC">
        <!-- Campo de Usuario -->
        <div class="fdCSlG">
          <UInput 
            id="username-input"
            :class="{'input-error': fieldErrors.username}" 
            color="purple"
            icon="i-heroicons-user"
            type="text" 
            placeholder="Usuario" 
            v-model="username"
            maxlength="16" 
          />
          <span v-if="fieldErrors.username" class="field-error">{{ fieldErrors.username }}</span>
        </div>
        
        <!-- Campo de Correo -->
        <div class="fdCSlG">
          <UInput 
            id="email-input"
            :class="{'input-error': fieldErrors.email}" 
            color="purple"
            icon="i-heroicons-envelope"
            type="email" 
            placeholder="Correo" 
            v-model="email"
          />
          <span v-if="fieldErrors.email" class="field-error">{{ fieldErrors.email }}</span>
        </div>

        <!-- Campo de Contraseña -->
        <div class="fdCSlG">
          <UInput 
            id="password-input"
            :class="{'input-error': fieldErrors.password}" 
            color="purple"
            icon="i-heroicons-lock-closed"
            type="password" 
            placeholder="Contraseña" 
            v-model="password"
          />
          <span v-if="fieldErrors.password" class="field-error">{{ fieldErrors.password }}</span>
        </div>
      </div>

      <!-- Botón de Crear Cuenta -->
      <div class="jGQTZC">
        <UButton 
          id="create-account-button"
          class="bjhGPG"
          color="purple"
          type="submit"
          :loading="loading"
          :disabled="!isFormValid"
          :style="{ opacity: isFormValid ? 1 : 0.6 }"
        >
          Crear cuenta
        </UButton>
      </div>
      
      <!-- Enlace para iniciar sesión -->
      <div id="login-link" class="mt-4 text-center">
        <span>Ya tienes cuenta? </span>
        <router-link to="/login" class="text-purple-800 hover:underline">Iniciar sesión</router-link>
      </div>
    </form>
  </div>
</template>


<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue';
import { useSupabaseAuthClient, useSupabaseUser, navigateTo } from '#imports';

definePageMeta({
  layout: "auth"
});
useHead({
  title: 'Registro | supaAuth'
});

// Variables de estado
const email = ref('');
const password = ref('');
const username = ref('');
const authError = ref('');
const succAlert = ref('');
const client = useSupabaseAuthClient();
const user = useSupabaseUser();
const loading = ref(false);
const fieldErrors = reactive({ username: '', email: '', password: '' });

// Verificar si el formulario es válido
const isFormValid = computed(() => {
  return (
    !fieldErrors.username &&
    !fieldErrors.email &&
    !fieldErrors.password &&
    username.value &&
    email.value &&
    password.value &&
    password.value.length >= 8
  );
});

// Validar cada campo en tiempo real
watch(username, (newVal) => {
  if (!newVal) {
    fieldErrors.username = 'El nombre de usuario es requerido.';
  } else if (newVal.length > 16) {
    fieldErrors.username = 'El nombre de usuario no puede exceder los 16 caracteres.';
  } else {
    fieldErrors.username = '';
  }
});

watch(email, (newVal) => {
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!newVal) {
    fieldErrors.email = 'El correo electrónico es requerido.';
  } else if (!emailPattern.test(newVal)) {
    fieldErrors.email = 'El correo electrónico no es válido.';
  } else {
    fieldErrors.email = '';
  }
});

watch(password, (newVal) => {
  if (!newVal) {
    fieldErrors.password = 'La contraseña es requerida.';
  } else if (newVal.length < 8) {
    fieldErrors.password = 'La contraseña debe tener al menos 8 caracteres.';
  } else {
    fieldErrors.password = '';
  }
});

const clearError = () => {
  authError.value = '';
  succAlert.value = '';
};

// Función de registro
const signUp = async () => {
  if (!isFormValid.value) return;
  loading.value = true;
  const { data } = await client.rpc('check_auth_email_exists', { email_input: email.value });
  if(data){
    authError.value = 'Email ya registrado';
  } else {
    const { error } = await client.auth.signUp({
      email: email.value,
      password: password.value,
      options: {
        data: {
          username: username.value,
        }
      }
    });
    succAlert.value = 'Registrado. Revisa correo.'
  }
  loading.value = false;
};
</script>

<style scoped>
.field-error {
  color: #d9534f;
  font-size: 0.8rem; /* Ajuste del tamaño */
  margin-top: 4px;
  display: block;
  text-align: left;
}

.fdCSlG {
  display: flex;
  flex-direction: column;
}

.input-error {
  border: 2.5px solid #d9534f !important;
  border-radius: 9px;
}

.bjhGPG:disabled {
  cursor: not-allowed;
}
</style>
