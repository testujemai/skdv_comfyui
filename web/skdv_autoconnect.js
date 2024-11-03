(() => {
  const connectButton = document.getElementById("skdv-connect-comfyapi");
  if (connectButton == null) {
    console.error("[skdv_comfyui] Could not find ComfyAPI button to autoconnect.")
    return;
  }

  console.log("[skdv_comfyui] Attempting autoconnecting to ComfyAPI...")
  connectButton.click();
})()
