#!/usr/bin/env node

/**
 * Script para configurar el cron job de auto-generación de blog en cron-job.org
 * 
 * INSTRUCCIONES:
 * 1. Ve a https://console.cron-job.org
 * 2. Crea una cuenta o inicia sesión
 * 3. Ve a Settings > API Keys > Generate API Key
 * 4. Copia la API key
 * 5. Ejecuta: node scripts/setup-blog-cron.js TU_API_KEY
 */

const API_URL = "https://api.cron-job.org";

async function setupBlogCron(apiKey) {
  console.log("Configurando cron job para blog de ViajApp...");
  console.log("URL del endpoint:", "https://japan-travel-api.onrender.com/v1/blog/generate");

  const response = await fetch(`${API_URL}/jobs`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      job: {
        url: "https://japan-travel-api.onrender.com/v1/blog/generate",
        enabled: true,
        saveResponses: true,
        schedule: {
          timezone: "Europe/Madrid",
          expiresAt: 0,
          hours: [10],
          mdays: [1, 15],
          minutes: [0],
          months: [-1],
          wdays: [-1],
        },
        requestMethod: 1, // POST
        notification: {
          onFailure: {
            type: 0,
          },
        },
      },
    }),
  });

  if (response.ok) {
    const data = await response.json();
    console.log("\n✅ Cron job creado exitosamente!");
    console.log("   Job ID:", data.jobId);
    console.log("   Frecuencia: 1º y 15 de cada mes a las 10:00 AM (Europe/Madrid)");
    console.log("   Endpoint: POST https://japan-travel-api.onrender.com/v1/blog/generate");
    console.log("\n   Puedes gestionar tu cron job en: https://console.cron-job.org/jobs");
  } else {
    const error = await response.json();
    console.error("\n❌ Error al crear cron job:", error);
  }
}

const apiKey = process.argv[2];
if (!apiKey) {
  console.error("Uso: node scripts/setup-blog-cron.js TU_API_KEY_CRONJOB");
  console.error("\nObtén tu API key en: https://console.cron-job.org/settings");
  process.exit(1);
}

setupBlogCron(apiKey);
