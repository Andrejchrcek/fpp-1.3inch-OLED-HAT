<?php
// Názov pluginu
$pluginName = "fpp-oled_remote";

// Cesty k súborom
$pluginDir = "/home/fpp/media/plugins/{$pluginName}";
$configFile = "{$pluginDir}/config.json";
$helperScript = "{$pluginDir}/helper.sh";
$logFile = "/home/fpp/media/logs/{$pluginName}.log";

// Predvolené nastavenia, ak konfiguračný súbor neexistuje
$defaults = [
    'enabled' => false,
    'showBattery' => true
];

// Spracovanie uloženia formulára
if (isset($_POST['save'])) {
    $newSettings['enabled'] = isset($_POST['enabled']);
    $newSettings['showBattery'] = isset($_POST['showBattery']);

    file_put_contents($configFile, json_encode($newSettings, JSON_PRETTY_PRINT));
    
    // Spustíme pomocný skript, aby aplikoval zmeny
    exec("sudo {$helperScript} >> {$logFile} 2>&1");
}

// Načítanie aktuálnych nastavení pre zobrazenie
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
                <input type="checkbox" name="enabled" id="enabled" <?php echo $settings['enabled'] ? 'checked' : ''; ?>>
                <label for="enabled"><span></span></label>
                <em>When checked, the remote control script will start automatically with FPP after a restart.</em>
            </div>
        </div>

        <div class="settingsSetting">
            <label class="col-form-label">Show Battery Status:</label>
            <div class="setting">
                <input type="checkbox" name="showBattery" id="showBattery" <?php echo $settings['showBattery'] ? 'checked' : ''; ?>>
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
</div>
