async function main() {
  // Load Pyodide.
  let pyodide = await loadPyodide();
  console.log("Pyodide loaded.");

  // Load the pygame-ce package.
  await pyodide.loadPackage(["pygame-ce"], { checkIntegrity: false });
  console.log("pygame-ce package loaded.");

  // Use micropip to install the 'noise' package, required by your Python code.
  await pyodide.runPythonAsync(`
import micropip
await micropip.install("noise")
  `);
  console.log("noise package installed.");

  // Get the canvas element from the document.
  const canvas = document.getElementById("canvas");
  // Expose the canvas to Pyodide's SDL/pygame integration.
  pyodide.canvas.setCanvas2D(canvas);

  // Set the SDL video driver to use the canvas.
  await pyodide.runPythonAsync(`
import os
os.environ["SDL_VIDEODRIVER"] = "canvas"  # Alternatively, "webgl" may be tried if needed.
  `);
  console.log("SDL_VIDEODRIVER set to 'canvas'.");

  // Fetch the contents of your python file "marchingsquares.py".
  try {
    let response = await fetch("marchingsquares.py");
    if (!response.ok) {
      throw new Error("Failed to load marchingsquares.py: " + response.statusText);
    }
    let code = await response.text();
    console.log("Python code loaded from marchingsquares.py.");

    // Execute the Python code via Pyodide.
    // Ensure your script is designed to cooperate with asynchronous execution.
    await pyodide.runPythonAsync(code);
    console.log("Python code executed successfully.");
  } catch (err) {
    console.error("Error loading or executing Python code:", err);
  }
}

main();
