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

  const hoverMenuButtonsComfyUI = document.querySelectorAll('[id^="skdv_comfyui_button_"]')
  if (hoverMenuButtonsComfyUI == null || hoverMenuButtonsComfyUI == undefined || hoverMenuButtonsComfyUI.length == 0) {
    console.error("[skdv_comfyui] Could not find new hover menu button.");
    return;
  }

  hoverMenuButtonsComfyUI.forEach(node => hoverMenu.insertBefore(node, hoverMenu.firstChild))
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

(() => {
  const dots = document.getElementById("skdv_comfyui_generating_dots");
  if (dots == null) {
    console.error("[skdv_comfyui] Could not find generation dots");
    return;
  }

  const originalTypyingDots = document.getElementById("typing-container");
  if (originalTypyingDots == null) {
    console.error("[skdv_comfyui] Could not find typing dots");
    return;
  }

  originalTypyingDots.parentElement.insertBefore(dots, originalTypyingDots.parentElement.firstChild);
})();
