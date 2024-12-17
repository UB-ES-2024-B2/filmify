<template>
    <footer class="bg-gray-900 text-white py-10">
      <div class="container mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 px-6">
        <!-- Logo & About -->
        <div>
          <h2 class="text-lg font-semibold">Filmify</h2>
          <p class="mt-4 text-sm">
            Accede a la información más completa sobre tus películas favoritas y únete a una comunidad de cinéfilos como tú que siempre tienen algo nuevo que compartir.
          </p>
        </div>
  
        <!-- Navigation Links -->
        <div>
          <h3 class="text-lg font-semibold mb-4">Vínculos rápidos</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="/" class="hover:underline">Home</a></li>
            <li><a href="/login" class="hover:underline">Login</a></li>
            <li><a href="/register" class="hover:underline">Signup</a></li>
          </ul>
        </div>
  
        <!-- Social Media Links -->
        <div>
          <h3 class="text-lg font-semibold mb-4">Síguenos</h3>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <ul class="space-y-2">
                <li><a href="https://github.com/jjiglesias-ub" class="hover:underline">José Javier</a></li>
                <li><a href="https://github.com/em1ttal" class="hover:underline">Eshaan</a></li>
                <li><a href="https://github.com/HyKei04" class="hover:underline">Carlos</a></li>
            </ul>
            <ul class="space-y-2">
                <li><a href="https://github.com/AlbertPalavecino" class="hover:underline">Albert</a></li>
                <li><a href="https://github.com/davidvilajosana" class="hover:underline">David</a></li>
                <li><a href="https://github.com/ronaldortiz99" class="hover:underline">Ronald</a></li>
            </ul>
            </div>
        </div>
      </div>
  
      <!-- Bottom Section -->
      <div class="border-t border-gray-700 mt-10 pt-6 text-center text-sm">
        <p>&copy; {{ new Date().getFullYear() }} Filmify. Todos los derechos reservados.</p>
      </div>
    </footer>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  // Date auto-update
  const currentYear = ref(new Date().getFullYear());
  </script>
  