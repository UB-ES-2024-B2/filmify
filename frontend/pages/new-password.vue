<template>
  <div class="DaoRb">
    <!-- Heading -->
    <h1 id="new-password-heading" class="eSHwvX">Reestablece tu contraseña</h1>

    <form @submit.prevent="updatePassword">
      <!-- Error and Success Alerts -->
      <ErrorAlert id='error' :error-msg="authError" @clearError="clearError" />
      <SuccessAlert id='success' :success-msg="authSuccess" @clearSuccess="clearSuccess" />

      <!-- Password Inputs -->
      <div class="jGQTZC">
        <div class="fdCSlG">
          <UInput
            id="new-password-input"
            class="cmCuLh"
            color="purple"
            icon="i-heroicons-lock-closed"
            type="password"
            placeholder="Nueva contraseña"
            v-model="password"
          />
        </div>
        <div class="fdCSlG">
          <UInput
            id="confirm-password-input"
            class="cmCuLh"
            color="purple"
            icon="i-heroicons-lock-closed"
            type="password"
            placeholder="Reescribe contraseña"
            v-model="passwordConfirm"
          />
        </div>
      </div>

      <!-- Submit Button -->
      <div class="jGQTZC">
        <UButton
          id="save-password-button"
          class="bjhGPG"
          color="purple"
          type="submit"
          :loading="loading"
        >
          Guardar
        </UButton>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "auth"
});
useHead({
  title: "New Password | supaAuth",
});
const password = ref("");
const passwordConfirm = ref("");
const client = useSupabaseAuthClient();
const loading = ref(false);
const authSuccess = ref("");
const authError = ref("");

const updatePassword = async () => {
  if (password.value !== passwordConfirm.value)
    return (authError.value = "Contraseñas no coinciden");
  loading.value = true;
  const { error } = await client.auth.updateUser({
    password: password.value,
  });
  await client.auth.signOut();
  if (error) {
    loading.value = false;
    authError.value = "Error";
    setTimeout(() => {
      authError.value = "";
    }, 5000);
  } else {
    loading.value = false;
    authSuccess.value = `Contraseña actualizada`;
    setTimeout(() => {
      authSuccess.value = "";
      navigateTo("/login");
    }, 5000);
  }
};

const clearError = () => {
  authError.value = "";
};

const clearSuccess = () => {
  authSuccess.value = "";
  navigateTo("/login");
};
</script>
