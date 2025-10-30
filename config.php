<?php
// Názov pluginu
$pluginName = "fpp-oled_remote";

// Cesty k súborom
$configFile = "/home/fpp/media/config/plugin." . $pluginName . ".json";
$helperScript = "/home/fpp/media/plugins/" . $pluginName . "/helper.sh";
$logFile = "/home/fpp/media/logs/" . $pluginName . ".log";

// Predvolené nastavenia
$defaults = [
    'enabled' => "0",
    'showBattery' => "1"
];

// Spracovanie uloženia formulára
if (isset($_POST['save'])) {
    $newSettings['enabled'] = isset($_POST['enabled']) ? "1" : "0";
    $newSettings['showBattery'] = isset($_POST['showBattery']) ? "1" : "0";

    file_put_contents($configFile, json_encode($newSettings, JSON_PRETTY_PRINT));
    
    // Spustíme helper.sh, aby aplikoval zmeny
    exec("sudo " . $helperScript . " >> " . $logFile . " 2>&1");
}

// Načítanie aktuálnych nastavení
$settings = $defaults;
if (file_exists($configFile)) {
    $loadedSettings = json_decode(file_get_contents($configFile), true);
    if (is_array($loadedSettings)) {
        $settings = array_merge($defaults, $loadedSettings);
    }
}
?>

<div id="oled-remote-settings" class="settingsGroup">
    <legend>🔌 OLED Remote Control Settings</legend>

    <?php if (isset($_POST['save'])): ?>
        <div class="alert alert-success">✅ Settings have been saved successfully!</div>
    <?php endif; ?>

    <form method="POST" action="">
        <div class="settingsSetting">
            <label class="col-form-label">Enable Plugin on Startup:</label>
            <div class="setting">
                <input type="checkbox" name="enabled" id="enabled" <?php echo $settings['enabled'] === "1" ? 'checked' : ''; ?>>
                <label for="enabled"><span></span></label>
                <em>When checked, the remote control script will start automatically with FPP after a restart.</em>
            </div>
        </div>

        <div class="settingsSetting">
            <label class="col-form-label">Show Battery Status:</label>
            <div class="setting">
                <input type="checkbox" name="showBattery" id="showBattery" <?php echo $settings['showBattery'] === "1" ? 'checked' : ''; ?>>
                <label for="showBattery"><span></span></label>
                <em>Displays the battery percentage on the OLED screen.</em>
            </div>
        </div>

        <div class="settingsSetting">
            <div class="setting">
                <button type="submit" name="save" class="buttons btn-success">Save Settings</button>
            </div>
        </div>
    </form>
    
    <hr style="margin-top: 25px; margin-bottom: 25px;">
    
    <legend>ℹ️ Hardware Pinout (BCM)</legend>
    <p>This plugin uses the following GPIO pins (BCM numbering) for the I2C version of the hardware:</p>
    
    <style>
        .pin-table {
            width: 90%;
            max-width: 600px;
            margin-top: 15px;
            margin-bottom: 15px;
            border-collapse: collapse;
            border: 1px solid #ccc; /* Svetlý okraj */
            color: #333; /* Tmavé písmo pre celú tabuľku */
            background-color: #fff; /* Biele pozadie */
        }
        .pin-table th, .pin-table td {
            border: 1px solid #ccc; /* Svetlé okraje buniek */
            padding: 8px;
            text-align: left;
        }
        .pin-table th {
            background-color: #f0f0f0; /* Veľmi svetlo šedá hlavička */
            font-weight: bold;
        }
        .pin-table tr:nth-child(even) {
            background-color: #f9f9f9; /* Jemné "zebra" pruhy */
        }
        .pin-table .category-row td {
            background-color: #e9e9e9; /* Trochu tmavšia šedá pre kategóriu */
            font-weight: bold;
            color: #000; /* Zaistenie čierneho písma */
        }
    </style>
    <table class="pin-table">
        <thead>
            <tr>
                <th>Pin (BCM)</th>
                <th>Function</th>
            </tr>
        </thead>
        <tbody>
            <tr class="category-row">
                <td colspan="2">Controls (Inputs)</td>
            </tr>
            <tr>
                <td>GPIO 5</td>
                <td>Joystick Left</td>
            </tr>
            <tr>
                <td>GPIO 6</td>
                <td>Joystick Up</td>
            </tr>
            <tr>
                <td>GPIO 13</td>
                <td>Joystick Press</td>
            </tr>
            <tr>
                <td>GPIO 16</td>
                <td>Button 3 (Shutdown)</td>
            </tr>
            <tr>
                <td>GPIO 19</td>
                <td>Joystick Down</td>
            </tr>
            <tr>
                <td>GPIO 20</td>
                <td>Button 2 (Stop)</td>
            </tr>
            <tr>
                <td>GPIO 21</td>
                <td>Button 1 (Play)</td>
            </tr>
            <tr>
                <td>GPIO 26</td>
                <td>Joystick Right</td>
            </tr>
            <tr class="category-row">
                <td colspan="2">Communication & Power (I2C)</td>
            </tr>
            <tr>
                <td>GPIO 2 (SDA)</td>
                <td>I2C Data (Shared: Display & INA219)</td>
            </tr>
            <tr>
                <td>GPIO 3 (SCL)</td>
                <td>I2C Clock (Shared: Display & INA219)</td>
            </tr>
            <tr>
                <td>GPIO 25</td>
                <td>Display Power / Reset (Output)</td>
            </tr>
        </tbody>
    </table>
    <em>Note: This list assumes the I2C communication mode. Unused SPI-related pins (GPIO 8, 10, 11, 18, 24) are not required.</em>
    
</div>
