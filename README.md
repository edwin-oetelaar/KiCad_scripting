# KiCad Custom Connector Footprint Wizard

This repository contains a Python script that adds a custom footprint wizard to KiCad's Footprint Editor. 
It is designed to quickly generate footprints for common rectangular pin headers and connectors, such as those found on AliExpress or from manufacturers like Phoenix Contact.

This wizard allows you to define custom parameters like pin count, pitch, and pad dimensions to create a tailored footprint in seconds.

## Features

-   Generate footprints for dual-row connectors.
-   Customizable parameters:
    -   Number of pins
    -   Pin pitch (distance between pins)
    -   Pad shape, size, and drill hole diameter
    -   Custom silk screen outlines
    -   Pin 1 indicator marking (TBD)
-   Live preview within the wizard.
-   Simple and intuitive user interface.

## Gallery

Here are a few examples of what the wizard can generate:

| Wizard UI (AliExpress style)                               | Wizard UI (Phoenix Contact style)                                 | Result in KiCad Footprint Editor                       |
| ---------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------ |
| ![AliExpress connector wizard](Selection_070.png) | ![Phoenix Contact connector wizard](Selection_071.png) | ![Footprint in KiCad](kicad_screen1.png) |

## ✅ Prerequisites

Before you begin, ensure you have the following:

-   **KiCad**: Version 9.x or later is recommended. The script may work on older versions, but this is not guaranteed.
-   No external Python installation is required; the script uses the Python interpreter that is bundled with KiCad.

## ⚙️ Installation

To use this wizard, you need to place the Python script file in KiCad's user scripts directory. Follow these steps carefully.

### Step 1: Find your KiCad Scripting Path

KiCad stores plugins in a specific folder. The easiest way to find this folder is from within KiCad itself:

1.  Open KiCad.
2.  Go to the main menu and select **Preferences -> Configure Paths...**.
3.  In the list of paths, look for the variable `KICAD_USER_SCRIPTING_DIR` (or `KICAD7_USER_SCRIPTING_DIR` in v7, etc.).
4.  Copy this path. This is your user scripting directory. 

> **Typical Default Paths:**
>
> -   **Linux:** `~/.local/share/kicad/9.0/scripting/` or `~/.config/kicad/7.0/scripting/`

### Step 2: Download the Wizard Script

You can get the script in one of two ways:

-   **Option A: Download ZIP**
    1.  Click the green **`<> Code`** button at the top of this GitHub page.
    2.  Select **Download ZIP**.
    3.  Extract the ZIP file on your computer. Inside, you will find the Python script (e.g., `connector_wizard.py`).

-   **Option B: Git Clone (for developers)**
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    ```

### Step 3: Place the Script in the Correct Folder

1.  Navigate to the scripting path you found in Step 1.
2.  Inside the `scripting` folder, you should see a `plugins` folder. If it doesn't exist, create it.
3.  Copy the Python script file (e.g., `connector_wizard.py`) into this `plugins` folder.

Your final file structure should look like this:

```
<Your_KiCad_Scripting_Path>/
└── plugins/
    └── connector_wizard.py  <-- The script goes here
```

### Step 4: Restart KiCad

Close KiCad completely and reopen it. The program scans the plugin directories on startup.

## 🚀 Usage

Once installed, the footprint wizard will be available in the Footprint Editor.

1.  Open your project in KiCad.
2.  Launch the **Footprint Editor**.
3.  From the top menu, select **File -> Create Footprint...**.
4.  A "Footprint Wizard" selection dialog will appear. Your new **"Custom Connector Wizard"** (or a similar name) should now be in the list.
5.  Select it and click **OK**.
6.  The wizard's graphical interface will open. Enter your desired parameters (pin count, pitch, etc.).
7.  Click **OK** to generate the footprint.
8.  Save your new footprint to a library.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements, find a bug, or want to add new features, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/my-new-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -am 'Add some feature'`).
5.  Push to the branch (`git push origin feature/my-new-feature`).
6.  Open a new Pull Request.

Alternatively, you can open an issue to report a bug or suggest a feature.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
