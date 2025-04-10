async function main() {
    // Load Pyodide
    let pyodide = await loadPyodide();
    console.log("Pyodide loaded.");

    // Load the pygame-ce package (the checkIntegrity option may be required based on your setup)
    await pyodide.loadPackage(["pygame-ce"], { checkIntegrity: false });
    console.log("pygame-ce package loaded.");

    // Get the canvas element and expose it to Pyodide so pygame uses it for drawing.
    const canvas = document.getElementById("canvas");
    // The API below depends on your Pyodide build;
    // Here, we set the canvas for SDL to render on using pyodide's exposed module
    pyodide.canvas.setCanvas2D(canvas);

    // Optionally, tell SDL/pygame to use the canvas driver:
    await pyodide.runPythonAsync(`
  import os
  os.environ["SDL_VIDEODRIVER"] = "canvas"  # Alternatively "webgl" may work
    `);

    // Fetch the contents of your python file "marchingsquares.py"
    try {
      let response = await fetch("marchingsquares.py");
      if (!response.ok) {
        throw new Error("Failed to load marchingsquares.py: " + response.statusText);
      }
      let code = await response.text();
      console.log("Python code loaded from marchingsquares.py.");

      // Run the Python code via Pyodide.
      // Make sure your marchingsquares.py script is designed for asynchronous execution
      // (e.g. using asyncio in its main loop) so it cooperates with the browser.
      await pyodide.runPythonAsync(code);
      console.log("Python code executed successfully.");
    } catch (err) {
      console.error("Error loading or executing Python code:", err);
    }
  }

  main();
  