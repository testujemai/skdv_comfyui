// Autoconnect to ComfyAPI.
(() => {
  const connectButton = document.getElementById("skdv-connect-comfyapi");
  if (connectButton == null) {
    console.error(
      "[skdv_comfyui] Could not find ComfyAPI button to autoconnect."
    );
    return;
  }

  console.log("[skdv_comfyui] Attempting connection to ComfyAPI...");
  connectButton.click();
})();

// Mounting ComfyAPI components.
(() => {
  const hoverMenu = document.getElementById("hover-menu");
  if (hoverMenu == null) {
    console.error("[skdv_comfyui] Could not find hover menu.");
    return;
  }

  const generateButton = document.getElementById(
    "skdv_comfyui_generate_button"
  );
  if (generateButton == null) {
    console.error("[skdv_comfyui] Could not find generate button.");
    return;
  }

  hoverMenu.insertBefore(generateButton, hoverMenu.firstChild);
})();

(() => {
  const extensionSection = document.getElementById("extensions");
  if (extensionSection == null) {
    console.error("[skdv_comfyui] Could not find extension section.");
    return;
  }

  const comfyui_panel = document.getElementById(
    "skdv_comfyui_generation_panel"
  );
  if (comfyui_panel == null) {
    console.error("[skdv_comfyui] Could not find comfyui panel.");
    return;
  }

  extensionSection.insertBefore(comfyui_panel, extensionSection.firstChild);
})();
