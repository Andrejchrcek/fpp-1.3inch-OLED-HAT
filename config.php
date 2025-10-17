<?php
// Názov pluginu - zmeň podľa potreby
$pluginName = "OLED-Remote";

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

// --- Spracovanie uloženia formulára ---
if (isset($_POST['save'])) {
    // Načítaj hodnoty z formulára. Ak checkbox nie je zaškrtnutý, nepríde v POST, preto táto logika.
    $newSettings['enabled'] = isset($_POST['enabled']);
    $newSettings['showBattery'] = isset($_POST['showBattery']);

    // Zapíš nové nastavenia do config.json súboru
    file_put_contents($configFile, json_encode($newSettings, JSON_PRETTY_PRINT));

    // Spusti pomocný skript, ktorý aplikuje systémové zmeny (napr. registráciu štartovacieho skriptu)
    // Výstup a chyby presmerujeme do logu pre jednoduchšie ladenie
    exec("sudo {$helperScript} >> {$logFile} 2>&1");
}

// --- Načítanie aktuálnych nastavení pre zobrazenie na stránke ---
$settings = $defaults; // Začni s predvolenými hodnotami
if (file_exists($configFile)) {
    // Ak konfiguračný súbor existuje, načítaj ho
    $loadedSettings = json_decode(file_get_contents($configFile), true);
    // Spoj načítané hodnoty s predvolenými, aby sa zabezpečilo, že všetky kľúče existujú
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
                <em>When checked, the remote control script will start automatically with FPP.<br>
                <strong>Important:</strong> FPP needs to be restarted for this change to take effect.</em>
            </div>
        </div>

        <div class="settingsSetting">
            <label class="col-form-label">Show Battery Status:</label>
            <div class="setting">
                <input type="checkbox" name="showBattery" id="showBattery" <?php echo $settings['showBattery'] ? 'checked' : ''; ?>>
                <label for="showBattery"><span></span></label>
                <em>Displays the battery percentage on the OLED screen. Your Python script will need to read this setting.</em>
            </div>
        </div>

        <div class="settingsSetting">
            <div class="setting">
                <button type="submit" name="save" class="buttons btn-success">Save Settings</button>
            </div>
        </div>
    </form>
</div>

<div id="plugin-instructions" class="settingsGroup">
    <legend>📝 Instructions & Status</legend>
    <p>This plugin provides a simple remote control interface using an OLED screen and buttons connected to your FPP device's GPIO pins.</p>
    <ul>
        <li>Use the settings above to enable or disable features.</li>
        <li>Your main Python script (<code>oled_remote.py</code>) must be located in <code>/home/fpp/media/scripts/</code>.</li>
        <li>For debugging, check the plugin log file at: <code><?php echo $logFile; ?></code></li>
    </ul>
</div>
